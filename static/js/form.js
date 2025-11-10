// static/js/form.js
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('leadForm');
  const statusEl = document.getElementById('formStatus');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const payload = Object.fromEntries(new FormData(form));

    statusEl.textContent = 'Submitting…';
    statusEl.style.color = '#007bff';

    try {
      const resp = await fetch('/api/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await resp.json();

      statusEl.textContent = data.message;
      statusEl.style.color = data.success ? 'green' : 'red';

      if (data.success) form.reset();
    } catch (err) {
      statusEl.textContent = 'Network error: ' + err.message;
      statusEl.style.color = 'red';
    }
  });
});