<h1 align="center">🚍 ZTM Warszawa w Home Assistant</h1>

<p align="center">
  <strong>Rozkłady jazdy warszawskiej komunikacji miejskiej w Home Assistant.<br>Najbliższe odjazdy na pulpicie i w automatyzacjach. Konfiguracja bez YAML-a.</strong>
</p>

<p align="center">
  🇬🇧 <a href="README.md">English</a>
  &nbsp;·&nbsp;
  🇵🇱 <strong>Polski</strong>
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
<summary><strong>Spis treści</strong></summary>

- [Funkcje](#-funkcje)
- [Zrzuty ekranu](#-zrzuty-ekranu)
- [Wymagania](#-wymagania)
- [Klucz i token](#-klucz-i-token)
- [Instalacja](#-instalacja)
- [Konfiguracja](#-konfiguracja)
- [Rozwiązywanie problemów](#-rozwiązywanie-problemów)
- [Dokumentacja](#-dokumentacja)
- [Współpraca i bezpieczeństwo](#-współpraca-i-bezpieczeństwo)
- [Dane i podziękowania](#-dane-i-podziękowania)
- [Licencja](#-licencja)

</details>

Integracja wyświetla w Home Assistant, **kiedy z Twojego przystanku odjedzie najbliższy autobus, tramwaj albo pociąg**. Dla każdej linii na wybranym słupku tworzy jeden sensor, który możesz umieścić na pulpicie albo wykorzystać w automatyzacji, na przykład żeby dostać powiadomienie, kiedy trzeba wyjść z domu. Dane bierze z otwartych danych m.st. Warszawy, więc nie potrzebujesz żadnego dodatkowego sprzętu.

Integracja korzysta z rozkładu jazdy, więc wyświetla **planowane** odjazdy. Nie pokazuje opóźnień ani utrudnień, nie zna rozkładów na inne dni niż bieżąca doba rozkładowa i nie planuje podróży (do tego służy [wtp.waw.pl](https://wtp.waw.pl)). Jeśli masz token, możesz dodatkowo zobaczyć na mapie pojazdy swoich linii.

---

## 🔧 Funkcje

- ✅ Integracja obsługuje autobusy, tramwaje, metro i SKM, także linie nocne, ekspresowe i lokalne.
- ✅ Stanem sensora jest godzina najbliższego odjazdu. Trzy następne odjazdy oraz pierwszy i ostatni odjazd doby znajdziesz w atrybutach.
- ✅ Osobny sensor *Status* wyjaśnia zwykłymi słowami, co się dzieje, na przykład „Na dziś odjazdów już nie ma”.
- ✅ Przystanek dodajesz, wpisując fragment jego nazwy. Potem wybierasz kierunek, w którym jedziesz (gdy przystanek ma więcej niż jeden słupek), i linię, więc nie musisz szukać żadnych numerów.
- ✅ Możesz dodać wiele linii i przystanków, ustawić czas dojścia na przystanek, włączyć kalendarz odjazdów i zobaczyć pojazd na mapie. Kalendarz i pojazd są domyślnie wyłączone.
- ✅ Interfejs jest w ośmiu językach: angielskim, polskim, ukraińskim, rosyjskim, niemieckim, hiszpańskim, francuskim i włoskim. Sześć nowszych wersji przetłumaczył program, więc poprawki w postaci pull requestów są mile widziane.

---

## 📸 Zrzuty ekranu

### Konfiguracja integracji
*Formularz z danymi dostępu, linią i przystankiem.*

<div align="center"><img width="478" alt="image" src="https://github.com/user-attachments/assets/9a77591e-5b1a-4fe5-a29d-637d3c9b566c" /></div>

### Wygląd encji

<div align="center"><img width="555" alt="image" src="https://github.com/user-attachments/assets/ef709b81-1575-4718-9c39-f6c135cf3cca" /></div>

### Atrybuty
*Szczegóły rozkładu, w tym godziny odjazdów i kierunek jazdy.*

<div align="center"><img width="530" alt="image" src="https://github.com/user-attachments/assets/95cde9db-1182-41ba-9ae6-3187bd6a527c" /></div>

---

## 📋 Wymagania

- Home Assistant 2026.1 lub nowszy
- Klucz API lub token z portalu danych miasta (opis poniżej)

---

## 🧭 Klucz i token

Bezpłatny token pobierzesz na stronie [dane.um.warszawa.pl/pl/key-api](https://dane.um.warszawa.pl/pl/key-api): wpisz dowolny pseudonim, zaakceptuj regulamin i pobierz token. Token to długi tekst złożony z trzech części oddzielonych kropkami.

Stary klucz API (`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`, ze strony [api.um.warszawa.pl](https://api.um.warszawa.pl)) już nie działa. Obsługujący go serwer przestał odpowiadać 21 października 2026, a integracja już go nie pyta. Linia ze starym kluczem nie dostaje więc nowego rozkładu, dopóki nie wymienisz klucza na token: otwórz powiadomienie w **Problemach** albo wybierz przy linii **Konfiguruj** i wklej token. Ustawienia linii zostaną zachowane.

---

## 📦 Instalacja

<!-- ha-marketplace:exclude-start -->

### Przez Marketplace (Home Assistant 2026.11+)

Otwórz **Ustawienia → Marketplace**, wyszukaj **Warsaw Public Transport** i zainstaluj integrację. Następnie przejdź do konfiguracji opisanej poniżej; uruchom ponownie Home Assistant, jeśli pojawi się taka prośba.

Korzystasz już z HACS? Home Assistant automatycznie przeniesie zainstalowane repozytoria i ich aktualizacje do Marketplace.

### Przez HACS (Home Assistant 2026.1–2026.10)

1. W Home Assistant otwórz **HACS → Integracje**.
2. Wyszukaj **Warszawski Transport Publiczny**.
3. Kliknij **Pobierz** i potwierdź.
4. Uruchom ponownie Home Assistant.

### Ręcznie

1. Pobierz najnowszą wersję z [GitHub Releases](https://github.com/solarssk/ztm_warsaw/releases).
2. Skopiuj folder `ztm_warsaw` do `/config/custom_components/`.
3. Uruchom ponownie Home Assistant.

---

<!-- ha-marketplace:exclude-end -->

## 🔌 Konfiguracja

1. Przejdź do **Ustawienia → Urządzenia oraz usługi**.
2. Kliknij **+ Dodaj integrację** i wyszukaj **Warszawski Transport Publiczny**.
3. Wklej token, potem wpisz fragment nazwy przystanku (na przykład `Rondo Daszyńskiego`) albo jego ID i wybierz przystanek.
4. Wybierz słupek według kierunku, w którym jedzie (numer jest na tabliczce przystanku, a integracja wyświetla kierunek odczytany z rozkładu), potem linię: na liście są tylko linie, które dziś tam się zatrzymują.

Integracja nazwie sensor na przykład `sensor.line_151_from_7009_01`. Kolejny przystanek tej linii dodasz przyciskiem **Dodaj przystanek**. Jeśli znasz numery, zaznacz na pierwszym ekranie **Znam numery: wpiszę je sam**. Czas dojścia, kalendarz, pojazd na mapie i usuwanie linii opisuje [wiki](https://github.com/solarssk/ztm_warsaw/wiki/1.-Configuration).

---

## 🩺 Rozwiązywanie problemów

- **Sensor ma stan `unknown` i atrybut „No service”.** Linia dziś nie kursuje albo jej ostatni odjazd już był. To nie jest błąd. Którą z tych dwóch sytuacji mamy, powie sensor *Status*. Rozkład sprawdzisz na [wtp.waw.pl](https://wtp.waw.pl) albo pod numerem 19115.
- **Sensor ma stan `unavailable`.** Miasto nie zwróciło poprawnego rozkładu, bo odrzuciło token albo nie zna przystanku, słupka lub linii. Przyczynę znajdziesz w logu Home Assistant. Klucze i tokeny nigdy się w nim nie pojawiają.
- **Linia pokazuje, że stare API już nie działa.** Stare API miasta przestało odpowiadać 21 października 2026, a integracja już go nie pyta. Linia zachowuje rozkład, który miała, do końca doby rozkładowej. Wymień stary klucz na token, tak jak opisano wyżej.
- **Home Assistant prosi o nowy klucz.** Miasto odrzuciło klucz trzy razy z rzędu. Wpisz w formularzu nowy klucz albo token. Ustawienia zostaną zachowane.
- **Chcesz zgłosić problem.** Wybierz przy wpisie *Pobierz diagnostykę* i dołącz plik do zgłoszenia. Klucz i token są w nim zastąpione napisem `**REDACTED**`.

Więcej odpowiedzi znajdziesz w [wiki](https://github.com/solarssk/ztm_warsaw/wiki/4.-Troubleshooting).

---

## 📚 Dokumentacja

Instrukcja obsługi jest w [wiki](https://github.com/solarssk/ztm_warsaw/wiki): [Konfiguracja](https://github.com/solarssk/ztm_warsaw/wiki/1.-Configuration) opisuje czas dojścia i usuwanie linii, [Pojęcia](https://github.com/solarssk/ztm_warsaw/wiki/2.-Concepts) wyjaśniają dobę rozkładową i to, co wyświetla każda encja, [Przykłady](https://github.com/solarssk/ztm_warsaw/wiki/3.-Examples) zawierają karty i automatyzacje do skopiowania, a [Rozwiązywanie problemów](https://github.com/solarssk/ztm_warsaw/wiki/4.-Troubleshooting) odpowiada na typowe pytania. Wiki jest po angielsku, a pliki źródłowe leżą w [`docs/wiki/`](docs/wiki).

---

## 🧑‍💻 Współpraca i bezpieczeństwo

Chcesz zgłosić błąd, zaproponować funkcję lub przesłać poprawkę? Zasady współpracy znajdziesz w [CONTRIBUTING.md](CONTRIBUTING.md). Luki w zabezpieczeniach zgłaszaj zgodnie z instrukcją w [SECURITY.md](SECURITY.md).

---

## 🙌 Dane i podziękowania

Dane: Miasto Stołeczne Warszawa i Zarząd Transportu Miejskiego (ZTM), z portalu otwartych danych ([dane.um.warszawa.pl](https://dane.um.warszawa.pl)), na licencji [Creative Commons Uznanie autorstwa](https://creativecommons.org/licenses/by/4.0/deed.pl).

Sam opracowałem koncepcję integracji, jej funkcje, strukturę i sposób korzystania z publicznego API Warszawy. Nie jestem zawodowym programistą Pythona, ale znajomość jego podstaw pozwoliła mi zaplanować działanie projektu.

Podczas pisania kodu korzystałem z pomocy ChatGPT, przede wszystkim przy składni, diagnozowaniu błędów i szczegółach implementacji. Decyzje dotyczące projektu i jego działania podejmowałem sam.

Dziękuję [@peetereczek](https://github.com/peetereczek/ztm), którego wcześniejszy projekt był dla mnie inspiracją. Ta integracja powstała od podstaw jako niezależny projekt.

Zapraszam do rozwijania projektu — zgłaszania pomysłów, błędów i propozycji poprawek.

---

## 📄 Licencja

Licencja MIT
