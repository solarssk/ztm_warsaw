<h1 align="center">🚍 ZTM Varsovia para Home Assistant</h1>

<p align="center">
  <strong>Horarios del transporte público de Varsovia en Home Assistant.<br>Próximas salidas en tus paneles y automatizaciones. Configuración sin YAML.</strong>
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
  🇪🇸 <strong>Español</strong>
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
<summary><strong>Índice</strong></summary>

- [Funciones](#-funciones)
- [Capturas de pantalla](#-capturas-de-pantalla)
- [Requisitos](#-requisitos)
- [Cómo conseguir una clave o un token](#-cómo-conseguir-una-clave-o-un-token)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Solución de problemas](#-solución-de-problemas)
- [Documentación](#-documentación)
- [Colaboración y seguridad](#-colaboración-y-seguridad)
- [Datos y agradecimientos](#-datos-y-agradecimientos)
- [Licencia](#-licencia)

</details>

La integración muestra en Home Assistant **cuándo sale de tu parada el próximo autobús, tranvía o tren**. Para cada línea en el punto de parada que elijas crea un sensor que puedes poner en un panel o usar en una automatización, por ejemplo para recibir un aviso cuando toca salir de casa. Usa los datos abiertos de la ciudad de Varsovia, así que no necesitas hardware adicional.

La integración lee horarios, por eso muestra salidas **programadas**. No muestra retrasos ni incidencias, no tiene horarios de otros días que no sean el día de servicio actual y no planifica viajes (para eso está [wtp.waw.pl](https://wtp.waw.pl)). Con un token también puedes ver en el mapa los vehículos de tus líneas.

---

## 🔧 Funciones

- ✅ La integración admite autobuses, tranvías, metro y cercanías (SKM), también líneas nocturnas, exprés y locales.
- ✅ El estado del sensor es la hora de la próxima salida. Las tres siguientes, y la primera y la última salida del día, están en los atributos.
- ✅ Un sensor de *Estado* aparte explica con palabras sencillas lo que ocurre, por ejemplo «Hoy ya no hay más salidas».
- ✅ Añades una parada escribiendo parte de su nombre. Después eliges la dirección en la que viajas (si la parada tiene más de un punto de parada) y la línea, así que no tienes que buscar ningún número.
- ✅ Puedes añadir varias líneas y paradas, fijar un tiempo de paseo hasta la parada, activar un calendario de salidas y ver el vehículo en el mapa. El calendario y el vehículo vienen desactivados.
- ✅ La interfaz está en ocho idiomas: inglés, polaco, ucraniano, ruso, alemán, español, francés e italiano. Un programa tradujo los seis más recientes, así que las correcciones en forma de pull request son bienvenidas.

---

## 📸 Capturas de pantalla

### Configuración de la integración
*Formulario de configuración con las credenciales y los datos de la línea y la parada.*

<div align="center"><img width="478" alt="image" src="https://github.com/user-attachments/assets/9a77591e-5b1a-4fe5-a29d-637d3c9b566c" /></div>

### Aspecto de la entidad

<div align="center"><img width="555" alt="image" src="https://github.com/user-attachments/assets/ef709b81-1575-4718-9c39-f6c135cf3cca" /></div>

### Atributos
*Detalles del horario, incluidas las horas de salida y el sentido de circulación.*

<div align="center"><img width="530" alt="image" src="https://github.com/user-attachments/assets/95cde9db-1182-41ba-9ae6-3187bd6a527c" /></div>

---

## 📋 Requisitos

- Home Assistant 2026.1 o posterior
- Una clave API o un token de la ciudad de Varsovia (abajo)

---

## 🧭 Cómo conseguir una clave o un token

Un token gratuito lo consigues en [dane.um.warszawa.pl/pl/key-api](https://dane.um.warszawa.pl/pl/key-api): escribe un apodo cualquiera, acepta las condiciones y descarga el token. Un token es un texto largo formado por tres partes separadas por puntos.

Una clave antigua de la API (`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`, de [api.um.warszawa.pl](https://api.um.warszawa.pl)) ya no funciona. El servidor que la atendía dejó de responder el 21 de octubre de 2026, y la integración ya no le pregunta. Por eso una línea con clave antigua no recibe horarios nuevos hasta que sustituyas la clave por un token: abre el aviso en **Reparaciones** o elige **Configurar** en la línea y pega el token. Los ajustes de la línea se conservan.

---

## 📦 Instalación

<!-- ha-marketplace:exclude-start -->

### Con Marketplace (Home Assistant 2026.11+)

Abre **Ajustes → Marketplace**, busca **Warsaw Public Transport** e instala la integración. Después, sigue los pasos de configuración que aparecen más abajo; reinicia Home Assistant si te lo pide.

¿Ya usas HACS? Home Assistant trasladará automáticamente los repositorios instalados y sus actualizaciones a Marketplace.

### Con HACS (Home Assistant 2026.1–2026.10)

1. En Home Assistant, ve a **HACS → Integraciones**.
2. Busca **Transporte público de Varsovia**.
3. Pulsa **Descargar** y confirma.
4. Reinicia Home Assistant.

### Manualmente

1. Descarga la última versión de [GitHub Releases](https://github.com/solarssk/ztm_warsaw/releases).
2. Copia la carpeta `ztm_warsaw` en `/config/custom_components/`.
3. Reinicia Home Assistant.

---

<!-- ha-marketplace:exclude-end -->

## 🔌 Configuración

1. Ve a **Configuración → Dispositivos y servicios**.
2. Pulsa **+ Añadir integración** y busca **Transporte público de Varsovia**.
3. Pega tu token, escribe parte del nombre de la parada (por ejemplo, `Rondo Daszyńskiego`) o su ID y elige la parada.
4. Elige el punto de parada por hacia dónde va (su número está en el cartel de la parada, y la integración muestra la dirección que lee del horario), y después la línea: solo aparecen las líneas que paran allí hoy.

La integración llamará al sensor, por ejemplo, `sensor.line_151_from_7009_01`. Otra parada de la línea la añades con **Añadir parada**. Si conoces los números, marca en la primera pantalla **Conozco los números: los introduciré yo**. El tiempo de paseo, el calendario, el vehículo en el mapa y cómo quitar una línea se explican en la [wiki](https://github.com/solarssk/ztm_warsaw/wiki/1.-Configuration).

---

## 🩺 Solución de problemas

- **El sensor está en `unknown` y tiene el atributo «No service».** La línea no circula hoy o ya salió su última salida. No es un error. Cuál de los dos casos es lo dice el sensor de *Estado*. El horario lo puedes consultar en [wtp.waw.pl](https://wtp.waw.pl) o llamando al 19115.
- **El sensor está en `unavailable`.** La ciudad no devolvió un horario válido porque rechazó el token o no conoce la parada, el punto de parada o la línea. El motivo está en el registro de Home Assistant. Las claves y los tokens nunca aparecen en él.
- **Tu línea indica que la API antigua ya no funciona.** La API antigua de la ciudad dejó de responder el 21 de octubre de 2026, y la integración ya no le pregunta. La línea conserva el horario que tenía hasta que termine el día de servicio. Sustituye la clave antigua por un token, como se describe arriba.
- **Home Assistant pide una clave nueva.** La ciudad rechazó la clave tres veces seguidas. Introduce en el formulario una clave o un token nuevo. Los ajustes se conservan.
- **Quieres informar de un problema.** Elige *Descargar diagnósticos* en la entrada y adjunta el archivo a tu issue. La clave y el token aparecen en él como `**REDACTED**`.

Hay más respuestas en la [wiki](https://github.com/solarssk/ztm_warsaw/wiki/4.-Troubleshooting).

---

## 📚 Documentación

El manual de usuario está en la [wiki](https://github.com/solarssk/ztm_warsaw/wiki): [Configuración](https://github.com/solarssk/ztm_warsaw/wiki/1.-Configuration) describe el tiempo de paseo y cómo quitar una línea, [Conceptos](https://github.com/solarssk/ztm_warsaw/wiki/2.-Concepts) explica el día de servicio y lo que muestra cada entidad, [Ejemplos](https://github.com/solarssk/ztm_warsaw/wiki/3.-Examples) trae tarjetas y automatizaciones para copiar, y [Solución de problemas](https://github.com/solarssk/ztm_warsaw/wiki/4.-Troubleshooting) responde a las preguntas habituales. La wiki está en inglés y su código fuente está en [`docs/wiki/`](docs/wiki).

---

## 🧑‍💻 Colaboración y seguridad

Puedes proponer ideas, informar de errores o enviar pull requests. Encontrarás las pautas de colaboración en [CONTRIBUTING.md](CONTRIBUTING.md). Para comunicar vulnerabilidades, sigue las instrucciones de [SECURITY.md](SECURITY.md).

---

## 🙌 Datos y agradecimientos

Datos: la ciudad de Varsovia (**Miasto Stołeczne Warszawa**) y la Autoridad de Transporte Público de Varsovia (**Zarząd Transportu Miejskiego**, ZTM), a través del portal de datos abiertos de la ciudad ([dane.um.warszawa.pl](https://dane.um.warszawa.pl)), bajo la licencia [Creative Commons Attribution](https://creativecommons.org/licenses/by/4.0/deed.es).

He diseñado el concepto, las funciones, la estructura y la conexión con la API pública de la ciudad de Varsovia. No soy desarrollador profesional de Python, pero mis conocimientos básicos me han permitido planificar el funcionamiento del proyecto.

He utilizado ChatGPT como apoyo para la sintaxis, la depuración y los detalles de implementación. Las decisiones sobre el diseño y el funcionamiento del proyecto las he tomado yo.

Gracias a [@peetereczek](https://github.com/peetereczek/ztm), cuyo proyecto anterior me sirvió de inspiración. Esta integración se ha creado desde cero como un proyecto independiente.

Te invito a participar en el desarrollo del proyecto con ideas, informes de errores y propuestas de mejora.

---

## 📄 Licencia

Licencia MIT
