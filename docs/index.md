<!-- DYNAMIC_PROFILE_START -->
<!-- DYNAMIC_PROFILE_END -->

<hr class="section-divider">

## Compétences Techniques

<div class="skills-grid">
  <div class="skill-category-card">
    <div class="skill-category-header">
      :fontawesome-solid-server: Backend & Architecture
    </div>
    <p style="font-size: 0.88rem; color: var(--md-default-fg-color--light); margin-bottom: 0.8rem;">
      Conception modulaire, architecture hexagonale et APIs REST/WebSocket à haute disponibilité.
    </p>
    <div>
      <span class="tech-badge">:fontawesome-brands-java: Java 21</span>
      <span class="tech-badge">:fontawesome-solid-leaf: Spring Boot 3.5</span>
      <span class="tech-badge">:fontawesome-brands-python: Python 3.12</span>
      <span class="tech-badge">:fontawesome-solid-bolt: FastAPI</span>
      <span class="tech-badge">Hexagonal Arch</span>
      <span class="tech-badge">REST APIs</span>
      <span class="tech-badge">WebSocket & noVNC</span>
      <span class="tech-badge">Hibernate / JPA</span>
      <span class="tech-badge">Flyway</span>
    </div>
  </div>

  <div class="skill-category-card">
    <div class="skill-category-header">
      :fontawesome-brands-docker: DevOps & Conteneurisation
    </div>
    <p style="font-size: 0.88rem; color: var(--md-default-fg-color--light); margin-bottom: 0.8rem;">
      Environnements conteneurisés reproductibles, orchestration et virtualisation d'infrastructures.
    </p>
    <div>
      <span class="tech-badge">:fontawesome-brands-docker: Docker</span>
      <span class="tech-badge">Docker Compose</span>
      <span class="tech-badge">:material-kubernetes: K3s / Kubernetes</span>
      <span class="tech-badge">Helm Charts</span>
      <span class="tech-badge">:material-server: Proxmox VE</span>
      <span class="tech-badge">Packer</span>
      <span class="tech-badge">Cloud-Init</span>
      <span class="tech-badge">:fontawesome-brands-linux: Linux & Bash</span>
    </div>
  </div>

  <div class="skill-category-card">
    <div class="skill-category-header">
      :fontawesome-solid-gears: Automatisation, CI/CD & IaC
    </div>
    <p style="font-size: 0.88rem; color: var(--md-default-fg-color--light); margin-bottom: 0.8rem;">
      Chaînes de livraison automatisées "Pipeline as Code" et approvisionnement déclaratif.
    </p>
    <div>
      <span class="tech-badge">:fontawesome-brands-jenkins: Jenkins</span>
      <span class="tech-badge">Jenkins JCasC</span>
      <span class="tech-badge">Job DSL</span>
      <span class="tech-badge">:fontawesome-brands-github: GitHub Actions</span>
      <span class="tech-badge">:material-terraform: Terraform</span>
      <span class="tech-badge">:material-ansible: Ansible</span>
      <span class="tech-badge">Pipeline as Code</span>
    </div>
  </div>

  <div class="skill-category-card">
    <div class="skill-category-header">
      :fontawesome-solid-shield-halved: Données, Sécurité & Observabilité
    </div>
    <p style="font-size: 0.88rem; color: var(--md-default-fg-color--light); margin-bottom: 0.8rem;">
      Gestion de données résilientes, sécurité shift-left et surveillance télémétrique proactive.
    </p>
    <div>
      <span class="tech-badge">:material-database: PostgreSQL</span>
      <span class="tech-badge">:material-database: MySQL</span>
      <span class="tech-badge">:material-database-sync: Redis</span>
      <span class="tech-badge">:material-chart-line: Prometheus</span>
      <span class="tech-badge">:material-chart-bar: Grafana</span>
      <span class="tech-badge">OAuth 2.0 / OIDC</span>
      <span class="tech-badge">JWT RS256</span>
      <span class="tech-badge">HashiCorp Vault</span>
      <span class="tech-badge">Trivy & Gitleaks</span>
    </div>
  </div>
