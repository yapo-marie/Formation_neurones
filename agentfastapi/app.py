import os
import json
import csv
from pathlib import Path
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, EmailStr
from string import Template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from typing import Dict, Any, Optional

# --- Google Sheets (service account) ---
try:
    import gspread
    from google.oauth2.service_account import Credentials
    HAS_SHEETS = True
except Exception:
    HAS_SHEETS = False

# -----------------------------
# CONFIG
# -----------------------------
USE_LLM = False  # rendu déterministe

# -----------------------------
# PROMPT "PARFAIT" (option LLM)
# -----------------------------
PROMPT = """
Tu es un assistant IA pour la génération de messages de bienvenue MLC dans un processus automatisé.

BUT :
1) Produire un email HTML professionnel (identique au template fourni, en remplaçant seulement {nom} et {email}).
2) Produire un message WhatsApp strictement conforme au template fourni (ne changer que {nom}).

RÈGLES ABSOLUES :
- Ne modifie ni le style, ni la structure du HTML.
- Conserve EXACTEMENT le texte, les emojis, la ponctuation et les sauts de ligne du message WhatsApp.
- Ne fais AUCUNE allusion à l’email dans le message WhatsApp.
- Réponds UNIQUEMENT en JSON valide avec les champs :
  {
    "email_body": "<HTML string>",
    "whatsapp_message": "<plain text>"
  }

DONNÉES :
- nom: {nom}
- email: {email}
- contact: {contact}

[TEMPLATE HTML EMAIL]
{html_email}

[TEMPLATE WHATSAPP — texte exact, ne changer que {{nom}} → {nom}]
Salut {nom} ! 👋✨

Tu veux en savoir plus sur notre programme MLC et découvrir comment il peut transformer ta vie ? 🌟

Voici les étapes à suivre :
ETAPE 1 : Inscris-toi sur la plateforme officielle MLC ici 👉 https://mlc.health/fr/fsd865
ETAPE 2 : Rejoins le groupe WhatsApp ici 👉 https://chat.whatsapp.com/CuYWhHMHkin9PjwO4t2JMM?mode=ac_t

Avec MLC, c’est une transformation garantie et un accompagnement sur mesure ❤️

"""

