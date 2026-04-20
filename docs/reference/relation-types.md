# Relation Types

Dieses Dokument definiert die verbindliche Semantik für die zulässigen Relationen (Edges) im Device-Graph. Alle Kanten müssen einem dieser Typen entsprechen.

* **`connected_to`**: Physische oder logische (Netzwerk-)Verbindung. Wird primär verwendet, um Geräte mit Netzwerken zu verknüpfen (reine Topologie, keine Semantik über Autorität).
* **`depends_on`**: Funktionale Abhängigkeit. Ein Knoten benötigt einen anderen für seine primäre Funktion (z.B. Routing, Zugriff), erfordert aber nicht zwingend eine Vertrauensbeziehung.
* **`managed_by`**: Administrative Steuerung. Ein Knoten wird durch einen anderen konfiguriert, orchestriert oder überwacht.
* **`trusts`**: Vertrauensbeziehung (Security/Identity). Ein Knoten delegiert Autorität (z.B. Namensauflösung, Authentifizierung, kanonische Wahrheit) explizit an einen anderen Knoten.
* **`exposed_to`**: Ingress/Exposure. Ein Dienst oder Port wird einem Netzwerk oder einem anderen Knoten gegenüber offengelegt.