</div>

<hr class="section-divider">

## Décisions & Comparatifs Techniques

=== ":fontawesome-brands-docker: Docker vs Podman"

    | Critère | Docker (Moteur Standard) | Podman (Alternative Rootless) |
    |---|---|---|
    | **Architecture** | Client/Serveur avec démon centralisé (`dockerd`) | Sans démon (daemonless), processus fils direct |
    | **Privilèges** | Nécessite souvent les droits `root` (sauf mode rootless configuré) | Exécution sans privilèges (*rootless*) par défaut |
    | **Compatibilité K8s** | Standards OCI & containerd | Génération directe de pods Kubernetes (`podman generate kube`) |
    | **Cas d'usage retenu** | Standard pour les pipelines CI/CD Jenkins & GitHub Actions | Idéal pour environnements HPC et serveurs ultra-durcis |

    !!! tip "Recommandation d'Ingénierie"
        Docker reste la référence pour la compatibilité out-of-the-box avec les agents CI/CD Jenkins (Docker-in-Docker / Docker-outside-of-Docker). Pour les hôtes partagés en production où la surface d'attaque root doit être minimisée, Podman s'impose.

=== ":fontawesome-solid-cubes: Architecture Monolithe vs Hexagonale"

    | Aspect | Monolithe Traditionnel en Couches | Architecture Hexagonale (Ports & Adapters) |
    |---|---|---|
    | **Couplage Métier / BDD** | Fort (entités JPA traversent souvent les couches) | Nul (le domaine métier est isolé au centre) |
    | **Testabilité** | Nécessite des mocks complexes de bases de données | Tests unitaires purs sur le domaine sans infrastructure |
    | **Interchangeabilité** | Difficile de changer de SGBD ou d'interface client | Remplacement simple des adaptateurs (ex. REST, CLI, WebSockets) |

    !!! note "Principe Appliqué"
        Dans le projet de cloud privé (PFE DBM Maroc), l'architecture hexagonale permet d'isoler la logique d'allocation des laboratoires virtuels de l'infrastructure de virtualisation sous-jacente (Proxmox VE, K3s, Docker).

=== ":fontawesome-brands-jenkins: Jenkins (JCasC) vs GitHub Actions"

    | Fonctionnalité | Jenkins avec JCasC & Job DSL | GitHub Actions |
    |---|---|---|
    | **Hébergement** | Auto-hébergé sur cluster K3s / serveurs dédiés | SaaS managé par GitHub (avec options de self-hosted runners) |
    | **Configuration as Code** | Tout est versionné via `jenkins.yaml` et scripts DSL | Fichiers YAML dans `.github/workflows/` |
    | **Contrôle d'accès & Secrets** | Intégration avancée avec HashiCorp Vault et LDAP | GitHub Secrets par dépôt ou organisation |
    | **Budget** | 0 EUR de coût de licence (Open Source sur infra interne) | Gratuit pour l'Open Source, quotas sur dépôts privés |

<hr class="section-divider">

## Architecture d'Infrastructure & Pipeline CI/CD

```mermaid
graph LR
    Dev(["Développeur"]):::actor -->|Git Push| Repo[("GitHub / Git")]:::repo
    
    subgraph Pipeline ["Pipeline Automatisé CI/CD (Jenkins / GitHub Actions)"]
        Repo --> Scan["1. Lint & Security<br/><i>Ruff, Gitleaks, Trivy</i>"]:::step
        Scan --> Test["2. Tests & Qualité<br/><i>JUnit, Pytest, Mockito</i>"]:::step
        Test --> Build["3. Build & Package<br/><i>Docker Multi-stage</i>"]:::step
        Build --> Push["4. Registry Image<br/><i>GHCR / Docker Hub</i>"]:::step
    end
    
    subgraph DeployEnv ["Environnement de Déploiement Cloud & Edge"]
        Push --> Orchestrator{"Orchestrateur<br/>K3s / Kubernetes"}:::orch
        Orchestrator --> App["Application Backend Pods<br/>Java 21 / FastAPI"]:::app
        App --> DB[("PostgreSQL / Redis")]:::db
    end

    subgraph Monitoring ["Observabilité & Métriques"]
        App -.->|Expose /metrics| Prom["Prometheus"]:::obs
        Prom --> Grafana["Tableaux de Bord Grafana"]:::obs
    end

    classDef actor fill:#3f51b5,stroke:#283593,stroke-width:2px,color:#fff;
    classDef repo fill:#263238,stroke:#37474f,stroke-width:2px,color:#fff;
    classDef step fill:#e8eaf6,stroke:#3f51b5,stroke-width:2px,color:#1a237e;
    classDef orch fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#bf360c;
    classDef app fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20;
    classDef db fill:#ede7f6,stroke:#512da8,stroke-width:2px,color:#311b92;
    classDef obs fill:#fce4ec,stroke:#c2185b,stroke-width:2px,color:#880e4f;
```

