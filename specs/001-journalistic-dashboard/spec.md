# Feature Specification: Dashboard Journalistique Olympique

**Feature Branch**: `001-journalistic-dashboard`  
**Created**: 2025-12-16  
**Status**: Draft  
**Input**: User description: "Nous souhaitons transformer le MVP actuel en un Dashboard Journalistique Olympique complet avec cartographie mondiale interactive, section top athlètes, comparateur de nations, export CSV et interface à onglets Streamlit."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Exploration Géographique des Médailles (Priority: P1)

En tant que journaliste olympique, je veux visualiser la distribution géographique des médailles sur une carte mondiale interactive pour identifier rapidement les puissances sportives par région et par période.

**Why this priority**: La carte choroplèthe est l'élément visuel le plus distinctif qui transforme le MVP en un outil journalistique complet. Elle apporte une valeur immédiate en rendant les données géographiques accessibles visuellement.

**Independent Test**: Peut être testé en ajoutant un onglet "Carte Mondiale" avec une carte Plotly choroplèthe montrant le nombre de médailles par pays. Les filtres Année/Sport doivent mettre à jour la carte en temps réel. Délivre une nouvelle perspective géographique sur les données olympiques.

**Acceptance Scenarios**:

1. **Given** l'utilisateur est sur l'onglet "Carte Mondiale", **When** aucun filtre n'est appliqué, **Then** la carte affiche la densité totale de médailles par pays (1896-2004)
2. **Given** l'utilisateur sélectionne "2000-2004" dans le filtre Année, **When** la carte se rafraîchit, **Then** seules les médailles de cette période sont affichées par pays
3. **Given** l'utilisateur sélectionne "Athletics" dans le filtre Sport, **When** la carte se met à jour, **Then** seules les médailles d'athlétisme sont comptabilisées par pays
4. **Given** l'utilisateur survole un pays sur la carte, **When** le curseur est sur le pays, **Then** une infobulle affiche le nom du pays et le nombre exact de médailles
5. **Given** la carte affiche les données, **When** l'utilisateur combine plusieurs filtres (Année + Sport + Pays spécifique), **Then** la carte reflète tous les filtres appliqués

---

### User Story 2 - Identification des Stars Olympiques (Priority: P2)

En tant que rédacteur sportif, je veux voir le top 10 des athlètes les plus médaillés selon mes critères de filtrage pour rédiger des portraits d'athlètes d'exception.

**Why this priority**: Cette fonctionnalité enrichit l'analyse en mettant en avant les individus, pas seulement les pays. Elle complète la vue globale en apportant une dimension humaine aux statistiques.

**Independent Test**: Peut être testé en ajoutant une section "Top Athlètes" affichant un tableau ou des cartes avec les 10 athlètes ayant le plus de médailles selon les filtres actifs. Fonctionne indépendamment des autres onglets.

**Acceptance Scenarios**:

1. **Given** aucun filtre n'est appliqué, **When** l'utilisateur consulte la section "Top Athlètes", **Then** les 10 athlètes les plus médaillés de tous les temps sont affichés avec leur nom, pays, et nombre de médailles (Or/Argent/Bronze)
2. **Given** l'utilisateur filtre par pays "USA", **When** la section se met à jour, **Then** seuls les athlètes américains apparaissent dans le classement
3. **Given** l'utilisateur filtre par sport "Swimming", **When** le classement se recalcule, **Then** seuls les nageurs médaillés sont listés
4. **Given** l'utilisateur combine filtres Année (ex: 1992-2004) et Sport, **When** le top 10 s'affiche, **Then** seuls les athlètes correspondant aux deux critères sont classés
5. **Given** le tableau affiche les athlètes, **When** l'utilisateur consulte les détails, **Then** chaque athlète montre le détail de ses médailles (Gold: X, Silver: Y, Bronze: Z)

---

### User Story 3 - Comparaison Historique de Nations (Priority: P3)

En tant qu'analyste sportif, je veux comparer l'évolution des performances de deux pays au fil du temps pour produire des analyses de rivalités historiques (ex: USA vs URSS).

**Why this priority**: Cette fonctionnalité est plus avancée et s'adresse à des analyses approfondies. Elle complète le dashboard mais n'est pas essentielle au premier déploiement.

**Independent Test**: Peut être testé en créant un onglet "Comparateur" avec deux sélecteurs de pays et un graphique en ligne superposant les courbes de médailles des deux pays par année. Fonctionne de manière autonome.

**Acceptance Scenarios**:

