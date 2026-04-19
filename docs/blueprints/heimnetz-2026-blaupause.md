---
document_type: blueprint
status: active
precedence: target-semantics
linked_plans: []
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

6. **Fail-closed:**
   Fehler führen zu **sichtbarem Ausfall**, nicht zu impliziten Fallbacks

7. **Enforcement vor Konvention:**
   Regeln gelten nur, wenn sie technisch erzwungen werden

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

* einziger Resolver für `home.arpa`
* einzige Quelle für DNS-Antworten
* alle Clients nutzen ausschließlich Heimberry

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

* kein DNS
* kein VPN-Core
* keine Dev-Primärumgebung

**Invarianten:**

* alle Services nur über Caddy erreichbar
* keine direkten Containerports

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
* kein Proxy / DNS

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

Heimberry:

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

## 3. DNS-Architektur (erzwingbar gemacht)

### 3.1 Root

* `home.arpa`

### 3.2 Zonen

* `heimgewebe.home.arpa`
* `weltgewebe.home.arpa`

### 3.3 Harte Regeln

* Heimberry = einziger Nameserver
* Router verteilt **nur Heimberry als DNS**
* Tailscale DNS → Heimberry
* keine externen Resolver für interne Domains

### 3.4 Enforcement (neu)

Clients müssen:

```bash
resolv.conf → 192.168.178.2
```

Optionaler Guard:

```bash
iptables: block outbound DNS except Heimberry
```

---

## 4. DNS-Stack

```text
Client → Pi-hole → Unbound → Root
```

### Invarianten

* kein externer Upstream
* keine zweite Resolverinstanz
* keine lokalen Overrides

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

### Enforcement

* Docker: keine exposed ports
* Firewall: block direct container access

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
* MagicDNS optional (nicht führend)

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

* 53 (DNS)
* Tailscale intern

### Heimserver

* 80/443 (Caddy)
* 22 (SSH)

### Heim-PC

* Sunshine Ports (Tailnet-only)

### Global

* keine offenen Internetports
* keine direkten Serviceports

---

## 9. IPv6-Policy (explizit gehärtet)

### Zustand

* deaktiviert systemweit

### Enforcement

* Router IPv6 aus
* OS-Level deaktiviert

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

* `/etc/hosts` Overrides
* lokale DNS-Resolver
* direkte Ports
* Shadow-Proxies

### Regel für neue Services

```text
DNS → Caddy → Container
```

---

## 13. Failure-Modell (neu, entscheidend)

### Verhalten

| Komponente fällt aus | Wirkung                              |
| -------------------- | ------------------------------------ |
| Heimberry            | kein DNS → kompletter Zugriff stoppt |
| Heimserver           | DNS ok, aber Services down           |
| Heim-PC              | Dev nicht erreichbar                 |

### Designziel

→ Fehler sind **lokalisierbar und eindeutig**

---

## 14. Migrationsplan (geschärft)

### Phase 1 — Truth

* Heimberry deployen
* DNS vollständig migrieren
* Router DNS erzwingen

**Stop:**

```bash
dig leitstand.home.arpa
```

---

### Phase 2 — Access

* Tailscale auf allen Geräten
* Subnet Routing aktivieren

**Stop:**
iPad erreicht interne FQDNs

---

### Phase 3 — Service

* Caddy konsolidieren
* Container isolieren

**Stop:**
kein direkter Portzugriff

---

### Phase 4 — Interaction

* Sunshine stabilisieren

---

### Phase 5 — Cleanup

* WireGuard entfernen
* alte DNS löschen

---

## 15. Invarianten (unverhandelbar)

1. DNS = Heimberry
2. Overlay = Tailscale
3. Proxy = Heimserver
4. Dev = Heim-PC
5. kein Splitbrain
6. keine Direkt-Exposures

---

## 16. Anti-Patterns

* Dual DNS
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
→ Regeln erzwingbar

---

## 18. Unsicherheits- & Interpolationsanalyse

**Unsicherheitsgrad:** 0.22
Ursachen:

* reale Last Heimberry unbekannt
* Router-Verhalten variabel
* Client-Compliance nicht garantiert

**Interpolationsgrad:** 0.18
Annahmen:

* vollständige DNS-Disziplin möglich
* keine externen Anforderungen an IPv6
* Tailscale stabil akzeptiert