!!! tip "Philosophie Shift-Left"
    La sécurité et la qualité ne sont pas reléguées en fin de cycle : chaque commit est audité (détection de secrets via **Gitleaks**, analyse statique de vulnérabilités conteneur via **Trivy**, couverture de tests unitaires et d'intégration avant toute mise en production).

<hr class="section-divider">

## Expériences Professionnelles

!!! info "Cycle de Vie & Traçabilité (SDLC & DevOps)"
    Chaque projet ci-dessous est documenté selon notre démarche d'ingénierie en 10 étapes. Cliquez sur le titre ou sur le bouton de chaque projet pour consulter son **étude de cas détaillée** (Architecture, IaC, CI/CD, Sécurité, Monitoring).
    Consultez également le [**Guide Méthodologique du Cycle de Vie**](04-projets/guide-cycle-de-vie.md).

<!-- DYNAMIC_EXPERIENCES_START -->
<!-- DYNAMIC_EXPERIENCES_END -->

<hr class="section-divider">

## Formations & Diplômes

<div class="timeline">
  <div class="timeline-item">
    <div class="timeline-dot"></div>
    <div class="timeline-date">2023 – 2024</div>
    <div class="timeline-content">
      <h4>Master en Ingénierie des Systèmes Informatiques Répartis</h4>
      <div class="timeline-subtitle">Faculté des Sciences et Techniques (FST) — Mohammadia</div>
      <p class="timeline-desc">
        Spécialisation dans les architectures réparties, systèmes distribués, cloud computing, réseaux et sécurité avancée des infrastructures.
      </p>
    </div>
  </div>

  <div class="timeline-item">
    <div class="timeline-dot"></div>
    <div class="timeline-date">2021 – 2023</div>
    <div class="timeline-content">
      <h4>DEUST MIPC (Mathématiques, Informatique, Physique, Chimie)</h4>
      <div class="timeline-subtitle">Faculté des Sciences et Techniques (FST) — Marrakech</div>
      <p class="timeline-desc">
        Socle scientifique et algorithmique solide, programmation procédurale et orientée objet, structures de données fondamentales.
      </p>
    </div>
  </div>

  <div class="timeline-item">
    <div class="timeline-dot"></div>
    <div class="timeline-date">2020</div>
    <div class="timeline-content">
      <h4>Baccalauréat Scientifique — Sciences Physiques</h4>
      <div class="timeline-subtitle">Lycée Labrikiyne</div>
    </div>
  </div>
</div>

<hr class="section-divider">

## Certifications Officielles

| Certification | Organisme Émetteur | Année | Domaine Clé |
|---|---|---|---|
| **Oracle Cloud Infrastructure 2025 - DevOps Professional** | Oracle Cloud | 2025 | Automatisation CI/CD, OCI DevOps, OKE, OCI Registry |
| **Oracle Cloud 2025 - Developer Professional** | Oracle Cloud | 2025 | Cloud Native, Microservices, API Gateway, Serverless |
| **Oracle Cloud 2025 - Foundations Associate** | Oracle Cloud | 2025 | Architecture Cloud, Compute, Networking, Storage & IAM |

<hr class="section-divider">

## Projets Phares

<div class="skills-grid">
  <div class="skill-category-card">
    <div class="skill-category-header">
      :material-rocket-launch: <a href="04-projets/pipeline-devops-end-to-end.md" class="project-title-link">Pipeline CI/CD DevOps End-to-End <span class="arrow-icon">↗</span></a>
    </div>
    <p style="font-size: 0.9rem; margin-bottom: 0.8rem;">
      Chaîne d'automatisation complète de commit à déploiement avec Jenkins, Docker, K8s, Prometheus et Grafana sur Azure. Déploiement en moins de 5 min avec rollback automatique.
    </p>
    <div>
      <span class="tech-badge">Jenkins</span>
      <span class="tech-badge">Docker</span>
      <span class="tech-badge">Kubernetes</span>
      <span class="tech-badge">Prometheus</span>
      <span class="tech-badge">Azure</span>
    </div>
    <div class="project-cta-container">
      <a href="04-projets/pipeline-devops-end-to-end.md" class="project-card-cta">
        <span>Cycle de vie & Architecture →</span>
      </a>
    </div>
  </div>

  <div class="skill-category-card">
    <div class="skill-category-header">
      :material-clock-outline: <a href="04-projets/timewise-microservices.md" class="project-title-link">TimeWise — Coach de Productivité <span class="arrow-icon">↗</span></a>
    </div>
    <p style="font-size: 0.9rem; margin-bottom: 0.8rem;">
      Application de productivité full-stack basée sur une architecture de microservices pilotée par les événements (EDA). WebSocket, NLP, Docker et CI/CD automatisée.
    </p>
    <div>
      <span class="tech-badge">Spring Boot 3</span>
      <span class="tech-badge">Python NLP</span>
      <span class="tech-badge">PostgreSQL</span>
      <span class="tech-badge">EDA</span>
      <span class="tech-badge">Docker</span>
    </div>
    <div class="project-cta-container">
      <a href="04-projets/timewise-microservices.md" class="project-card-cta">
        <span>Cycle de vie & Architecture →</span>
      </a>
    </div>
  </div>

  <div class="skill-category-card">
    <div class="skill-category-header">
      :material-recycle: <a href="04-projets/smartwaste-iot.md" class="project-title-link">SmartWaste — Gestion Temps Réel <span class="arrow-icon">↗</span></a>
    </div>
    <p style="font-size: 0.9rem; margin-bottom: 0.8rem;">
      Application citoyenne et tableau de bord administrateur pour la gestion optimisée des déchets en temps réel. Déploiement cloud via Docker et CI/CD GitHub Actions.
    </p>
    <div>
      <span class="tech-badge">Java 17</span>
      <span class="tech-badge">Spring Boot</span>
      <span class="tech-badge">React.js</span>
      <span class="tech-badge">MySQL</span>
      <span class="tech-badge">GitHub Actions</span>
    </div>
    <div class="project-cta-container">
      <a href="04-projets/smartwaste-iot.md" class="project-card-cta">
        <span>Cycle de vie & Architecture →</span>
      </a>
    </div>
  </div>

  <div class="skill-category-card">
    <div class="skill-category-header">
      :material-book-open-page-variant: <a href="04-projets/guide-cycle-de-vie.md" class="project-title-link">Engineering Logbook & Méthodologie <span class="arrow-icon">↗</span></a>
    </div>
    <p style="font-size: 0.9rem; margin-bottom: 0.8rem;">
      Ce site web interactif — portfolio d'ingénierie et carnet de bord technique documentant l'ensemble du cycle SDLC (10 étapes), avec CMS headless découplé.
    </p>
    <div>
      <span class="tech-badge">MkDocs Material</span>
      <span class="tech-badge">GitHub Pages</span>
      <span class="tech-badge">Decap CMS</span>
      <span class="tech-badge">Cloudflare Workers</span>
    </div>
    <div class="project-cta-container">
      <a href="04-projets/guide-cycle-de-vie.md" class="project-card-cta">
        <span>Découvrir la Méthodologie →</span>
      </a>
    </div>
  </div>
</div>
