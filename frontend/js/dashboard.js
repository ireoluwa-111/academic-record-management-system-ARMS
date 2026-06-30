/* ==========================================================================
   ARMS — dashboard.js (shared across all role dashboards)
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
  /* Mobile sidebar toggle */
  const sidebar = document.querySelector(".dash-sidebar");
  const toggleBtn = document.querySelector(".sidebar-toggle");
  const overlay = document.querySelector(".dash-overlay");

  const closeSidebar = () => {
    sidebar?.classList.remove("open");
    overlay?.classList.remove("show");
  };
  const openSidebar = () => {
    sidebar?.classList.add("open");
    overlay?.classList.add("show");
  };

  toggleBtn?.addEventListener("click", () => {
    sidebar?.classList.contains("open") ? closeSidebar() : openSidebar();
  });
  overlay?.addEventListener("click", closeSidebar);

  /* Randomize demo chart bar heights slightly for a "live" feel */
  document.querySelectorAll(".chart-placeholder .bar").forEach((bar) => {
    const base = parseInt(bar.dataset.height || "50", 10);
    bar.style.height = base + "%";
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
