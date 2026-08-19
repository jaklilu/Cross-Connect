import { buildGrids, renderTable } from "./family.js";
import { fetchFamily } from "./api.js";

document.getElementById("tooltip-toggle").addEventListener("click", () => {
  const tooltip = document.getElementById("tooltip");
  tooltip.style.display = tooltip.style.display === "none" ? "block" : "none";
});

async function main() {
  const params = new URLSearchParams(window.location.search);
  const index = Number(params.get("index") || 0);
  const data = await fetchFamily();
  const grids = buildGrids(data);
  if (index < 0 || index >= grids.length) {
    document.getElementById("grid").innerHTML =
      "<tr><td>Card not found.</td></tr>";
    return;
  }
  document.title = `Grid ${index + 1}`;
  document.getElementById("grid").innerHTML = renderTable(grids[index]);
}

main().catch((err) => {
  document.getElementById("grid").innerHTML = `<tr><td>${err.message}</td></tr>`;
});
