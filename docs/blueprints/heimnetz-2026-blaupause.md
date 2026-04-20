---
document_type: blueprint
status: final
precedence: target-semantics
linked_plans:
  - ../plans/roadmap.md
  - ../plans/next-steps.md
---
# **Blaupause: Heimnetz 2026+ (Deterministische Layer-Architektur)**

> **Hinweis zur Repository-Grenze:**
> Dieses Dokument im `device-graph`-Repo definiert **ausschließlich die geräteübergreifende Modellsemantik** (Zielrollen, abstrakte Invarianten, Trust-Zonen).
> Jegliche operative Betriebslogik, hostspezifische Runbooks, konkrete Enforcement-Befehle, Detection-Scripts und Port-Regeln sind kanonisch im `heimserver`-Repo angesiedelt.

---

## 1. Abstrakte Leitprinzipien

1. **Single Source of Truth (SoT):** DNS/Name-Auflösung liegt exklusiv bei einem dezidierten Truth-Knoten.
2. **Strikte Ebenentrennung:** Truth ≠ Service ≠ Interaction ≠ Access.
3. **Internal-First + Zero-Exposure:** Kein direkter öffentlicher Ingress. Zugriff erfolgt ausschließlich über ein authentifiziertes Overlay.
4. **Eindeutige Abbildung:** Keine konkurrierenden Wahrheiten oder implizite Fallbacks im kanonischen Architektur-Raum.

---

## 2. Zielrollen der Geräte auf Modellniveau

Das Netzwerk wird über klare, isolierte Geräterollen modelliert:

* **Truth Layer (aktuell: Heimberry):** Autoritative Quelle für Namens- und Netzwerkwahrheit.
* **Service Layer (aktuell: Heimserver):** Führt Applikationen aus und stellt zentrale Zugriffskomponenten bereit. Keine Primärauthorität für das Netz.
* **Interaction Layer (aktuell: Heim-PC):** Zustandsbehafteter Knoten für Entwicklung und Interaktion. Keine Netzwerkautorität.
* **Access Layer (aktuell: iPad):** Zustandsloser Zugriffsknoten über das Overlay-Netzwerk.

---

## 3. Zielnetzwerke und Modell-Beziehungen

* **LAN:** Bildet die physische Unterbauschicht für stationäre Knoten (Heimberry, Heimserver, Heim-PC).
* **Overlay:** Dient als primäre Zugriffsschicht für Routing und Zero-Trust-Isolation.
* **Interdependenz:** Service- und Interaction-Layer vertrauen dem Truth Layer als primärem Namens- und Netzwerk-Verteiler.

---

## 4. Trust-Zonen und Invarianten

* **Kanonischer Namensraum:** Es gibt exakt einen autoritativen, internen FQDN-Namensraum, geführt vom Truth Layer.
* **Isolierte Ausführung:** Der Service Layer ist strikt konsolidiert. Dienste werden nur über zentrale Zugriffskomponenten zugänglich gemacht.
* **Zentraler Zugriff:** Kein Splitbrain zwischen LAN und WAN; das Overlay bildet die einheitliche Vertrauenszone für den Access Layer.

---

## 5. Abgrenzung: Kanonische Wahrheit vs. Administrativer Notpfad

Auf Modellniveau wird zwischen dem intendierten Soll-Zustand und dem betrieblichen Fallback unterschieden:

* **Kanonische Wahrheit:** Der primäre FQDN-Raum, der durch den Truth Layer erzwungen wird.
* **Administrativer Notzugang:** Ein separater, isolierter Namensraum (z.B. über Overlay-Node-Namen), der ausdrücklich *nicht* Teil der kanonischen Zielarchitektur ist, sondern ein operatives Notfallwerkzeug des Service-Layers.

---

## 6. Migrationsziel

Das übergeordnete Modell-Ziel ist die Transition von einer historisch gewachsenen, monolithischen Struktur zu einer deterministischen Schichtenarchitektur:
1. Verlagerung der Netzwerk-Wahrheit auf den dedizierten Truth Layer.
2. Reduktion bestehender Knoten auf reine Service-Rollen ohne Netzwerkautorität.
3. Vollständige Etablierung des Overlay-Netzwerks als primäre Access-Schicht.

*(Hinweis: Alle operativen Migrationspläne, Rollback-Prozeduren und Test-Validierungen liegen im `heimserver`-Repo).*
