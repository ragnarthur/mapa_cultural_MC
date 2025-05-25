// static/core/js/map.js

document.addEventListener("DOMContentLoaded", function() {
  // 1. Lê os dados serializados do template
  const dataEl = document.getElementById("spaces-data");
  let spaces = [];
  if (dataEl) {
    try {
      spaces = JSON.parse(dataEl.textContent.trim());
    } catch (e) {
      console.error("Falha ao ler dados de espaços:", e, dataEl.textContent);
    }
  }

  // 2. Inicializa o mapa (foco em Monte Carmelo)
  const mapContainer = document.getElementById("mapid");
  if (!mapContainer) return; // Só executa se existir o container do mapa

  const map = L.map("mapid").setView([-18.7315, -47.4982], 13);

  // 3. Adiciona camada base OpenStreetMap
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors"
  }).addTo(map);

  // 4. Ícone vermelho customizado
  const redIcon = new L.Icon({
    iconUrl: "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png",
    shadowUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png",
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });

  // 5. Cria marcadores e vincula ao índice
  const markers = [];
  if (Array.isArray(spaces)) {
    spaces.forEach(function(sp) {
      if (
        sp.lat !== undefined && sp.lng !== undefined &&
        !isNaN(parseFloat(sp.lat)) && !isNaN(parseFloat(sp.lng))
      ) {
        const marker = L.marker([parseFloat(sp.lat), parseFloat(sp.lng)], {icon: redIcon})
          .bindPopup("<b>" + sp.name + "</b>")
          .addTo(map);
        markers.push(marker);
      } else {
        markers.push(null);
      }
    });
  }

  // 6. Liga clique no nome da lista ao marcador no mapa
  document.querySelectorAll('.space-link').forEach(function(link, idx) {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const marker = markers[idx];
      if (marker) {
        map.setView(marker.getLatLng(), 16);
        marker.openPopup();
      }
    });
  });
});
