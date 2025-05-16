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

// 5. Máscara input telefone
document.addEventListener('DOMContentLoaded', function() {
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
