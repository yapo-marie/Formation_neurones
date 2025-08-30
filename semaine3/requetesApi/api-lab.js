
const genre = document.getElementById("genre");
const nomComplet = document.getElementById("nom");
const titre = document.getElementById("titre");
const prenom = document.getElementById("premier");
const nomFamille = document.getElementById("dernier");

async function getUser() {
  try {
    const response = await fetch("https://randomuser.me/api/");


    if (!response.ok) {
      throw new Error("Erreur HTTP : " + response.status);
    }

    
    const data = await response.json();

    const user = data.results[0];

  
    genre.innerText = user.gender;
    nomComplet.innerText = `${user.name.first} ${user.name.last}`;
    titre.innerText = user.name.title;
    prenom.innerText = user.name.first;
    nomFamille.innerText = user.name.last;

    console.log("Utilisateur récupéré :", user);
  } catch (error) {
    console.error("Une erreur s'est produite :", error.message);
    genre.innerText = "Erreur";
    nomComplet.innerText = "Impossible de charger";
  }
}


getUser();
