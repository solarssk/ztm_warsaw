<h1 align="center">🚍 ZTM Varsavia per Home Assistant</h1>

<p align="center">
  <strong>Gli orari del trasporto pubblico di Varsavia in Home Assistant.<br>Le prossime partenze nelle dashboard e nelle automazioni. Configurazione senza YAML.</strong>
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
  🇩🇪 <a href="README.de.md">Deutsch</a>
  &nbsp;·&nbsp;
  🇪🇸 <a href="README.es.md">Español</a>
  &nbsp;·&nbsp;
  🇫🇷 <a href="README.fr.md">Français</a>
  &nbsp;·&nbsp;
  🇮🇹 <strong>Italiano</strong>
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
<summary><strong>Indice</strong></summary>

- [Funzionalità](#-funzionalità)
- [Schermate](#-schermate)
- [Requisiti](#-requisiti)
- [Come ottenere una chiave o un token](#-come-ottenere-una-chiave-o-un-token)
- [Installazione](#-installazione)
- [Configurazione](#-configurazione)
- [Risoluzione dei problemi](#-risoluzione-dei-problemi)
- [Documentazione](#-documentazione)
- [Contribuire e sicurezza](#-contribuire-e-sicurezza)
- [Dati e ringraziamenti](#-dati-e-ringraziamenti)
- [Licenza](#-licenza)

</details>

L’integrazione mostra in Home Assistant **quando parte dalla tua fermata il prossimo autobus, tram o treno**. Per ogni linea al punto di fermata scelto crea un sensore che puoi mettere in una dashboard o usare in un’automazione, per esempio per ricevere una notifica quando è ora di uscire di casa. Usa i dati aperti della città di Varsavia, quindi non serve hardware aggiuntivo.

L’integrazione legge gli orari, perciò mostra partenze **programmate**. Non mostra ritardi né disservizi, non conosce gli orari di giorni diversi dal giorno di servizio in corso e non pianifica viaggi (per questo c’è [wtp.waw.pl](https://wtp.waw.pl)). Con un token puoi anche vedere sulla mappa i veicoli delle tue linee.

---

## 🔧 Funzionalità

- ✅ L’integrazione supporta autobus, tram, metropolitana e treni urbani (SKM), comprese le linee notturne, espresse e locali.
- ✅ Lo stato del sensore è l’ora della prossima partenza. Le tre successive, la prima e l’ultima partenza della giornata si trovano negli attributi.
- ✅ Un sensore *Stato* a parte spiega con parole semplici cosa succede, per esempio «Oggi non ci sono più partenze».
- ✅ Aggiungi una fermata scrivendo una parte del suo nome. Poi scegli la direzione in cui viaggi (se la fermata ha più di un punto di fermata) e la linea, quindi non devi cercare nessun numero.
- ✅ Puoi aggiungere più linee e fermate, impostare un tempo di cammino fino alla fermata, attivare un calendario delle partenze e vedere il veicolo sulla mappa. Calendario e veicolo sono disattivati per impostazione predefinita.
- ✅ L’interfaccia è disponibile in otto lingue: inglese, polacco, ucraino, russo, tedesco, spagnolo, francese e italiano. Un programma ha tradotto le sei più recenti, quindi le correzioni come pull request sono benvenute.

---

## 📸 Schermate

### Configurazione dell’integrazione
*Il modulo di configurazione con le credenziali e i dati della linea e della fermata.*

<div align="center"><img width="478" alt="image" src="https://github.com/user-attachments/assets/9a77591e-5b1a-4fe5-a29d-637d3c9b566c" /></div>

### Aspetto dell’entità

<div align="center"><img width="555" alt="image" src="https://github.com/user-attachments/assets/ef709b81-1575-4718-9c39-f6c135cf3cca" /></div>

### Attributi
*I dettagli dell’orario, comprese le ore di partenza e la direzione di viaggio.*

<div align="center"><img width="530" alt="image" src="https://github.com/user-attachments/assets/95cde9db-1182-41ba-9ae6-3187bd6a527c" /></div>

---

## 📋 Requisiti

- Home Assistant 2026.1 o successivo
- Una chiave API o un token della città di Varsavia (sotto)

---

## 🧭 Come ottenere una chiave o un token

Un token gratuito si ottiene su [dane.um.warszawa.pl/pl/key-api](https://dane.um.warszawa.pl/pl/key-api): inserisci un nickname qualsiasi, accetta le condizioni e scarica il token. Un token è un testo lungo composto da tre parti separate da punti.

Una vecchia chiave API (`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`, da [api.um.warszawa.pl](https://api.um.warszawa.pl)) non funziona più. Il server che la gestiva ha smesso di rispondere il 21 ottobre 2026 e l’integrazione non lo interroga più. Una linea con una vecchia chiave non riceve quindi nuovi orari finché non sostituisci la chiave con un token: apri l’avviso in **Riparazioni** oppure scegli **Configura** sulla linea e incolla il token. Le impostazioni della linea restano.

---

## 📦 Installazione

<!-- ha-marketplace:exclude-start -->

### Con Marketplace (Home Assistant 2026.11+)

Apri **Impostazioni → Marketplace**, cerca **Warsaw Public Transport** e installa l’integrazione. Poi segui la configurazione qui sotto; riavvia Home Assistant se richiesto.

Usi già HACS? Home Assistant trasferisce automaticamente i repository installati e i relativi aggiornamenti in Marketplace.

### Con HACS (Home Assistant 2026.1–2026.10)

1. In Home Assistant vai su **HACS → Integrazioni**.
2. Cerca **Trasporto pubblico di Varsavia**.
3. Clicca su **Scarica** e conferma.
4. Riavvia Home Assistant.

### Manualmente

1. Scarica l’ultima versione da [GitHub Releases](https://github.com/solarssk/ztm_warsaw/releases).
2. Copia la cartella `ztm_warsaw` in `/config/custom_components/`.
3. Riavvia Home Assistant.

---

<!-- ha-marketplace:exclude-end -->

## 🔌 Configurazione

1. Vai su **Impostazioni → Dispositivi e servizi**.
2. Fai clic su **+ Aggiungi integrazione** e cerca **Trasporto pubblico di Varsavia**.
3. Incolla il token, scrivi una parte del nome della fermata (per esempio `Rondo Daszyńskiego`) o il suo ID e scegli la fermata.
4. Scegli il punto di fermata in base a dove va (il numero è sul cartello della fermata, e l’integrazione mostra la direzione letta dall’orario), poi la linea: sono elencate solo le linee che oggi vi fermano.

L’integrazione chiama il sensore per esempio `sensor.line_151_from_7009_01`. Un’altra fermata della linea si aggiunge con **Aggiungi fermata**. Se conosci i numeri, spunta nella prima schermata **Conosco i numeri: li inserisco io**. Tempo di cammino, calendario, veicolo sulla mappa e rimozione di una linea sono spiegati nella [wiki](https://github.com/solarssk/ztm_warsaw/wiki/1.-Configuration).

---

## 🩺 Risoluzione dei problemi

- **Il sensore è `unknown` e ha l’attributo «No service».** La linea oggi non circola oppure la sua ultima partenza è passata. Non è un errore. Quale dei due casi sia lo dice il sensore *Stato*. L’orario si controlla su [wtp.waw.pl](https://wtp.waw.pl) o chiamando il 19115.
- **Il sensore è `unavailable`.** La città non ha restituito un orario valido, perché ha rifiutato il token oppure non conosce la fermata, il punto di fermata o la linea. Il motivo è nel registro di Home Assistant. Chiavi e token non vi compaiono mai.
- **La tua linea indica che la vecchia API non funziona più.** La vecchia API della città ha smesso di rispondere il 21 ottobre 2026 e l’integrazione non la interroga più. La linea tiene l’orario che aveva fino alla fine del giorno di servizio. Sostituisci la vecchia chiave con un token, come descritto sopra.
- **Home Assistant chiede una nuova chiave.** La città ha rifiutato la chiave tre volte di fila. Inserisci nel modulo una nuova chiave o un nuovo token. Le impostazioni restano.
- **Vuoi segnalare un problema.** Scegli *Scarica la diagnostica* sulla voce e allega il file alla tua issue. La chiave e il token vi compaiono come `**REDACTED**`.

Altre risposte sono nella [wiki](https://github.com/solarssk/ztm_warsaw/wiki/4.-Troubleshooting).

---

## 📚 Documentazione

Il manuale d’uso è nella [wiki](https://github.com/solarssk/ztm_warsaw/wiki): [Configurazione](https://github.com/solarssk/ztm_warsaw/wiki/1.-Configuration) descrive il tempo di cammino e la rimozione di una linea, [Concetti](https://github.com/solarssk/ztm_warsaw/wiki/2.-Concepts) spiega il giorno di servizio e cosa mostra ogni entità, [Esempi](https://github.com/solarssk/ztm_warsaw/wiki/3.-Examples) offre schede e automazioni da copiare, e [Risoluzione dei problemi](https://github.com/solarssk/ztm_warsaw/wiki/4.-Troubleshooting) risponde alle domande più comuni. La wiki è scritta in inglese e i sorgenti sono in [`docs/wiki/`](docs/wiki).

---

## 🧑‍💻 Contribuire e sicurezza

Idee, segnalazioni di errori e pull request sono benvenute. Le indicazioni per contribuire sono in [CONTRIBUTING.md](CONTRIBUTING.md). Per segnalare una vulnerabilità, segui le istruzioni in [SECURITY.md](SECURITY.md).

---

## 🙌 Dati e ringraziamenti

Dati: la città di Varsavia (**Miasto Stołeczne Warszawa**) e l’Autorità del trasporto pubblico di Varsavia (**Zarząd Transportu Miejskiego**, ZTM), tramite il portale dei dati aperti della città ([dane.um.warszawa.pl](https://dane.um.warszawa.pl)), con licenza [Creative Commons Attribution](https://creativecommons.org/licenses/by/4.0/deed.it).

Ho progettato il concetto, le funzionalità, la struttura e il collegamento con l’API pubblica della città di Varsavia. Non sono uno sviluppatore Python professionista, ma le mie conoscenze di base mi hanno permesso di pianificare il funzionamento del progetto.

Ho utilizzato ChatGPT come supporto per la sintassi, il debug e i dettagli di implementazione. Ho preso personalmente le decisioni sul progetto e sul suo funzionamento.

Grazie a [@peetereczek](https://github.com/peetereczek/ztm), il cui progetto precedente mi ha ispirato. Questa integrazione è stata sviluppata da zero come progetto indipendente.

Puoi contribuire allo sviluppo del progetto con idee, segnalazioni di errori e proposte di miglioramento.

---

## 📄 Licenza

Licenza MIT
