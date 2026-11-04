<h1 align="center">🚍 ZTM Warschau für Home Assistant</h1>

<p align="center">
  <strong>Fahrpläne des Warschauer Nahverkehrs in Home Assistant.<br>Die nächsten Abfahrten für Dashboards und Automationen. Einrichtung ohne YAML.</strong>
</p>

<p align="center">
  🇬🇧 <a href="README.md">English</a>
  &nbsp;·&nbsp;
  🇵🇱 <a href="README.pl.md">Polski</a>
  &nbsp;·&nbsp;
  🇺🇦 <a href="README.uk.md">Українська</a>
  &nbsp;·&nbsp;
  🇷🇺 <a href="README.ru.md">Русский</a>
  &nbsp;·&nbsp;
  🇩🇪 <strong>Deutsch</strong>
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
<summary><strong>Inhaltsverzeichnis</strong></summary>

- [Funktionen](#-funktionen)
- [Screenshots](#-screenshots)
- [Voraussetzungen](#-voraussetzungen)
- [Schlüssel oder Token besorgen](#-schlüssel-oder-token-besorgen)
- [Installation](#-installation)
- [Konfiguration](#-konfiguration)
- [Fehlerbehebung](#-fehlerbehebung)
- [Dokumentation](#-dokumentation)
- [Mitwirken und Sicherheit](#-mitwirken-und-sicherheit)
- [Daten und Danksagung](#-daten-und-danksagung)
- [Lizenz](#-lizenz)

</details>

Die Integration zeigt in Home Assistant, **wann an deiner Haltestelle der nächste Bus, die nächste Straßenbahn oder der nächste Zug abfährt**. Für jede Linie an der gewählten Halteposition legt sie einen Sensor an, den du in ein Dashboard setzen oder in einer Automation nutzen kannst, zum Beispiel für eine Benachrichtigung, wann du losgehen musst. Sie nutzt die offenen Daten der Stadt Warschau, du brauchst also keine zusätzliche Hardware.

Die Integration liest Fahrpläne, deshalb zeigt sie **planmäßige** Abfahrten. Verspätungen und Störungen zeigt sie nicht, Fahrpläne für andere Tage als den aktuellen Betriebstag kennt sie nicht, und Reisen plant sie nicht (dafür gibt es [wtp.waw.pl](https://wtp.waw.pl)). Mit einem Token kannst du zusätzlich die Fahrzeuge deiner Linien auf der Karte sehen.

---

## 🔧 Funktionen

- ✅ Die Integration unterstützt Busse, Straßenbahnen, die U-Bahn und die S-Bahn (SKM), auch Nacht-, Express- und Lokallinien.
- ✅ Der Zustand des Sensors ist die Zeit der nächsten Abfahrt. Die drei folgenden Abfahrten sowie die erste und die letzte Abfahrt des Tages findest du in den Attributen.
- ✅ Ein eigener *Status*-Sensor erklärt in einfachen Worten, was gerade los ist, zum Beispiel „Heute keine Abfahrten mehr“.
- ✅ Eine Haltestelle fügst du hinzu, indem du einen Teil ihres Namens tippst. Danach wählst du die Richtung, in die du fährst (wenn die Haltestelle mehr als eine Halteposition hat), und die Linie. Du musst also keine Nummern nachschlagen.
- ✅ Du kannst mehrere Linien und Haltestellen hinzufügen, eine Gehzeit zur Haltestelle festlegen, einen Abfahrtskalender einschalten und das Fahrzeug auf der Karte sehen. Kalender und Fahrzeug sind standardmäßig ausgeschaltet.
- ✅ Die Oberfläche gibt es in acht Sprachen: Englisch, Polnisch, Ukrainisch, Russisch, Deutsch, Spanisch, Französisch und Italienisch. Die sechs neueren hat ein Programm übersetzt, Korrekturen als Pull Request sind daher willkommen.

---

## 📸 Screenshots

### Einrichtung der Integration
*Das Einrichtungsformular für Zugangsdaten, Linie und Haltestelle.*

<div align="center"><img width="478" alt="image" src="https://github.com/user-attachments/assets/9a77591e-5b1a-4fe5-a29d-637d3c9b566c" /></div>

### Darstellung der Entität

<div align="center"><img width="555" alt="image" src="https://github.com/user-attachments/assets/ef709b81-1575-4718-9c39-f6c135cf3cca" /></div>

### Attribute
*Fahrplandetails mit Abfahrtszeiten und Fahrtrichtung.*

<div align="center"><img width="530" alt="image" src="https://github.com/user-attachments/assets/95cde9db-1182-41ba-9ae6-3187bd6a527c" /></div>

---

## 📋 Voraussetzungen

- Home Assistant 2026.1 oder neuer
- Ein API-Schlüssel oder Token der Stadt Warschau (siehe unten)

---

## 🧭 Schlüssel oder Token besorgen

Ein kostenloses Token bekommst du unter [dane.um.warszawa.pl/pl/key-api](https://dane.um.warszawa.pl/pl/key-api): Gib einen beliebigen Spitznamen ein, akzeptiere die Bedingungen und lade das Token herunter. Ein Token ist ein langer Text aus drei Teilen, die durch Punkte getrennt sind.

Ein alter API-Schlüssel (`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`, von [api.um.warszawa.pl](https://api.um.warszawa.pl)) funktioniert nicht mehr. Der Server dahinter antwortet seit dem 21. Oktober 2026 nicht mehr, und die Integration fragt ihn nicht mehr an. Eine Linie mit altem Schlüssel bekommt deshalb keinen neuen Fahrplan, bis du den Schlüssel durch ein Token ersetzt: Öffne den Hinweis unter **Reparaturen** oder wähle bei der Linie **Konfigurieren** und füge das Token ein. Die Einstellungen der Linie bleiben erhalten.

---

## 📦 Installation

<!-- ha-marketplace:exclude-start -->

### Mit Marketplace (Home Assistant 2026.11+)

Öffne **Einstellungen → Marketplace**, suche nach **Warsaw Public Transport** und installiere die Integration. Fahre dann mit der Konfiguration unten fort; starte Home Assistant neu, wenn du dazu aufgefordert wirst.

Du nutzt bereits HACS? Home Assistant übernimmt die installierten Repositorys und ihre Updates automatisch in den Marketplace.

### Mit HACS (Home Assistant 2026.1–2026.10)

1. Öffne in Home Assistant **HACS → Integrationen**.
2. Suche nach **Öffentlicher Nahverkehr Warschau**.
3. Klicke auf **Herunterladen** und bestätige.
4. Starte Home Assistant neu.

### Manuell

1. Lade die neueste Version von [GitHub Releases](https://github.com/solarssk/ztm_warsaw/releases) herunter.
2. Kopiere den Ordner `ztm_warsaw` nach `/config/custom_components/`.
3. Starte Home Assistant neu.

---

<!-- ha-marketplace:exclude-end -->

## 🔌 Konfiguration

1. Öffne **Einstellungen → Geräte & Dienste**.
2. Klicke auf **+ Integration hinzufügen** und suche nach **Öffentlicher Nahverkehr Warschau**.
3. Füge dein Token ein, tippe dann einen Teil des Haltestellennamens (zum Beispiel `Rondo Daszyńskiego`) oder die ID ein und wähle die Haltestelle.
4. Wähle die Halteposition nach ihrer Richtung (die Nummer steht auf dem Haltestellenschild, und die Integration zeigt die Richtung, die sie aus dem Fahrplan liest), dann die Linie: Aufgelistet sind nur Linien, die dort heute halten.

Die Integration benennt den Sensor zum Beispiel `sensor.line_151_from_7009_01`. Eine weitere Haltestelle der Linie fügst du mit **Haltestelle hinzufügen** hinzu. Kennst du die Nummern, setze auf dem ersten Bildschirm den Haken bei **Ich kenne die Nummern: Ich gebe sie selbst ein**. Gehzeit, Kalender, Fahrzeug auf der Karte und das Entfernen einer Linie erklärt das [Wiki](https://github.com/solarssk/ztm_warsaw/wiki/1.-Configuration).

---

## 🩺 Fehlerbehebung

- **Der Sensor hat den Zustand `unknown` und das Attribut „No service“.** Die Linie fährt heute nicht, oder ihre letzte Abfahrt ist vorbei. Das ist kein Fehler. Welcher der beiden Fälle vorliegt, sagt der *Status*-Sensor. Den Fahrplan findest du auf [wtp.waw.pl](https://wtp.waw.pl) oder unter der Nummer 19115.
- **Der Sensor hat den Zustand `unavailable`.** Die Stadt hat keinen gültigen Fahrplan geliefert, weil sie das Token abgelehnt hat oder die Haltestelle, die Halteposition oder die Linie nicht kennt. Den Grund findest du im Protokoll von Home Assistant. Schlüssel und Token tauchen dort nie auf.
- **Deine Linie meldet, dass die alte API nicht mehr funktioniert.** Die alte API der Stadt antwortet seit dem 21. Oktober 2026 nicht mehr, und die Integration fragt sie nicht mehr an. Die Linie behält ihren Fahrplan bis zum Ende des Betriebstags. Ersetze den alten Schlüssel durch ein Token, wie oben beschrieben.
- **Home Assistant verlangt einen neuen Schlüssel.** Die Stadt hat den Schlüssel dreimal hintereinander abgelehnt. Gib im Formular einen neuen Schlüssel oder ein Token ein. Die Einstellungen bleiben erhalten.
- **Du möchtest ein Problem melden.** Wähle beim Eintrag *Diagnosedaten herunterladen* und hänge die Datei an dein Issue an. Schlüssel und Token sind darin durch `**REDACTED**` ersetzt.

Weitere Antworten stehen im [Wiki](https://github.com/solarssk/ztm_warsaw/wiki/4.-Troubleshooting).

---

## 📚 Dokumentation

Das Benutzerhandbuch steht im [Wiki](https://github.com/solarssk/ztm_warsaw/wiki): [Konfiguration](https://github.com/solarssk/ztm_warsaw/wiki/1.-Configuration) beschreibt die Gehzeit und das Entfernen einer Linie, [Konzepte](https://github.com/solarssk/ztm_warsaw/wiki/2.-Concepts) erklären den Betriebstag und was jede Entität anzeigt, [Beispiele](https://github.com/solarssk/ztm_warsaw/wiki/3.-Examples) enthalten Karten und Automationen zum Kopieren, und [Fehlerbehebung](https://github.com/solarssk/ztm_warsaw/wiki/4.-Troubleshooting) beantwortet häufige Fragen. Das Wiki ist auf Englisch geschrieben, die Quelldateien liegen in [`docs/wiki/`](docs/wiki).

---

## 🧑‍💻 Mitwirken und Sicherheit

Ideen, Fehlermeldungen und Pull Requests sind willkommen. Hinweise zur Mitarbeit findest du in [CONTRIBUTING.md](CONTRIBUTING.md). Sicherheitslücken meldest du nach der Anleitung in [SECURITY.md](SECURITY.md).

---

## 🙌 Daten und Danksagung

Daten: Die Stadt Warschau (**Miasto Stołeczne Warszawa**) und die Warschauer Verkehrsbehörde (**Zarząd Transportu Miejskiego**, ZTM) über das Open-Data-Portal der Stadt ([dane.um.warszawa.pl](https://dane.um.warszawa.pl)), unter der Lizenz [Creative Commons Attribution](https://creativecommons.org/licenses/by/4.0/deed.de).

Konzept, Funktionen, Struktur und die Anbindung an die öffentliche API der Stadt Warschau habe ich selbst entworfen. Ich bin kein professioneller Python-Entwickler, konnte aber mit meinen Grundkenntnissen die Funktionsweise des Projekts planen.

ChatGPT hat mich bei Syntax, Fehlersuche und Implementierungsdetails unterstützt. Die Entscheidungen zu Aufbau und Funktionsweise des Projekts habe ich selbst getroffen.

Vielen Dank an [@peetereczek](https://github.com/peetereczek/ztm), dessen früheres Projekt mich inspiriert hat. Diese Integration wurde als eigenständiges Projekt von Grund auf neu entwickelt.

Du kannst das Projekt mit Ideen, Fehlermeldungen und Verbesserungsvorschlägen unterstützen.

---

## 📄 Lizenz

MIT-Lizenz
