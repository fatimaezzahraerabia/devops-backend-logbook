# 🛒 Plateforme E-Commerce Complète & Gestion Commerciale

> **Cadre** : Stage Développeuse Full Stack  
> **Entreprise** : Seratel (Marrakech, Maroc)  
> **Période** : 04/2024 – 06/2024  
> **Rôle** : Développeuse Full Stack  
> **Statut** : :material-check-decagram: Livré & Déployé  

---

## 1. Contexte & Objectifs

Conception et mise en production d'une application e-commerce moderne permettant la gestion de catalogues multi-catégories, un panier d'achat persistant, un tunnel de commande sécurisé et un tableau de bord d'administration pour le suivi des stocks et des ventes.

---

## 2. Architecture Technique

```mermaid
flowchart LR
    Browser["🖥️ Interface Client (React.js)"] -->|REST API (JSON)| API["Spring Boot 3 REST Backend"]
    API --> Security["Spring Security & Authentification JWT"]
    API --> JPA["Spring Data JPA / Hibernate"]
    JPA --> DB[("Base de Données MySQL")]
```

---

## 3. Cycle de Vie du Projet (SDLC & DevOps)

1. **Planification & Modélisation** : Conception du schéma relationnel de la base de données (entités *Utilisateur*, *Produit*, *Commande*, *LigneDeCommande*, *Catégorie*).
2. **Backend Spring Boot** : Création d'APIs RESTful suivant les bonnes pratiques (Codes HTTP conformes, DTOs, pagination et filtres).
3. **Sécurité & Contrôle d'Accès** : Configuration de **Spring Security** avec filtres JWT personnalisés, isolation des rôles `ADMIN` et `USER`.
4. **Frontend React** : Interface responsive développée avec React et gestion d'état centralisée pour le panier client.
5. **Validation des Données** : Validation côté serveur via Hibernate Validator (`@NotNull`, `@Size`, `@Positive`).
6. **Tests Unitaires & End-to-End** : Couverture des services métiers (calcul des totaux de commandes, décrémentation des stocks) avec JUnit et Mockito.
7. **Conteneurisation Docker** : Création d'un environnement Docker Compose liant l'application backend et la base MySQL.
8. **Déploiement** : Déploiement automatisé avec scripts shell et reverse proxy Nginx.
9. **Supervision** : Surveillance des temps de réponse SQL et des connexions au pool HikariCP.
10. **Bilan** : Réduction du temps de traitement des commandes grâce à l'automatisation des factures et des alertes de rupture de stock.

---

## 4. Technologies Utilisées

<div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1rem;">
  <span class="tech-badge">Java</span>
  <span class="tech-badge">Spring Boot</span>
  <span class="tech-badge">Spring Security</span>
  <span class="tech-badge">React.js</span>
  <span class="tech-badge">MySQL</span>
  <span class="tech-badge">REST APIs</span>
  <span class="tech-badge">Docker</span>
</div>
