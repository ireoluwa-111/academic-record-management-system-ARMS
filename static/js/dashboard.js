/* ==========================================================================
   ARMS — dashboard.js (shared across all role dashboards)
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
  const shell    = document.querySelector(".dash-shell");
  const sidebar  = document.querySelector(".dash-sidebar");
  const toggleBtn = document.querySelector(".sidebar-toggle");
  const overlay  = document.querySelector(".dash-overlay");

  /* ── Desktop collapse (icon-rail) ── */
  const STORAGE_KEY = "arms_sidebar_collapsed";
  const isMobile = () => window.innerWidth < 992;

  // Helper to update button tooltip and icon direction
  const updateCollapseState = (isCollapsed) => {
    const icon = document.querySelector(".sidebar-collapse-btn .collapse-icon");
    const btn = document.querySelector(".sidebar-collapse-btn");
    if (isCollapsed) {
      if (icon) {
        icon.classList.remove("bi-chevron-left");
        icon.classList.add("bi-chevron-right");
      }
      if (btn) {
        btn.setAttribute("data-tooltip", "Expand Sidebar");
      }
    } else {
      if (icon) {
        icon.classList.remove("bi-chevron-right");
        icon.classList.add("bi-chevron-left");
      }
      if (btn) {
        btn.setAttribute("data-tooltip", "Collapse Sidebar");
      }
    }
  };

  // Restore saved state on page load (desktop only)
  if (!isMobile() && localStorage.getItem(STORAGE_KEY) === "1") {
    shell?.classList.add("sidebar-collapsed");
    updateCollapseState(true);
  }

  const toggleDesktopCollapse = () => {
    const collapsed = shell?.classList.toggle("sidebar-collapsed");
    localStorage.setItem(STORAGE_KEY, collapsed ? "1" : "0");
    updateCollapseState(collapsed);
  };

  /* ── Mobile slide-in overlay ── */
  const closeMobileSidebar = () => {
    sidebar?.classList.remove("open");
    overlay?.classList.remove("show");
  };
  const openMobileSidebar = () => {
    sidebar?.classList.add("open");
    overlay?.classList.add("show");
  };

  // Dedicated sidebar collapse trigger on desktop
  const collapseBtn = document.querySelector(".sidebar-collapse-btn");
  collapseBtn?.addEventListener("click", (e) => {
    e.preventDefault();
    toggleDesktopCollapse();
  });

  toggleBtn?.addEventListener("click", () => {
    if (isMobile()) {
      sidebar?.classList.contains("open") ? closeMobileSidebar() : openMobileSidebar();
    } else {
      toggleDesktopCollapse();
    }
  });
  overlay?.addEventListener("click", closeMobileSidebar);

  /* Randomize demo chart bar heights slightly for a "live" feel */
  document.querySelectorAll(".chart-placeholder .bar").forEach((bar) => {
    const base = parseInt(bar.dataset.height || "50", 10);
    bar.style.height = base + "%";
  });

  /* Apply progress bar widths from data-progress attribute */
  document.querySelectorAll(".bar-fill[data-progress]").forEach((bar) => {
    bar.style.width = (bar.dataset.progress || "0") + "%";
  });

  /* Animate GPA ring stroke based on data-value (0-100) */
  document.querySelectorAll(".gpa-ring circle.ring-progress").forEach((circle) => {
    const value = parseFloat(circle.closest(".gpa-ring").dataset.value || "0");
    const radius = circle.r.baseVal.value;
    const circumference = 2 * Math.PI * radius;
    circle.style.strokeDasharray = `${circumference} ${circumference}`;
    circle.style.strokeDashoffset = circumference - (value / 100) * circumference;
  });

  /* Simple table search filter (Registrar / Admin tables) */
  document.querySelectorAll("[data-table-search]").forEach((input) => {
    const tableId = input.getAttribute("data-table-search");
    const table = document.getElementById(tableId);
    if (!table) return;
    input.addEventListener("input", () => {
      const q = input.value.trim().toLowerCase();
      table.querySelectorAll("tbody tr").forEach((row) => {
        row.style.display = row.textContent.toLowerCase().includes(q) ? "" : "none";
      });
    });
  });
});
