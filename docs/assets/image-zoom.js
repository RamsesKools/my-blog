// Click-to-zoom lightbox for opt-in images (class="zoomable", added via
// Markdown attr_list, e.g. `![alt](img.png){: .zoomable }`). Not applied
// site-wide on purpose - only specific detailed diagrams/images opt in.
document.addEventListener("DOMContentLoaded", () => {
  const images = document.querySelectorAll("img.zoomable");
  if (!images.length) return;

  const overlay = document.createElement("div");
  overlay.className = "image-zoom-overlay";
  overlay.innerHTML =
    '<button class="image-zoom-close" aria-label="Close">&times;</button>' +
    '<img class="image-zoom-full" alt="">';
  document.body.appendChild(overlay);

  const fullImg = overlay.querySelector(".image-zoom-full");
  const closeBtn = overlay.querySelector(".image-zoom-close");

  function open(img) {
    fullImg.src = img.currentSrc || img.src;
    fullImg.alt = img.alt || "";
    overlay.classList.add("image-zoom-overlay--visible");
    document.body.classList.add("image-zoom-lock");
  }

  function close() {
    overlay.classList.remove("image-zoom-overlay--visible");
    document.body.classList.remove("image-zoom-lock");
  }

  images.forEach((img) => {
    img.addEventListener("click", () => open(img));
  });

  overlay.addEventListener("click", (event) => {
    if (event.target === overlay || event.target === fullImg) close();
  });
  closeBtn.addEventListener("click", close);

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && overlay.classList.contains("image-zoom-overlay--visible")) {
      close();
    }
  });
});
