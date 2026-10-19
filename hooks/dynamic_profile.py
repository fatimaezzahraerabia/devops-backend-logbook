import os
import re
import yaml

def on_config(config):
    """
    Configure globalement le copyright dynamique et désactive la mention 'Made with Material for MkDocs'.
    """
    docs_dir = config.get('docs_dir', 'docs')
    profil_path = os.path.join(docs_dir, 'data', 'profil.yml')
    full_name = 'Fatima-Ezzahrae Rabia'
    if os.path.exists(profil_path):
        try:
            with open(profil_path, 'r', encoding='utf-8') as f:
                profil = yaml.safe_load(f) or {}
                full_name = profil.get('full_name', full_name)
        except Exception:
            pass
    config['copyright'] = f"Copyright &copy; 2026 {full_name}"
    if 'extra' not in config:
        config['extra'] = {}
    config['extra']['generator'] = False
    return config

def on_page_markdown(markdown, page, config, files):
    """
    Hook MkDocs dynamique :
    1. Lit les données du profil dans docs/data/profil.yml (géré par Decap CMS).
    2. Construit une section Hero complète (Photo ronde gauche, texte droite, boutons alignés).
    3. Ajoute la grille de 4 cartes "Ce que je fais" (Backend, DevOps, CI/CD, Cloud).
    4. Propose l'aperçu interactif du CV en accordéon.
    """
    docs_dir = config.get('docs_dir', 'docs')
    profil_path = os.path.join(docs_dir, 'data', 'profil.yml')
    
    profil = {}
    if os.path.exists(profil_path):
        try:
            with open(profil_path, 'r', encoding='utf-8') as f:
                profil = yaml.safe_load(f) or {}
        except Exception as e:
            print(f"[hook:dynamic_profile] Erreur de lecture de {profil_path}: {e}")

    exp_path = os.path.join(docs_dir, 'data', 'experiences.yml')
    experiences = []
    if os.path.exists(exp_path):
        try:
            with open(exp_path, 'r', encoding='utf-8') as f:
                exp_data = yaml.safe_load(f) or []
                if isinstance(exp_data, dict):
                    experiences = exp_data.get('experiences', [])
                elif isinstance(exp_data, list):
                    experiences = exp_data
        except Exception as e:
            print(f"[hook:dynamic_profile] Erreur de lecture de {exp_path}: {e}")

    # Normalisation des chemins (supprimer le slash initial pour GitHub Pages)
    def clean_path(val):
        if not val:
            return ""
        s = str(val).strip()
        while s.startswith('/'):
            s = s[1:]
        return s

    photo = clean_path(profil.get('photo', ''))
    cv_pdf = clean_path(profil.get('cv_pdf', ''))
    full_name = profil.get('full_name', 'Fatima-Ezzahrae Rabia')
    title = profil.get('title', 'Ingénieure Backend & DevOps')
    tagline = profil.get('bio', "Ingénieure spécialisée dans la conception d'architectures backend robustes, la conteneurisation et l'automatisation des pipelines CI/CD cloud.")
    github = profil.get('github', 'https://github.com/fatimaezzahraerabia')
    linkedin = profil.get('linkedin', 'https://linkedin.com/in/fatima-ezzahrae-rabia')
    email = profil.get('email', '')
    location = profil.get('location', '')

    # Remplacement des variables simples {{ profil.* }}
    replacements = {
        'profil.full_name': full_name,
        'profil.title': title,
        'profil.bio': tagline,
        'profil.photo': photo,
        'profil.cv_pdf': cv_pdf,
        'profil.github': github,
        'profil.linkedin': linkedin,
        'profil.email': email,
        'profil.location': location,
    }
    for var, val in replacements.items():
        markdown = markdown.replace(f"{{{{ {var} }}}}", str(val))
        markdown = markdown.replace(f"{{{{{var}}}}}", str(val))

    src_path = page.file.src_path.replace('\\', '/')

    # Génération du Hero pour index.md
    if src_path == "index.md":
        # Avatar circulaire
        if photo:
            avatar_html = f'''<div class="hero-avatar">
    <img src="{photo}" alt="{full_name}">
  </div>'''
        else:
            initials = full_name[:2].upper() if full_name else "FE"
            avatar_html = f'''<div class="hero-avatar">
    <div class="hero-avatar-placeholder">{initials}</div>
  </div>'''

        # Badges de contact & statut
        badges = []
        if location and "Votre Ville" not in location:
            badges.append(f'<span><svg style="width: 14px; height: 14px; vertical-align: -2px; fill: currentColor; margin-right: 4px;" viewBox="0 0 384 512"><path d="M172.268 501.67C26.97 291.031 0 269.413 0 192 0 85.961 85.961 0 192 0s192 85.961 192 192c0 77.413-26.97 99.031-172.268 309.67-9.535 13.774-29.93 13.773-39.464 0zM192 272c44.183 0 80-35.817 80-80s-35.817-80-80-80-80 35.817-80 80 35.817 80 80 80z"/></svg>{location}</span>')
        elif not location:
            badges.append('<span><svg style="width: 14px; height: 14px; vertical-align: -2px; fill: currentColor; margin-right: 4px;" viewBox="0 0 384 512"><path d="M172.268 501.67C26.97 291.031 0 269.413 0 192 0s192 85.961 192 192c0 77.413-26.97 99.031-172.268 309.67-9.535 13.774-29.93 13.773-39.464 0zM192 272c44.183 0 80-35.817 80-80s-35.817-80-80-80-80 35.817-80 80 35.817 80 80 80z"/></svg>Maroc</span>')

        badges.append('<span><svg style="width: 10px; height: 10px; vertical-align: 0px; fill: #10b981; margin-right: 6px;" viewBox="0 0 512 512"><circle cx="256" cy="256" r="256"/></svg>À l\'écoute d\'opportunités</span>')

        badges_html = ""
        if badges:
            badges_html = f'<div class="hero-badges-line">{"".join(badges)}</div>'

        # Boutons d'action alignés (hauteur identique 42px)
        cv_btn_html = ""
        cv_preview_block = ""
        if cv_pdf:
            cv_btn_html = f'''<a href="{cv_pdf}" class="hero-btn hero-btn-primary" target="_blank" download>
        <svg width="18" height="18" style="width: 18px; height: 18px; min-width: 18px; max-width: 18px; flex-shrink: 0; vertical-align: middle; fill: currentColor;" viewBox="0 0 512 512"><path d="M64 0C28.7 0 0 28.7 0 64L0 448c0 35.3 28.7 64 64 64l256 0c35.3 0 64-28.7 64-64l0-288-128 0c-17.7 0-32-14.3-32-32L224 0 64 0zM256 0l0 128 128 0L256 0zM152 288l32 0c22.1 0 40 17.9 40 40c0 22.1-17.9 40-40 40l-16 0 0 32c0 8.8-7.2 16-16 16s-16-7.2-16-16l0-96c0-8.8 7.2-16 16-16zm32 48c4.4 0 8-3.6 8-8s-3.6-8-8-8l-16 0 0 16 16 0z"/></svg>
        <span>Télécharger mon CV (PDF)</span>
      </a>'''
            cv_preview_block = f'''
???+ info ":fontawesome-solid-file-pdf: Consulter mon CV directement en ligne (Aperçu interactif)"
    <object data="{cv_pdf}" type="application/pdf" width="100%" height="750px" style="border-radius: 8px; border: 1px solid var(--md-default-fg-color--lightest, #ccc); margin-top: 0.5rem;">
      <iframe src="{cv_pdf}" width="100%" height="750px" style="border: none;">
        <p>Aperçu indisponible. <a href="{cv_pdf}" target="_blank">Cliquez ici pour télécharger le CV en PDF</a>.</p>
      </iframe>
    </object>
'''

        contact_btn_html = ""
        if email and "exemple.com" not in email:
            contact_btn_html = f'''<a href="mailto:{email}" class="hero-btn hero-btn-secondary" title="M'envoyer un email">
        <svg width="18" height="18" style="width: 18px; height: 18px; min-width: 18px; max-width: 18px; flex-shrink: 0; vertical-align: middle; fill: currentColor;" viewBox="0 0 512 512"><path d="M48 64C21.5 64 0 85.5 0 112c0 15.1 7.1 29.3 19.2 38.4L236.8 313.6c11.4 8.5 27 8.5 38.4 0L492.8 150.4c12.1-9.1 19.2-23.3 19.2-38.4c0-26.5-21.5-48-48-48L48 64zM0 176L0 384c0 35.3 28.7 64 64 64l384 0c35.3 0 64-28.7 64-64l0-208L308.8 340.8c-30.4 22.8-72 22.8-102.4 0L0 176z"/></svg>
        <span>Me contacter</span>
      </a>'''

        linkedin_btn_html = f'''<a href="{linkedin}" class="hero-btn hero-btn-secondary" target="_blank">
        <svg width="18" height="18" style="width: 18px; height: 18px; min-width: 18px; max-width: 18px; flex-shrink: 0; vertical-align: middle; fill: currentColor;" viewBox="0 0 448 512"><path d="M100.28 448H7.4V148.9h92.88zM53.79 108.1C24.09 108.1 0 83.5 0 53.8a53.79 53.79 0 0 1 107.58 0c0 29.7-24.1 54.3-53.79 54.3zM447.9 448h-92.68V302.4c0-34.7-.7-79.2-48.29-79.2-48.3 0-55.7 37.7-55.7 76.7V448h-92.78V148.9h89.08v40.8h1.3c12.4-23.5 42.7-48.3 87.9-48.3 94 0 111.3 61.9 111.3 142.3V448z"/></svg>
        <span>LinkedIn</span>
      </a>'''

        github_btn_html = f'''<a href="{github}" class="hero-btn hero-btn-secondary" target="_blank">
        <svg width="18" height="18" style="width: 18px; height: 18px; min-width: 18px; max-width: 18px; flex-shrink: 0; vertical-align: middle; fill: currentColor;" viewBox="0 0 496 512"><path d="M165.9 397.4c0 2-2.3 3.6-5.2 3.6-3.3.3-5.6-1.3-5.6-3.6 0-2 2.3-3.6 5.2-3.6 3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9 2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5.3-6.2 2.3zm44.2-1.7c-2.9.7-4.9 2.6-4.6 4.9.3 2 3 3.3 6 2.6 2.9-.7 4.9-2.6 4.6-4.6-.3-1.9-3-3.2-6-2.9zM244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2 12.8 2.3 17.3-5.6 17.3-12.1 0-6.2-.3-40.4-.3-61.4 0 0-70 15-84.7-29.8 0 0-11.4-29.1-27.8-36.6 0 0-22.9-15.7 1.6-15.4 0 0 24.9 2 38.6 25.8 21.9 38.6 58.6 27.5 72.9 20.9 2.3-16 8.8-27.1 16-33.7-55.9-6.2-112.3-14.3-112.3-110.5 0-27.5 7.6-41.3 23.6-58.9-2.6-6.5-11.1-33.3 2.6-67.9 20.9-6.5 69 27 69 27 20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27 13.7 34.7 5.2 61.4 2.6 67.9 16 17.7 25.8 31.5 25.8 58.9 0 96.5-58.9 104.2-114.8 110.5 9.2 7.9 17 22.9 17 46.4 0 33.7-.3 75.4-.3 83.6 0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252 496 113.3 383.5 8 244.8 8zM97.2 352.9c-1.3 1-1 3.3.7 5.2 1.6 1.6 3.9 2.3 5.2 1 1.3-1 1-3.3-.7-5.2-1.6-1.6-3.9-2.3-5.2-1zm-10.8-8.1c-.7 1.3.3 2.9 2.3 3.9 1.6 1 3.6.7 4.3-.7.7-1.3-.3-2.9-2.3-3.9-2-.6-3.6-.3-4.3.7zm32.4 35.6c-1.6 1.3-1 4.3 1.3 6.2 2.3 2.3 5.2 2.6 6.5 1 1.3-1.3.7-4.3-1.3-6.2-2.2-2.3-5.2-2.6-6.5-1zm-11.4-14.7c-1.6 1-1.6 3.6 0 5.9 1.6 2.3 4.3 3.3 5.6 2.3 1.6-1.3 1.6-3.9 0-6.2-1.4-2.3-4-3.3-5.6-2z"/></svg>
        <span>GitHub</span>
      </a>'''

        # Utiliser un trait d'union insécable pour éviter que Fatima- et Ezzahrae soient scindés
        display_name = full_name.replace("-", "&#8209;") if full_name else ""

        hero_section = f'''<!-- DYNAMIC_PROFILE_START -->
<div class="hero-container">
  {avatar_html}
  <div class="hero-content">
    <h1 class="hero-name">{display_name}</h1>
    <div class="hero-title">
      <svg style="width: 20px; height: 20px; fill: currentColor;" viewBox="0 0 640 512"><path d="M392.8 1.2c-17-4.9-34.7 5-39.6 22l-128 448c-4.9 17 5 34.7 22 39.6s34.7-5 39.6-22l128-448c4.9-17-5-34.7-22-39.6zm80.6 120.1c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L514.7 256 428.1 342.6c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l112-112c12.5-12.5 12.5-32.8 0-45.3l-112-112zm-306.8 0l-112 112c-12.5 12.5-12.5 32.8 0 45.3l112 112c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L125.3 256l86.6-86.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0z"/></svg>
      <span>{title}</span>
    </div>
    {badges_html}
    <p class="hero-tagline">{tagline}</p>
    <div class="hero-actions">
      {cv_btn_html}
      {contact_btn_html}
      {linkedin_btn_html}
      {github_btn_html}
    </div>
  </div>
</div>


{cv_preview_block}

<div class="section-intro-title">
  <svg style="width: 24px; height: 24px; fill: var(--md-primary-fg-color, #3f51b5);" viewBox="0 0 512 512"><path d="M326.7 1.2c-1.7-.8-3.6-1.2-5.5-1.2-4.1 0-7.9 2-10.2 5.4L208.6 153.2c-2.4 3.6-2.5 8.2-.3 11.9 2.2 3.7 6.2 6 10.5 6h73.4l-71.6 179c-2.4 6 0 12.8 5.6 16.1 5.6 3.3 12.8 2.2 17.2-2.8l176-200c3.5-4 4.1-9.7 1.6-14.3-2.5-4.6-7.3-7.5-12.5-7.5H336.8l56.4-123.6c2.5-5.5.9-12-3.9-15.7-4.8-3.7-11.4-3.7-16.2 0L248 104.9c-4.9 3.8-6.9 10.3-4.8 16.1s7.5 9.8 13.6 9.8h46.7L181.8 322c-2.6 4.7-2.3 10.5.8 14.9 3.1 4.4 8.3 7 13.8 7h76.8l-87.1 161.4c-2.8 5.2-1.9 11.6 2.2 15.9 4.1 4.3 10.6 5.5 16 2.9l192-96c4.6-2.3 7.6-7.1 7.6-12.2s-3-9.9-7.6-12.2l-51.2-25.6 75.3-138.1c2.4-4.4 2.2-9.8-.5-14s-7.4-6.8-12.4-6.8H424l51.6-113.6c2.5-5.5.9-12-3.9-15.7z"/></svg>
  <span>Ce que je fais & Domaines d'expertise</span>
</div>

<div class="features-grid">
  <div class="feature-card">
    <div class="feature-icon-box">
      <svg viewBox="0 0 640 512"><path d="M392.8 1.2c-17-4.9-34.7 5-39.6 22l-128 448c-4.9 17 5 34.7 22 39.6s34.7-5 39.6-22l128-448c4.9-17-5-34.7-22-39.6zm80.6 120.1c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L514.7 256 428.1 342.6c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l112-112c12.5-12.5 12.5-32.8 0-45.3l-112-112zm-306.8 0l-112 112c-12.5 12.5-12.5 32.8 0 45.3l112 112c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L125.3 256l86.6-86.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0z"/></svg>
    </div>
    <div class="feature-title">Architecture Backend & APIs</div>
    <div class="feature-desc">Conception de services robustes en architecture hexagonale, APIs REST asynchrones, authentification sécurisée (OAuth 2.0, OIDC, JWT RS256) et temps réel via WebSockets.</div>
    <div class="feature-tags">
      <span class="tech-badge">Java 21</span>
      <span class="tech-badge">Spring Boot 3</span>
      <span class="tech-badge">Python 3.12</span>
      <span class="tech-badge">FastAPI</span>
      <span class="tech-badge">PostgreSQL</span>
      <span class="tech-badge">Redis</span>
    </div>
  </div>

  <div class="feature-card">
    <div class="feature-icon-box">
      <svg viewBox="0 0 640 512"><path d="M349.9 236.3h-66.1v-59.4h66.1v59.4zm0-204.3h-66.1v59.4h66.1V32zm78.2 144.9H362v59.4h66.1v-59.4zm0-72.5H362v59.4h66.1v-59.4zm-156.4 72.5h-66.1v59.4h66.1v-59.4zm0-72.5h-66.1v59.4h66.1v-59.4zm-78.2 72.5H127.4v59.4h66.1v-59.4zm0-72.5H127.4v59.4h66.1v-59.4zM624 208c0-35.3-28.7-64-64-64h-32c-17.7 0-32 14.3-32 32v16h-48V64c0-17.7-14.3-32-32-32H112C94.3 32 80 46.3 80 64v128H48c-17.7 0-32 14.3-32 32v128c0 70.7 57.3 128 128 128h352c70.7 0 128-57.3 128-128V208z"/></svg>
    </div>
    <div class="feature-title">Conteneurisation & K8s</div>
    <div class="feature-desc">Création d'images Docker multi-stage optimisées, gestion de clusters K3s/Kubernetes, Helm charts et automatisation d'infrastructures de virtualisation sous Proxmox VE.</div>
    <div class="feature-tags">
      <span class="tech-badge">Docker</span>
      <span class="tech-badge">K3s</span>
      <span class="tech-badge">Kubernetes</span>
      <span class="tech-badge">Proxmox VE</span>
      <span class="tech-badge">Helm</span>
      <span class="tech-badge">Packer</span>
    </div>
  </div>

  <div class="feature-card">
    <div class="feature-icon-box">
      <svg viewBox="0 0 512 512"><path d="M480 352H32c-17.7 0-32 14.3-32 32v64c0 17.7 14.3 32 32 32h448c17.7 0 32-14.3 32-32v-64c0-17.7-14.3-32-32-32zm-416 72c-13.3 0-24-10.7-24-24s10.7-24 24-24 24 10.7 24 24-10.7 24-24 24zm416-272H32c-17.7 0-32 14.3-32 32v64c0 17.7 14.3 32 32 32h448c17.7 0 32-14.3 32-32v-64c0-17.7-14.3-32-32-32zm-416 72c-13.3 0-24-10.7-24-24s10.7-24 24-24 24 10.7 24 24-10.7 24-24 24zm416-272H32C14.3 80 0 94.3 0 112v64c0 17.7 14.3 32 32 32h448c17.7 0 32-14.3 32-32v-64c0-17.7-14.3-32-32-32zm-416 72c-13.3 0-24-10.7-24-24s10.7-24 24-24 24 10.7 24 24-10.7 24-24 24z"/></svg>
    </div>
    <div class="feature-title">Pipelines CI/CD & IaC</div>
    <div class="feature-desc">Orchestration complète du code à la production : Jenkins (JCasC, Job DSL), GitHub Actions, provisioning déclaratif avec Terraform, configuration via Ansible et scripts Bash.</div>
    <div class="feature-tags">
      <span class="tech-badge">Jenkins</span>
      <span class="tech-badge">GitHub Actions</span>
      <span class="tech-badge">Terraform</span>
      <span class="tech-badge">Ansible</span>
      <span class="tech-badge">Bash</span>
    </div>
  </div>

  <div class="feature-card">
    <div class="feature-icon-box">
      <svg viewBox="0 0 640 512"><path d="M537.6 226.6c4.1-10.7 6.4-22.4 6.4-34.6 0-53-43-96-96-96-19.7 0-38.1 6-53.3 16.2C367 64.2 315.3 32 256 32c-88.4 0-160 71.6-160 160 0 2.7.1 5.4.2 8.1C40.2 219.8 0 273.2 0 336c0 79.5 64.5 144 144 144h384c61.9 0 112-50.1 112-112 0-56.5-41.9-103.2-96.4-110.4-1.2-10.4-2.8-20.6-5-30.6zM320 288c-17.7 0-32-14.3-32-32s14.3-32 32-32 32 14.3 32 32-14.3 32-32 32zm96 96H224c-17.7 0-32-14.3-32-32s14.3-32 32-32h192c17.7 0 32 14.3 32 32s-14.3 32-32 32z"/></svg>
    </div>
    <div class="feature-title">Cloud & Observabilité</div>
    <div class="feature-desc">Déploiements résilients sur Oracle Cloud (OCI 3x certifiée) et Azure, supervision proactive avec Prometheus & Grafana, traçabilité des logs, scans de sécurité Trivy et Gitleaks.</div>
    <div class="feature-tags">
      <span class="tech-badge">Oracle Cloud</span>
      <span class="tech-badge">Azure</span>
      <span class="tech-badge">Prometheus</span>
      <span class="tech-badge">Grafana</span>
      <span class="tech-badge">Trivy</span>
      <span class="tech-badge">Vault</span>
    </div>
  </div>
</div>
<!-- DYNAMIC_PROFILE_END -->'''

        pattern = r"<!-- DYNAMIC_PROFILE_START -->.*?<!-- DYNAMIC_PROFILE_END -->"
        if re.search(pattern, markdown, flags=re.DOTALL):
            markdown = re.sub(pattern, hero_section, markdown, flags=re.DOTALL)
        else:
            markdown = hero_section + "\n\n" + markdown

        # Génération dynamique de la timeline des expériences & projets
        if experiences:
            timeline_html = f'''<!-- DYNAMIC_EXPERIENCES_START -->
{_build_timeline_html(experiences, docs_dir)}
<!-- DYNAMIC_EXPERIENCES_END -->'''
            exp_pattern = r"<!-- DYNAMIC_EXPERIENCES_START -->.*?<!-- DYNAMIC_EXPERIENCES_END -->"
            if re.search(exp_pattern, markdown, flags=re.DOTALL):
                markdown = re.sub(exp_pattern, timeline_html, markdown, flags=re.DOTALL)

    elif src_path == "10-experience/index.md":
        if experiences:
            list_md = f'''<!-- DYNAMIC_EXPERIENCES_LIST_START -->
{_build_experiences_list_markdown(experiences, docs_dir)}
<!-- DYNAMIC_EXPERIENCES_LIST_END -->'''
            list_pattern = r"<!-- DYNAMIC_EXPERIENCES_LIST_START -->.*?<!-- DYNAMIC_EXPERIENCES_LIST_END -->"
            if re.search(list_pattern, markdown, flags=re.DOTALL):
                markdown = re.sub(list_pattern, list_md, markdown, flags=re.DOTALL)

    return markdown

