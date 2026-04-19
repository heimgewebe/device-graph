# Agentenanweisung für `device-graph`

Du arbeitest in einem **Modell-Repo**, nicht in einem Infrastruktur- oder Konfigurations-Repo.

Deine Aufgabe ist es, das Repo als **konsistentes, explizites und maschinenlesbares Modell** von Geräten, Netzwerken, Rollen, Beziehungen, Vertrauenszonen und Migrationen zu pflegen.

## Lies zuerst

1. `README.md`
2. `repo.meta.yaml`
3. `AGENTS.md`
4. `docs/index.md`
5. relevante Dateien in `docs/reference/`, `data/` und `schemas/`

## Grundregeln

* Triff keine stillen Annahmen.
* Füge keine implizite Semantik ein.
* Markiere Unsicherheit explizit.
* Behandle das Repo als **Karte von Realität und Zielzuständen**, nicht als Laufzeitkonfiguration.

## Modellgrenzen

Dieses Repo ist zuständig für:

* Geräte
* Netzwerke
* Rollen
* Rollen-Zuordnungen
* allgemeine Graph-Beziehungen
* Vertrauenszonen
* Migrationen

Dieses Repo ist **nicht** zuständig für:

* host-spezifische Primärkonfiguration
* Secrets
* produktive Runbooks
* Spiegel anderer Infra-Repos

## Strukturdisziplin

Nutze die Verzeichnisse strikt nach ihrer Funktion:

* `data/devices/` → Geräte
* `data/networks/` → Netzwerke
* `data/roles/` → Rollen
* `data/assignments/` → Rolle-zu-Gerät-Zuordnungen
* `data/relations/` → allgemeine Graph-Kanten

Wichtig:

* Rolle-zu-Gerät-Zuordnungen nur in `data/assignments/`
* keine `HAS_ROLE`-ähnlichen Relationen in `data/relations/`

## Epistemische Disziplin

Zukünftige, unsichere oder nur teilweise beobachtete Zustände müssen explizit markiert werden.

Verwende insbesondere:

* `status`
* `confidence`
* `visibility`

Spekulative Architektur darf nie als Fakt dargestellt werden.

## Blueprint vs Plan

* `docs/blueprints/` enthält **Sollbilder, Architekturziele, Modelllogik**
* `docs/plans/` enthält **operative Schritte, Reihenfolgen, Umsetzungspfad**

Wenn Blaupause und Plan auseinanderlaufen:

* Blaupause regelt die Zielsemantik
* Plan regelt die Ausführungsreihenfolge
* jede Abweichung muss explizit gemacht werden

Alle Blaupausen und Pläne sollen wechselseitig aufeinander verweisen, damit ihre Beziehung für Menschen und Agents nachvollziehbar bleibt.

## Referenzdisziplin

* `docs/reference/` definiert die semantischen Leitplanken
* Änderungen an Relationen und Zustandsfeldern müssen mit den aktiven Schemas und den Referenzdokumenten vereinbar sein
* Wenn Referenzdokumente noch unvollständig sind, darfst du keine stillen Bedeutungen ergänzen

## Validierung

Bei jeder Änderung an `data/` oder `schemas/` ist verpflichtend:

```bash
make validate
```

Ohne erfolgreiche Validierung gilt eine Änderung nicht als abgeschlossen.

## Generated Content

* `docs/_generated/` niemals manuell editieren
* Wenn dort etwas falsch ist: Quelle korrigieren, nicht Ausgabe

## Was gute Änderungen auszeichnet

Eine gute Änderung:

* erhöht Klarheit
* reduziert Ambiguität
* hält Unsicherheit sichtbar
* wahrt die Trennung der Konzepte
* bleibt schema- und modellkonform

Eine schlechte Änderung:

* versteckt Annahmen
* vermischt Rolle, Gerät und Relation
* erzeugt doppelte Wahrheit
* verletzt Validierung
* löst operative Probleme durch semantische Unschärfe

## Wenn du unsicher bist

Bevorzuge:

* explizite Felder statt Abkürzungen
* einfache Struktur statt impliziter Logik
* markierte Unsicherheit statt Spekulation
* Verweise statt stiller Parallelwelten
