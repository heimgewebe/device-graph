# State Model

Dieses Dokument definiert, wie Zielzustände, Migrationen und Unsicherheiten im Device-Graph modelliert werden. Da dieses Repository sich in einer aktiven Modellierungsphase befindet, ist epistemische Disziplin unerlässlich.

## Confidence Levels (Zuweisungssicherheit)

Für Zuordnungen (Assignments) verwenden wir `confidence`, um den Grad der Gewissheit oder den Implementierungsstatus auszudrücken:

* **`confirmed`**: Der Zustand ist in der Realität existent und durch technische Gegenstücke verifiziert (Ist-Zustand).
* **`planned`**: Der Zustand ist noch nicht oder nicht vollständig realisiert, bildet aber das beschlossene Architekturziel (Soll-Zustand).
* **`speculative`**: Ein möglicher künftiger Zustand oder eine unbestätigte Annahme.