1. **Given** l'utilisateur est sur l'onglet "Comparateur", **When** il sélectionne deux pays (ex: USA et RUS), **Then** un graphique en ligne affiche les deux courbes de médailles superposées de 1896 à 2004
2. **Given** deux pays sont sélectionnés, **When** l'utilisateur applique un filtre Sport (ex: "Athletics"), **Then** les courbes ne montrent que les médailles d'athlétisme pour chaque pays
3. **Given** le graphique affiche les courbes, **When** l'utilisateur survole une année, **Then** une infobulle montre le nombre exact de médailles pour chaque pays cette année-là
4. **Given** aucun pays n'est sélectionné, **When** l'utilisateur est sur cet onglet, **Then** un message explicatif invite à sélectionner deux pays pour commencer la comparaison
5. **Given** deux pays sont comparés, **When** l'utilisateur change un des pays sélectionnés, **Then** le graphique se met à jour instantanément avec la nouvelle comparaison

---

### User Story 4 - Export des Données Filtrées (Priority: P2)

En tant qu'utilisateur du dashboard, je veux exporter les données actuellement filtrées en CSV pour effectuer des analyses personnalisées dans Excel ou d'autres outils.

**Why this priority**: L'export de données est une fonctionnalité attendue dans tout outil d'analyse professionnel. Elle augmente l'utilité du dashboard en permettant des workflows externes.

**Independent Test**: Peut être testé en ajoutant un bouton "Télécharger CSV" dans la sidebar qui génère un fichier CSV contenant uniquement les lignes correspondant aux filtres actifs. Fonctionne indépendamment des visualisations.

**Acceptance Scenarios**:

1. **Given** l'utilisateur a appliqué des filtres (Année, Pays, Sport), **When** il clique sur "Télécharger CSV", **Then** un fichier CSV contenant uniquement les données filtrées est téléchargé
2. **Given** aucun filtre n'est appliqué, **When** l'utilisateur clique sur "Télécharger CSV", **Then** le fichier contient l'intégralité du dataset (1896-2004)
3. **Given** le fichier CSV est téléchargé, **When** l'utilisateur l'ouvre dans Excel, **Then** les colonnes incluent Year, City, Sport, Discipline, Athlete Name, NOC, Gender, Event, Event Gender, Medal, Position
4. **Given** l'utilisateur filtre par Pays = "FRA" et Année = "2000-2004", **When** il exporte les données, **Then** seules les lignes françaises entre 2000 et 2004 sont présentes dans le CSV
5. **Given** le bouton est dans la sidebar, **When** l'utilisateur le localise, **Then** il est clairement visible et étiqueté "📥 Télécharger les données (CSV)"

---

### User Story 5 - Navigation par Onglets (Priority: P1)

En tant qu'utilisateur, je veux naviguer entre différentes vues du dashboard via des onglets Streamlit pour éviter le défilement excessif et accéder rapidement aux analyses qui m'intéressent.

**Why this priority**: L'organisation en onglets est critique pour l'ergonomie du dashboard enrichi. Sans elle, l'ajout de nouvelles sections rendrait la page principale trop longue et difficile à naviguer.

**Independent Test**: Peut être testé en restructurant l'interface avec `st.tabs()` créant des onglets "Vue d'ensemble", "Carte Mondiale", "Top Athlètes", "Comparateur". Chaque onglet charge son contenu indépendamment.

**Acceptance Scenarios**:

1. **Given** l'utilisateur arrive sur le dashboard, **When** la page se charge, **Then** des onglets horizontaux sont visibles en haut du contenu principal avec les intitulés: "Vue d'ensemble", "Carte Mondiale", "Top Athlètes", "Comparateur"
2. **Given** l'utilisateur est sur l'onglet "Vue d'ensemble" (par défaut), **When** il consulte le contenu, **Then** il voit les KPIs, les graphiques d'évolution et de répartition genre (contenu MVP actuel)
3. **Given** l'utilisateur clique sur l'onglet "Carte Mondiale", **When** l'onglet s'active, **Then** le contenu passe à la carte choroplèthe interactive
4. **Given** l'utilisateur navigue entre onglets, **When** il change d'onglet, **Then** les filtres de la sidebar restent appliqués et cohérents entre toutes les vues
5. **Given** un onglet est actif, **When** l'utilisateur applique un nouveau filtre, **Then** le contenu de l'onglet actuel se met à jour immédiatement sans changer d'onglet

---

### Edge Cases

