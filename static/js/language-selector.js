/* static/js/language-selector.js
   Purpose: switch site language by navigating to /pl, /en, /de, /ukr
   Works with:
   - Native <select id="language-picker-select">…</select>
   - CodyHouse-style custom list with .language-picker__list and .language-picker__item
*/

(function () {
  // Build the target URL for a language code
  function getLanguageUrl(code) {
    if (!code) return '/';
    code = String(code).toLowerCase();

    // List of all supported language codes
    const supportedLanguages = ['pl', 'en', 'de', 'ukr'];

    // If the code is not supported, default to Polish
    if (!supportedLanguages.includes(code)) {
      code = 'pl';
    }

    return '/' + code;
  }

  // Prevent a form submit if the select sits inside a <form>
  function preventFormSubmit(selectEl) {
    if (!selectEl) return;
    var form = selectEl.closest('form');
    if (form) {
      form.addEventListener('submit', function (e) { e.preventDefault(); });
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    // 1) Native <select> support
    var select = document.getElementById('language-picker-select');
    if (select) {
      preventFormSubmit(select);
      select.addEventListener('change', function (e) {
        var code = e.target.value;
        window.location.assign(getLanguageUrl(code));
      });
    }

    // 2) CodyHouse-style custom dropdown (optional)
    var picker = document.querySelector('.language-picker');
    if (picker) {
      var list = picker.querySelector('.language-picker__list');
      if (list) {
        list.addEventListener('click', function (event) {
          var item = event.target.closest('.language-picker__item');
          if (!item) return;
          event.preventDefault();
          var code = item.getAttribute('data-value')
                  || item.getAttribute('lang')
                  || (item.textContent || '').trim().toLowerCase();
          window.location.assign(getLanguageUrl(code));
        });
      }

      // Also catch clicks on inner <a> if present
      picker.addEventListener('click', function (event) {
        var a = event.target.closest('.language-picker__item a');
        if (!a) return;
        event.preventDefault();
        var code = a.getAttribute('data-value')
                 || a.getAttribute('lang')
                 || (a.textContent || '').trim().toLowerCase();
        window.location.assign(getLanguageUrl(code));
      });
    }
  });
})();