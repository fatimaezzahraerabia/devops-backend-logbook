# 🐧 Cheatsheet Linux & Administration Système

## 🌐 Diagnostics Réseau & Ports

```bash
# Vérifier quels processus écoutent sur quels ports TCP/UDP
ss -tulpn

# Vérifier la connectivité HTTP et afficher les en-têtes
curl -Iv https://api.votre-domaine.com
```

---

## 💾 Disque & Processus

```bash
# Recherche des 10 plus gros dossiers consommant de l'espace disque
du -ah / | sort -rh | head -n 10

# Trouver tous les processus utilisant un fichier ou port spécifique
lsof -i :8080
```
