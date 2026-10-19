# ☁️ Plateforme de Cloud Privé pour Laboratoires Virtuels d'Apprentissage

> **Cadre** : Projet de Fin d'Études (PFE) d'Ingénieur  
> **Entreprise** : DBM Maroc (Mohammadia, Maroc)  
> **Période** : 02/2026 – 07/2026  
> **Rôle** : Ingénieure Full Stack / DevOps  
> **Statut** : :material-check-decagram: Projet Réalisé & Validé  

---

## 1. Contexte & Problématique Métier

Dans le cadre de formations techniques universitaires et professionnelles, le déploiement manuel d'environnements d'apprentissage (machines virtuelles, conteneurs, réseaux isolés) présentait des limites majeures :

* **Goulot d'étranglement logistique** : Plusieurs heures nécessaires pour préparer manuellement les salles de travaux pratiques.
* **Consommation excessive de ressources** : Absence de mutualisation et de destruction automatique après les sessions.
* **Sécurité et étanchéité** : Risque d'interférence entre les environnements étudiants et l'infrastructure de l'établissement.
* **Manque d'intégration** : Pas de lien direct avec la plateforme pédagogique centrale (**Moodle LMS**).

### Objectifs Techniques du Projet
1. Concevoir une plateforme d'orchestration de Cloud privé capable de provisionner des laboratoires virtuels (VMs et conteneurs) à la volée en moins de **90 secondes**.
2. Intégrer l'authentification et le lancement transparent depuis Moodle via la norme éducative internationale **LTI 1.3 Advantage** (OIDC / OAuth 2.0).
3. Offrir un accès direct aux consoles des machines via un navigateur web moderne sans agent lourd, grâce à **noVNC** et des passerelles **WebSockets sécurisées**.
4. Automatiser 100% de l'infrastructure et de la livraison logicielle via **Terraform**, **Ansible**, **Packer** et des pipelines **Jenkins as Code**.

---

## 2. Architecture Globale du Système

Le système repose sur un découpage en **Architecture Hexagonale (Ports & Adapters)** côté backend, garantissant une indépendance totale entre la logique métier d'attribution des labs et les moteurs de virtualisation sous-jacents.

```mermaid
flowchart TB
    subgraph LMS ["🎓 Plateforme Pédagogique"]
        Moodle["Moodle LMS"]
    end

    subgraph AuthPortal ["🔐 Authentification & Ingress"]
        OIDC["LTI 1.3 Advantage (OIDC / OAuth 2.0)"]
        Traefik["Traefik Reverse Proxy & TLS"]
    end

    subgraph CoreBackend ["⚙️ Backend Plateforme (Java 21 / Spring Boot 3.5)"]
        direction TB
        API["API Gateway & Controllers REST"]
        HexCore["Domaine Métier (Architecture Hexagonale)
        • Quotas & Politiques de Lab
        • Cycle de vie sessions
        • Audit & Facturation"]
        AdapterProxmox["Adaptateur Proxmox REST API"]
        AdapterK3s["Adaptateur Kubernetes (K3s Client)"]
        AdapterWS["Passerelle WebSocket / noVNC"]
    end

    subgraph InfraVirtualization ["🖥️ Couche Virtualisation & Conteneurs"]
        PVE["Cluster Proxmox VE (Hyperviseur KVM / LXC)"]
        K3s["Cluster K3s (Conteneurs Docker éphémères)"]
        Postgres[("PostgreSQL 16 (Persistance de l'état)")]
    end

    subgraph ClientStudent ["💻 Navigateur Étudiant"]
        Browser["Interface Web (Console noVNC HTML5)"]
    end

    Moodle -->|LTI Launch (JWT RS256)| OIDC
    OIDC --> Traefik
    Traefik --> API
    API --> HexCore
    HexCore --> AdapterProxmox
    HexCore --> AdapterK3s
    HexCore --> AdapterWS
    HexCore --> Postgres

    AdapterProxmox -->|Provisioning QEMU/KVM| PVE
    AdapterK3s -->|Orchestration Pods| K3s
    Browser <-->|WebSocket wss://| AdapterWS
    AdapterWS <-->|Proxy VNC / SPICE| PVE

    classDef highlight fill:#0f172a,stroke:#4dd0e1,stroke-width:2px,color:#fff;
    classDef infra fill:#1e293b,stroke:#80deea,stroke-width:1px,color:#e2e8f0;
    class CoreBackend,HexCore highlight;
    class InfraVirtualization,PVE,K3s infra;
```

