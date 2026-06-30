const DEVICE_INFO = {
  "0111": { type: "Licht", circuit: "A", description: "spots devant meubles cuisine", room: "Cuisine", address: "1.11" },
  "0110": { type: "Licht", circuit: "A", description: "spots hall d'entrée", room: "Hall d'entrée", address: "1.10" },
  "0112": { type: "Licht", circuit: "A", description: "spots îlot cuisine", room: "Cuisine", address: "1.12" },
  "0113": { type: "Licht", circuit: "A", description: "groupe 5 spots salon", room: "Salon", address: "1.13" },
  "0114": { type: "Licht", circuit: "A", description: "spots hall 1er étage", room: "Hall 1er étage", address: "1.14" },
  "0115": { type: "Licht", circuit: "A", description: "spots hall chambres", room: "Hall chambres", address: "1.15" },
  "0001": { type: "Licht", circuit: "B", description: "point lumineux sol jardin", room: "Jardin", address: "0.1" },
  "0002": { type: "Licht", circuit: "B", description: "points lumineux terrasse salon façade", room: "Terrasse salon", address: "0.2" },
  "0003": { type: "Licht", circuit: "B", description: "points lumineux terrasse salon encastrés", room: "Terrasse salon", address: "0.3" },
  "0004": { type: "Licht", circuit: "B", description: "point lumineux sol entrée extérieur", room: "Entrée extérieur", address: "0.4" },
  "0005": { type: "Steckdose", circuit: "B", description: "prise commandée salle à manger", room: "Salle à manger", address: "0.5" },
  "0006": { type: "Licht", circuit: "B", description: "applique dressing", room: "Dressing", address: "0.6" },
  "0007": { type: "Licht", circuit: "B", description: "spot cheminée", room: "Cheminée", address: "0.7" },
  "0008": { type: "Licht", circuit: "B", description: "combles", room: "Combles", address: "0.8" },
  "0009": { type: "Licht", circuit: "C", description: "applique salle de douche", room: "Salle de douche", address: "0.9" },
  "0010": { type: "Licht", circuit: "C", description: "applique salle de bain", room: "Salle de bain", address: "0.10" },
  "0011": { type: "Licht", circuit: "C", description: "cellier cuisine", room: "Cellier cuisine", address: "0.11" },
  "0012": { type: "Licht", circuit: "C", description: "buanderie", room: "Buanderie", address: "0.12" },
  "0013": { type: "Licht", circuit: "C", description: "buanderie", room: "Buanderie", address: "0.13" },
  "0015": { type: "Licht", circuit: "C", description: "points lumineux garage", room: "Garage", address: "0.15" },
  "0101": { type: "Licht", circuit: "C", description: "combles", room: "Combles", address: "1.1" },
  "0102": { type: "Steckdose", circuit: "D", description: "prise commandée hall d'entrée", room: "Hall d'entrée", address: "1.2" },
  "0103": { type: "Licht", circuit: "D", description: "point lumineux terrasse cuisine", room: "Terrasse cuisine", address: "1.3" },
  "0104": { type: "Licht", circuit: "D", description: "local technique", room: "Local technique", address: "1.4" },
  "0413": { type: "Licht", circuit: "E", description: "groupe 2 spots cuisine", room: "Cuisine", address: "4.13" },
  "0509": { type: "Licht", circuit: "E", description: "brick escalier haut", room: "Escalier", address: "5.9" },
  "0406": { type: "Licht", circuit: "E", description: "point lumineux table cuisine", room: "Cuisine", address: "4.6" },
  "0407": { type: "Licht", circuit: "E", description: "spots chambre enfant avant", room: "Chambre enfant avant", address: "4.7" },
  "0508": { type: "Licht", circuit: "E", description: "spots chambre enfants arrière", room: "Chambre enfants arrière", address: "5.8" },
  "0409": { type: "Licht", circuit: "E", description: "groupe 4 spots salle à manger", room: "Salle à manger", address: "4.9" },
  "0411": { type: "Licht", circuit: "E", description: "point lumineux table salle à manger", room: "Salle à manger", address: "4.11" },
  "0415": { type: "Licht", circuit: "F", description: "spots douche salle de douche", room: "Salle de douche", address: "4.15" },
  "0414": { type: "Licht", circuit: "F", description: "groupe 3 spots salle de douche", room: "Salle de douche", address: "4.14" },
  "0404": { type: "Licht", circuit: "F", description: "2 spots baignoire", room: "Salle de bain", address: "4.4" },
  "0506": { type: "Licht", circuit: "F", description: "spots salle de bain", room: "Salle de bain", address: "5.6" },
  "0410": { type: "Licht", circuit: "F", description: "2 spots coin TV", room: "Salon", address: "4.10" },
  "0405": { type: "Licht", circuit: "G", description: "spots douche salle de bain", room: "Salle de bain", address: "4.5" },
  "0408": { type: "Licht", circuit: "G", description: "spots WC", room: "WC", address: "4.8" },
  "0401": { type: "Licht", circuit: "G", description: "spots salle de jeux (baby-foot)", room: "Salle de jeux", address: "4.1" },
  "0502": { type: "Licht", circuit: "G", description: "spots salle de jeux (centre)", room: "Salle de jeux", address: "5.2" },
  "0504": { type: "Licht", circuit: "G", description: "spot salle de jeux (TV)", room: "Salle de jeux", address: "5.4" },
  "0412": { type: "Licht", circuit: "G", description: "spots chambre parents", room: "Chambre parents", address: "4.12" },
  "0503": { type: "Licht", circuit: "G", description: "spots dressing", room: "Dressing", address: "5.3" },
  "0402": { type: "Licht", circuit: "H", description: "spots bureau", room: "Bureau", address: "4.2" },
  "0510": { type: "Licht", circuit: "H", description: "spots bureau", room: "Bureau", address: "5.10" },
  "0403": { type: "Licht", circuit: "H", description: "cheminée", room: "Cheminée", address: "4.3" },
  "0507": { type: "Steckdose", circuit: "H", description: "prise commandée salle à manger", room: "Salle à manger", address: "5.7" },
  "0501": { type: "Steckdose", circuit: "H", description: "prise commandée salon", room: "Salon", address: "5.1" },
  "0310": { type: "Rollladen", circuit: "I", description: "volet chambre enfants arrière", room: "Chambre enfants arrière", address: "3.10" },
  "0311": { type: "Rollladen", circuit: "I", description: "volet chambre enfants arrière", room: "Chambre enfants arrière", address: "3.11" },
  "0312": { type: "Rollladen", circuit: "I", description: "volet bureau", room: "Bureau", address: "3.12" },
  "0313": { type: "Rollladen", circuit: "I", description: "volet bureau", room: "Bureau", address: "3.13" },
  "0201": { type: "Rollladen", circuit: "I", description: "volet salle de jeux", room: "Salle de jeux", address: "2.1" },
  "0202": { type: "Rollladen", circuit: "I", description: "volet dressing", room: "Dressing", address: "2.2" },
  "0203": { type: "Rollladen", circuit: "I", description: "volet chambre enfants avant", room: "Chambre enfants avant", address: "2.3" },
  "0204": { type: "Rollladen", circuit: "I", description: "volet chambre enfants avant", room: "Chambre enfants avant", address: "2.4" },
  "0206": { type: "Rollladen", circuit: "J", description: "volet salle de bain", room: "Salle de bain", address: "2.6" },
  "0205": { type: "Rollladen", circuit: "J", description: "volet salle de douche", room: "Salle de douche", address: "2.5" },
  "0209": { type: "Rollladen", circuit: "J", description: "volet salon droit/gauche", room: "Salon", address: "2.9" },
  "0212": { type: "Rollladen", circuit: "J", description: "volet salon droit/gauche", room: "Salon", address: "2.12" },
  "0210": { type: "Rollladen", circuit: "J", description: "volet salle à manger", room: "Salle à manger", address: "2.10" },
  "0211": { type: "Rollladen", circuit: "J", description: "volet salle à manger", room: "Salle à manger", address: "2.11" },
  "0208": { type: "Rollladen", circuit: "J", description: "volet hall chambre", room: "Hall chambre", address: "2.8" },
  "0207": { type: "Rollladen", circuit: "J", description: "volet chambre parents", room: "Chambre parents", address: "2.7" },
  "0213": { type: "Rollladen", circuit: "K", description: "volet salon centre", room: "Salon", address: "2.13" },
  "0214": { type: "Rollladen", circuit: "K", description: "volet WC", room: "WC", address: "2.14" },
  "0215": { type: "Rollladen", circuit: "K", description: "volet hall 1er", room: "Hall 1er étage", address: "2.15" },
  "0301": { type: "Rollladen", circuit: "K", description: "volet cuisine", room: "Cuisine", address: "3.1" },
  "0302": { type: "Rollladen", circuit: "K", description: "volet cuisine", room: "Cuisine", address: "3.2" },
  "0303": { type: "Rollladen", circuit: "K", description: "volet cuisine", room: "Cuisine", address: "3.3" },
  "0304": { type: "Rollladen", circuit: "K", description: "volet cuisine", room: "Cuisine", address: "3.4" },
  "0305": { type: "Rollladen", circuit: "K", description: "volet cuisine", room: "Cuisine", address: "3.5" },
};

