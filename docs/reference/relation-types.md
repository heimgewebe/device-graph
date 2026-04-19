# Relation Types

Dieses Dokument definiert die zulässigen Relationstypen im Graph und ihre erlaubte Verwendung.

## `connected_to`
- **Bedeutung**: Ein Gerät ist physisch oder auf L2/L3-Ebene mit einem Netzwerk verbunden.
- **Erlaubte Source-Klassen**: Device
- **Erlaubte Target-Klassen**: Network
- **Beispiel**: `dev-heimserver-01` connected_to `net-lan-main`

## `depends_on`
- **Bedeutung**: Eine Ressource setzt das Funktionieren einer anderen Ressource voraus (z.B. logische Abhängigkeit).
- **Erlaubte Source-Klassen**: Device, Role
- **Erlaubte Target-Klassen**: Device, Role
- **Beispiel**: `role-reverse-proxy` depends_on `role-dns`

## `managed_by`
- **Bedeutung**: Ein Gerät wird von einem anderen Gerät (z.B. Hub, Controller) konfiguriert oder verwaltet.
- **Erlaubte Source-Klassen**: Device
- **Erlaubte Target-Klassen**: Device
- **Beispiel**: `dev-hue-bulb-1` managed_by `dev-hue-bridge`

## `trusts`
- **Bedeutung**: Eine definierte Vertrauensbeziehung, oft uni-direktional, für Zugriffe oder Zertifikate.
- **Erlaubte Source-Klassen**: Device, Network
- **Erlaubte Target-Klassen**: Device, Network
- **Beispiel**: `net-guest` trusts (not) `net-lan-main`

## `exposed_to`
- **Bedeutung**: Ein Gerät oder eine Rolle ist von außen oder aus einem anderen Netz sichtbar.
- **Erlaubte Source-Klassen**: Device, Role
- **Erlaubte Target-Klassen**: Network, Device
- **Beispiel**: `role-reverse-proxy` exposed_to `net-wan`
