# 🗺️ Plan d'Apprentissage & Roadmap (90 Jours)

> Cette feuille de route formalise ma progression technique et la réalisation du projet fil rouge sur 90 jours, en couvrant **l'intégralité du cycle de vie logiciel (SDLC)**.

---

## 📅 Chronologie par Phases

### Phase 1 : Cadrage, Fondations & Première API (Jours 1 à 30)
- [x] **J1 - J7 : Initialisation & Logbook**
  - Mise en place du carnet MkDocs Material avec CI/CD sur GitHub Pages.
  - Configuration de Decap CMS pour l'édition dynamique sans terminal.
  - Définition du cahier des charges et de l'architecture cible.
- [ ] **J8 - J30 : Backend FastAPI & PostgreSQL**
  - Conception de l'API REST FastAPI avec architecture propre par modules.
  - Intégration de PostgreSQL et des migrations de schéma avec **Alembic**.
  - Mise en place de l'authentification **JWT** et hachage des mots de passe avec Passlib/Bcrypt.
  - Rédaction des tests unitaires et d'intégration avec **Pytest** (couverture ≥ 70%).
  - Logs structurés JSON et middleware Correlation ID.

---

### Phase 2 : Conteneurisation, CI/CD & Sécurité (Jours 31 à 60)
- [ ] **J31 - J45 : Docker & Qualité CI**
  - Écriture d'un `Dockerfile` multi-stage optimisé (taille minimale, utilisateur non-root).
  - Orchestration locale avec `docker-compose.yml` (API + Postgres + Redis + Worker).
  - Pipeline GitHub Actions : Linter (Ruff), tests Pytest, scan de sécurité Docker (Hadolint).
- [ ] **J46 - J60 : Sécurité & Registre Container**
  - Scan des vulnérabilités avec **Trivy** et détection des fuites de secrets avec **Gitleaks**.
  - Publication automatisée des images conteneurs sur **GitHub Container Registry (GHCR)** avec tagging SemVer.
  - Gestion sécurisée des secrets avec **SOPS / Age**.

---

### Phase 3 : Infrastructure, Kubernetes, Monitoring & Incident (Jours 61 à 90)
- [ ] **J61 - J75 : Infra as Code & Kubernetes**
  - Provisionnement d'infrastructures avec **Terraform** (VMs, réseaux sur Oracle Cloud Free Tier).
  - Packaging de l'application Kubernetes avec **Helm / Kustomize**.
  - Déploiement local sur cluster **Kind** / **k3s** et déploiement démo cloud (Render + Neon DB).
- [ ] **J76 - J90 : Observabilité & Chaos Engineering**
  - Exposition des métriques `/metrics` avec **Prometheus** et génération de tableaux de bord **Grafana**.
  - Simulation d'un incident volontaire (Chaos Engineering : latence DB ou saturation mémoire).
  - Détection par alerte Grafana, correction de l'incident et publication du **Postmortem #001**.

---

## 📊 Suivi des Livrables

| Livrable | Exigence | Statut |
|---|---|---|
| **Site Logbook en ligne** | Déploiement auto GitHub Pages | ✅ Terminé |
| **CMS Web Dynamique** | Decap CMS configuré sur `/admin` | ✅ Terminé |
| **API Gestion de Tâches** | FastAPI + Postgres + JWT | 🔄 En cours |
| **Pipeline CI/CD Vert** | Lint, Test, Scan, Build & Push | 🔄 En cours |
| **Postmortem Incident** | Modèle + 1 Incident documenté | ✅ Initialisé |
| **ADR (Architecture)** | Modèle + 3 Décisions rédigées | ✅ Initialisé |
| **Cheatsheets** | 6 Fiches mémos rédigées | ✅ Initialisé |
