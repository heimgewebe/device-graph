---
id: runbook-short
title: "Minimales Notfall-Runbook"
doc_type: operations
role: emergency-runbook
status: active
canonicality: canonical
last_reviewed: 2026-04-19
summary: "Die 10 wichtigsten Zeilen zur Wiederherstellung von DNS und Proxy im Totalausfall."
depends_on: []
related_docs: []
verifies_with: []
---

# Minimales Notfall-Runbook

**Szenario 1: Heimberry (DNS) tot**
1. `ssh user@192.168.178.2` (oder via MagicDNS `ssh user@heimberry`)
2. `docker ps | grep pihole`
3. `docker-compose restart` (oder `sudo systemctl restart docker`)
4. `sudo reboot`
5. *Hardware tot?* Router DHCP auf Provider-DNS (z.B. 1.1.1.1) umstellen.

**Szenario 2: Caddy (Proxy) tot**
1. `ssh user@192.168.178.46` (oder via MagicDNS `ssh user@heimserver`)
2. `docker logs caddy --tail 50`
3. `docker exec -w /etc/caddy caddy caddy validate`
4. `docker restart caddy`
5. `ssh -L 3000:localhost:3000 user@heimserver` (lokales Port-Forwarding für Direktzugriff)
