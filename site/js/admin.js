import {
  GROUPS,
  addPerson,
  buildGrids,
  groupCounts,
  groupedPeople,
  movePerson,
  newYear,
  removePerson,
  renamePerson,
  updateSettings,
} from "./family.js";
import {
  clearAdminPassword,
  fetchFamily,
  getAdminPassword,
  login,
  saveFamily,
} from "./api.js";

let data = null;

function showMessage(text, isError = false) {
  const box = document.getElementById("message");
  box.innerHTML = `<div class="flash${isError ? " error" : ""}">${text}</div>`;
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function groupOptions(selected) {
  return GROUPS.map(
    ([key, label, help]) =>
      `<option value="${key}"${key === selected ? " selected" : ""}>${label}</option>`
  ).join("");
}

function renderAdmin() {
  const counts = groupCounts(data);
  const grouped = groupedPeople(data);
  const cardCount = buildGrids(data).length;

  const statCards = GROUPS.map(
    ([key, label]) =>
      `<div class="card"><strong>${counts[key] || 0}</strong>${label}</div>`
  ).join("");

  const groupSections = GROUPS.map(([key, label, help]) => {
    const people = grouped[key] || [];
    const rows = people.length
      ? people
          .map(
            (person) => `
        <tr>
          <td>${person.name}</td>
          <td>
            <form class="row-form move-form" data-name="${person.name}">
              <select name="group">${groupOptions(person.group)}</select>
              <button type="submit">Save age</button>
            </form>
            <form class="row-form rename-form" data-old="${person.name}">
              <input type="text" name="new_name" value="${person.name}" required>
              <button type="submit">Rename</button>
            </form>
          </td>
          <td>
            <form class="remove-form" data-name="${person.name}">
              <button class="danger" type="submit">Remove</button>
            </form>
          </td>
        </tr>`
          )
          .join("")
      : `<tr><td colspan="3" class="muted">No one in this group yet.</td></tr>`;

    return `
      <section>
        <h2>${label}</h2>
        <p class="help">${help}</p>
        <table>
          <tr><th>Name</th><th>Correct age / rename</th><th>Remove</th></tr>
          ${rows}
        </table>
      </section>`;
  }).join("");

  document.getElementById("admin-panel").innerHTML = `
    <div class="cards">
      <div class="card"><strong>${data.assignment_year}</strong>Assignment year</div>
      <div class="card"><strong>${data.people.length}</strong>People</div>
      <div class="card"><strong>${cardCount}</strong>Personal cards</div>
      ${statCards}
    </div>

    <section>
      <h2>Start a new year</h2>
      <p class="help">Reshuffles who sits left, right, top, and bottom on every card.</p>
      <button id="new-year-btn" class="year" type="button">Refresh pairings for ${Number(data.assignment_year) + 1}</button>
    </section>

    <section>
      <h2>Add a person</h2>
      <form id="add-form">
        <label for="add-name">Name</label>
        <input id="add-name" name="name" type="text" required>
        <label for="add-group">Age group</label>
        <select id="add-group" name="group">${groupOptions("20s30s")}</select>
        <div style="margin-top: 12px;"><button type="submit">Add person</button></div>
      </form>
    </section>

    ${groupSections}

    <section>
      <h2>Page text</h2>
      <form id="settings-form">
        <label for="site_title">Browser title</label>
        <input id="site_title" name="site_title" type="text" value="${data.site_title || ""}">
        <label for="welcome">Heading</label>
        <input id="welcome" name="welcome" type="text" value="${data.welcome || ""}">
        <label for="intro">Intro line</label>
        <textarea id="intro" name="intro">${data.intro || ""}</textarea>
        <div style="margin-top: 12px;"><button type="submit">Save text</button></div>
      </form>
    </section>
  `;

  bindAdminEvents();
}

async function persist(message) {
  await saveFamily(data);
  renderAdmin();
  showMessage(message);
}

function bindAdminEvents() {
  document.getElementById("new-year-btn").addEventListener("click", async () => {
    const next = Number(data.assignment_year) + 1;
    if (!window.confirm(`Reshuffle all pairings and move to ${next}?`)) return;
    try {
      newYear(data);
      await persist(`New year started. Pairings for ${data.assignment_year} are ready.`);
    } catch (err) {
      showMessage(err.message, true);
    }
  });

  document.getElementById("add-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.target;
    try {
      const name = addPerson(data, form.name.value, form.group.value);
      await persist(`Added ${name}.`);
      form.reset();
    } catch (err) {
      showMessage(err.message, true);
    }
  });

  document.getElementById("settings-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.target;
    try {
      updateSettings(data, form.welcome.value, form.intro.value, form.site_title.value);
      await persist("Page text saved.");
    } catch (err) {
      showMessage(err.message, true);
    }
  });

  document.querySelectorAll(".move-form").forEach((form) => {
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      try {
        const name = movePerson(data, form.dataset.name, new FormData(form).get("group"));
        await persist(`Updated age group for ${name}.`);
      } catch (err) {
        showMessage(err.message, true);
      }
    });
  });

  document.querySelectorAll(".rename-form").forEach((form) => {
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      try {
        const name = renamePerson(
          data,
          form.dataset.old,
          new FormData(form).get("new_name")
        );
        await persist(`Renamed to ${name}.`);
      } catch (err) {
        showMessage(err.message, true);
      }
    });
  });

  document.querySelectorAll(".remove-form").forEach((form) => {
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const name = form.dataset.name;
      if (!window.confirm(`Remove ${name}?`)) return;
      try {
        removePerson(data, name);
        await persist(`Removed ${name}.`);
      } catch (err) {
        showMessage(err.message, true);
      }
    });
  });
}

function showAdmin() {
  document.getElementById("login-panel").classList.add("hidden");
  document.getElementById("admin-panel").classList.remove("hidden");
  document.getElementById("sign-out").classList.remove("hidden");
  renderAdmin();
}

async function boot() {
  data = await fetchFamily();

  document.getElementById("login-btn").addEventListener("click", async () => {
    const password = document.getElementById("password").value;
    const ok = await login(password);
    if (!ok) {
      showMessage("That password did not match.", true);
      return;
    }
    showAdmin();
    showMessage("Signed in.");
  });

  document.getElementById("sign-out").addEventListener("click", () => {
    clearAdminPassword();
    document.getElementById("admin-panel").classList.add("hidden");
    document.getElementById("login-panel").classList.remove("hidden");
    document.getElementById("sign-out").classList.add("hidden");
    document.getElementById("password").value = "";
    showMessage("Signed out.");
  });

  if (getAdminPassword()) showAdmin();
}

boot().catch((err) => showMessage(err.message, true));
