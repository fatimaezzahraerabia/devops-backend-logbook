# 🐳 Cheatsheet Docker & Docker Compose

## 🧹 Nettoyage Système & Ressources

```bash
# Supprimer tous les conteneurs arrêtés, réseaux inutilisés et images orphelines
docker system prune -a --volumes

# Voir la taille consommée par Docker sur le disque
docker system df
```

---

## 🔍 Débogage & Inspection

```bash
# Consulter les logs d'un conteneur en temps réel avec timestamps
docker logs -f --tail 100 <container_name>

# Entrer dans le shell d'un conteneur en cours d'exécution
docker exec -it <container_name> /bin/sh

# Inspecter l'utilisation CPU/RAM en temps réel
docker stats
```

---

## 🐙 Docker Compose

```bash
# Démarrer tous les services en arrière-plan et rebuilder les images si besoin
docker compose up -d --build

# Arreter les services et supprimer les volumes de données
docker compose down -v
```
