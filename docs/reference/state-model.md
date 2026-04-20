# State Model

Dieses Dokument definiert, wie Zielzustände, Migrationen und Unsicherheiten im Device-Graph modelliert werden. Da dieses Repository sich in einer aktiven Modellierungsphase befindet, ist epistemische Disziplin unerlässlich.

## Status (Geräte & Netzwerke)

Für Knoten wie Geräte und Netzwerke verwenden wir `status`, um ihren Lebenszyklus auszudrücken:

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