def _build_timeline_html(experiences, docs_dir):
    items_html = []
    for exp in experiences:
        exp_id = exp.get('id', '')
        title = exp.get('title', '')
        period = exp.get('period', '')
        location = exp.get('location', '')
        subtitle = exp.get('subtitle', '')
        desc = exp.get('description', [])
        stack = exp.get('stack', [])
        project_page = exp.get('project_page', '')

        # Résolution dynamique automatique de la page de projet si non spécifiée
        if not project_page and exp_id:
            candidate = os.path.join(docs_dir, '04-projets', f'{exp_id}.md')
            if os.path.exists(candidate):
                project_page = f'04-projets/{exp_id}.md'

        date_line = f"{period} | {location}" if location else period

        # Titre cliquable si page de projet liée
        if project_page:
            title_html = f'<a href="{project_page}" class="project-title-link">{title} <span class="arrow-icon">↗</span></a>'
        else:
            title_html = title

        # Description
        if isinstance(desc, list):
            desc_lines = []
            for d in desc:
                clean_d = str(d).strip()
                if not clean_d.startswith('•') and not clean_d.startswith('-'):
                    if ' : ' in clean_d and not clean_d.startswith('<strong>'):
                        lbl, rest = clean_d.split(' : ', 1)
                        clean_d = f"• <strong>{lbl} :</strong> {rest}"
                    else:
                        clean_d = f"• {clean_d}"
                desc_lines.append(clean_d)
            desc_html = "<br>\n        ".join(desc_lines)
        else:
            desc_html = str(desc)

        # Badges stack
        stack_html = "".join([f'<span class="tech-badge">{tech}</span>\n        ' for tech in stack])

        # Bouton d'action vers le cycle complet de projet
        cta_html = ""
        if project_page:
            cta_html = f'''<div class="project-cta-container">
        <a href="{project_page}" class="project-card-cta">
          <span>Consulter le cycle de vie complet du projet (SDLC & DevOps)</span>
          <svg viewBox="0 0 448 512"><path d="M438.6 278.6c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L338.8 224 32 224c-17.7 0-32 14.3-32 32s14.3 32 32 32l306.7 0-105.4 105.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l160-160z"/></svg>
        </a>
      </div>'''

        item = f'''  <div class="timeline-item">
    <div class="timeline-dot"></div>
    <div class="timeline-date">{date_line}</div>
    <div class="timeline-content">
      <h4>{title_html}</h4>
      <div class="timeline-subtitle">{subtitle}</div>
      <p class="timeline-desc">
        {desc_html}
      </p>
      <div>
        {stack_html}
      </div>
      {cta_html}
    </div>
  </div>'''
        items_html.append(item)

    return '<div class="timeline">\n' + "\n\n".join(items_html) + '\n</div>'

def _build_experiences_list_markdown(experiences, docs_dir):
    blocks = []
    for i, exp in enumerate(experiences, start=1):
        exp_id = exp.get('id', '')
        title = exp.get('title', '')
        period = exp.get('period', '')
        location = exp.get('location', '')
        subtitle = exp.get('subtitle', '')
        stack = exp.get('stack', [])
        project_page = exp.get('project_page', '')

        if not project_page and exp_id:
            candidate = os.path.join(docs_dir, '04-projets', f'{exp_id}.md')
            if os.path.exists(candidate):
                project_page = f'04-projets/{exp_id}.md'

        stack_str = ", ".join(stack)
        loc_str = f" | {location}" if location else ""

        link_line = ""
        if project_page:
            rel_page = project_page
            if not rel_page.startswith('../') and not rel_page.startswith('/'):
                rel_page = f"../{rel_page}"
            link_line = f"\n* 👉 **[:material-arrow-right-circle: Consulter le cycle de vie complet du projet (SDLC & DevOps)]({rel_page})**"

        block = f'''### {i}. {title}
* **Période** : {period}{loc_str}
* **Projet** : {subtitle}
* **Technologies** : {stack_str}{link_line}'''
        blocks.append(block)

    return "\n\n---\n\n".join(blocks)

