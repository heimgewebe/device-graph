---
id: runtime-system
title: "Runtime-System (Betrieb und Detection)"
doc_type: operations
role: runtime-mechanics
status: active
canonicality: canonical
last_reviewed: 2026-04-19
summary: "Konkrete Implementierung der Runtime-Detection, Metriken, Alerts und Test-Rituale für das Heimnetz."
depends_on:
  - ../blueprints/heimnetz-2026-blaupause.md
related_docs:
  - runbook-short.md
verifies_with: []
---

# Runtime-System: Detection & Betrieb

Die Architektur-Blaupause fordert Determinismus und Einhaltung von Regeln. Dieses Dokument beschreibt, wie diese Regeln operativ überwacht, gemessen und validiert werden. Das System muss auch dann stabil laufen und Abweichungen (Drift) aufzeichnen, wenn nicht aktiv administriert wird.

---

## A) Detection-Implementierung

Die reine Theorie benötigt zwingend eine technische Exekutive zur Sichtbarmachung von Regelverstößen (Shadow-Configs, DNS-Bypasses).

**Ort der Ausführung:**
* Alle Skripte laufen auf dem **Heimserver** (via `cron` oder `systemd-timers`), um den Heimberry von Nebenaufgaben zu entlasten.

**Notwendige Skripte:**
1. `dns-check.sh`: Führt DNS-Lookups gegen den Heimberry aus und misst Antwortzeit/Erreichbarkeit.
2. `port-scan.sh`: Scannt per Nmap die internen Tailnet/LAN-IPs von Heimberry und Heimserver auf unerwartet offene Ports.
3. `doh-detection.sh`: Prüft Pi-hole Query-Logs (via API oder Logfile) auf bekannte Bootstrap-Domains von DoH-Providern.

**Frequenz:**
* Minütlich: `dns-check.sh`
* Stündlich: `port-scan.sh`
* Täglich: `doh-detection.sh`

**Speicherort für Ergebnisse:**
* Alle Skripte schreiben in simple, rotierende Text-Logs: `/var/log/heimnetz/*.log`

---

## B) Metriken (Persistiert)

Metriken dienen der empirischen Messung des Determinismusgrades. Wir verzichten auf komplexe Monitoring-Stacks (kein Prometheus/Grafana Zwang), sondern nutzen simple Datenstrukturen.

**Erfasste Werte:**
* **DNS-Requests pro Stunde:** Ausgelesen via Pi-hole API.
* **Anteil Heimberry vs. Extern:** (Sofern über Router-Firewall-Zähler erfassbar).
* **Failed Lookups / NXDOMAIN Rate:** Aus Pi-hole Logs.

**Speicherung:**
* Die Werte werden als einfache CSV- oder JSON-Lines-Dateien abgelegt.
* Dies erlaubt eine simple Analyse im Fehlerfall, ohne den Service-Layer mit komplexen Ingest-Pipelines zu belasten.

---

## C) Alerts (Minimal)

Das Ziel ist es, Lärm zu vermeiden, aber bei hartem Architektur-Bruch oder Ausfall sofort zu reagieren. Kein Overengineering.

**Auslöser:**
1. **CRITICAL:** DNS (Heimberry) antwortet nicht auf `dns-check.sh` -> **Sofortiger Alert**.
2. **WARNING:** Das DNS-Request-Volumen droppt unerklärlich um >20% (Indikator für großflächigen Bypass oder DoH-Aktivierung im Netzwerk) -> **Tägliche Warnung**.

**Mechanismus:**
* Simpler Versand per E-Mail, Telegram-Bot oder Gotify-Push-Nachricht.

---

## D) Operational Proof als Ritual

Architektur-Theorien (z.B. "Recovery dauert < 5 Minuten") verfallen, wenn sie nicht geprobt werden.

**Feste Regel:**
Einmal pro Monat wird ein Operational Proof durchgeführt:

1. **Heimberry Reboot testen:** Auslösen eines OS-Reboots, Messung der Zeit bis zur erneuten DNS-Auflösung.
2. **DNS-Ausfall simulieren:** Pi-hole Docker-Container gezielt stoppen, prüfen wie Caddy und kritische Clients reagieren.
3. **Recovery messen:** Abgleich der gemessenen Zeiten mit den harten Zielwerten aus der Blaupause.

**Dokumentation:**
Die Ergebnisse jedes Rituals werden zwingend als Markdown-Log abgelegt unter:
`docs/operations/tests/YYYY-MM.md`
