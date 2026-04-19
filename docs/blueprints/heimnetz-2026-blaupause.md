---
id: heimnetz-2026
title: "Blaupause: Heimnetz 2026+ (Deterministische Layer-Architektur, gehärtet & durchsetzbar)"
doc_type: blueprint
role: target-semantics
status: active
canonicality: canonical
last_reviewed: 2026-04-19
summary: "Architektur-Blaupause für eine deterministische, ebenen-basierte Heimnetz-Infrastruktur mit klarem Failure-Tiering und Enforcement-Regeln."
depends_on: []
related_docs:
  - ../plans/roadmap.md
  - ../plans/next-steps.md
verifies_with: []
---
# **Blaupause: Heimnetz 2026+ (Deterministische Layer-Architektur, gehärtet & durchsetzbar)**

---

## 0. Leitprinzipien (kanonisch, präzisiert)

1. **Single Source of Truth (SoT):**
   DNS/Name → **Heimberry** (erzwingbar, nicht nur intendiert)

2. **Strikte Ebenentrennung:**
   **Truth ≠ Service ≠ Interaction ≠ Access**

3. **Internal-First + Zero-Exposure:**
   Kein Internet-Ingress. Zugriff ausschließlich über Overlay.

4. **Determinismus vor Komfort:**
   Jeder Request ist rekonstruierbar (DNS → Proxy → Service)

5. **Eindeutige Abbildung:**
   `1 FQDN → 1 IP → 1 Proxy → 1 Upstream`

6. **Kontrollierte Fehlertoleranz:**
   Fehler führen zu **vorhersehbaren, degradierten Zuständen**, anstatt das Gesamtsystem untrennbar ausfallen zu lassen.

7. **Enforcement vor Konvention:**
   Regeln gelten nur, wenn sie technisch erzwungen und kontinuierlich verifiziert werden.

---

## 1. Geräte-Rollen (final, gehärtet)

### 1.1 Heimberry — **Truth Layer**

**OS/Runtime:** Debian Bookworm Lite + Docker

**Pflichtdienste:**

* Pi-hole (DNS authoritative + filtering)
* Unbound (rekursiver Resolver)
* Tailscale (Subnet Router + DNS Advertiser)

**Optionale Dienste:**

* DHCP (nur bei vollständiger Router-Deaktivierung)
* node-exporter (Observability)

**Explizit ausgeschlossen:**

* kein Reverse Proxy
* keine App-Container
* keine GUI / Dev / Media

**Invarianten:**

* einziger primärer Resolver für `home.arpa`
* primäre Quelle für DNS-Antworten
* alle Clients nutzen primär Heimberry

**Betriebsanforderungen (SPOF-Mitigation):**
* **Monitoring:** Erreichbarkeit und DNS-Antwortzeiten müssen extern (z.B. vom Heimserver) überwacht werden.
* **Recovery:** Automatischer Docker-Restart bei Crash; dokumentierte manuelle Restart-Prozedur für das OS.
* **Backup:** Tägliche Backups der Pi-hole-Konfiguration und Tailscale-State auf ein externes Ziel.

---

### 1.2 Heimserver — **Service Layer**

**Runtime:** Docker + Compose

**Pflichtdienste:**

* Caddy (Reverse Proxy + interne CA)
* Applikationen

**Optionale Dienste:**

* Worker / Queues
* interne Tools (nicht kanonisch)

**Explizit ausgeschlossen:**

* kein primäres DNS
* kein VPN-Core
* keine Dev-Primärumgebung

**Invarianten:**

* alle Services nur über Caddy erreichbar
* keine direkten Containerports
* stellt Monitoring-Watchdog für Heimberry bereit

---

### 1.3 Heim-PC — **Interaction Layer**

**Rolle:** Entwicklung + GPU + Zustandsträger

**Pflichtdienste:**

* VS Code / Toolchain
* Sunshine

**Optionale Dienste:**

* temporäre Testcontainer (nicht persistent)

**Explizit ausgeschlossen:**

* keine Netzwerkautorität
* kein Proxy / primäres DNS

**Invarianten:**

* einziger kanonischer Dev-State
* keine parallelen Arbeitskopien als Wahrheit

---

### 1.4 iPad — **Access Layer**

**Rolle:** Zustandsloser Zugriff

**Tools:**

* Moonlight
* Tailscale
* optional SSH

**Invariante:**

* keine Persistenz
* keine lokale Logik

---

## 2. Netzwerk-Topologie (präzisiert)

### 2.1 LAN

