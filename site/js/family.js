export const BASE_YEAR = 2026;

export const GROUPS = [
  ["under12", "Under 12", "Bottom of each card — encourage and mentor"],
  ["20s30s", "20s & 30s", "Gets a personal card; chats with the same age group on the right"],
  ["30s40s", "30s & 40s", "Gets a personal card; chats with the same age group on the right"],
  ["50s60s", "50s & 60s", "Gets a personal card; chats with the same age group on the right"],
  ["65plus", "65 & over", "Top of each card — call and check on"],
];

export const GROUP_LISTS = {
  under12: ["kids_20s", "kids_30s", "kids_50s"],
  "20s30s": ["twenties", "twenties_for_30s"],
  "30s40s": ["thirties", "thirties_for_20s", "thirties_for_50s"],
  "50s60s": ["fifties"],
  "65plus": ["elders_20s", "elders_30s", "elders_50s"],
};

function pick(names, index) {
  if (!names || !names.length) return "";
  return names[index % names.length];
}

function formatValue(value) {
  if ([1, 3, 7, 9, null, undefined, ""].includes(value)) return "";
  const s = String(value);
  const width = 12;
  const pad = Math.max(0, width - s.length);
  const left = Math.floor(pad / 2);
  return " ".repeat(left) + s + " ".repeat(pad - left);
}

function makeCards(centers, rightGroup, leftGroup, elders, kids, offset = 0) {
  return centers.map((name, i) => {
    const grid = [
      [1, pick(elders, i + offset), 3],
      [pick(leftGroup, i + offset), name, pick(rightGroup, i + 1 + offset)],
      [7, pick(kids, i + offset), 9],
    ];
    return grid.map((row) => row.map(formatValue));
  });
}

export function yearOffset(data) {
  return Number(data.assignment_year || BASE_YEAR) - BASE_YEAR;
}

export function buildGrids(data) {
  const lists = data.lists || {};
  const offset = yearOffset(data);
  return [
    ...makeCards(
      lists.twenties || [],
      lists.twenties || [],
      lists.thirties_for_20s || [],
      lists.elders_20s || [],
      lists.kids_20s || [],
      offset
    ),
    ...makeCards(
      lists.thirties || [],
      lists.thirties || [],
      lists.twenties_for_30s || [],
      lists.elders_30s || [],
      lists.kids_30s || [],
      offset
    ),
    ...makeCards(
      lists.fifties || [],
      lists.fifties || [],
      lists.thirties_for_50s || [],
      lists.elders_50s || [],
      lists.kids_50s || [],
      offset
    ),
  ];
}

export function findPerson(data, name) {
  const key = name.trim().toLowerCase();
  return data.people.find((p) => p.name.toLowerCase() === key) || null;
}

export function groupCounts(data) {
  const counts = Object.fromEntries(GROUPS.map(([key]) => [key, 0]));
  for (const person of data.people) counts[person.group] = (counts[person.group] || 0) + 1;
  return counts;
}

export function groupedPeople(data) {
  const grouped = Object.fromEntries(GROUPS.map(([key]) => [key, []]));
  for (const person of data.people) grouped[person.group].push({ ...person });
  for (const list of Object.values(grouped)) {
    list.sort((a, b) => a.name.localeCompare(b.name, undefined, { sensitivity: "base" }));
  }
  return grouped;
}

function removeFromLists(data, name) {
  for (const names of Object.values(data.lists)) {
    while (names.includes(name)) names.splice(names.indexOf(name), 1);
  }
}

function addToGroupLists(data, name, group) {
  for (const listName of GROUP_LISTS[group]) {
    if (!data.lists[listName]) data.lists[listName] = [];
    if (!data.lists[listName].includes(name)) data.lists[listName].push(name);
  }
}

export function addPerson(data, name, group) {
  name = name.trim().replace(/\s+/g, " ");
  if (!name) throw new Error("Name is required.");
  if (!GROUP_LISTS[group]) throw new Error("Choose a valid age group.");
  if (findPerson(data, name)) throw new Error(`${name} is already in the family list.`);
  data.people.push({ name, group });
  addToGroupLists(data, name, group);
  return name;
}

export function removePerson(data, name) {
  const person = findPerson(data, name);
  if (!person) throw new Error(`${name} was not found.`);
  data.people = data.people.filter((p) => p.name !== person.name);
  removeFromLists(data, person.name);
  return person.name;
}

export function movePerson(data, name, newGroup) {
  if (!GROUP_LISTS[newGroup]) throw new Error("Choose a valid age group.");
  const person = findPerson(data, name);
  if (!person) throw new Error(`${name} was not found.`);
  if (person.group === newGroup) return person.name;
  removeFromLists(data, person.name);
  person.group = newGroup;
  addToGroupLists(data, person.name, newGroup);
  return person.name;
}

export function renamePerson(data, oldName, newName) {
  newName = newName.trim().replace(/\s+/g, " ");
  if (!newName) throw new Error("New name is required.");
  const person = findPerson(data, oldName);
  if (!person) throw new Error(`${oldName} was not found.`);
  const other = findPerson(data, newName);
  if (other && other.name !== person.name) throw new Error(`${newName} is already in the family list.`);
  const old = person.name;
  person.name = newName;
  for (const names of Object.values(data.lists)) {
    for (let i = 0; i < names.length; i += 1) {
      if (names[i] === old) names[i] = newName;
    }
  }
  return newName;
}

export function updateSettings(data, welcome, intro, siteTitle) {
  data.welcome = welcome.trim() || data.welcome;
  data.intro = intro.trim();
  data.site_title = siteTitle.trim() || data.site_title;
}

export function formatRefreshDate(iso) {
  if (!iso) return "Not yet";
  return new Date(`${iso}T12:00:00`).toLocaleDateString(undefined, {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

export function newYear(data) {
  data.assignment_year = Number(data.assignment_year || BASE_YEAR) + 1;
  data.last_refreshed = new Date().toISOString().slice(0, 10);
  return data.assignment_year;
}

export function renderTable(grid) {
  return grid
    .map(
      (row) =>
        "<tr>" +
        row.map((cell) => `<td>${cell ? cell : "&nbsp;"}</td>`).join("") +
        "</tr>"
    )
    .join("");
}
