let btn = document.querySelector("#Qbtn");
let quote = document.querySelector(".quote");
let writer = document.querySelector(".writer");

btn.addEventListener("click", () => {
    fetch("/quote")
        .then(res => res.json())
        .then(data => {
            quote.innerHTML = `"${data.quote.body}"`;
            writer.innerHTML = `– ${data.quote.author}`;
        })
        .catch(err => {
            console.error("Erreur lors de la récupération :", err);
            quote.innerHTML = `"Une erreur est survenue."`;
            writer.innerHTML = "";
        });
});