# -----------------------------
# TEMPLATES DÉTERMINISTES
# -----------------------------
HTML_EMAIL_TEMPLATE = Template(r"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Bienvenue chez MLC</title>
<style>
  @media only screen and (max-width:600px) {
    .container { width:100% !important; }
    .stack-column, .stack-cell { display:block !important; width:100% !important; max-width:100% !important; }
    .greeting { font-size:1.25rem !important; }
    .logo-img { height:44px !important; }
    .feature-img { width:40px !important; height:auto !important; }
    .cta-button { padding:12px 20px !important; font-size:16px !important; }
  }
</style>
</head>
<body style="margin:0;padding:0;background-color:#f8f9fa;font-family:Arial, Helvetica, sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f8f9fa;">
  <tr>
    <td align="center" style="padding:20px;">
      <table role="presentation" class="container" width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px;width:100%;background-color:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.06);">
        <tr>
          <td style="background:linear-gradient(135deg,#2563eb 0%,#1d4ed8 100%);padding:22px 20px;text-align:left;">
            <table role="presentation" width="100%">
              <tr>
                <td>
                  <a href="https://mlc.health" target="_blank" style="text-decoration:none;display:inline-block;">
                    <img src="https://mlc.health/img/logo.png" alt="MLC" class="logo-img" width="60" height="60" style="display:block;max-width:100%;width:60px;height:60px;border-radius:50%;background-color:#ffffff;padding:6px;box-shadow:0 0 5px rgba(0,0,0,0.1);border:0;outline:0;">
                  </a>
                </td>
                <td style="text-align:right;color:#e8f0ff;font-size:14px;">
                  <div style="font-weight:600">Programme de Santé Globale</div>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <tr>
          <td style="padding:34px 30px 20px 30px;">
            <div class="greeting" style="font-size:1.6rem;color:#1f2937;font-weight:600;margin-bottom:14px;">
              Bonjour <span style="color:#2563eb;font-weight:700;">$nom</span> !
            </div>

            <div style="font-size:1.02rem;color:#4b5563;line-height:1.6;margin-bottom:16px;">
              Bienvenue dans l'aventure <span style="color:#2563eb;font-weight:600;">MLC</span> ! Nous sommes ravis de vous accueillir dans notre programme innovant de santé globale qui aide déjà de nombreuses personnes à transformer leur quotidien.
            </div>

            <div style="font-size:1.02rem;color:#4b5563;line-height:1.6;margin-bottom:22px;">
              Cette <span style="color:#2563eb;font-weight:600;">opportunité unique</span> dans le domaine de la santé et du bien-être va vous permettre d'améliorer durablement votre énergie, votre forme physique et votre équilibre de vie.
            </div>

            <table role="presentation" width="100%" style="margin-bottom:18px;">
              <tr>
                <td class="stack-cell" valign="top" align="center" style="padding:8px;">
                  <table role="presentation" style="background:#f8fafc;border:1px solid #e5e7eb;border-radius:10px;padding:18px;width:100%;">
                    <tr><td align="center" style="padding-bottom:8px;">
                      <img src="https://cdn-icons-png.flaticon.com/512/1828/1828884.png" alt="Innovation" class="feature-img" width="45" style="display:block;width:45px;height:auto;border:0;outline:0;">
                    </td></tr>
                    <tr><td align="center" style="font-size:0.95rem;font-weight:600;color:#374151;">Innovation</td></tr>
                    <tr><td align="center" style="font-size:0.85rem;color:#6b7280;">Programme révolutionnaire</td></tr>
                  </table>
                </td>
                <td class="stack-cell" valign="top" align="center" style="padding:8px;">
                  <table role="presentation" style="background:#f8fafc;border:1px solid #e5e7eb;border-radius:10px;padding:18px;width:100%;">
                    <tr><td align="center" style="padding-bottom:8px;">
                      <img src="https://cdn-icons-png.flaticon.com/512/869/869869.png" alt="Bien-être" class="feature-img" width="45">
                    </td></tr>
                    <tr><td align="center" style="font-size:0.95rem;font-weight:600;color:#374151;">Bien-être</td></tr>
                    <tr><td align="center" style="font-size:0.85rem;color:#6b7280;">Transformation durable</td></tr>
                  </table>
                </td>
                <td class="stack-cell" valign="top" align="center" style="padding:8px;">
                  <table role="presentation" style="background:#f8fafc;border:1px solid #e5e7eb;border-radius:10px;padding:18px;width:100%;">
                    <tr><td align="center" style="padding-bottom:8px;">
                      <img src="https://cdn-icons-png.flaticon.com/512/1256/1256650.png" alt="Communauté" class="feature-img" width="45">
                    </td></tr>
                    <tr><td align="center" style="font-size:0.95rem;font-weight:600;color:#374151;">Communauté</td></tr>
                    <tr><td align="center" style="font-size:0.85rem;color:#6b7280;">Accompagnement expert</td></tr>
                  </table>
                </td>
              </tr>
            </table>

            <div style="background:#f0f9ff;border-left:4px solid #2563eb;padding:14px 18px;margin-bottom:22px;font-size:1rem;color:#374151;line-height:1.6;">
              <strong>Voici les étapes à suivre :</strong><br>
              <strong>ÉTAPE 1 :</strong> Inscrivez-vous sur la plateforme officielle MLC en cliquant 👉 <a href="https://mlc.health/fr/fsd865" target="_blank" style="color:#2563eb;font-weight:600;">ici</a><br>
              <strong>ÉTAPE 2 :</strong> Rejoignez le groupe WhatsApp en cliquant 👉 <a href="https://chat.whatsapp.com/CuYWhHMHkin9PjwO4t2JMM?mode=ac_t" target="_blank" style="color:#2563eb;font-weight:600;">ici</a>
            </div>
          </td>
        </tr>

        <tr>
          <td style="background-color:#f8fafc;padding:18px 24px 24px 24px;text-align:center;border-top:1px solid #e5e7eb;color:#6b7280;font-size:0.95rem;">
            <div style="font-weight:700;color:#374151;margin-bottom:6px;">Votre parcours vers un mieux-être optimal commence ici !</div>
            <div style="font-size:0.85rem;color:#9ca3af;">MLC Health • noeliagui.mlc@gmail.com</div>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
</body>
</html>
""")

WHATSAPP_TEMPLATE = Template("""Salut $nom ! 👋✨

Tu veux en savoir plus sur notre programme MLC et découvrir comment il peut transformer ta vie ? 🌟

Voici les étapes à suivre :
ETAPE 1 : Inscris-toi sur la plateforme officielle MLC ici 👉 https://mlc.health/fr/fsd865
ETAPE 2 : Rejoins le groupe WhatsApp ici 👉 https://chat.whatsapp.com/CuYWhHMHkin9PjwO4t2JMM?mode=ac_t