- Que se passe-t-il si un pays n'a aucune médaille pour la période filtrée? La carte doit afficher le pays en gris clair (couleur neutre distincte) avec une infobulle indiquant "0 médailles"
- Comment le système gère-t-il les codes pays (NOC) qui ont changé historiquement (ex: URSS → RUS)? (Utiliser les codes NOC tels quels du dataset, pas de fusion automatique)
- Comment sont classés les athlètes ayant le même nombre total de médailles dans le top 10? (Appliquer le système de départage olympique: d'abord par nombre d'or, puis argent, puis bronze)
- Que se passe-t-il si l'utilisateur sélectionne le même pays deux fois dans le comparateur? (Afficher un message d'erreur: "Veuillez sélectionner deux pays différents")
- Comment réagit le système si aucun athlète ne correspond aux filtres appliqués? (Afficher "Aucun athlète trouvé pour ces critères")
- Que se passe-t-il si l'utilisateur tente d'exporter un dataset vide (filtres trop restrictifs)? (Générer un CSV vide avec les headers uniquement et afficher un avertissement)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Le système DOIT ajouter un onglet "Carte Mondiale" contenant une carte choroplèthe Plotly affichant la densité de médailles par code pays (NOC). Les pays avec zéro médaille DOIVENT être affichés en gris clair avec une infobulle "0 médailles"
- **FR-002**: La carte DOIT réagir aux filtres Année, Pays (NOC), et Sport en temps réel sans rechargement complet de la page
- **FR-003**: Le système DOIT afficher une section "Top Athlètes" montrant les 10 athlètes les plus médaillés selon les filtres actifs. En cas d'égalité du nombre total de médailles, le classement DOIT suivre la logique olympique: nombre de médailles d'or d'abord, puis d'argent, puis de bronze
- **FR-004**: La section "Top Athlètes" DOIT être affichée sous forme de tableau stylisé avec les colonnes suivantes: Rang (Rank), Nom (Name), Pays (Country), Total, Or (Gold), Argent (Silver), Bronze
- **FR-005**: Le système DOIT ajouter un onglet "Comparateur" permettant de sélectionner deux pays via des widgets Streamlit (selectbox ou multiselect limité à 2)
- **FR-006**: Le comparateur DOIT afficher un graphique en ligne (line chart) superposant les courbes de médailles des deux pays sélectionnés par année. Chaque pays est représenté par une seule ligne montrant le total de médailles par année (2 lignes au total)
- **FR-007**: Le système DOIT ajouter un bouton "Télécharger CSV" dans la sidebar qui exporte les données actuellement filtrées
- **FR-008**: Le fichier CSV exporté DOIT contenir toutes les colonnes du dataset original avec uniquement les lignes correspondant aux filtres actifs. Le nom du fichier DOIT suivre le format: olympics_filtered_YYYY-MM-DD_HHMMSS.csv avec horodatage pour éviter les écrasements
- **FR-009**: Le système DOIT utiliser `st.tabs()` pour organiser l'interface en onglets: "Vue d'ensemble", "Carte Mondiale", "Top Athlètes", "Comparateur"
- **FR-010**: Les filtres de la sidebar DOIVENT rester cohérents et appliqués lors de la navigation entre onglets
- **FR-011**: Tous les graphiques DOIVENT respecter le thème couleur défini dans `.streamlit/config.toml` (teal/blue-green)
- **FR-012**: Toutes les fonctions de chargement de données lourdes DOIVENT utiliser `@st.cache_data` pour garantir les performances
- **FR-013**: Le système DOIT gérer les cas où aucune donnée ne correspond aux filtres (afficher des messages informatifs)
- **FR-014**: Les infobulles des cartes et graphiques DOIVENT afficher les informations en français avec les unités appropriées

### Key Entities *(include if feature involves data)*

- **Medal Country Aggregation**: Agrégation des médailles par code pays (NOC), incluant le nombre total et la distribution Or/Argent/Bronze par période
- **Top Athlete**: Athlète classé avec rang, nom, pays (NOC), total de médailles, et détail par type (Or/Argent/Bronze), affiché dans un tableau stylisé, filtré par critères utilisateur
- **Country Comparison Data**: Série temporelle du total de médailles par année pour deux pays sélectionnés, permettant la superposition graphique sur deux lignes distinctes
- **Filtered Dataset Export**: Snapshot du dataset filtré par les critères actifs, exportable en format CSV

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Les utilisateurs peuvent visualiser la distribution géographique des médailles sur une carte interactive en moins de 5 secondes après application des filtres
- **SC-002**: Le système affiche le top 10 des athlètes médaillés avec mise à jour en moins de 2 secondes lors d'un changement de filtre
- **SC-003**: Les utilisateurs peuvent comparer deux nations et voir leurs courbes superposées en moins de 3 secondes
- **SC-004**: L'export CSV génère un fichier téléchargeable contenant les données filtrées en moins de 2 secondes pour un dataset de 10 000 lignes
- **SC-005**: 90% des utilisateurs réussissent à naviguer entre les onglets sans confusion lors de tests d'utilisation
- **SC-006**: La performance de chargement initial reste sous 3 secondes malgré l'ajout de nouvelles fonctionnalités (respect du principe de caching)
- **SC-007**: Tous les graphiques et visualisations respectent le thème couleur établi (0 régression visuelle)
- **SC-008**: Le système gère correctement 100% des cas limites identifiés (filtres vides, pays identiques, etc.) sans crash

