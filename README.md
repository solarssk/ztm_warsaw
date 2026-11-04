<h1 align="center">🚍 ZTM Warsaw for Home Assistant</h1>

<p align="center">
  <strong>Warsaw public transport timetables in Home Assistant.<br>Upcoming departures for your dashboards and automations. No YAML required.</strong>
</p>

<p align="center">
  🇬🇧 <strong>English</strong>
  &nbsp;·&nbsp;
  🇵🇱 <a href="README.pl.md">Polski</a>
  &nbsp;·&nbsp;
  🇺🇦 <a href="README.uk.md">Українська</a>
  &nbsp;·&nbsp;
  🇷🇺 <a href="README.ru.md">Русский</a>
  &nbsp;·&nbsp;
  🇩🇪 <a href="README.de.md">Deutsch</a>
  &nbsp;·&nbsp;
  🇪🇸 <a href="README.es.md">Español</a>
  &nbsp;·&nbsp;
  🇫🇷 <a href="README.fr.md">Français</a>
  &nbsp;·&nbsp;
  🇮🇹 <a href="README.it.md">Italiano</a>
</p>

<p align="center">
  <a href="https://github.com/solarssk/ztm_warsaw/actions/workflows/ci.yml"><img src="https://github.com/solarssk/ztm_warsaw/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  &nbsp;
  <a href="https://codecov.io/gh/solarssk/ztm_warsaw"><img src="https://codecov.io/gh/solarssk/ztm_warsaw/graph/badge.svg" alt="Codecov"></a>
  &nbsp;
  <a href="https://sonarcloud.io/summary/new_code?id=solarssk_ztm_warsaw"><img src="https://sonarcloud.io/api/project_badges/measure?project=solarssk_ztm_warsaw&metric=alert_status" alt="Quality Gate Status"></a>
  &nbsp;
  <a href="https://securityscorecards.dev/viewer/?uri=github.com/solarssk/ztm_warsaw"><img src="https://api.securityscorecards.dev/projects/github.com/solarssk/ztm_warsaw/badge" alt="OpenSSF Scorecard"></a>
</p>

<p align="center">
  <a href="https://github.com/solarssk/ztm_warsaw/releases"><img src="https://img.shields.io/github/v/release/solarssk/ztm_warsaw?include_prereleases&label=release&color=066fd1" alt="release"></a>
  &nbsp;
  <a href="https://hacs.xyz/"><img src="https://img.shields.io/badge/HACS-Default-41BDF5" alt="HACS Default"></a>
  &nbsp;
  <img src="https://img.shields.io/badge/Home%20Assistant-2026.1%2B-41BDF5?logo=homeassistant&logoColor=white" alt="Home Assistant 2026.1+">
  &nbsp;
  <a href="LICENSE"><img src="https://img.shields.io/github/license/solarssk/ztm_warsaw" alt="License: MIT"></a>
</p>

<details>
<summary><strong>Table of contents</strong></summary>

