# 🔴 Cheatsheet Redis & Cash Management

## ⚡ Commandes CLI Fréquentes

```bash
# Se connecter au serveur Redis
redis-cli -h localhost -p 6379 -a "votre_mot_de_passe"

# Vérifier la consommation mémoire et le nombre de clés
INFO memory
INFO keyspace

# Monitorer toutes les requêtes arrivant sur Redis en temps réel
MONITOR

# Vider toutes les clés du cache (ATTENTION en production)
FLUSHALL
```
