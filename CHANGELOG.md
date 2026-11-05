# Changelog

What changed, written for the people who use the integration. Entries are grouped under `### Added`, `### Changed`, `### Fixed` and `### Removed` ([Keep a Changelog](https://keepachangelog.com/en/1.1.0/)), and each is a bold title with one short, friendly sentence: what you can do now, not how it was built. The details are in the pull requests.

This file is the source of the GitHub Release notes, and a published Release is what makes Marketplace and HACS offer an update. A beta (`X.Y.ZbN`) takes its notes from `[Unreleased]`. A version that needs something from you starts with an `### Adopter action` list.

Releases before 1.1.4 are described on the [GitHub Releases](https://github.com/solarssk/ztm_warsaw/releases) page.

## [Unreleased]

## [1.2.1] - 2026-11-04

Update through Marketplace or HACS and restart Home Assistant. No reconfiguration is needed.

### Changed

- **Installation with Marketplace**: the installation guide now covers Home Assistant 2026.11 and keeps the HACS instructions for older versions.

## [1.2.0] - 2026-10-23

Upgrading from 1.1.4: update through HACS and restart Home Assistant. Nothing has to be set up again.

### Adopter action

- **Your stops are grouped by line**: each line becomes one entry with its stops under it, and your sensors keep their names, IDs and settings. An automation or card that points at the old *device* needs choosing again, and there is no way back to 1.1.4, so take a backup first.
- **Home Assistant 2026.1 or newer**: this version needs it, and HACS will not offer the update on an older one, so you stay on 1.1.4 until you upgrade Home Assistant.
- **Replace an old key with a token now**: the City's old API stopped answering on 21 October 2026, so a line with an old key gets no new timetables. Get a token at [dane.um.warszawa.pl/pl/key-api](https://dane.um.warszawa.pl/pl/key-api) and paste it in the notice in Repairs.
- **More departures on every sensor**: each sensor now lists the next departure and the three after it, so the "number of departures" choice is gone.
- **Two entries for the same stop and line?** The second one never had a sensor, so remove it when Repairs tells you.

### Added

- **Works with the City's new API**: log in with a token from the new portal, and each key goes only to the right server.
- **A friendlier setup**: type a part of the stop's name, pick the pole and then a line that really stops there, and the City's abbreviations are understood. Tick *I know the numbers* to type them yourself.
- **Every stop of a line under one entry**: add another with **Add stop**, and each stop is a device of its own. Entries you already have are grouped for you.
- **Change your key any time**: **Configure** or **Reconfigure** swaps the key or token, and a token you already use is offered again instead of being pasted twice.
- **One notice for an old key**: Repairs and the integration page ask once for the whole line, and you can paste a token, reuse another line's (picked by its last four characters) or ignore the notice.
- **A notice when the City stays silent**: if a line gets no answer for hours (a revoked or expired token looks exactly like that), Repairs says so and tells you what to check. It goes by itself when the City answers.
- **A status in words**: every stop has a *Status* sensor that says what is going on (runs today, no more today, does not run today, timetables are being updated ...) in your language.
- **Next departures as their own entities** (off by default): switch on *Next 1*, *Next 2* or *Next 3* in the entity settings to use each following departure in a card or an automation.
- **First and last bus of the day**: every sensor has `Timetable, First Departure` and `Timetable, Last Departure`, so a card can still say "the last bus left at 23:41" after the last departure.
- **A walking time for every stop**: set how many minutes it takes you to walk to a stop (*Reconfigure* on the stop), and its sensor skips the departures you could not catch any more.
- **A calendar of departures** (off by default): switch it on in the entity settings to see the whole day in Home Assistant's calendar, or start an automation "8 minutes before the bus".
- **Stops and vehicles on the map**: every stop pole is one pin, and a line can show its vehicles too (*Configure* on the line, token needed) with the badge of its line in the colours of ZTM's own signs.
- **Everything the City says about a vehicle**: its brigade and planned destination, route, operator, depot, registration, year, make, model, floor, number of places, speed and course.
- **How far the bus is** (off by default, needs a token): switch on *Vehicle distance* in a stop's entity settings for an automation such as "the bus is 500 m away".
- **Entity names in your language**: the names of the sensors and the calendar are translated, and their IDs stay the same, so nothing you built on them breaks.
- **Eight languages**: the setup, notices, dialogs and README are now in Polish, Ukrainian, Russian, German, Spanish, French and Italian too. The new languages are machine-translated, so corrections are welcome.
- **Error messages in your language**: when the City does not answer or refuses a request, the message in the log and in the entry's state is translated too.
- **Download diagnostics**: one click gives you a file for bug reports, with your key hidden.
- **Delete a stop's old device**: when a stop is gone from a line, its leftover device has a *Delete* button, and a device still in use cannot be deleted by mistake.
- **Logo and icons**: the integration carries its own logo, and the next departures, the last update and the calendar have icons of their own.
- **Releases you can check**: each release has the integration as a signed zip, and the steps to verify it are in SECURITY.md.
- **A real manual**: the wiki is rewritten in short pages with a quick start, cards and automations to copy, and answers to common questions.

### Changed

- **The stop's name where you look for it**: entries are titled "Line 176 from Rondo Daszyńskiego 15" (a title you chose stays), and notices in Repairs name the line and the stop.
- **Clearer texts**: the README and the setup messages explain configuration, keys and errors more naturally in all eight languages.
- **Proper credits**: the sensor names the City of Warsaw, ZTM and the licence, and the README says plainly that these are scheduled departures.

### Fixed

- **Night lines and midnight**: times after midnight follow the City's own timetable day, so no more "No service" gaps or yesterday's times.
- **Errors look like errors**: a rejected key or an unreadable answer shows as `unavailable`, not as a misleading "No service".
- **A quick second try after a hiccup**: if the City cannot be reached for a moment (right after Home Assistant starts, say), your sensors keep their timetable and ask again within minutes instead of an hour.
- **The stop's name stays after a slow start**: a sensor no longer loses its stop name and map pin when the City is slow to answer after a restart.
- **No more requests to the old API**: a line with an old key says why it has no timetable, the log says it once, and a new line cannot be set up with an old key.
- **A quiet log during an outage**: when the City is out for hours, the log says so once and the integration asks less and less often.
- **Lighter on the City**: the stop list is downloaded once for all your sensors, not once each.
- **No duplicate entries**: you can no longer add the same stop, pole and line twice.

## [1.1.4] - 2026-05-19

Upgrading from 1.1.3: update through HACS and restart Home Assistant. No reconfiguration is needed.

### Fixed

- Changing the number of departures in the options no longer crashes the reload.
- Every coordinator called the City of Warsaw API twice on startup; each line now fetches once.
- New entities always get a numeric entity ID such as `sensor.line_28_from_5161_03`, never one derived from the stop name. An existing entity with a name-based ID can be renamed in Settings > Devices & Services.
- The hourly refresh timer is cancelled when the integration is unloaded instead of leaking on every reload.

### Changed

- Connection errors are retried like timeouts; the sensor keeps the last known data during a short outage.
- API responses larger than 2 MB are refused.
- A sensor writes its state only when something changed, and schedules its own update at the next departure time instead of ticking every minute.
