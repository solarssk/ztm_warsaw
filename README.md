# 🚍 ZTM Warsaw Integration for Home Assistant

[![GitHub release](https://img.shields.io/github/v/release/solarssk/ztm_warsaw)](https://github.com/solarssk/ztm_warsaw/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-%F0%9F%A7%A1-blue)](https://www.home-assistant.io)
[![HACS](https://img.shields.io/badge/HACS-Default-blue.svg)](https://hacs.xyz/)
[![Validate with hassfest](https://github.com/solarssk/ztm_warsaw/actions/workflows/hassfest.yaml/badge.svg)](https://github.com/solarssk/ztm_warsaw/actions)
[![custom_component](https://img.shields.io/badge/type-custom_component-red.svg)](https://github.com/solarssk/ztm_warsaw)

ZTM Warsaw Integration brings real-time public transport departure data from the City of Warsaw API directly into Home Assistant. Whether you're tracking buses, trams, or metro lines, this integration allows you to view live departures at a glance.

> Powered by data from [api.um.warszawa.pl](https://api.um.warszawa.pl) – the official public transport data provider.

---

## 🔧 Features

- ✅ Real-time and static timetable support for buses, trams, metro, night, cemetery, express and local lines.
- ✅ Supports multiple instances (you can monitor multiple stops and lines).
- ✅ Displays current or upcoming departure as timestamp (compatible with UI and automations).
- ✅ Optional display of up to 3 upcoming departures.
- ✅ Automatically recognizes and handles no-schedule days, seasonal or partial-day routes.
- ✅ Full Home Assistant UI configuration – no YAML needed.
- ✅ Custom attributes: stop info, direction, timetable link and contextual notes.

---

## 📸 Screenshots

### Integration Setup
*Add your API key and stop info...*

<div align="center"><img width="478" alt="image" src="https://github.com/user-attachments/assets/9a77591e-5b1a-4fe5-a29d-637d3c9b566c" /></div>

### Entity Display

<div align="center"><img width="555" alt="image" src="https://github.com/user-attachments/assets/ef709b81-1575-4718-9c39-f6c135cf3cca" /></div>

### Attributes
*Example entity showing departures with attributes like time, direction...*

<div align="center"><img width="530" alt="image" src="https://github.com/user-attachments/assets/95cde9db-1182-41ba-9ae6-3187bd6a527c" /></div>

---

## ⚙️ Requirements

- Home Assistant 2024.4+
- API key from [City of Warsaw](https://api.um.warszawa.pl)

---

## 🧭 How to Get API Key?

1. Go to [https://api.um.warszawa.pl](https://api.um.warszawa.pl)
2. Register or log in
3. Copy your key and paste it into the integration setup

---

## 📦 Installation

### Manual installation:

1. Download the latest version from [GitHub Releases](https://github.com/solarssk/ztm_warsaw/releases).
2. Copy the `ztm_warsaw` folder to `/config/custom_components/`.
3. Restart Home Assistant.

### Installation via HACS:

1. In Home Assistant, go to **HACS → Integrations**.
2. Search for **Warsaw Public Transport**.
3. Click **Download** and confirm.
4. Restart Home Assistant.

---

## ⚙️ Configuration

Once installed:

1. Go to **Settings → Devices & Services**
2. Click **+ Add Integration**
3. Search for **Warsaw Public Transport**
4. Fill in:
   - **API key**: You can get it at [https://api.um.warszawa.pl](https://api.um.warszawa.pl)
   - **Stop ID** and **Stop number** (e.g., 7009 / 01)
   - **Line number** (e.g., 151)
   - **Number of departures to show**

The entity name will be generated automatically, e.g., `sensor.line_151_from_7009_01`.

## 🔄 Reconfiguration

You can change the number of upcoming departures at any time by going to Settings → Devices & Services → Warsaw Public Transport → Configure of specific entity.

## 🧾 Notes

This integration depends on the official City of Warsaw public API, which has several known limitations:

- **🧭 Stop ID (busstopId) vs. Stop Pole (busstopNr)**
  These are not the same — both are required for a valid query:
  - `busstopId`: The ID of the stop (shared by all poles at that stop).
  - `busstopNr`: The specific pole number — typically 01, 02, etc.
  It’s the number painted on the physical bus/tram stop sign (słupek).
  If a stop has multiple directions or platforms, each usually has a different pole number.

- **📅 Schedule data availability is limited to the current day only**  
  The API does not provide access to schedules for the upcoming days. This means:
  - If a bus line (e.g., `E-2`) does not operate today (e.g., during weekends), it **won’t appear in the API at all**, even if it normally runs on weekdays. As a result, you won’t be able to add the integration for such a line on a day when it doesn’t operate, because the validation will fail with a `no_departures` error.
  - If you add an entity when the line is active, it will work correctly.  
    On days when the line is inactive, the entity will show a `60+ min` state and the following attribute will appear:
    ```
    note: "No upcoming schedule available. Please verify on wtp.waw.pl or call 19115 for more information."
    ```

- **🔍 Some lines visible on wtp.waw.pl are not available in the API**  
  The official journey planner (wtp.waw.pl) uses internal systems that may include more complete data than what’s exposed by the public API. If a line exists on the website but not in the integration — that’s a limitation of the API. Nothing can be done on my end.

- **🌙 Night line schedules (e.g. `N01`, `N44`) and how they’re handled**  
  ZTM (Zarząd Transportu Publicznego) treats the **entire night as part of the same service day**, so buses departing at `24:50`, `26:20`, etc. are **still part of the "previous" day’s schedule**.

  This integration now correctly interprets such hours by **treating all times up to 4:59 as part of the previous service day**. This fix has been implemented starting from version `v1.0.2`.

  - This ensures that **night departures do not disappear after midnight**.
  - You can expect to see accurate countdowns like "15 min" even if it’s `02:00` and the bus is scheduled for `02:15` (`26:15` in the API).

**Important Reminder**
These limitations are caused by the official API and are **out of scope of this integration**. I always recommend checking the official journey planner: [wtp.waw.pl](https://wtp.waw.pl)

---

## 🙌 Acknowledgments

Data provided by **Miasto Stołeczne Warszawa** and **Warszawski Transport Publiczny** via [api.um.warszawa.pl](https://api.um.warszawa.pl)

This project was fully planned and designed by me — from the concept and expected behavior of the integration, to how it interacts with the City of Warsaw’s public API. While I’m not a professional Python developer, I understand the essentials well enough to define the structure, logic, and features I wanted this integration to offer.

To bring it all to life, I used AI support (ChatGPT), which assisted me mainly with syntax, debugging, and implementation details. However, the overall design, behavior, and workflow were all thoughtfully laid out on my end.

Special thanks to [@peetereczek](https://github.com/peetereczek/ztm), whose previous project inspired me at the beginning. Although this final version was built independently from scratch, his work gave me the initial push to approach things in my own way.

If you’re interested in improving or extending the project — go ahead! Contributions, ideas, and pull requests are always welcome.

---

## 📄 License

MIT License
