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
  const frontendParsed = parseTelegram(entry.raw);
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

class ZmartMyhomePanel extends HTMLElement {
  set hass(hass) {
    this._hass = hass;
    this.render();
    this.renderRows();
  }

  connectedCallback() {
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
          grid-template-columns: minmax(180px, 1fr) repeat(3, minmax(120px, 180px)) auto auto auto auto;
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
        .table-wrap {
          overflow-x: auto;
        }
        table {
          border-collapse: collapse;
          width: 100%;
          min-width: 1180px;
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
            <button id="clear-filter" type="button">Reset</button>
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
                  <th>Telegramm</th>
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
      this._entries = data.map((entry) => ({ ...entry, parsed: mergeParsedTelegram(entry) }));
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
    this.querySelector("#clear-filter")?.addEventListener("click", () => {
      ["#search", "#type-filter", "#room-filter", "#direction-filter"].forEach((selector) => {
        const control = this.querySelector(selector);
        if (control) control.value = "";
      });
      this.renderRows();
    });
    this.querySelector("#download-csv")?.addEventListener("click", () => this.downloadCsv());
    this.querySelector("#download-json")?.addEventListener("click", () => this.downloadJson());
    this.querySelector("#clear-monitor")?.addEventListener("click", () => this.clearMonitor());
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
        entry.raw,
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
    rows.replaceChildren(...filtered.slice().reverse().map((entry) => {
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
      tr.appendChild(raw);

      return tr;
    }));

    const total = this._entries?.length || 0;
    empty.hidden = filtered.length > 0;
    status.textContent = total
      ? `${filtered.length} von ${total} Telegrammen angezeigt${this._monitorVersion ? ` · Monitor ${this._monitorVersion}` : ""}`
      : `Warte auf Telegramme${this._monitorVersion ? ` · Monitor ${this._monitorVersion}` : ""}...`;
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
      raw: entry.raw || "",
    }));
  }

  createEntityButton(entry) {
    const parsed = entry.parsed || {};
    const platform = parsed.suggested_domain || parsed.domain || "";
    if (parsed.matched || !parsed.where || !platform || !["light", "switch", "cover", "binary_sensor", "sensor"].includes(platform)) {
      return null;
    }

    const button = document.createElement("button");
    button.type = "button";
    button.textContent = "Anlegen";
    button.addEventListener("click", () => this.createEntityFromEntry(entry));
    return button;
  }

  async createEntityFromEntry(entry) {
    const parsed = entry.parsed || {};
    const defaultPlatform = parsed.suggested_domain || parsed.domain || "light";
    const platform = window.prompt("Platform", defaultPlatform);
    if (!platform) return;

    const name = window.prompt("Name", parsed.description || `${parsed.type || "MyHome"} ${parsed.where}`);
    if (!name) return;

    const model = window.prompt("Modell optional", parsed.model || "");
    const entityClass = platform === "switch"
      ? window.prompt("Class optional: switch oder outlet", "switch")
      : "";

    const data = {
      platform,
      name,
      where: parsed.where,
    };
    if (model) data.model = model;
    if (entityClass) data.class = entityClass;

    await this._hass.callService("myhome", "create_entity", data);
    window.alert("Entität wurde in myhome.yaml angelegt. Bitte Integration neu laden.");
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
    const headers = ["time", "gateway", "direction", "who", "where", "type", "domain", "model", "room", "description", "action", "value", "decoded", "monitor_version", "raw"];
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