* `192.168.178.0/24`
* Heimberry: `192.168.178.2`
* Heimserver: `192.168.178.46`
* Heim-PC: `192.168.178.25`

### 2.2 Overlay

* ausschließlich **Tailscale**

Heimberry (Primärer Router/DNS):

```bash
tailscale up \
  --advertise-routes=192.168.178.0/24 \
  --accept-dns=false
```

### 2.3 Routing-Invarianten

* kein Portforwarding
* kein Dual-VPN
* kein implizites Routing
* kein Internet-Ingress

---

## 3. DNS-Architektur & Resilienz (erzwingbar gemacht)

### 3.1 Root

* `home.arpa`

### 3.2 Zonen

* `heimgewebe.home.arpa`
* `weltgewebe.home.arpa`

### 3.3 Harte Regeln & Resilienz-Strategie

* **Primär:** Heimberry = primärer Nameserver für alle Zonen. `home.arpa` bleibt exklusiv Heimberry-geführt.
* **Secondary/Fallback (Neu):** Tailscale MagicDNS ist **NICHT** sekundäre Wahrheit für `home.arpa`. Es ist ein **separater administrativer Notzugangspfad** außerhalb des kanonischen Heimnetz-Namensraums für kritische Knoten-IPs, falls Heimberry ausfällt. Ein degradierter Betrieb bedeutet hier nicht, dass sich die DNS-Wahrheit verlagert, sondern nur, dass ein eingeschränkter Admin-Zugriff möglich bleibt.
* **Router DHCP Ziel:** Kein konkurrierender zweiter Resolver im DHCP. Keine gleichrangigen DNS-Server verteilen. Notfallpfade laufen bewusst außerhalb von DHCP.
* Tailscale DNS → Heimberry.

### 3.4 Enforcement (Konkretisiert)

Clients müssen explizit konfiguriert werden.

**Mechanismen:**
* **Linux/Server (`resolv.conf`):** Hardcoded auf `nameserver 192.168.178.2`.
* **Tailscale Admin Console:** Global Nameserver auf `192.168.178.2` gesetzt, Override Local DNS aktiviert.
* **Router DHCP:** DHCP-Option 6 (DNS) verteilt ausschließlich `192.168.178.2`.

**Überprüfbare Bedingung (CI/Monitoring):**
```bash
# Muss immer eine IP liefern, nicht NXDOMAIN oder Timeout
dig @192.168.178.2 leitstand.heimgewebe.home.arpa +short
```

---

## 4. DNS-Stack

```text
Client → Pi-hole → Unbound → Root
```

### Invarianten

* kein externer Upstream im Pi-hole (immer Unbound)
* keine zweite aktive *vollwertige* Resolverinstanz (MagicDNS ist nur Notnagel)
* keine lokalen Overrides in `/etc/hosts` für Produktionsdienste

---

## 5. Reverse Proxy & TLS (gehärtet)

### Ort

* ausschließlich Heimserver

### Regeln

* jede App → FQDN
* interne CA verpflichtend
* kein Direktzugriff auf Container

### Beispiel

```caddy
leitstand.heimgewebe.home.arpa {
    reverse_proxy http://leitstand:3000
}
```

### Enforcement (Konkretisiert)

* **Docker Compose (Heimserver):** App-Container binden Ports ausschließlich an `127.0.0.1` oder spezifisch an ein isoliertes Caddy-Netzwerk. Striktes Verbot von `ports: - "3000:3000"` ohne IP-Bindung für alle Dienste, außer Caddy selbst. Caddy verwaltet als einziger Dienst die Host-Ports 80/443.
* **Host Firewall (UFW/iptables):**
  * **Heimberry:** Erlaubt nur Port 53 (DNS) aus dem LAN/Tailnet sowie Tailscale-interne Ports. Pi-hole Webinterface ist nur über Tailscale erreichbar.
  * **Heimserver:** Erlaubt nur Ports 80/443 (Caddy) aus dem LAN/Tailnet und Port 22 (SSH) als Admin-Zugang. Alle direkten App-Ports von außen sind strikt verboten.
  * **Heim-PC:** Erlaubt Sunshine-Ports ausschließlich Tailnet-only. SSH ist Tailnet-only.

---

## 6. Access Layer (VPN, final)

### Entscheidung

* ausschließlich **Tailscale**

### Funktionen

* Device Mesh
* Subnet Routing
* DNS Integration

### DNS-Konfig

* Nameserver → Heimberry
* MagicDNS aktiv, aber streng limitiert als separater administrativer Notzugang (nicht als kanonischer Fallback)

### Invarianten

* kein zweites VPN
* keine alternative Routinglogik

---