Avec MLC, c’est une transformation garantie et un accompagnement sur mesure ❤️
Des questions ou des doutes ? Je suis là pour t’aider 😊
""")

# -----------------------------
# FastAPI
# -----------------------------
app = FastAPI(title="MLC Automation", version="1.2.0")

class Prospect(BaseModel):
    nom: str
    email: EmailStr
    contacts: str  # numéro WhatsApp E.164 sans '+', ex: 2250700000000

class WhatsAppTemplateRequest(BaseModel):
    to: str
    template_name: str = "hello_world"
    language_code: str = "en_US"
    components: list[dict] | None = None

# -----------------------------
# Génération de contenus
# -----------------------------
def render_deterministic(nom: str, email: str) -> Dict[str, str]:
    email_body = HTML_EMAIL_TEMPLATE.substitute(nom=nom)
    whatsapp_message = WHATSAPP_TEMPLATE.substitute(nom=nom)
    return {"email_body": email_body, "whatsapp_message": whatsapp_message}

# -----------------------------
# Email via SMTP Gmail
# -----------------------------
def send_email_smtp(to_email: str, subject: str, html_body: str) -> Optional[Dict[str, Any]]:
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    sender = os.getenv("SMTP_FROM", smtp_user)

    if not smtp_user or not smtp_pass:
        return {"skipped": True, "reason": "SMTP_USER ou SMTP_PASS non configuré"}

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to_email
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(sender, [to_email], msg.as_string())
        return {"sent": True}
    except Exception as e:
        return {"sent": False, "error": str(e)}

# -----------------------------
# WhatsApp Cloud: texte et template
# -----------------------------
def send_whatsapp_cloud(to_phone: str, message: str) -> Optional[Dict[str, Any]]:
    token = os.getenv("WHATSAPP_TOKEN")
    phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    if not token or not phone_number_id:
        return {"skipped": True, "reason": "WHATSAPP_TOKEN ou WHATSAPP_PHONE_NUMBER_ID non configuré"}

    url = f"https://graph.facebook.com/v23.0/{phone_number_id}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "type": "text",
        "text": {"body": message, "preview_url": False},
    }
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    try:
        r = requests.post(url, json=payload, headers=headers, timeout=20)
        ok = r.status_code in (200, 201)
        return {
            "sent": ok,
            "status_code": r.status_code,
            "response": r.json() if r.content else None,
        }
    except Exception as e:
        return {"sent": False, "error": str(e)}

def send_whatsapp_template(
    to_phone: str,
    template_name: str,
    lang_code: str = "en_US",
    components: list[dict] | None = None,
) -> dict:
    token = os.getenv("WHATSAPP_TOKEN")
    phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    if not token or not phone_number_id:
        return {"skipped": True, "reason": "WHATSAPP_TOKEN ou WHATSAPP_PHONE_NUMBER_ID non configuré"}

    url = f"https://graph.facebook.com/v23.0/{phone_number_id}/messages"
    payload: dict = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "type": "template",
        "template": {"name": template_name, "language": {"code": lang_code}},
    }
    if components:
        payload["template"]["components"] = components

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    r = requests.post(url, json=payload, headers=headers, timeout=20)

    return {
        "sent": r.status_code in (200, 201),
        "status_code": r.status_code,
        "response": r.json() if r.content else None,
    }

def _looks_like_window_error(resp: dict | None) -> bool:
    if not resp:
        return False
    msg = str(resp).lower()
    return any(s in msg for s in [
        "customer care window",
        "outside the 24-hour window",
        "no matching template",
        "131047",
        "470",
    ])

# -----------------------------
# Google Sheets helpers
# -----------------------------
def _load_service_account_creds():
    """
    Charge les credentials service account Google.
    GOOGLE_SHEETS_CREDENTIALS_JSON peut être:
      - un chemin vers le .json
      - le contenu JSON complet (string)
    """
    raw = os.getenv("GOOGLE_SHEETS_CREDENTIALS_JSON")
    if not raw:
        raise RuntimeError("GOOGLE_SHEETS_CREDENTIALS_JSON manquant")

    # Chemin de fichier ?
    p = Path(raw)
    if p.exists():
        info = json.loads(p.read_text())
    else:
        # Contenu JSON
        info = json.loads(raw)

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    return Credentials.from_service_account_info(info, scopes=scopes)

def append_row_google_sheet(nom: str, email: str, contacts: str, whatsapp_status: dict, email_status: dict) -> Dict[str, Any]:
    spreadsheet_id = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")  # ex: 1FXqOIRi...
    worksheet_name = os.getenv("GOOGLE_SHEETS_WORKSHEET", "Feuille 1")
    if not spreadsheet_id:
        return {"skipped": True, "reason": "GOOGLE_SHEETS_SPREADSHEET_ID non défini"}
    if not HAS_SHEETS:
        return {"skipped": True, "reason": "Modules gspread/google-auth non installés"}

    try:
        creds = _load_service_account_creds()
        gc = gspread.authorize(creds)
        sh = gc.open_by_key(spreadsheet_id)
        ws = sh.worksheet(worksheet_name)

        ts = datetime.now(timezone.utc).isoformat()
        wamid = None
        try:
            wamid = whatsapp_status.get("response", {}).get("messages", [{}])[0].get("id")
        except Exception:
            pass

        row = [
            ts,          # horodatage (UTC)
            nom,
            email,
            contacts,
            email_status.get("sent"),
            whatsapp_status.get("status_code"),
            wamid,
        ]
        ws.append_row(row, value_input_option="RAW")
        return {"appended": True}
    except Exception as e:
        return {"appended": False, "error": str(e)}

# -----------------------------
# Log CSV local
# -----------------------------
def log_to_csv(nom: str, email: str, contacts: str, email_status: dict, whatsapp_status: dict) -> Dict[str, Any]:
    path = os.getenv("LOG_CSV_PATH", "./sent_log.csv")
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    try:
        file_exists = Path(path).exists()
        with open(path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["ts_utc","nom","email","contacts","email_sent","whatsapp_status_code","whatsapp_message_id"])
            ts = datetime.now(timezone.utc).isoformat()
            wamid = None
            try:
                wamid = whatsapp_status.get("response", {}).get("messages", [{}])[0].get("id")
            except Exception:
                pass
            writer.writerow([
                ts, nom, email, contacts,
                email_status.get("sent"),
                whatsapp_status.get("status_code"),
                wamid
            ])
        return {"logged": True, "path": str(Path(path).resolve())}
    except Exception as e:
        return {"logged": False, "error": str(e)}

# -----------------------------
# Webhook (optionnel) pour statuts WhatsApp
# -----------------------------
VERIFY_TOKEN = os.getenv("WAPP_VERIFY_TOKEN", "my-verify-token")

@app.get("/webhook/whatsapp")
def verify_webhook(mode: str = "", token: str = "", challenge: str = ""):
    if mode == "subscribe" and token == VERIFY_TOKEN:
        try:
            return int(challenge)
        except Exception:
            return challenge
    raise HTTPException(status_code=403, detail="Verification failed")

@app.post("/webhook/whatsapp")
async def receive_webhook(req: Request):
    body = await req.json()
    print("WAPP WEBHOOK:", body)
    return {"status": "received"}

# -----------------------------
# Endpoints
# -----------------------------
@app.get("/health")
def health():
    return {"ok": True, "version": "1.2.0"}

@app.post("/whatsapp/send-template")
def send_template(req: WhatsAppTemplateRequest):
    status = send_whatsapp_template(
        to_phone=req.to,
        template_name=req.template_name,
        lang_code=req.language_code,
        components=req.components,
    )
    return {"ok": bool(status.get("sent")), "whatsapp_send_status": status}

@app.post("/mlc/send")
def send_mlc(data: Prospect):
    """
    Endpoint unique : génère l'email HTML et le message WhatsApp,
    tente l'envoi texte; si échec 24h, fallback sur un template pour ouvrir la session,
    puis journalise (Google Sheets + CSV).
    """
    # 1) Génération
    generated = render_deterministic(data.nom, data.email)

    # 2) Envois
    email_status = send_email_smtp(
        to_email=data.email,
        subject="Bienvenue au programme MLC",
        html_body=generated["email_body"],
    )
    whatsapp_status = send_whatsapp_cloud(
        to_phone=data.contacts,
        message=generated["whatsapp_message"],
    )
    if not whatsapp_status.get("sent") and whatsapp_status.get("status_code") == 400:
        if _looks_like_window_error(whatsapp_status.get("response")):
            whatsapp_status = send_whatsapp_template(
                to_phone=data.contacts,
                template_name=os.getenv("WAPP_FALLBACK_TEMPLATE", "hello_world"),
                lang_code=os.getenv("WAPP_FALLBACK_LANG", "en_US"),
            )

    # 3) Append Google Sheets (si configuré)
    sheet_status = append_row_google_sheet(
        nom=data.nom,
        email=data.email,
        contacts=data.contacts,
        whatsapp_status=whatsapp_status,
        email_status=email_status,
    )

    # 4) Log local CSV
    csv_status = log_to_csv(
        nom=data.nom,
        email=data.email,
        contacts=data.contacts,
        email_status=email_status,
        whatsapp_status=whatsapp_status,
    )

    return {
        "ok": True,
        "preview": {
            "email_to": data.email,
            "whatsapp_to": data.contacts,
            "whatsapp_message": generated["whatsapp_message"],
        },
        "email_send_status": email_status,
        "whatsapp_send_status": whatsapp_status,
        "sheet_append_status": sheet_status,
        "csv_log_status": csv_status,
    }
