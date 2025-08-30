import express from 'express';
import fetch from 'node-fetch';
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

dotenv.config();

const app = express();
const PORT = 3005;


const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);


app.use(express.static(path.join(__dirname, 'public')));

const API_KEY = process.env.FAVQS_API_KEY;

app.get("/quote", async (req, res) => {
  try {
    const response = await fetch("https://favqs.com/api/qotd", {
      headers: {
        "Authorization": `Token token="${API_KEY}"`
      }
    });

    const data = await response.json();

    if (!data.quote) {
      throw new Error("Réponse inattendue : données manquantes");
    }

    res.json(data);
  } catch (err) {
    console.error("Erreur côté serveur :", err.message);
    res.status(500).json({ error: "Erreur lors de la récupération de la citation" });
  }
});

app.listen(PORT, () => {
  console.log(`Serveur démarré sur http://localhost:${PORT}`);
});
