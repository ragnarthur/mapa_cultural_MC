// static/core/js/map.js

document.addEventListener("DOMContentLoaded", function() {
  // 1. Lê os dados serializados no template
  const dataEl = document.getElementById("spaces-data");
  let spaces = [];
  if (dataEl) {
    try {
      spaces = JSON.parse(dataEl.textContent);
    } catch (e) {
      console.error("Falha ao ler dados de espaços:", e);
    }
  }

  // 2. Inicializa o mapa em coordenadas padrão
  const map = L.map("map").setView([-18, -45], 6);

  // 3. Adiciona camada base
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors"
  }).addTo(map);

  // 4. Insere marcadores para cada espaço
  spaces.forEach(function(sp) {
    L.marker([sp.lat, sp.lng])
      .bindPopup("<b>" + sp.name + "</b>")
      .addTo(map);
  });
});