const ADDRESS_MODELS = {
  "0201": "F411/4",
  "0202": "F411/4",
  "0203": "F411/4",
  "0204": "F411/4",
  "0205": "F411/4",
  "0206": "F411/4",
  "0207": "F411/4",
  "0208": "F411/4",
  "0209": "F411/4",
  "0210": "F411/4",
  "0211": "F411/4",
  "0212": "F411/4",
  "0213": "F411/4",
  "0214": "F411/4",
  "0215": "F411/4",
  "0301": "F411/4",
  "0302": "F411/4",
  "0303": "F411/4",
  "0304": "F411/4",
  "0305": "F411/4",
  "0310": "F411/4",
  "0311": "F411/4",
  "0312": "F411/4",
  "0313": "F411/4",
  "0110": "F417U2",
  "0111": "F417U2",
  "0112": "F417U2",
  "0113": "F417U2",
  "0114": "F417U2",
  "0115": "F417U2",
  "0401": "F418",
  "0402": "F418",
  "0403": "F418",
  "0404": "F418",
  "0405": "F418",
  "0406": "F418",
  "0407": "F418",
  "0408": "F418",
  "0409": "F418",
  "0410": "F418",
  "0411": "F418",
  "0412": "F418",
  "0413": "F418",
  "0414": "F418",
  "0415": "F418",
  "0501": "F418",
  "0502": "F418",
  "0503": "F418",
  "0504": "F418",
  "0506": "F418",
  "0507": "F418",
  "0508": "F418",
  "0509": "F418",
  "0510": "F418",
};

