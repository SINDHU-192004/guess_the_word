document.addEventListener('DOMContentLoaded', function () {
  // Auto-uppercase guess input and limit to A-Z only
  const guessInput = document.querySelector('.guess-input');
  if (guessInput) {
    // Ensure field is cleared on load (after back/forward navigation)
    guessInput.value = '';

    guessInput.addEventListener('input', function (e) {
      let v = e.target.value.toUpperCase();
      v = v.replace(/[^A-Z]/g, '');
      e.target.value = v.slice(0, 5);
    });

    // Submit on Enter
    guessInput.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        const form = e.target.closest('form');
        if (form) form.submit();
      }
    });

    // Autofocus input
    guessInput.focus();

    // On submit: blur to hide soft keyboard and clear the field
    const form = guessInput.closest('form');
    if (form) {
      form.addEventListener('submit', function () {
        // Hide virtual keyboard
        guessInput.blur();
        // Clear value so it doesn't stick after navigation
        setTimeout(() => {
          guessInput.value = '';
        }, 0);
        // Optional: disable submit button to prevent double submit
        const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
        if (submitBtn) submitBtn.disabled = true;
      });
    }
  }
});