## 7. Remote Development (präzisiert)

### Primär

```text
iPad → Tailscale → Heim-PC → Moonlight → Dev
```

### Sekundär

```text
iPad → Heimserver → SSH/code-server
```

### Regeln

* Dev-State nur auf Heim-PC
* keine Cloud als Primärsystem
* keine Sync-basierten Doppelzustände

---

## 8. Port-Disziplin

### Heimberry

* 53 (DNS) - LAN & Tailnet
* Tailscale intern
* Pi-hole Webinterface - Tailnet-only

### Heimserver

* 80/443 (Caddy) - LAN & Tailnet
* 22 (SSH) - LAN & Tailnet

### Heim-PC

* Sunshine Ports - Tailnet-only
* 22 (SSH) - Tailnet-only

### Global

* keine offenen Internetports
* keine direkten Serviceports

---

## 9. IPv6-Policy (explizit gehärtet)

### Zustand

* deaktiviert systemweit

### Enforcement

* Router IPv6 aus
* OS-Level (`sysctl net.ipv6.conf.all.disable_ipv6=1`) deaktiviert

### Aktivierung nur wenn:

* DNS vollständig IPv6-fähig
* Pi-hole + Unbound integriert
* kein paralleler Resolver entsteht

---

## 10. Sicherheitsmodell

* Zero Trust via Overlay
* interne TLS-CA verpflichtend
* keine extern erreichbaren Dienste
* keine impliziten Trust-Zonen

---

## 11. Observability (erweitert)

### Minimal

* Pi-hole Query Logs
* Caddy Access Logs

### Erweiterung

* **Heimberry Health-Check:** Skript auf dem Heimserver prüft minütlich DNS-Auflösung und alarmiert bei Ausfall.
* zentraler Log-Aggregator (optional)
* Query-Tracing möglich

### Ziel

```text
jede Anfrage nachvollziehbar:
Client → DNS → Proxy → Service
```

---

## 12. Drift-Prevention (erzwingbar)

### Verbote

* `/etc/hosts` Overrides bleiben im Normalbetrieb strikt verboten. Temporäre Incident-Overrides sind nur auf definierten Admin-Clients zulässig, sind dokumentations- und rollbackpflichtig, und gelten ausdrücklich nicht als kanonische Konfiguration.
* lokale DNS-Resolver
* direkte Ports
* Shadow-Proxies

### Regel für neue Services

```text
DNS → Caddy → Container
```

---

## 13. Failure-Tiering (Fehlertoleranz-Modell)

Das System muss vorhersehbar reagieren, wenn Komponenten ausfallen.

### Zustand 1: Normalbetrieb
Alle Systeme online.
* **Routing:** FQDNs werden via Heimberry aufgelöst.
* **Services:** Voller Zugriff via Caddy mit TLS.

### Zustand 2: Degradierter Admin-Zugriff (Heimberry offline)
Heimberry (DNS) fällt aus, aber Heimserver & PC laufen noch.
* **Was funktioniert noch:** Physische Verbindungen, IP-Routing, Tailscale-Verbindungen. Services laufen im Hintergrund weiter.
* **Was ist kaputt:** Kanonische `.home.arpa` DNS-Auflösung schlägt global fehl. Ad-Filtering ist inaktiv.
* **Gültige Namenspfade:** Nur MagicDNS Node-Namen (`heimserver`, `heim-pc`) als administrativer Notzugang. Kanonische FQDNs sind offline.
* **Zulässige Zugriffswege (Degraded Access Path):**
  * SSH-Zugriff über IP (`192.168.178.46` oder Tailscale-IP).
  * Administrative Zugriffe über MagicDNS Node-Namen.
* **Temporäre Ausnahmen:** Lokale `/etc/hosts` Notfall-Einträge auf definierten Admin-Clients für kritische Caddy-Dienste (dokumentations- und rollbackpflichtig).
* **Aktion:** Prio 1 Restart Heimberry.

### Zustand 2b: Degradierter App-Betrieb
DNS ist online, aber Reverse Proxy (Caddy) ist in Teilen gestört oder intern blockiert.
* **Was funktioniert noch:** DNS-Auflösung.
* **Was ist kaputt:** App-Erreichbarkeit über FQDNs.
* **Zulässige Zugriffswege:** Lokales Port-Forwarding (SSH-Tunnel) an `127.0.0.1` des Heimservers zur Diagnose. Direkte IP-Zugriffe bleiben verboten.