Object.entries(ADDRESS_MODELS).forEach(([where, model]) => {
  DEVICE_INFO[where] = {
    ...(DEVICE_INFO[where] || { address: `${Number(where.slice(0, 2))}.${Number(where.slice(2))}` }),
    model,
  };
});

const HARDWARE_MODELS = [
  "067219",
  "BMSW1005",
  "F411/4",
  "F417U2",
  "F418",
  "F422",
  "F430R8",
  "H4652/2",
  "HC/HS/HD4659",
  "LN4652",
  "LN4691",
];

const DIMMER_MODELS = new Set(["F418", "F430R8"]);

function getMessageParts(raw) {
  const message = String(raw || "")
    .replace(/^`|`$/g, "")
    .replace(/##$/, "");
  const body = message.startsWith("*#")
    ? message.slice(2)
    : message.startsWith("*")
      ? message.slice(1)
      : message;
  return body
    .split("*")
    .filter(Boolean);
}

function findDeviceInfo(raw, parts = getMessageParts(raw)) {
  const message = String(raw || "");
  for (const part of parts) {
    if (DEVICE_INFO[part]) {
      return { where: part, ...DEVICE_INFO[part] };
    }
  }
  for (const where of Object.keys(DEVICE_INFO)) {
    if (message.includes(where)) {
      return { where, ...DEVICE_INFO[where] };
    }
  }
  return {};
}

function parseTelegram(raw) {
  const message = String(raw || "");
  const isStatus = message.startsWith("*#");
  const parts = getMessageParts(message);
  const who = parts[0] || "";
  const device = findDeviceInfo(message, parts);
  let action = "";
  let value = "";
  let decoded = "";

  if (who === "1") {
    if (isStatus) {
      action = parts.length > 3 ? "Statusantwort" : "Statusabfrage";
      if (parts.length > 3) {
        const statusValue = Number(parts[3]);
        if (statusValue === 100) {
          value = "Aus";
        } else if (statusValue >= 101 && statusValue <= 200) {
          value = `${statusValue - 100}%`;
        } else if (!Number.isNaN(statusValue)) {
          value = String(statusValue);
        }
        decoded = value ? `Lichtstatus: ${value}` : "";
      }
    } else if (parts[1] === "1") {
      action = "Ein";
      decoded = "Lichtbefehl: Ein";
    } else if (parts[1] === "0") {
      action = "Aus";
      decoded = "Lichtbefehl: Aus";
    } else if (parts[1] === "9") {
      action = "Dimmer/Level";
      decoded = "Lichtbefehl: Dimmer/Level";
    } else if (parts[1]) {
      action = `Licht ${parts[1]}`;
      decoded = action;
    }
  } else if (who === "2") {
    if (parts[1] === "1") {
      action = "Öffnen/Hoch";
      decoded = "Rollladenbefehl: Öffnen/Hoch";
    } else if (parts[1] === "2") {
      action = "Schließen/Runter";
      decoded = "Rollladenbefehl: Schließen/Runter";
    } else if (parts[1] === "0") {
      action = "Stopp";
      decoded = "Rollladenbefehl: Stopp";
    } else if (isStatus) {
      action = parts.length > 3 ? "Statusantwort" : "Statusabfrage";
      decoded = parts.length > 3 ? `Rollladenstatus: ${parts.slice(2).join("/")}` : action;
    } else if (parts[1]) {
      action = `Rollladen ${parts[1]}`;
      decoded = action;
    }
  } else if (who === "4") {
    action = isStatus ? "Temperatur/Heizung Status" : "Temperatur/Heizung";
    decoded = `${action}: ${parts.slice(1).join("/")}`;
  } else if (who === "18") {
    action = isStatus ? "Energie Status" : "Energie";
    decoded = `${action}: ${parts.slice(1).join("/")}`;
  } else if (who) {
    action = isStatus ? `WHO ${who} Status` : `WHO ${who}`;
    decoded = `${action}: ${parts.slice(1).join("/")}`;
  }

  return {
    ...device,
    who,
    action,
    value,
    decoded,
  };
}

function mergeParsedTelegram(entry) {
  const backendParsed = entry.parsed || {};
  const frontendParsed = parseTelegram(entry.telegram || entry.raw);
  return {
    ...frontendParsed,
    ...Object.fromEntries(
      Object.entries(backendParsed).filter(([, value]) => value !== undefined && value !== null && value !== ""),
    ),
  };
}

function escapeCsv(value) {
  return `"${String(value ?? "").replaceAll('"', '""')}"`;
}

function compactJson(value) {
  if (!value || (typeof value === "object" && !Object.keys(value).length)) return "";
  try {
    return JSON.stringify(value);
  } catch (err) {
    return String(value);
  }
}

function inferAutoEntityOptions(parsed) {
  const model = String(parsed.model || "").toUpperCase();
  if (model === "F411/4") {
    return { platform: "cover", advanced: false };
  }
  if (model === "F417U2") {
    return { platform: "light", dimmable: false };
  }
  if (DIMMER_MODELS.has(model)) {
    return { platform: "light", dimmable: true };
  }

  const text = [
    parsed.type,
    parsed.description,
    parsed.room,
    parsed.decoded,
  ].join(" ").toLowerCase();

  if (text.includes("steckdose") || text.includes("prise command")) {
    return { platform: "switch", class: "outlet" };
  }
  if (text.includes("thermostat") || text.includes("heizung") || text.includes("chauffage")) {
    return { platform: "climate", heat: true, cool: false, fan: false, standalone: false, central: false };
  }
  if (text.includes("rollladen") || text.includes("volet")) {
    return { platform: "cover", advanced: false };
  }
  if (text.includes("dimmer")) {
    return { platform: "light", dimmable: true };
  }
  if (
    text.includes("licht")
    || text.includes("spot")
    || text.includes("applique")
    || text.includes("point lumineux")
  ) {
    return { platform: "light", dimmable: false };
  }

  return { platform: parsed.suggested_domain || parsed.domain || "light" };
}

class ZmartMyhomePanel extends HTMLElement {
  set hass(hass) {
    this._hass = hass;
    this._collapsedGroups = this._collapsedGroups || new Set();
    this.render();
    this.renderRows();
  }

  connectedCallback() {
    this._collapsedGroups = this._collapsedGroups || new Set();
    this.render();
    this.loadData();
    this._interval = window.setInterval(() => this.loadData(), 1000);
  }

  disconnectedCallback() {
    if (this._interval) {
      window.clearInterval(this._interval);
      this._interval = undefined;
    }
  }

  render() {
    if (this._rendered) return;
    this._rendered = true;

    this.innerHTML = `
      <style>
        .page {
          padding: 24px;
          font-family: var(--paper-font-body1_-_font-family);
        }
        .card {
          background: var(--card-background-color);
          border-radius: 8px;
          padding: 24px;
          box-shadow: var(--ha-card-box-shadow);
        }
        h1 {
          margin-top: 0;
          color: var(--primary-color);
        }
        .status {
          color: var(--secondary-text-color);
          margin-bottom: 16px;
        }
        .toolbar {
          display: grid;
          grid-template-columns: minmax(180px, 1fr) repeat(4, minmax(120px, 180px)) minmax(150px, 190px) minmax(150px, 190px) auto auto auto auto;
          gap: 8px;
          margin-bottom: 16px;
          align-items: center;
        }
        input,
        select,
        button {
          background: var(--card-background-color);
          border: 1px solid var(--divider-color);
          border-radius: 6px;
          color: var(--primary-text-color);
          font: inherit;
          min-height: 36px;
          padding: 0 10px;
        }
        button {
          cursor: pointer;
        }
        button.primary {
          background: #1b7f46;
          border-color: #1b7f46;
          color: #fff;
          font-weight: 700;
        }
        button.primary:disabled {
          cursor: wait;
          opacity: 0.65;
        }
        .table-wrap {
          overflow-x: auto;
        }
        table {
          border-collapse: collapse;
          width: 100%;
          min-width: 1480px;
        }
        th,
        td {
          border-bottom: 1px solid var(--divider-color);
          padding: 8px;
          text-align: left;
          vertical-align: top;
        }
        th {
          color: var(--secondary-text-color);
          font-weight: 500;
        }
        .group-row td {
          background: rgba(27, 127, 70, 0.14);
          color: var(--primary-text-color);
          font-weight: 700;
          position: sticky;
          top: 0;
          z-index: 1;
        }
        .group-toggle {
          align-items: center;
          background: transparent;
          border: 0;
          color: inherit;
          display: inline-flex;
          font: inherit;
          font-weight: 700;
          gap: 8px;
          min-height: 0;
          padding: 0;
          text-align: left;
        }
        .group-toggle-icon {
          display: inline-block;
          font-size: 14px;
          width: 16px;
        }
        code {
          color: var(--primary-color);
          white-space: pre-wrap;
          word-break: break-word;
        }
        .direction-badge {
          border-radius: 999px;
          color: #fff;
          display: inline-block;
          font-size: 12px;
          font-weight: 700;
          line-height: 1;
          min-width: 52px;
          padding: 5px 8px;
          text-align: center;
          text-transform: uppercase;
        }
        .direction-in {
          background: #2e7d32;
        }
        .direction-out {
          background: #1565c0;
        }
        .direction-status {
          background: #ef6c00;
        }
        .empty {
          color: var(--secondary-text-color);
          padding: 24px 0 0;
        }
        @media (max-width: 900px) {
          .toolbar {
            grid-template-columns: 1fr 1fr;
          }
        }
      </style>

      <div class="page">
        <div class="card">
          <h1>Zmart-Home Live Bus Monitor</h1>
          <div class="status" id="status">Warte auf Telegramme...</div>
          <div class="toolbar">
            <input id="search" type="search" placeholder="Suche">
            <select id="type-filter"><option value="">Alle Typen</option></select>
            <select id="room-filter"><option value="">Alle Räume</option></select>
            <select id="direction-filter">
              <option value="">Alle Richtungen</option>
              <option value="in">in</option>
              <option value="out">out</option>
              <option value="status">status</option>
            </select>
            <select id="group-by">
              <option value="">Nicht gruppieren</option>
              <option value="type">Nach Typ</option>
              <option value="room">Nach Raum</option>
              <option value="direction">Nach Richtung</option>
              <option value="gateway">Nach Gateway</option>
              <option value="matched">Nach Status</option>
            </select>
            <select id="create-type">
              <option value="auto">Automatisch</option>
              <option value="light">Licht</option>
              <option value="dimmer">Dimmer</option>
              <option value="switch">Schalter</option>
              <option value="outlet">Steckdose</option>
              <option value="cover">Rollladen</option>
              <option value="advanced_cover">Rollladen Position</option>
              <option value="climate">Thermostat</option>
              <option value="binary_sensor">Binärsensor</option>
              <option value="sensor">Sensor</option>
            </select>
            <select id="create-model">
              <option value="">Hardware optional</option>
              ${HARDWARE_MODELS.map((model) => `<option value="${model}">${model}</option>`).join("")}
            </select>
            <button id="clear-filter" type="button">Reset</button>
            <button id="create-found" class="primary" type="button">Gefundene anlegen</button>
            <button id="clear-monitor" type="button">Leeren</button>
            <button id="download-csv" type="button">CSV</button>
            <button id="download-json" type="button">JSON</button>
          </div>
          <div class="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Zeit</th>
                  <th>Gateway</th>
                  <th>Richtung</th>
                  <th>WHO</th>
                  <th>Where</th>
                  <th>Typ</th>
                  <th>Entity</th>
                  <th>Modell</th>
                  <th>Raum</th>
                  <th>Beschreibung</th>
                  <th>Aktion</th>
                  <th>Wert</th>
                  <th>Dekodiert</th>
                  <th>Anlegen</th>
                  <th>Socket-Telegramm</th>
                  <th>Telegramm</th>
                  <th>Details</th>
                </tr>
              </thead>
              <tbody id="rows"></tbody>
            </table>
          </div>
          <div class="empty" id="empty">Noch keine Daten empfangen.</div>
        </div>
      </div>
    `;
    this.bindControls();
  }

  async loadData() {
    if (!this._rendered || !this._hass) return;

    const rows = this.querySelector("#rows");
    const status = this.querySelector("#status");
    const empty = this.querySelector("#empty");
    if (!rows || !status || !empty) return;

    try {
      const data = await this._hass.callApi("GET", "myhome/bus_monitor/data");
      this._entries = data.map((entry) => ({
        ...entry,
        telegram: entry.telegram || entry.raw || "",
        parsed: mergeParsedTelegram(entry),
      }));
      this._monitorVersion = data.find((entry) => entry.monitor_version)?.monitor_version || "";
      this.updateFilterOptions();
      this.renderRows();
    } catch (err) {
      status.textContent = `Fehler beim Laden: ${err.message}`;
      empty.hidden = false;
    }
  }

  bindControls() {
    this.querySelector("#search")?.addEventListener("input", () => this.renderRows());
    this.querySelector("#type-filter")?.addEventListener("change", () => this.renderRows());
    this.querySelector("#room-filter")?.addEventListener("change", () => this.renderRows());
    this.querySelector("#direction-filter")?.addEventListener("change", () => this.renderRows());
    this.querySelector("#group-by")?.addEventListener("change", () => {
      this._collapsedGroups = new Set();
      this.renderRows();
    });
    this.querySelector("#clear-filter")?.addEventListener("click", () => {
      ["#search", "#type-filter", "#room-filter", "#direction-filter", "#group-by"].forEach((selector) => {
        const control = this.querySelector(selector);
        if (control) control.value = "";
      });
      this._collapsedGroups = new Set();
      this.renderRows();
    });
    this.querySelector("#download-csv")?.addEventListener("click", () => this.downloadCsv());
    this.querySelector("#download-json")?.addEventListener("click", () => this.downloadJson());
    this.querySelector("#clear-monitor")?.addEventListener("click", () => this.clearMonitor());
    this.querySelector("#create-found")?.addEventListener("click", () => this.createFoundEntities());
  }

  updateFilterOptions() {
    const updateSelect = (selector, values, label) => {
      const select = this.querySelector(selector);
      if (!select) return;
      const current = select.value;
      select.replaceChildren(new Option(label, ""));
      [...values].sort((a, b) => a.localeCompare(b)).forEach((value) => {
        select.appendChild(new Option(value, value));
      });
      select.value = values.has(current) ? current : "";
    };
    const types = new Set(this._entries?.map((entry) => entry.parsed.type).filter(Boolean));
    const rooms = new Set(this._entries?.map((entry) => entry.parsed.room).filter(Boolean));
    updateSelect("#type-filter", types, "Alle Typen");
    updateSelect("#room-filter", rooms, "Alle Räume");
  }

  filteredEntries() {
    const entries = this._entries || [];
    const search = this.querySelector("#search")?.value.toLowerCase().trim() || "";
    const type = this.querySelector("#type-filter")?.value || "";
    const room = this.querySelector("#room-filter")?.value || "";
    const direction = this.querySelector("#direction-filter")?.value || "";

    return entries.filter((entry) => {
      const parsed = entry.parsed || {};
      const haystack = [
        entry.time,
        entry.gateway,
        entry.direction || "in",
        entry.telegram,
        entry.raw,
        compactJson(entry.details),
        parsed.who,
        parsed.where,
        parsed.type,
        parsed.domain,
        parsed.model,
        parsed.room,
        parsed.description,
        parsed.action,
        parsed.value,
        parsed.decoded,
      ].join(" ").toLowerCase();
      return (!search || haystack.includes(search))
        && (!type || parsed.type === type)
        && (!room || parsed.room === room)
        && (!direction || (entry.direction || "in") === direction);
    });
  }

  renderRows() {
    if (!this._rendered) return;

    const rows = this.querySelector("#rows");
    const status = this.querySelector("#status");
    const empty = this.querySelector("#empty");
    if (!rows || !status || !empty) return;

    const filtered = this.filteredEntries();
    rows.replaceChildren(...this.renderableRows(filtered.slice().reverse()));

    const total = this._entries?.length || 0;
    empty.hidden = filtered.length > 0;
    status.textContent = total
      ? `${filtered.length} von ${total} Telegrammen angezeigt${this._monitorVersion ? ` · Monitor ${this._monitorVersion}` : ""}`
      : `Warte auf Telegramme${this._monitorVersion ? ` · Monitor ${this._monitorVersion}` : ""}...`;
  }

  renderableRows(entries) {
    const groupBy = this.querySelector("#group-by")?.value || "";
    if (!groupBy) {
      return entries.map((entry) => this.createTableRow(entry));
    }

    const nodes = [];
    const groups = new Map();
    entries.forEach((entry) => {
      const group = this.groupLabel(entry, groupBy);
      if (!groups.has(group)) groups.set(group, []);
      groups.get(group).push(entry);
    });

    groups.forEach((groupEntries, group) => {
      const groupKey = this.groupKey(groupBy, group);
      const collapsed = this._collapsedGroups?.has(groupKey);
      nodes.push(this.createGroupRow(group, groupEntries.length, groupKey, collapsed));
      if (!collapsed) {
        groupEntries.forEach((entry) => nodes.push(this.createTableRow(entry)));
      }
    });
    return nodes;
  }

  groupLabel(entry, groupBy) {
    const parsed = entry.parsed || {};
    if (groupBy === "type") return parsed.type || "Ohne Typ";
    if (groupBy === "room") return parsed.room || "Ohne Raum";
    if (groupBy === "direction") return entry.direction || "in";
    if (groupBy === "gateway") return entry.gateway || "Ohne Gateway";
    if (groupBy === "matched") return parsed.matched ? "Bekannt" : "Neu / nicht angelegt";
    return "";
  }

  groupKey(groupBy, label) {
    return `${groupBy}:${label}`;
  }

  toggleGroup(groupKey) {
    this._collapsedGroups = this._collapsedGroups || new Set();
    if (this._collapsedGroups.has(groupKey)) {
      this._collapsedGroups.delete(groupKey);
    } else {
      this._collapsedGroups.add(groupKey);
    }
    this.renderRows();
  }

  createGroupRow(label, count, groupKey, collapsed) {
    const tr = document.createElement("tr");
    tr.className = "group-row";
    const td = document.createElement("td");
    td.colSpan = 17;

    const button = document.createElement("button");
    button.type = "button";
    button.className = "group-toggle";
    button.addEventListener("click", () => this.toggleGroup(groupKey));

    const icon = document.createElement("span");
    icon.className = "group-toggle-icon";
    icon.textContent = collapsed ? ">" : "v";
    button.appendChild(icon);

    const text = document.createElement("span");
    text.textContent = `${label} (${count})`;
    button.appendChild(text);

    td.appendChild(button);
    tr.appendChild(td);
    return tr;
  }

  createTableRow(entry) {
    const tr = document.createElement("tr");
    const parsed = entry.parsed || {};
    [
      entry.time,
      entry.gateway,
      parsed.who,
      parsed.where,
      parsed.type,
      parsed.domain,
      parsed.model,
      parsed.room,
      parsed.description,
      parsed.action,
      parsed.value,
      parsed.decoded,
    ].forEach((value) => {
      const td = document.createElement("td");
      td.textContent = value || "";
      tr.appendChild(td);
    });

    const direction = entry.direction || "in";
    const directionCell = document.createElement("td");
    const directionBadge = document.createElement("span");
    directionBadge.className = `direction-badge direction-${direction}`;
    directionBadge.textContent = direction;
    directionCell.appendChild(directionBadge);
    tr.insertBefore(directionCell, tr.children[2]);

    const createCell = document.createElement("td");
    const createButton = this.createEntityButton(entry);
    if (createButton) {
      createCell.appendChild(createButton);
    }
    tr.appendChild(createCell);

    const raw = document.createElement("td");
    const code = document.createElement("code");
    code.textContent = entry.raw || "";
    raw.appendChild(code);

    const telegram = document.createElement("td");
    const telegramCode = document.createElement("code");
    telegramCode.textContent = entry.telegram || entry.raw || "";
    telegram.appendChild(telegramCode);
    tr.appendChild(telegram);

    tr.appendChild(raw);

    const details = document.createElement("td");
    const detailsCode = document.createElement("code");
    detailsCode.textContent = compactJson(entry.details);
    details.appendChild(detailsCode);
    tr.appendChild(details);

    return tr;
  }

  exportRows() {
    return this.filteredEntries().map((entry) => ({
      time: entry.time || "",
      gateway: entry.gateway || "",
      direction: entry.direction || "in",
      who: entry.parsed?.who || "",
      where: entry.parsed?.where || "",
      type: entry.parsed?.type || "",
      room: entry.parsed?.room || "",
      description: entry.parsed?.description || "",
      domain: entry.parsed?.domain || "",
      model: entry.parsed?.model || "",
      action: entry.parsed?.action || "",
      value: entry.parsed?.value || "",
      decoded: entry.parsed?.decoded || "",
      monitor_version: entry.monitor_version || this._monitorVersion || "",
      telegram: entry.telegram || entry.raw || "",
      raw: entry.raw || "",
      details: compactJson(entry.details),
    }));
  }

  createEntityButton(entry) {
    const parsed = entry.parsed || {};
    const platform = this.entityOptionsForEntry(entry).platform;
    if (parsed.matched || !parsed.where || !platform || !["light", "switch", "cover", "climate", "binary_sensor", "sensor"].includes(platform)) {
      return null;
    }

    const button = document.createElement("button");
    button.type = "button";
    button.textContent = "Anlegen";
    button.addEventListener("click", () => this.createEntityFromEntry(entry, this.selectedCreateModel()));
    return button;
  }

  creatableEntries() {
    const seen = new Set();
    return this.filteredEntries().filter((entry) => {
      const parsed = entry.parsed || {};
      const platform = this.entityOptionsForEntry(entry).platform;
      if (parsed.matched || !parsed.where || !platform || !["light", "switch", "cover", "climate", "binary_sensor", "sensor"].includes(platform)) {
        return false;
      }
      const key = `${platform}:${parsed.where}`;
      if (seen.has(key)) {
        return false;
      }
      seen.add(key);
      return true;
    });
  }

  selectedCreateType() {
    return this.querySelector("#create-type")?.value || "auto";
  }

  selectedCreateModel() {
    return this.querySelector("#create-model")?.value || "";
  }

  entityOptionsForEntry(entry, selectedType = this.selectedCreateType()) {
    const parsed = entry.parsed || {};
    if (selectedType === "light") return { platform: "light", dimmable: false };
    if (selectedType === "dimmer") return { platform: "light", dimmable: true };
    if (selectedType === "switch") return { platform: "switch", class: "switch" };
    if (selectedType === "outlet") return { platform: "switch", class: "outlet" };
    if (selectedType === "cover") return { platform: "cover", advanced: false };
    if (selectedType === "advanced_cover") return { platform: "cover", advanced: true };
    if (selectedType === "climate") return { platform: "climate", heat: true, cool: false, fan: false, standalone: false, central: false };
    if (selectedType === "binary_sensor") return { platform: "binary_sensor" };
    if (selectedType === "sensor") return { platform: "sensor" };
    return inferAutoEntityOptions(parsed);
  }

  defaultEntityName(parsed, platform) {
    const fallback = parsed.description || parsed.room || parsed.type || "MyHome";
    const where = parsed.where || "entity";
    if (platform === "cover") return `Rolladen ${where}`;
    if (platform === "light") return `Licht ${where}`;
    if (platform === "switch") return `Schalter ${where}`;
    if (platform === "climate") return `Thermostat ${where}`;
    if (platform === "binary_sensor") return `Sensor ${where}`;
    if (platform === "sensor") return `Sensor ${where}`;
    return `${fallback} ${where}`.trim();
  }

  defaultModelForEntry(parsed, platform, options = {}) {
    if (platform !== "light") return "";
    if (parsed.model) return parsed.model;
    const text = [parsed.type, parsed.description, parsed.room, parsed.decoded].join(" ").toLowerCase();
    if (options.dimmable === true || /dimmer|niveau|level/.test(text)) return "F418";
    return "F417U2";
  }

  climateZoneFromWhere(where) {
    const zone = String(where || "#0").trim();
    if (!zone || zone === "#0") return "#0";
    return zone.replace(/^#0#/, "").replace(/^#+/, "").split("#")[0];
  }

  entityDataFromEntry(entry, selectedType = this.selectedCreateType(), selectedModel = this.selectedCreateModel()) {
    const parsed = entry.parsed || {};
    const options = this.entityOptionsForEntry(entry, selectedType);
    const platform = options.platform;
    const data = {
      platform,
      name: this.defaultEntityName(parsed, platform),
    };
    if (platform === "climate") {
      data.zone = this.climateZoneFromWhere(parsed.where);
    } else {
      data.where = parsed.where;
    }
    if (entry.gateway) data.gateway = entry.gateway;
    const defaultModel = this.defaultModelForEntry(parsed, platform, options);
    const model = selectedModel || parsed.model || defaultModel;
    if (model) data.model = model;
    if (options.class) data.class = options.class;
    if (options.dimmable !== undefined || DIMMER_MODELS.has(model)) {
      data.dimmable = options.dimmable === true || DIMMER_MODELS.has(model);
    }
    if (options.advanced !== undefined) data.advanced = options.advanced;
    if (options.heat !== undefined) data.heat = options.heat;
    if (options.cool !== undefined) data.cool = options.cool;
    if (options.fan !== undefined) data.fan = options.fan;
    if (options.standalone !== undefined) data.standalone = options.standalone;
    if (options.central !== undefined) data.central = options.central;
    return data;
  }

  async createEntityFromEntry(entry, selectedModel = this.selectedCreateModel()) {
    const parsed = entry.parsed || {};
    const defaultOptions = this.entityOptionsForEntry(entry);
    const defaultPlatform = defaultOptions.platform || "light";
    const platform = (window.prompt("Platform", defaultPlatform) || defaultPlatform).trim() || defaultPlatform;

    const defaultName = this.defaultEntityName(parsed, platform);
    const name = (window.prompt("Name", defaultName) || defaultName).trim() || defaultName;

    const entityClass = platform === "switch"
      ? window.prompt("Class optional: switch oder outlet", defaultOptions.class || "switch")
      : "";
    const dimmable = platform === "light"
      ? window.confirm("Als Dimmer anlegen?")
      : false;
    const advanced = platform === "cover"
      ? window.confirm("Als Rollladen mit Positionssteuerung anlegen?")
      : false;
    const heat = platform === "climate" ? window.confirm("Heizen unterstuetzen?") : true;
    const cool = platform === "climate" ? window.confirm("Kuehlen unterstuetzen?") : false;
    const fan = platform === "climate" ? window.confirm("Luefter unterstuetzen?") : false;
    const model = selectedModel || parsed.model || this.defaultModelForEntry(parsed, platform, { dimmable });
    const effectiveDimmable = dimmable || DIMMER_MODELS.has(model);

    const data = {
      platform,
      name,
    };
    if (platform === "climate") {
      data.zone = this.climateZoneFromWhere(parsed.where);
    } else {
      data.where = parsed.where;
    }
    if (model) data.model = model;
    if (entityClass) data.class = entityClass;
    if (platform === "light") data.dimmable = effectiveDimmable;
    if (platform === "cover") data.advanced = advanced;
    if (platform === "climate") {
      data.heat = heat;
      data.cool = cool;
      data.fan = fan;
      data.standalone = false;
      data.central = false;
    }

    await this._hass.callService("myhome", "create_entity", data);
    window.alert("Entität wurde in myhome.yaml angelegt. Bitte Integration neu laden.");
  }

  async createFoundEntities() {
    const entries = this.creatableEntries();
    if (!entries.length) {
      window.alert("Keine neuen gefundenen Identitäten in der aktuellen Ansicht.");
      return;
    }

    const selectedType = this.selectedCreateType();
    const selectedModel = this.selectedCreateModel();
    const typeLabel = this.querySelector("#create-type")?.selectedOptions?.[0]?.textContent || "Automatisch";
    const modelLabel = selectedModel ? ` mit Hardware "${selectedModel}"` : "";
    if (!window.confirm(`${entries.length} gefundene Identitäten als "${typeLabel}"${modelLabel} in myhome.yaml anlegen?`)) {
      return;
    }

    const button = this.querySelector("#create-found");
    if (button) button.disabled = true;
    let created = 0;
    let failed = 0;
    try {
      for (const entry of entries) {
        try {
          await this._hass.callService("myhome", "create_entity", this.entityDataFromEntry(entry, selectedType, selectedModel));
          created += 1;
        } catch (err) {
          failed += 1;
        }
      }
    } finally {
      if (button) button.disabled = false;
    }

    window.alert(`${created} Identitäten angelegt${failed ? `, ${failed} fehlgeschlagen` : ""}. Bitte Integration neu laden.`);
    await this.loadData();
  }

  download(filename, content, type) {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    link.click();
    URL.revokeObjectURL(url);
  }

  downloadCsv() {
    const rows = this.exportRows();
    const headers = ["time", "gateway", "direction", "who", "where", "type", "domain", "model", "room", "description", "action", "value", "decoded", "monitor_version", "telegram", "raw", "details"];
    const csv = [
      headers.map(escapeCsv).join(","),
      ...rows.map((row) => headers.map((header) => escapeCsv(row[header])).join(",")),
    ].join("\n");
    this.download("myhome-bus-monitor.csv", csv, "text/csv;charset=utf-8");
  }

  downloadJson() {
    this.download(
      "myhome-bus-monitor.json",
      JSON.stringify(this.exportRows(), null, 2),
      "application/json;charset=utf-8",
    );
  }

  async clearMonitor() {
    await this._hass.callApi("POST", "myhome/bus_monitor/clear");
    this._entries = [];
    this.renderRows();
    await this.loadData();
  }
}

customElements.define("zmart-myhome-panel", ZmartMyhomePanel);
