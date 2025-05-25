// static/core/js/mask.js

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll('.phone-input').forEach(function (phoneInput) {
    phoneInput.addEventListener('input', function (e) {
      // Guarda posição do cursor ANTES
      let oldValue = phoneInput.value;
      let oldCursor = phoneInput.selectionStart;

      // Remove tudo que não for número
      let numbers = oldValue.replace(/\D/g, '').slice(0, 11);
      let formatted = '';

      if (numbers.length > 0) {
        formatted += '(' + numbers.substring(0, 2);
      }
      if (numbers.length > 2) {
        formatted += ') ' + numbers.substring(2, 7);
      }
      if (numbers.length > 7) {
        formatted += '-' + numbers.substring(7, 11);
      }

      // Se cursor estava no fim, mantém no fim
      let newCursor = oldCursor;
      if (oldCursor === oldValue.length) {
        newCursor = formatted.length;
      } else {
        // Recalcula posição do cursor para casos de backspace em máscara
        let countNonDigitBefore = (oldValue.slice(0, oldCursor).match(/\D/g) || []).length;
        let countNonDigitAfter  = (formatted.slice(0, oldCursor).match(/\D/g) || []).length;
        newCursor = oldCursor + (countNonDigitAfter - countNonDigitBefore);
      }

      phoneInput.value = formatted;
      phoneInput.setSelectionRange(newCursor, newCursor);
    });

    // Força máscara ao colar (trata paste/cut)
    phoneInput.addEventListener('paste', function () {
      setTimeout(() => {
        let numbers = phoneInput.value.replace(/\D/g, '').slice(0, 11);
        let formatted = '';
        if (numbers.length > 0) {
          formatted += '(' + numbers.substring(0, 2);
        }
        if (numbers.length > 2) {
          formatted += ') ' + numbers.substring(2, 7);
        }
        if (numbers.length > 7) {
          formatted += '-' + numbers.substring(7, 11);
        }
        phoneInput.value = formatted;
        phoneInput.setSelectionRange(phoneInput.value.length, phoneInput.value.length);
      }, 1);
    });
  });
});