- [Features](#-features)
- [Screenshots](#-screenshots)
- [Requirements](#-requirements)
- [Getting a key or token](#-getting-a-key-or-token)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Documentation](#-documentation)
- [Contributing and security](#-contributing-and-security)
- [Data and acknowledgments](#-data-and-acknowledgments)
- [License](#-license)

</details>

The integration displays in Home Assistant **when the next bus, tram or train leaves your stop**. For every line at the stop pole you choose, it creates one sensor that you can put on a dashboard or use in an automation, for example to get a notification when it is time to leave home. It uses the City of Warsaw's open data, so you need no extra hardware.

The integration reads timetables, so it displays **scheduled** departures. It does not show delays or disruptions, it has no timetables for days other than the current service day, and it does not plan journeys (use [wtp.waw.pl](https://wtp.waw.pl) for that). With a token you can also see the vehicles of your lines on the map.

---

## 🔧 Features

- ✅ The integration supports buses, trams, the metro and urban rail (SKM), including night, express and local lines.
- ✅ The state of the sensor is the time of the next departure. You find the three after it, and the first and the last departure of the day, in the attributes.
- ✅ A separate *Status* sensor explains in plain words what is going on, for example "No more departures today".
- ✅ You add a stop by typing part of its name, then pick the direction you travel in (where the stop has more than one pole) and the line, so you never look up a number.
- ✅ You can add several lines and stops, set a walking time to the stop, turn on a calendar of departures and see the vehicle on the map. The calendar and the vehicle are off by default.
- ✅ The interface is in eight languages: English, Polish, Ukrainian, Russian, German, Spanish, French and Italian. A program translated the six newer ones, so corrections as pull requests are welcome.

---

## 📸 Screenshots

### Integration Setup
*The setup form for API credentials, line and stop details.*

<div align="center"><img width="478" alt="image" src="https://github.com/user-attachments/assets/9a77591e-5b1a-4fe5-a29d-637d3c9b566c" /></div>

### Entity Display

<div align="center"><img width="555" alt="image" src="https://github.com/user-attachments/assets/ef709b81-1575-4718-9c39-f6c135cf3cca" /></div>

### Attributes
*Timetable details, including departure times and direction of travel.*

<div align="center"><img width="530" alt="image" src="https://github.com/user-attachments/assets/95cde9db-1182-41ba-9ae6-3187bd6a527c" /></div>

---

## 📋 Requirements

- Home Assistant 2026.1 or newer
- An API key or token from the City of Warsaw (below)

---

## 🧭 Getting a key or token

You get a free token at [dane.um.warszawa.pl/pl/key-api](https://dane.um.warszawa.pl/pl/key-api): enter any nickname, accept the terms and download the token. A token is a long text made of three parts separated by dots.

An old API key (`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`, from [api.um.warszawa.pl](https://api.um.warszawa.pl)) no longer works. The server behind it stopped answering on 21 October 2026, and the integration does not ask it any more. A line with an old key therefore gets no new timetable until you replace the key with a token: open the notice in **Repairs**, or choose **Configure** on the line, and paste the token. The settings of the line stay.

---

## 📦 Installation

<!-- ha-marketplace:exclude-start -->

### With Marketplace (Home Assistant 2026.11+)

Open **Settings → Marketplace**, search for **Warsaw Public Transport** and install it. Continue with Configuration below; restart Home Assistant if prompted.

Upgrading from HACS? Home Assistant moves your installed repositories and updates to Marketplace automatically.

### With HACS (Home Assistant 2026.1–2026.10)

1. In Home Assistant, go to **HACS → Integrations**.
2. Search for **Warsaw Public Transport**.
3. Click **Download** and confirm.
4. Restart Home Assistant.

### Manually

1. Download the latest version from [GitHub Releases](https://github.com/solarssk/ztm_warsaw/releases).
2. Copy the `ztm_warsaw` folder to `/config/custom_components/`.
3. Restart Home Assistant.

---

<!-- ha-marketplace:exclude-end -->

## 🔌 Configuration

1. Go to **Settings → Devices & services**.
2. Click **+ Add Integration** and search for **Warsaw Public Transport**.
3. Paste your token, then type a part of the stop's name (for example `Rondo Daszyńskiego`) or its ID and pick the stop.
4. Pick the pole by where it goes (its number is on the stop sign; the integration shows the direction, read from the timetable), then the line: only lines that stop there today are listed.

The integration names the sensor, for example `sensor.line_151_from_7009_01`. You add another stop of the line with **Add stop**. If you know the numbers, tick **I know the numbers: let me enter them myself** on the first screen. The [wiki](https://github.com/solarssk/ztm_warsaw/wiki/1.-Configuration) explains the walking time, the calendar, the vehicle on the map and how to remove a line.

---

## 🩺 Troubleshooting

- **The sensor has the state `unknown` and the attribute "No service".** The line does not run today, or its last departure has gone. This is not an error. The *Status* sensor tells you which of the two it is. You can check the timetable at [wtp.waw.pl](https://wtp.waw.pl) or by calling 19115.
- **The sensor has the state `unavailable`.** The City did not return a valid timetable, because it rejected the token or does not know the stop, the pole or the line. You find the reason in the Home Assistant log. Keys and tokens never appear in it.
- **Your line says that the old API no longer works.** The City's old API stopped answering on 21 October 2026, and the integration does not ask it any more. The line keeps the timetable it had until the service day ends. Replace the old key with a token, as described above.
- **Home Assistant asks for a new key.** The City rejected the key three times in a row. Enter a new key or token in the form. Your settings stay.
- **You want to report a problem.** Choose *Download diagnostics* on the entry and attach the file to your issue. The key and the token are replaced in it with `**REDACTED**`.

More answers are in the [wiki](https://github.com/solarssk/ztm_warsaw/wiki/4.-Troubleshooting).

---

## 📚 Documentation

The user manual is in the [wiki](https://github.com/solarssk/ztm_warsaw/wiki): [Configuration](https://github.com/solarssk/ztm_warsaw/wiki/1.-Configuration) describes the walking time and removing a line, [Concepts](https://github.com/solarssk/ztm_warsaw/wiki/2.-Concepts) explains the service day and what each entity displays, [Examples](https://github.com/solarssk/ztm_warsaw/wiki/3.-Examples) has cards and automations to copy, and [Troubleshooting](https://github.com/solarssk/ztm_warsaw/wiki/4.-Troubleshooting) answers common questions. The wiki is in English and its source files are in [`docs/wiki/`](docs/wiki).

---

## 🧑‍💻 Contributing and security

Ideas, bug reports and pull requests are welcome: see [CONTRIBUTING.md](CONTRIBUTING.md). To report a vulnerability, see [SECURITY.md](SECURITY.md).

---

## 🙌 Data and acknowledgments

Data: the City of Warsaw (**Miasto Stołeczne Warszawa**) and the Warsaw Public Transport Authority (**Zarząd Transportu Miejskiego**, ZTM), via the City's open data portal ([dane.um.warszawa.pl](https://dane.um.warszawa.pl)), under the [Creative Commons Attribution](https://creativecommons.org/licenses/by/4.0/) licence.

I developed the integration’s concept, features, structure and approach to the City of Warsaw’s public API. I am not a professional Python developer, but my understanding of the basics allowed me to plan how the project should work.

I used ChatGPT to help with syntax, debugging and implementation details. I made the decisions about the project’s design and behaviour myself.

Thanks to [@peetereczek](https://github.com/peetereczek/ztm), whose earlier project inspired me. This integration was built from scratch as an independent project.

You are welcome to help develop the project by suggesting ideas, reporting bugs or submitting improvements.

---

## 📄 License

MIT License
