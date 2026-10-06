# 🐘 Cheatsheet PostgreSQL & SQL Performance

## 📊 Maintenance & Performance

```sql
-- Analyser le plan d'exécution d'une requête lente
EXPLAIN ANALYZE SELECT * FROM tasks WHERE status = 'COMPLETED';

-- Lister les requêtes actuellement en cours d'exécution
SELECT pid, user, query, state, age(clock_timestamp(), query_start) 
FROM pg_stat_activity 
WHERE state != 'idle';
```

---

## 📦 Import / Export (pg_dump)

```bash
# Sauvegarder une base de données dans un fichier compressé
pg_dump -U username -h localhost -d dbname -F c -b -v -f backup.dump

# Restaurer une base de données depuis un fichier .dump
pg_restore -U username -h localhost -d dbname -v backup.dump
```