---

## 3. Déclinaison Complète du Cycle de Vie (10 Étapes SDLC & DevOps)

### Étape 1 : Plan & Cadrage Fonctionnel
* Définition des profils utilisateurs : *Administrateur*, *Enseignant*, *Étudiant*.
* Rédaction des spécifications d'API REST selon le standard **OpenAPI 3.1**.
* Découpage des sprints avec tableau Agile Kanban sur GitHub Projects.

### Étape 2 : Architecture & Conception Backend
* **Java 21** et **Spring Boot 3.5** tirant parti des *Virtual Threads (Project Loom)* pour supporter plusieurs centaines de connexions WebSockets simultanées sans explosion mémoire.
* Modélisation en **Architecture Hexagonale** :
  * `core-domain` : Gestion des sessions d'apprentissage, durées maximales, quotas CPU/RAM.
  * `inbound-adapters` : Endpoints REST et WebSocket Handlers.
  * `outbound-adapters` : Clients HTTP résilients vers l'API Proxmox VE et le cluster K3s via client officiel Kubernetes.

### Étape 3 : Automatisation d'Infrastructure & Images Disques (IaC)
* **Packer & Cloud-Init** : Création automatisée d'images virtuelles Debian/Ubuntu et Alpine Linux durcies, pré-configurées avec les outils pédagogiques (compilateurs, Docker, Wireshark).
* **Terraform** : Définition déclarative de l'infrastructure hôte (pools de stockage ZFS, réseaux virtuels SDN, bridges Linux `vmbr0`).
* **Ansible** : Playbooks de configuration post-boot, déploiement des certificats SSL/TLS internes et sécurisation SSH.

### Étape 4 : Conteneurisation & Cluster Léger (K3s)
* Pour les travaux pratiques légers (ex. exercices Linux / réseaux / Python), allocation de pods conteneurisés éphémères sur un cluster **K3s**.
* Création de `Dockerfiles` multi-stage légers (< 80 Mo) avec utilisateur non-root.
* Définition de `NetworkPolicies` Kubernetes interdisant tout trafic latéral entre pods d'étudiants distincts.

### Étape 5 : Intégration Continue (Jenkins as Code)
* Mise en place de pipelines déclaratifs Jenkins versionnés dans le dépôt (`Jenkinsfile`).
* Configuration du master Jenkins via **JCasC (Jenkins Configuration as Code)** et génération dynamique des jobs avec **Job DSL**.
* Déroulement de la chaîne :
  1. Validation statique du code Java (`Checkstyle`, `SpotBugs`).
  2. Détection de secrets codés en dur avec **Gitleaks**.
  3. Tests unitaires et d'intégration.
  4. Analyse de vulnérabilités des conteneurs avec **Trivy**.
  5. Publication de l'image sur registre Docker privé avec tag SemVer.

### Étape 6 : Sécurité Shift-Left & Standard LTI 1.3
* Authentification basée sur la spécification **IMS Global LTI 1.3 Advantage** :
  * Flux OIDC 3-legged entre Moodle et la plateforme.
  * Échange et validation de tokens **JWT signés en RS256** avec rotation des clés publiques via endpoint `jwks.json`.
* Isolation réseau stricte : chaque groupe d'étudiants dispose d'un VLAN isolé ou d'un réseau VxLAN dédié sous Proxmox.

### Étape 7 : Tests & Validation Automatisée
* **Tests unitaires** : JUnit 5 et Mockito (couverture > 82%).
* **Tests d'intégration** : **Testcontainers** pour instancier à la volée une base PostgreSQL et un serveur mock simulant l'API Proxmox durant la CI.
* Tests de charge avec **k6** simulant 150 lancements simultanés de laboratoires.

