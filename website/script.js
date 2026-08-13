const copyButtons = document.querySelectorAll("[data-copy]");

async function copyText(text) {
  if (navigator.clipboard && window.isSecureContext) {
    try {
      await Promise.race([
        navigator.clipboard.writeText(text),
        new Promise((_, reject) => {
          window.setTimeout(() => reject(new Error("Clipboard timeout")), 500);
        }),
      ]);
      return;
    } catch {
      // Fall back when clipboard permissions are unavailable or the browser does not respond.
    }
  }

  const input = document.createElement("textarea");
  input.value = text;
  input.setAttribute("readonly", "");
  input.style.position = "fixed";
  input.style.opacity = "0";
  document.body.appendChild(input);
  input.select();
  const copied = document.execCommand("copy");
  input.remove();

  if (!copied) {
    throw new Error("Copy command failed");
  }
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