### Zustand 3: Total Failure (Heimserver offline)
Heimserver (Proxy/Services) fällt aus.
* **Was funktioniert noch:** DNS funktioniert weiterhin (wenn Heimberry online), liefert aber "Connection Refused" auf FQDNs.
* **Was ist kaputt:** Alle Applikationen nicht erreichbar. Reverse Proxy offline.
* **Zulässige Zugriffswege:** Direkter physischer oder SSH-Zugriff auf Heimserver (via IP oder MagicDNS) zur Fehlerbehebung.
* **Aktion:** Wiederherstellung des Service-Layers.

### Designziel
Fehler sind **lokalisierbar, eindeutig und erlauben administrativen Notfallzugriff.**

---

## 14. Gehärteter Migrationsplan

### Phase 1 — Truth (Risiko-Minimiert)

* Heimberry deployen & konfigurieren
* **Parallelbetrieb:** Router DNS bleibt vorerst unverändert. Einzelne Clients (z.B. Admin-PC) manuell auf Heimberry umstellen.
* **Validierung:** `dig @192.168.178.2 google.com` und `dig @192.168.178.2 leitstand.heimgewebe.home.arpa` müssen stabil antworten.
* Router DNS auf Heimberry umstellen (mit 24h Überwachungsphase).
* **Rollback-Plan:** Bei Störungen im LAN Router-DHCP sofort zurück auf Provider-DNS stellen.

### Phase 2 — Access

* Tailscale auf allen Geräten
* Subnet Routing aktivieren
* Tailscale DNS auf Heimberry lenken

**Validierung:** iPad erreicht interne FQDNs ohne lokales WLAN.

### Phase 3 — Service

* Caddy konsolidieren
* Container-Ports von `0.0.0.0` auf `127.0.0.1` oder internes Docker-Netz umstellen.

**Validierung:** `curl http://heimserver:3000` (direkter Port) muss fehlschlagen, `curl https://leitstand.heimgewebe.home.arpa` muss funktionieren.

### Phase 4 — Interaction

* Sunshine stabilisieren

### Phase 5 — Cleanup

* WireGuard entfernen
* alte DNS (alte Pi-holes etc.) löschen

---

## 15. Invarianten (unverhandelbar)

1. DNS = Heimberry (primär)
2. Overlay = Tailscale
3. Proxy = Heimserver
4. Dev = Heim-PC
5. kein Splitbrain (keine zwei gleichwertigen Wahrheiten)
6. keine Direkt-Exposures

---

## 16. Anti-Patterns

* Dual DNS (zwei unterschiedliche DNS Server im DHCP, führt zu zufälligen Ergebnissen)
* Dual VPN
* mehrere Proxies
* exposed Container
* mehrere Dev-Wahrheiten
* halb aktiviertes IPv6

---

## 17. Essenz

**Struktur:**

* Heimberry → Wahrheit
* Heimserver → Dienste
* Heim-PC → Interaktion
* iPad → Zugriff

**Logik:**

→ Wahrheit zentral
→ Zugriff flexibel
→ Ausführung isoliert
→ Regeln erzwingbar und bei Ausfall vorhersehbar

---

## 18. Unsicherheits- & Interpolationsanalyse

**Unsicherheitsgrad:** 0.15 (gesenkt durch Failure-Tiering)
Ursachen:

* reale Last Heimberry unbekannt
* Client-Verhalten bei MagicDNS Fallback im Detail zu testen

**Interpolationsgrad:** 0.20
Annahmen:

* vollständige DNS-Disziplin ist operativ durchhaltbar
* MagicDNS reicht als administrativer Notfall-Zugriff
* Heimberry-Hardware ist hinreichend stabil

---

## 19. Abgrenzung: Kanonische Wahrheit vs. Administrativer Notpfad

Um Splitbrain-Szenarien und Architekturdrift zu vermeiden, wird hiermit explizit getrennt:

* **Kanonischer DNS-Raum (`home.arpa`):** Die exklusive, autoritative Quelle für alle Dienste und Endpunkte im Normalbetrieb. Wird ausschließlich von Heimberry bereitgestellt.
* **Notzugang über Tailscale/MagicDNS:** Ein separater, isolierter Namensraum (`Node-Namen`), der **nicht** Teil der kanonischen Architektur ist. Er dient ausschließlich dem administrativen Notfallzugriff, wenn der kanonische Raum gestört ist.
* **Nicht-kanonische Incident-Hilfen:** Temporäre Overrides (z.B. `/etc/hosts` auf Admin-Maschinen) sind explizit keine Architekturmerkmale, sondern operative Werkzeuge für den Ausfallmodus. Sie unterliegen einer strikten Rollback-Pflicht nach Behebung des Incidents.
