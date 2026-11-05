<h1 align="center">🚍 ZTM Varsovie pour Home Assistant</h1>

<p align="center">
  <strong>Les horaires des transports publics de Varsovie dans Home Assistant.<br>Les prochains départs dans vos tableaux de bord et automatisations. Configuration sans YAML.</strong>
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
  🇫🇷 <strong>Français</strong>
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
<summary><strong>Sommaire</strong></summary>

- [Fonctionnalités](#-fonctionnalités)
- [Captures d’écran](#-captures-décran)
- [Prérequis](#-prérequis)
- [Obtenir une clé ou un jeton](#-obtenir-une-clé-ou-un-jeton)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Dépannage](#-dépannage)
- [Documentation](#-documentation)
- [Contribuer et sécurité](#-contribuer-et-sécurité)
- [Données et remerciements](#-données-et-remerciements)
- [Licence](#-licence)

</details>

L’intégration affiche dans Home Assistant **l’heure du prochain bus, tramway ou train à votre arrêt**. Pour chaque ligne au point d’arrêt choisi, elle crée un capteur que vous pouvez placer sur un tableau de bord ou utiliser dans une automatisation, par exemple pour recevoir une notification quand il est temps de partir. Elle utilise les données ouvertes de la ville de Varsovie : aucun matériel supplémentaire n’est nécessaire.

L’intégration lit les horaires, elle affiche donc des départs **prévus**. Elle ne montre ni retards ni perturbations, ne connaît pas les horaires des autres jours que la journée de service en cours et ne calcule pas d’itinéraire (pour cela, voir [wtp.waw.pl](https://wtp.waw.pl)). Avec un jeton, vous pouvez aussi voir sur la carte les véhicules de vos lignes.

---

## 🔧 Fonctionnalités

- ✅ L’intégration prend en charge les bus, les tramways, le métro et les trains urbains (SKM), y compris les lignes de nuit, express et locales.
- ✅ L’état du capteur est l’heure du prochain départ. Vous trouvez les trois suivants, ainsi que le premier et le dernier départ de la journée, dans les attributs.
- ✅ Un capteur *État* distinct explique en mots simples ce qui se passe, par exemple « Plus de départs aujourd’hui ».
- ✅ Vous ajoutez un arrêt en tapant une partie de son nom. Vous choisissez ensuite la direction dans laquelle vous voyagez (si l’arrêt a plus d’un point d’arrêt) et la ligne : inutile de chercher un numéro.
- ✅ Vous pouvez ajouter plusieurs lignes et arrêts, régler un temps de marche jusqu’à l’arrêt, activer un calendrier des départs et voir le véhicule sur la carte. Le calendrier et le véhicule sont désactivés par défaut.
- ✅ L’interface existe en huit langues : anglais, polonais, ukrainien, russe, allemand, espagnol, français et italien. Un programme a traduit les six plus récentes ; les corrections sous forme de pull request sont les bienvenues.

---

## 📸 Captures d’écran

### Configuration de l’intégration
*Le formulaire de configuration des identifiants d’accès, de la ligne et de l’arrêt.*

<div align="center"><img width="478" alt="image" src="https://github.com/user-attachments/assets/9a77591e-5b1a-4fe5-a29d-637d3c9b566c" /></div>

### Aspect de l’entité

<div align="center"><img width="555" alt="image" src="https://github.com/user-attachments/assets/ef709b81-1575-4718-9c39-f6c135cf3cca" /></div>

### Attributs
*Les détails des horaires, notamment les heures de départ et le sens de circulation.*

<div align="center"><img width="530" alt="image" src="https://github.com/user-attachments/assets/95cde9db-1182-41ba-9ae6-3187bd6a527c" /></div>

---

## 📋 Prérequis

- Home Assistant 2026.1 ou plus récent
- Une clé API ou un jeton de la ville de Varsovie (ci-dessous)

---

## 🧭 Obtenir une clé ou un jeton

Vous obtenez un jeton gratuit sur [dane.um.warszawa.pl/pl/key-api](https://dane.um.warszawa.pl/pl/key-api) : saisissez un pseudo quelconque, acceptez les conditions et téléchargez le jeton. Un jeton est un long texte composé de trois parties séparées par des points.

Une ancienne clé API (`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`, de [api.um.warszawa.pl](https://api.um.warszawa.pl)) ne fonctionne plus. Le serveur qui la gérait a cessé de répondre le 21 octobre 2026, et l’intégration ne l’interroge plus. Une ligne avec une ancienne clé ne reçoit donc plus de nouvel horaire tant que vous n’avez pas remplacé la clé par un jeton : ouvrez l’avis dans **Corrections** ou choisissez **Configurer** sur la ligne, puis collez le jeton. Les réglages de la ligne sont conservés.

---

## 📦 Installation

<!-- ha-marketplace:exclude-start -->

### Avec Marketplace (Home Assistant 2026.11+)

Ouvre **Paramètres → Marketplace**, recherche **Warsaw Public Transport** et installe l’intégration. Passe ensuite à la configuration ci-dessous ; redémarre Home Assistant si cela t’est demandé.

Tu utilises déjà HACS ? Home Assistant transfère automatiquement les dépôts installés et leurs mises à jour vers Marketplace.

### Avec HACS (Home Assistant 2026.1–2026.10)

1. Dans Home Assistant, allez dans **HACS → Intégrations**.
2. Recherchez **Transports publics de Varsovie**.
3. Cliquez sur **Télécharger** et confirmez.
4. Redémarrez Home Assistant.

### Manuellement

1. Téléchargez la dernière version depuis [GitHub Releases](https://github.com/solarssk/ztm_warsaw/releases).
2. Copiez le dossier `ztm_warsaw` dans `/config/custom_components/`.
3. Redémarrez Home Assistant.

---

<!-- ha-marketplace:exclude-end -->

## 🔌 Configuration

1. Allez dans **Paramètres → Appareils et services**.
2. Cliquez sur **+ Ajouter une intégration** et cherchez **Transports publics de Varsovie**.
3. Collez votre jeton, saisissez une partie du nom de l’arrêt (par exemple `Rondo Daszyńskiego`) ou son ID, puis choisissez l’arrêt.
4. Choisissez le point d’arrêt selon où il va (son numéro figure sur le panneau, et l’intégration affiche la direction lue dans l’horaire), puis la ligne : seules les lignes qui s’y arrêtent aujourd’hui sont proposées.

L’intégration nomme le capteur par exemple `sensor.line_151_from_7009_01`. Vous ajoutez un autre arrêt de la ligne avec **Ajouter un arrêt**. Si vous connaissez les numéros, cochez **Je connais les numéros : je les saisis moi-même** sur le premier écran. Le temps de marche, le calendrier, le véhicule sur la carte et la suppression d’une ligne sont expliqués dans le [wiki](https://github.com/solarssk/ztm_warsaw/wiki/1.-Configuration).

---

## 🩺 Dépannage

- **Le capteur est à `unknown` et porte l’attribut « No service ».** La ligne ne circule pas aujourd’hui, ou son dernier départ est passé. Ce n’est pas une erreur. Le capteur *État* indique de quel cas il s’agit. Vous pouvez vérifier l’horaire sur [wtp.waw.pl](https://wtp.waw.pl) ou en appelant le 19115.
- **Le capteur est à `unavailable`.** La ville n’a pas renvoyé d’horaire valide, parce qu’elle a refusé le jeton ou qu’elle ne connaît pas l’arrêt, le point d’arrêt ou la ligne. La raison figure dans le journal de Home Assistant. Les clés et les jetons n’y apparaissent jamais.
- **Votre ligne indique que l’ancienne API ne fonctionne plus.** L’ancienne API de la ville a cessé de répondre le 21 octobre 2026, et l’intégration ne l’interroge plus. La ligne garde l’horaire qu’elle avait jusqu’à la fin de la journée de service. Remplacez l’ancienne clé par un jeton, comme décrit plus haut.
- **Home Assistant demande une nouvelle clé.** La ville a refusé la clé trois fois de suite. Saisissez une nouvelle clé ou un nouveau jeton dans le formulaire. Les réglages sont conservés.
- **Vous voulez signaler un problème.** Choisissez *Télécharger les diagnostics* sur l’entrée et joignez le fichier à votre ticket. La clé et le jeton y sont remplacés par `**REDACTED**`.

D’autres réponses se trouvent dans le [wiki](https://github.com/solarssk/ztm_warsaw/wiki/4.-Troubleshooting).

---

## 📚 Documentation

Le manuel d’utilisation se trouve dans le [wiki](https://github.com/solarssk/ztm_warsaw/wiki) : [Configuration](https://github.com/solarssk/ztm_warsaw/wiki/1.-Configuration) décrit le temps de marche et la suppression d’une ligne, [Concepts](https://github.com/solarssk/ztm_warsaw/wiki/2.-Concepts) explique la journée de service et ce qu’affiche chaque entité, [Exemples](https://github.com/solarssk/ztm_warsaw/wiki/3.-Examples) propose des cartes et des automatisations à copier, et [Dépannage](https://github.com/solarssk/ztm_warsaw/wiki/4.-Troubleshooting) répond aux questions courantes. Le wiki est rédigé en anglais et ses sources sont dans [`docs/wiki/`](docs/wiki).

---

## 🧑‍💻 Contribuer et sécurité

Les idées, signalements de bugs et pull requests sont les bienvenus. Les consignes de contribution figurent dans [CONTRIBUTING.md](CONTRIBUTING.md). Pour signaler une vulnérabilité, suivez les instructions de [SECURITY.md](SECURITY.md).

---

## 🙌 Données et remerciements

Données : la ville de Varsovie (**Miasto Stołeczne Warszawa**) et l’autorité des transports publics de Varsovie (**Zarząd Transportu Miejskiego**, ZTM), via le portail de données ouvertes de la ville ([dane.um.warszawa.pl](https://dane.um.warszawa.pl)), sous licence [Creative Commons Attribution](https://creativecommons.org/licenses/by/4.0/deed.fr).

J’ai conçu le principe, les fonctionnalités, la structure et la connexion à l’API publique de la ville de Varsovie. Je ne suis pas développeur Python professionnel, mais mes connaissances de base m’ont permis de définir le fonctionnement du projet.

J’ai utilisé ChatGPT pour m’aider avec la syntaxe, le débogage et les détails de l’implémentation. J’ai pris moi-même les décisions concernant la conception et le fonctionnement du projet.

Merci à [@peetereczek](https://github.com/peetereczek/ztm), dont le projet précédent m’a inspiré. Cette intégration a été créée de toutes pièces comme un projet indépendant.

Vous pouvez contribuer au projet en proposant des idées, en signalant des bugs ou en soumettant des améliorations.

---

## 📄 Licence

Licence MIT
