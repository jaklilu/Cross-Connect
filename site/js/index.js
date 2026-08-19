import { buildGrids, renderTable } from "./family.js";
import { fetchFamily } from "./api.js";

async function main() {
  const data = await fetchFamily();
  document.title = data.site_title || "My Webpage";
  document.getElementById("welcome").textContent = data.welcome || "Welcome to Cousin's CrossConnect!";
  document.getElementById("intro").textContent = data.intro || "";

  const grids = buildGrids(data);
  const container = document.getElementById("grids");
  container.innerHTML = grids
    .map((grid, index) => {
      const center = grid[1][1].trim();
      return (
        `<a href="/grid.html?index=${index}" class="grid-link">${grid[1][1]}</a>` +
        `<table>${renderTable(grid)}</table>`
      );
    })
    .join("");
}

main().catch((err) => {
  document.getElementById("grids").innerHTML = `<p style="color:red;">${err.message}</p>`;
});
