# 🔀 Cheatsheet Git & Workflow Commit

## 🚀 Operations Courantes

```bash
# Annuler le dernier commit local en gardant les modifications dans le staging
git reset --soft HEAD~1

# Annuler complètement le dernier commit et effacer les modifications locales
git reset --hard HEAD~1

# Nettoyer les branches locales qui ont été supprimées sur le serveur distant
git fetch --prune

# Interposer des modifications sur la branche principale en rebase interactif
git rebase -i main

# Appliquer un commit spécifique d'une autre branche
git cherry-pick <commit-hash>
```

---

## 📝 Convention de Commit (Conventional Commits)

Format : `<type>(<périmètre>): <description>`

- `feat`: Nouvelles fonctionnalités
- `fix`: Correction de bug
- `docs`: Documentation uniquement
- `style`: Formattage, points-virgules manquants (aucun changement de code métier)
- `refactor`: Refactorisation de code (ni fix, ni feat)
- `test`: Ajout ou modification de tests
- `chore`: Tâches de maintenance, mise à jour des dépendances, CI/CD
