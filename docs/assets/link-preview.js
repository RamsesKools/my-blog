(function () {
  "use strict";

  // Disable preview on mobile
  if (window.matchMedia && window.matchMedia("(hover: none), (pointer: coarse)").matches) {
    return;
  }

  var scriptUrl = document.currentScript && document.currentScript.src;
  var dataUrl = scriptUrl
    ? new URL("post-preview.json", scriptUrl).toString()
    : "post-preview.json";

  var fetchPromise = null;
  function loadData() {
    if (!fetchPromise) {
      fetchPromise = fetch(dataUrl)
        .then(function (r) { return r.json(); })
        .catch(function () { return {}; });
    }
    return fetchPromise;
  }

  var card = null;
  var showTimer = null;
  var hideTimer = null;

  function buildCard() {
    var el = document.createElement("div");
    el.className = "link-preview-card";
    el.setAttribute("role", "tooltip");
    document.body.appendChild(el);
    return el;
  }

  function renderCard(entry) {
    var tags = (entry.tags || [])
      .map(function (t) {
        return '<span class="md-tag-pill" data-tag="' + t + '">' + t + "</span>";
      })
      .join("");
    var draft = entry.draft
      ? ' <span class="tag-filter-draft-marker" title="Draft">Draft</span>'
      : "";

    var metaParts = [];
    if (tags) metaParts.push('<span class="link-preview-tags">' + tags + "</span>");
    if (entry.date) {
      var readtimeLabel = entry.readtime === 1 ? "1 min read" : entry.readtime + " min read";
      metaParts.push('<span class="link-preview-info">' + entry.date + " &middot; " + readtimeLabel + "</span>");
    }

    card.innerHTML =
      '<div class="link-preview-title">' + entry.title + draft + "</div>" +
      (entry.excerptHtml
        ? '<div class="link-preview-excerpt md-typeset">' + entry.excerptHtml + "</div>"
        : "") +
      (metaParts.length
        ? '<div class="link-preview-meta">' + metaParts.join("") + "</div>"
        : "");
  }

  // Images have no known height until they load, so measuring/trimming
  // right after setting innerHTML would see a 0-height <img> and either
  // skip trimming or cut in the wrong place; wait for every image in the
  // excerpt to settle (load or error) first.
  function whenImagesReady(container) {
    var imgs = container.querySelectorAll("img");
    var pending = [];
    for (var i = 0; i < imgs.length; i++) {
      var img = imgs[i];
      if (!img.complete) {
        pending.push(
          new Promise(function (resolve) {
            img.addEventListener("load", resolve, { once: true });
            img.addEventListener("error", resolve, { once: true });
          })
        );
      }
    }
    return pending.length ? Promise.all(pending) : Promise.resolve();
  }

  // Images and code blocks still read fine cropped part-way (you can tell
  // there's more), but prose cut off mid-sentence looks broken - so those
  // are the only element types we let the container's overflow: hidden
  // crop in place instead of dropping whole.
  function isImageBlock(el) {
    if (el.tagName === "IMG") return true;
    // Markdown wraps a lone image in its own <p>.
    return el.tagName === "P" && el.children.length === 1 && el.firstElementChild.tagName === "IMG";
  }

  function isCodeBlock(el) {
    return el.tagName === "PRE" || el.classList.contains("highlight"); // pymdownx.superfences wrapper
  }

  // The excerpt's max-height/overflow (see custom.css) is what actually
  // bounds it; here we measure the real (already-laid-out) content against
  // that box. Prose blocks that don't fit get dropped whole, so the cut
  // lands between elements instead of an arbitrary CSS clip mid-line;
  // images/code blocks are left in place and cropped by the container,
  // with a fade + "..." overlaid right at the cut.
  function trimExcerptToFit(excerptEl) {
    var maxHeight = excerptEl.clientHeight;
    if (excerptEl.scrollHeight <= maxHeight + 1) return;

    // Reserve headroom so the "…" indicator itself doesn't land past the
    // same max-height boundary and get clipped away by overflow: hidden.
    var budget = maxHeight - 20;
    var containerTop = excerptEl.getBoundingClientRect().top;
    var children = excerptEl.children;
    var cutIndex = -1;
    for (var i = 0; i < children.length; i++) {
      var bottom = children[i].getBoundingClientRect().bottom - containerTop;
      if (bottom > budget) {
        cutIndex = i;
        break;
      }
    }
    if (cutIndex === -1) return;

    var overflowing = children[cutIndex];
    if (isImageBlock(overflowing) || isCodeBlock(overflowing)) {
      while (excerptEl.children.length > cutIndex + 1) {
        excerptEl.removeChild(excerptEl.children[cutIndex + 1]);
      }
      // Fade signals "this is cropped, not broken" for both; the "…" is
      // only needed for code blocks, since a cropped image already reads
      // as "there's more" on its own.
      var fadeEl = document.createElement("div");
      fadeEl.className = "link-preview-crop-fade";
      if (isCodeBlock(overflowing)) fadeEl.textContent = "…";
      excerptEl.appendChild(fadeEl);
      return;
    }

    if (cutIndex === 0) {
      if (children.length === 1) return; // one block too tall to safely trim; let CSS clip it
      cutIndex = 1; // always keep at least the first block
    }
    while (excerptEl.children.length > cutIndex) {
      excerptEl.removeChild(excerptEl.children[cutIndex]);
    }

    var moreEl = document.createElement("div");
    moreEl.className = "link-preview-more";
    moreEl.textContent = "…";
    excerptEl.appendChild(moreEl);
  }

  function positionCard(link) {
    var margin = 8;
    var rect = link.getBoundingClientRect();
    var cardRect = card.getBoundingClientRect();

    var top = rect.bottom + margin;
    if (top + cardRect.height > window.innerHeight - margin) {
      top = rect.top - cardRect.height - margin;
    }
    if (top < margin) top = margin;

    var left = rect.left;
    if (left + cardRect.width > window.innerWidth - margin) {
      left = window.innerWidth - cardRect.width - margin;
    }
    if (left < margin) left = margin;

    card.style.top = top + window.scrollY + "px";
    card.style.left = left + window.scrollX + "px";
  }

  function hideCard() {
    if (card) card.classList.remove("link-preview-card--visible");
  }

  function showCardFor(link, entry) {
    if (!card) card = buildCard();
    renderCard(entry);
    card.classList.add("link-preview-card--visible");
    positionCard(link);

    var excerptEl = card.querySelector(".link-preview-excerpt");
    if (excerptEl) {
      whenImagesReady(excerptEl).then(function () {
        // Bail if this card has since been hidden or re-rendered for a
        // different link while we were waiting on images to load.
        if (!excerptEl.isConnected || !card.classList.contains("link-preview-card--visible")) return;
        trimExcerptToFit(excerptEl);
        positionCard(link);
      });
    }
  }

  function scheduleShow(link, entry) {
    clearTimeout(hideTimer);
    clearTimeout(showTimer);
    showTimer = setTimeout(function () {
      showCardFor(link, entry);
    }, 250);
  }

  function scheduleHide() {
    clearTimeout(showTimer);
    clearTimeout(hideTimer);
    hideTimer = setTimeout(hideCard, 150);
  }

  function onEnter(e) {
    var link = e.target.closest && e.target.closest("a[href]");
    if (!link) return;
    loadData().then(function (data) {
      var entry = data[link.pathname];
      if (!entry) return;
      scheduleShow(link, entry);
    });
  }

  function onLeave(e) {
    var link = e.target.closest && e.target.closest("a[href]");
    if (!link) return;
    scheduleHide();
  }

  document.addEventListener("mouseover", onEnter);
  document.addEventListener("mouseout", onLeave);
  document.addEventListener("focusin", onEnter);
  document.addEventListener("focusout", onLeave);
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") hideCard();
  });

  function markInternalLinks() {
    loadData().then(function (data) {
      var links = document.querySelectorAll("a[href]");
      for (var i = 0; i < links.length; i++) {
        if (data[links[i].pathname]) {
          links[i].classList.add("link-preview-internal");
        }
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", markInternalLinks);
  } else {
    markInternalLinks();
  }
})();
