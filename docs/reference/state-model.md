# State Model

Das Repo nutzt Statusfelder, um zwischen Fakten, Plänen und Ungewissheiten zu differenzieren.

## Device Status (`status`)
- **`active`**: Gerät ist aktuell physisch im Netz in Betrieb.
- **`planned`**: Gerät ist geplant, bestellt oder existiert als reines Architektur-Vorhaben, ist aber noch nicht im Live-Netz.
- **`retired`**: Gerät existiert nicht mehr im Setup, wird aber aus historischen Gründen behalten.
- **`unknown`**: Status konnte noch nicht sauber festgestellt werden.

## Assignment Confidence (`confidence`)
- **`confirmed`**: Die Rollenzuweisung ist Fakt und aktuell in Produktion ausgerollt.
- **`planned`**: Eine bewusste Architekturentscheidung, die auf Umsetzung wartet.
- **`speculative`**: Ein noch nicht beschlossener, aber diskutierter Zielzustand.

## Visibility (`visibility`)
- **`direct`**: Das Gerät ist direkt im Netzwerk (z.B. per IP) ansprechbar.
- **`indirect`**: Das Gerät ist nur durch ein Gateway oder einen Hub (z.B. Zigbee) erreichbar.
- **`inferred`**: Das Gerät wurde nicht explizit gefunden, seine Existenz wird aber durch Traffic oder andere Logs abgeleitet.
- **`unknown`**: Sichtbarkeit unklar.
