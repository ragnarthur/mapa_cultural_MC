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

  // 7. Máscara input telefone (procura em toda a página)
  var phoneInput = document.querySelector('.phone-input');
  if (phoneInput) {
    phoneInput.addEventListener('input', function(e) {
      let x = e.target.value.replace(/\D/g, '').slice(0, 11); // limita a 11 dígitos
      let formatted = '';
      if (x.length > 0) {
        formatted += '(' + x.substring(0,2);
      }
      if (x.length >= 3) {
        formatted += ') ' + x.substring(2,7);
      }
      if (x.length >= 7) {
        formatted += '-' + x.substring(7,11);
      }
      e.target.value = formatted;
    });
  }
});
