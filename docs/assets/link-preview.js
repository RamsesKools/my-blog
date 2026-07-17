(function () {
  "use strict";

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
    var readtimeLabel = entry.readtime === 1 ? "1 min read" : entry.readtime + " min read";

    card.innerHTML =
      '<div class="link-preview-title">' + entry.title + draft + "</div>" +
      (entry.synopsis
        ? '<div class="link-preview-synopsis">' + entry.synopsis + "</div>"
        : "") +
      '<div class="link-preview-meta">' +
      (tags ? '<span class="link-preview-tags">' + tags + "</span>" : "") +
      '<span class="link-preview-info">' + entry.date + " &middot; " + readtimeLabel + "</span>" +
      "</div>";
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
