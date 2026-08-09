const copyButtons = document.querySelectorAll("[data-copy]");

async function copyText(text) {
  if (navigator.clipboard && window.isSecureContext) {
    await navigator.clipboard.writeText(text);
    return;
  }

  const input = document.createElement("textarea");
  input.value = text;
  input.setAttribute("readonly", "");
  input.style.position = "fixed";
  input.style.opacity = "0";
  document.body.appendChild(input);
  input.select();
  document.execCommand("copy");
  input.remove();
}

copyButtons.forEach((button) => {
  button.addEventListener("click", async () => {
    const originalLabel = button.textContent;

    try {
      await copyText(button.dataset.copy);
      button.textContent = "COPIED";
      button.dataset.copied = "true";
    } catch {
      button.textContent = "SELECT";
    }

    window.setTimeout(() => {
      button.textContent = originalLabel;
      delete button.dataset.copied;
    }, 1600);
  });
});
