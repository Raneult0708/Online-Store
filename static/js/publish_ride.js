

function publishPost1() {
  const textareas = document.querySelectorAll("#modal-conducteur textarea");

  let infos = [];
  textareas.forEach(textarea => {
    let value = textarea.value.trim();
    infos.push(value);
  });

  if (infos.includes("")) {
    alert("Veuillez remplir tous les champs.");
    return;
  }

  const post = document.createElement("div");
  post.className = "posted-message";
  post.innerHTML = `
    <strong>🚗 Trajet proposé :</strong><br>
    <b>Départ :</b> ${infos[0]}<br>
    <b>Arrivée :</b> ${infos[1]}<br>
    <b>Heure :</b> ${infos[2]}<br>
    <b>Places disponibles :</b> ${infos[3]}
  `;

  const feed = document.getElementById("feed1");
  if (feed) {
    feed.prepend(post);
  }

  textareas.forEach(t => t.value = "");
  closePubSpace1();
}
document.querySelector('.connect').style.display = 'none';
document.querySelector('.sign-up').style.display = 'none';
