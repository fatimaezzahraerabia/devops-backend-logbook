import os
import re
import yaml

def on_page_markdown(markdown, page, config, files):
    """
    Hook MkDocs exécuté avant le rendu de chaque page.
    Lit dynamiquement docs/data/profil.yml (édité via Decap CMS)
    et injecte automatiquement :
      - Photo de profil (avec avatar stylisé)
      - Nom, titre, localisation, contact
      - Bouton Télécharger CV (PDF)
      - Lecteur interactif pour afficher le CV PDF directement dans la page
      - Boutons de réseaux sociaux (LinkedIn, GitHub)
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

    # Nettoyer les chemins (enlever le slash initial pour assurer la compatibilité relative)
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
    bio = profil.get('bio', "Ingénieure passionnée par la conception de systèmes Backend robustes et l'automatisation des infrastructures DevOps.")
    github = profil.get('github', 'https://github.com/fatimaezzahraerabia')
    linkedin = profil.get('linkedin', 'https://linkedin.com/in/fatima-ezzahrae-rabia')
    email = profil.get('email', '')
    location = profil.get('location', '')

    # Remplacement des balises de template {{ profil.* }}
    replacements = {
        'profil.full_name': full_name,
        'profil.title': title,
        'profil.bio': bio,
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

    # Génération du Hero pour index.md
    if page.file.src_path == "index.md":
        # Avatar ou Photo de profil
        if photo:
            avatar_html = f'''<div style="flex-shrink: 0; text-align: center;">
    <img src="{photo}" alt="{full_name}" style="width: 145px; height: 145px; object-fit: cover; border-radius: 50%; box-shadow: 0 6px 20px rgba(0,0,0,0.18); border: 4px solid var(--md-primary-fg-color, #3f51b5);">
  </div>'''
        else:
            initials = full_name[:2].upper() if full_name else "FE"
            avatar_html = f'''<div style="flex-shrink: 0; text-align: center;">
    <div style="width: 135px; height: 135px; border-radius: 50%; background: var(--md-primary-fg-color, #3f51b5); color: #fff; display: flex; align-items: center; justify-content: center; font-size: 2.8rem; font-weight: 700; box-shadow: 0 6px 20px rgba(0,0,0,0.18);">
      {initials}
    </div>
  </div>'''

        # Bouton Télécharger CV en SVG pur + classes Material
        cv_actions_html = ""
        cv_preview_md = ""
        if cv_pdf:
            cv_actions_html = f'''<a href="{cv_pdf}" class="md-button md-button--primary" target="_blank" download style="display: inline-flex; align-items: center; gap: 0.5rem; font-weight: 600; text-decoration: none;">
        <svg style="width: 1.1rem; height: 1.1rem; fill: currentColor;" viewBox="0 0 512 512"><path d="M64 0C28.7 0 0 28.7 0 64L0 448c0 35.3 28.7 64 64 64l256 0c35.3 0 64-28.7 64-64l0-288-128 0c-17.7 0-32-14.3-32-32L224 0 64 0zM256 0l0 128 128 0L256 0zM152 288l32 0c22.1 0 40 17.9 40 40c0 22.1-17.9 40-40 40l-16 0 0 32c0 8.8-7.2 16-16 16s-16-7.2-16-16l0-96c0-8.8 7.2-16 16-16zm32 48c4.4 0 8-3.6 8-8s-3.6-8-8-8l-16 0 0 16 16 0z"/></svg>
        Télécharger mon CV (PDF)
      </a>'''
            cv_preview_md = f'''
???+ info ":fontawesome-solid-file-pdf: Aperçu interactif du CV en direct"
    <object data="{cv_pdf}" type="application/pdf" width="100%" height="750px" style="border-radius: 8px; border: 1px solid var(--md-default-fg-color--lightest, #ccc); margin-top: 0.5rem;">
      <iframe src="{cv_pdf}" width="100%" height="750px" style="border: none;">
        <p>Aperçu indisponible dans votre navigateur. <a href="{cv_pdf}" target="_blank">Cliquez ici pour télécharger le CV en PDF</a>.</p>
      </iframe>
    </object>
'''

        # Badges de contact
        badges = []
        if location:
            badges.append(f'<span style="display: inline-flex; align-items: center; gap: 0.3rem;"><svg style="width: 0.95rem; height: 0.95rem; fill: currentColor;" viewBox="0 0 384 512"><path d="M172.268 501.67C26.97 291.031 0 269.413 0 192 0 85.961 85.961 0 192 0s192 85.961 192 192c0 77.413-26.97 99.031-172.268 309.67-9.535 13.774-29.93 13.773-39.464 0zM192 272c44.183 0 80-35.817 80-80s-35.817-80-80-80-80 35.817-80 80 35.817 80 80 80z"/></svg>{location}</span>')
        if email and "exemple.com" not in email:
            badges.append(f'<a href="mailto:{email}" style="display: inline-flex; align-items: center; gap: 0.3rem; color: inherit; text-decoration: none;"><svg style="width: 0.95rem; height: 0.95rem; fill: currentColor;" viewBox="0 0 512 512"><path d="M48 64C21.5 64 0 85.5 0 112c0 15.1 7.1 29.3 19.2 38.4L236.8 313.6c11.4 8.5 27 8.5 38.4 0L492.8 150.4c12.1-9.1 19.2-23.3 19.2-38.4c0-26.5-21.5-48-48-48L48 64zM0 176L0 384c0 35.3 28.7 64 64 64l384 0c35.3 0 64-28.7 64-64l0-208L308.8 340.8c-30.4 22.8-72 22.8-102.4 0L0 176z"/></svg>{email}</a>')

        contact_badges_html = ""
        if badges:
            contact_badges_html = f'''<div style="display: flex; gap: 1.2rem; align-items: center; flex-wrap: wrap; margin-top: 0.4rem; margin-bottom: 0.9rem; font-size: 0.9rem; color: var(--md-default-fg-color--light);">
      {"".join(badges)}
    </div>'''

        profile_hero_block = f'''<!-- DYNAMIC_PROFILE_START -->
<div style="display: flex; flex-direction: row; align-items: center; gap: 2rem; padding: 1.8rem; background: var(--md-code-bg-color, rgba(63, 81, 181, 0.05)); border-radius: 14px; margin-bottom: 2rem; border: 1px solid var(--md-default-fg-color--lightest, #e0e0e0); flex-wrap: wrap;">
  {avatar_html}
  <div style="flex-grow: 1; min-width: 260px;">
    <h1 style="margin: 0 0 0.2rem 0; font-size: 1.8rem; font-weight: 700; color: var(--md-typeset-color);">{full_name}</h1>
    <div style="font-size: 1.15rem; font-weight: 600; color: var(--md-primary-fg-color, #3f51b5); margin-bottom: 0.3rem;">{title}</div>
    {contact_badges_html}
    <p style="margin: 0 0 1.2rem 0; line-height: 1.6; color: var(--md-typeset-color); font-size: 0.95rem;">{bio}</p>
    <div style="display: flex; gap: 0.8rem; align-items: center; flex-wrap: wrap;">
      {cv_actions_html}
      <a href="{linkedin}" class="md-button" target="_blank" style="display: inline-flex; align-items: center; gap: 0.4rem; text-decoration: none;">
        <svg style="width: 1.05rem; height: 1.05rem; fill: currentColor;" viewBox="0 0 448 512"><path d="M100.28 448H7.4V148.9h92.88zM53.79 108.1C24.09 108.1 0 83.5 0 53.8a53.79 53.79 0 0 1 107.58 0c0 29.7-24.1 54.3-53.79 54.3zM447.9 448h-92.68V302.4c0-34.7-.7-79.2-48.29-79.2-48.3 0-55.7 37.7-55.7 76.7V448h-92.78V148.9h89.08v40.8h1.3c12.4-23.5 42.7-48.3 87.9-48.3 94 0 111.3 61.9 111.3 142.3V448z"/></svg>
        LinkedIn
      </a>
      <a href="{github}" class="md-button" target="_blank" style="display: inline-flex; align-items: center; gap: 0.4rem; text-decoration: none;">
        <svg style="width: 1.05rem; height: 1.05rem; fill: currentColor;" viewBox="0 0 496 512"><path d="M165.9 397.4c0 2-2.3 3.6-5.2 3.6-3.3.3-5.6-1.3-5.6-3.6 0-2 2.3-3.6 5.2-3.6 3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9 2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5.3-6.2 2.3zm44.2-1.7c-2.9.7-4.9 2.6-4.6 4.9.3 2 3 3.3 6 2.6 2.9-.7 4.9-2.6 4.6-4.6-.3-1.9-3-3.2-6-2.9zM244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2 12.8 2.3 17.3-5.6 17.3-12.1 0-6.2-.3-40.4-.3-61.4 0 0-70 15-84.7-29.8 0 0-11.4-29.1-27.8-36.6 0 0-22.9-15.7 1.6-15.4 0 0 24.9 2 38.6 25.8 21.9 38.6 58.6 27.5 72.9 20.9 2.3-16 8.8-27.1 16-33.7-55.9-6.2-112.3-14.3-112.3-110.5 0-27.5 7.6-41.3 23.6-58.9-2.6-6.5-11.1-33.3 2.6-67.9 20.9-6.5 69 27 69 27 20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27 13.7 34.7 5.2 61.4 2.6 67.9 16 17.7 25.8 31.5 25.8 58.9 0 96.5-58.9 104.2-114.8 110.5 9.2 7.9 17 22.9 17 46.4 0 33.7-.3 75.4-.3 83.6 0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252 496 113.3 383.5 8 244.8 8zM97.2 352.9c-1.3 1-1 3.3.7 5.2 1.6 1.6 3.9 2.3 5.2 1 1.3-1 1-3.3-.7-5.2-1.6-1.6-3.9-2.3-5.2-1zm-10.8-8.1c-.7 1.3.3 2.9 2.3 3.9 1.6 1 3.6.7 4.3-.7.7-1.3-.3-2.9-2.3-3.9-2-.6-3.6-.3-4.3.7zm32.4 35.6c-1.6 1.3-1 4.3 1.3 6.2 2.3 2.3 5.2 2.6 6.5 1 1.3-1.3.7-4.3-1.3-6.2-2.2-2.3-5.2-2.6-6.5-1zm-11.4-14.7c-1.6 1-1.6 3.6 0 5.9 1.6 2.3 4.3 3.3 5.6 2.3 1.6-1.3 1.6-3.9 0-6.2-1.4-2.3-4-3.3-5.6-2z"/></svg>
        GitHub
      </a>
    </div>
  </div>
</div>

{cv_preview_md}
<!-- DYNAMIC_PROFILE_END -->'''

        pattern = r"<!-- DYNAMIC_PROFILE_START -->.*?<!-- DYNAMIC_PROFILE_END -->"
        if re.search(pattern, markdown, flags=re.DOTALL):
            markdown = re.sub(pattern, profile_hero_block, markdown, flags=re.DOTALL)
        else:
            markdown = profile_hero_block + "\n\n" + markdown

    return markdown
