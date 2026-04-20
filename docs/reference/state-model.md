# State Model

Dieses Dokument definiert, wie Zielzustände, Migrationen und Unsicherheiten im Device-Graph modelliert werden. Da dieses Repository sich in einer aktiven Modellierungsphase befindet, ist epistemische Disziplin unerlässlich.

## Status (Netzwerke)

Netzwerke verfügen über ein natives `status`-Feld im Schema, um ihren physischen/logischen Lebenszyklus auszudrücken. Geräte hingegen werden derzeit primär über Zuordnungen (Assignments), Relationen und Kontext in Migrationsphasen modelliert.

Für Knoten wie Netzwerke verwenden wir `status`:

* **`active`**: Real und in Produktion.
* **`planned`**: Noch nicht realisiert, aber als Zielzustand beschlossen. Ein `planned`-Zustand ist kein Fehler, sondern expliziter Teil des Modells.
* **`retired`**: Historisch, nicht mehr aktiv, aber zur Nachvollziehbarkeit im Modell verblieben.
* **`unknown`**: Epistemische Leerstelle, Datenlage unklar.

## Confidence Levels (Zuweisungen & Relationen)

Für Kanten (Relations) und Zuordnungen (Assignments) verwenden wir `confidence`:

* **`confirmed`**: Der Zustand ist in der Realität existent und durch technische Gegenstücke verifiziert (Ist-Zustand).
* **`planned`**: Der Zustand bildet das beschlossene Architekturziel (Soll-Zustand).
* **`speculative`**: Ein möglicher künftiger Zustand oder eine unbestätigte Annahme.

## Migrationen & Koexistenz

Das Repository modelliert Migrationen durch die bewusste Koexistenz von Ist- und Soll-Zuständen. Parallele Zustände (z. B. `current.yaml` vs. `target.yaml` oder ein `active` VPN neben einem `planned` Overlay) sind zulässig und beabsichtigt. Sie bilden den Zeitpfeil der Architektur ab.

## Rollenasymmetrie: Current vs. Target

Das Repository gestattet eine bewusste Asymmetrie der Rollen zwischen Ist- und Soll-Zustand, um Architekturübergänge zu modellieren:

* **`current.yaml`** (Ist-Zustand): Darf historische, funktionale Rollen (z.B. `dns`, `vpn-server`) tragen.
* **`target.yaml`** (Soll-Zustand): Implementiert die abstrakten, deterministischen Schichtenrollen (z.B. `truth-layer`, `service-layer`).

Diese semantische Dualität ist beabsichtigt. Sie verhindert, dass das Zielbild durch alte Taxonomien verwässert wird, während der aktuelle Betriebsstand wahrheitsgemäß dokumentiert bleibt.