### Étape 8 : Déploiement & Orchestration
* Déploiement des microservices plateforme sur **K3s** avec manifestes Kubernetes et Helm.
* Stratégie de déploiement *RollingUpdate* sans temps d'arrêt pour les mises à jour logicielles.
* Gestion des secrets sensibles (identifiants Proxmox API Token) via Secrets Kubernetes chiffrés.

### Étape 9 : Observabilité & Monitoring Proactif
* Exportateur de métriques Prometheus pour Proxmox VE (`proxmox-exporter`) et K3s.
* Dashboards **Grafana** dédiés affichant :
  * Nombre de laboratoires actifs en temps réel.
  * Utilisation agrégée RAM / CPU / Stockage NVMe du cluster physique.
  * Taux de latence des flux WebSockets noVNC.
* Alertes automatisées (Telegram / Email) en cas de saturation d'un nœud physique (> 85% de RAM).

### Étape 10 : Exploitation, Nettoyage & Postmortem
* Tâche cron / scheduler Spring interne vérifiant toutes les 2 minutes les sessions arrivées à expiration pour détruire automatiquement les VMs/conteneurs associés et libérer immédiatement les ressources.
* Rédaction d'un postmortem technique suite à un incident de saturation d'espace disque lors d'un TP sur Docker-in-Docker, menant à l'application de quotas stricts ZFS.

---

## 4. Difficultés Rencontrées & Solutions d'Ingénierie

### Défi 1 : Latence et maintien de session WebSocket pour noVNC
> **Problème** : Lors des pics d'utilisation, les connexions WebSocket subissaient des déconnexions intempestives via le proxy inverse HTTP standard.  
> **Solution** : Implémentation d'un tunnel WebSocket dédié avec configuration `proxy_read_timeout 3600s` et keep-alive ping périodique, couplé aux Virtual Threads de Java 21 pour éliminer le blocage de threads au niveau de la passerelle.

### Défi 2 : Lenteur du clonage de machines virtuelles
> **Problème** : Le clonage complet (*full clone*) de VMs prenait plus de 3 minutes par étudiant sur disque conventionnel.  
> **Solution** : Passage aux *linked clones* (clonage lié) sur pool de stockage **ZFS** avec snapshots copy-on-write. Temps de provisioning réduit à **moins de 8 secondes par machine**.

---

## 5. Synthèse des Résultats & Impact Métier

| Indicateur Clé | Avant le Projet | Avec la Plateforme | Amélioration |
|---|---|---|---|
| **Temps de mise à disposition d'un lab** | 45 à 60 minutes | **12 secondes** | :rocket: **97% de gain** |
| **Effort enseignant** | Configuration manuelle poste par poste | **1 clic dans Moodle** | :white_check_mark: Automatisation totale |
| **Taux de disponibilité** | Variable (dépendance matériel salle) | **99.6%** | :shield: Haute résilience |
| **Empreinte mémoire inactive** | Consommation statique continue | **Libération auto post-TP** | :chart_with_upwards_trend: Économie d'énergie |

---

## 6. Technologies Clés Utilisées

<div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1rem;">
  <span class="tech-badge">Java 21</span>
  <span class="tech-badge">Spring Boot 3.5</span>
  <span class="tech-badge">Architecture Hexagonale</span>
  <span class="tech-badge">Proxmox VE</span>
  <span class="tech-badge">K3s Kubernetes</span>
  <span class="tech-badge">Docker</span>
  <span class="tech-badge">Terraform</span>
  <span class="tech-badge">Ansible</span>
  <span class="tech-badge">Packer</span>
  <span class="tech-badge">Cloud-Init</span>
  <span class="tech-badge">Jenkins as Code (JCasC)</span>
  <span class="tech-badge">LTI 1.3 Advantage</span>
  <span class="tech-badge">noVNC & WebSockets</span>
  <span class="tech-badge">PostgreSQL</span>
  <span class="tech-badge">Prometheus</span>
  <span class="tech-badge">Grafana</span>
</div>