## Assumptions *(optional)*

- Le dataset olympique contient des codes pays standardisés (NOC) utilisables pour la cartographie Plotly
- Les codes NOC historiques (ex: URSS, TCH) ne nécessitent pas de fusion avec leurs équivalents modernes (RUS, CZE) - ils sont traités comme des entités distinctes
- Plotly Express supporte nativement les cartes choroplèthes avec les codes ISO/NOC pour l'affichage géographique
- Les performances de `@st.cache_data` sont suffisantes pour maintenir les temps de réponse cibles même avec les nouvelles agrégations
- L'utilisateur dispose d'une connexion permettant le chargement de la bibliothèque cartographique Plotly (pas de mode 100% offline pour les tuiles de carte)

## Clarifications

### Session 2025-12-16

- Q: For the choropleth map, how should countries with zero medals be displayed? → A: Display with a distinct neutral color (light gray) with tooltip showing "0 médailles"
- Q: For the "Top Athlètes" section, how should athletes with the same total medal count be ranked? → A: Sort by Gold medals first, then Silver, then Bronze (Olympic tiebreaker standard)
- Q: For the CSV export filename, what naming convention should be used? → A: olympics_filtered_YYYY-MM-DD_HHMMSS.csv with timestamp
- Q: In the "Comparateur" tab, should the comparison graph show total medals per year or separate lines for Gold/Silver/Bronze? → A: Single line per country showing total medals per year (2 lines total)
- Q: Should the "Top Athlètes" section be displayed as a styled table or as individual athlete cards? → A: Styled table with columns (Rank, Name, Country, Total, Gold, Silver, Bronze)

## Out of Scope *(optional)*

- Fusion automatique des codes pays historiques (URSS, GDR, etc.) avec leurs équivalents modernes
- Comparaison simultanée de plus de 2 pays (limité à 2 pour la simplicité)
- Export en formats autres que CSV (JSON, Excel, etc.)
- Animations temporelles sur la carte (play button montrant l'évolution année par année)
- Intégration de données post-2004 (le dataset s'arrête en 2004)
- Authentification utilisateur ou sauvegarde de préférences de filtres
- Mode sombre/clair interchangeable (le thème est fixé dans config.toml)

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - [Brief Title] (Priority: P1)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently - e.g., "Can be fully tested by [specific action] and delivers [specific value]"]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 2 - [Brief Title] (Priority: P2)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 3 - [Brief Title] (Priority: P3)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.
-->

- What happens when [boundary condition]?
- How does system handle [error scenario]?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST [specific capability, e.g., "allow users to create accounts"]
- **FR-002**: System MUST [specific capability, e.g., "validate email addresses"]  
- **FR-003**: Users MUST be able to [key interaction, e.g., "reset their password"]
- **FR-004**: System MUST [data requirement, e.g., "persist user preferences"]
- **FR-005**: System MUST [behavior, e.g., "log all security events"]

*Example of marking unclear requirements:*

- **FR-006**: System MUST authenticate users via [NEEDS CLARIFICATION: auth method not specified - email/password, SSO, OAuth?]
- **FR-007**: System MUST retain user data for [NEEDS CLARIFICATION: retention period not specified]

### Key Entities *(include if feature involves data)*

- **[Entity 1]**: [What it represents, key attributes without implementation]
- **[Entity 2]**: [What it represents, relationships to other entities]

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: [Measurable metric, e.g., "Users can complete account creation in under 2 minutes"]
- **SC-002**: [Measurable metric, e.g., "System handles 1000 concurrent users without degradation"]
- **SC-003**: [User satisfaction metric, e.g., "90% of users successfully complete primary task on first attempt"]
- **SC-004**: [Business metric, e.g., "Reduce support tickets related to [X] by 50%"]
