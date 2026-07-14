(function () {
  "use strict";

  function initTagFilter(root) {
    var cloud = root.querySelector("[data-tag-filter-cloud]");
    var list = root.querySelector("[data-tag-filter-list]");
    var empty = root.querySelector("[data-tag-filter-empty]");
    if (!cloud || !list) return;

    var selected = new Set();
    var rows = Array.prototype.slice.call(list.querySelectorAll(".tag-filter-row"));
    var buttons = Array.prototype.slice.call(cloud.querySelectorAll("[data-tag]"));

    function rowTags(row) {
      var raw = row.getAttribute("data-tags") || "";
      return raw ? raw.split(",") : [];
    }

    function applyFilter() {
      var anyVisible = false;
      rows.forEach(function (row) {
        var tags = rowTags(row);
        var visible = selected.size === 0 || tags.some(function (t) { return selected.has(t); });
        row.classList.toggle("tag-filter-row--hidden", !visible);
        if (visible) anyVisible = true;
      });
      if (empty) empty.style.display = anyVisible ? "none" : "block";
    }

    buttons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var tag = btn.getAttribute("data-tag");
        var isSelected = selected.has(tag);
        if (isSelected) {
          selected.delete(tag);
        } else {
          selected.add(tag);
        }
        btn.classList.toggle("md-tag-pill--selected", !isSelected);
        btn.setAttribute("aria-pressed", String(!isSelected));
        applyFilter();
      });
    });
  }

  function init() {
    document.querySelectorAll("[data-tag-filter]").forEach(initTagFilter);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
