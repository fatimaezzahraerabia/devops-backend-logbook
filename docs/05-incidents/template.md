# 🚨 Postmortem Incident — [Titre de l'Incident]

**Date de l'incident** : AAAA-MM-JJ  
**Auteur / Lead Incident** : [Votre Nom]  
**Sévérité** : P1 (Critique) / P2 (Majeur) / P3 (Mineur)  
**Durée de la panne** : [XX minutes / heures]  

---

## 1. Résumé Exécutif
[Bref résumé de ce qui s'est passé, l'impact utilisateur et la résolution apportée]

---

## 2. Impact Métier & Technique
- **Impact Utilisateur** : [ex: 100% des requêtes HTTP POST /tasks renvoyaient une erreur 500]
- **Services impactés** : [API FastAPI, Base de données PostgreSQL]
- **Perte de données** : Aucune / [Description]

---

## 3. Chronologie des Événements (UTC)

| Heure | Événement / Action |
|---|---|
| **14:00** | Injection du test de Chaos Engineering (ou déclenchement de la panne). |
| **14:02** | Alerte Grafana déclenchée : `HighHTTP5xxRate (> 5%)`. |
| **14:05** | Investigation des logs JSON dans Grafana/Loki. |
| **14:12** | Identification de la cause racine. |
| **14:20** | Application du correctif (Patch / Rollback). |
| **14:25** | Retour à la normale confirmé par Prometheus. |

---

## 4. Cause Racine (Root Cause)
[Explication technique détaillée de la cause principale de la panne (Pourquoi c'est arrivé)]

---

## 5. Actions Préventives & Correctives (CAPA)

| Action | Type | Responsable | Statut |
|---|---|---|---|
| [Fixer le bug dans le code] | Correctif immédiat | Dev | ✅ Fait |
| [Ajouter un test d'intégration] | Prévention | Dev | 🔄 En cours |
| [Ajuster le seuil d'alerte Grafana] | Monitoring | DevOps | 🔄 En cours |
