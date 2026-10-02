const form = document.querySelector('#fraud-form');
const input = document.querySelector('#event-json');
const button = form.querySelector('button');
const result = document.querySelector('#result');

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  result.hidden = false;

  let body;
  try {
    body = JSON.stringify(JSON.parse(input.value));
  } catch (error) {
    result.textContent = `Invalid JSON: ${error.message}`;
    return;
  }

  button.disabled = true;
  const analyzingFrames = ['Analyzing.', 'Analyzing..', 'Analyzing...'];
  let analyzingFrame = 0;
  result.textContent = analyzingFrames[analyzingFrame];
  const analyzingAnimation = setInterval(() => {
    analyzingFrame = (analyzingFrame + 1) % analyzingFrames.length;
    result.textContent = analyzingFrames[analyzingFrame];
  }, 400);

  try {
    const response = await fetch('/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body,
    });
    const data = await response.json();
    result.textContent = JSON.stringify(data, null, 2);
  } catch (error) {
    result.textContent = `Request failed: ${error.message}`;
  } finally {
    clearInterval(analyzingAnimation);
    button.disabled = false;
  }
});
