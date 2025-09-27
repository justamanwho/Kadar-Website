/* static/js/language-selector.js
   Purpose: switch site language by navigating to /pl or /en.
   Works with:
   - Native <select id="language-picker-select">…</select>
   - CodyHouse-style custom list with .language-picker__list and .language-picker__item
*/

(function () {
  // Build the target URL for a language code
  function getLanguageUrl(code) {
    if (!code) return '/';
    code = String(code).toLowerCase();
    if (code !== 'pl' && code !== 'en') code = 'pl';
    return '/' + code; // → /pl or /en
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
    //    Expect markup like:
    //    <div class="language-picker">
    //      <div class="language-picker__dropdown">
    //        <ul class="language-picker__list">
    //          <li class="language-picker__item" data-value="pl">PL</li>
    //          <li class="language-picker__item" data-value="en">EN</li>
    //        </ul>
    //      </div>
    //    </div>
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
