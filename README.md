# AudioScope

**Local-first video transcription, subtitles and debate intelligence, powered by NVIDIA Nemotron 3.5 Transcribe.**

AudioScope transforme une URL YouTube en une vidéo consultable avec transcription, sous-titres synchronisés, identification des intervenants et outils d'analyse. L'objectif est de construire une bibliothèque audiovisuelle intelligente, particulièrement adaptée aux conférences, débats politiques, interviews, podcasts et discussions réunissant plusieurs personnes.

Le projet utilise un serveur `llama.cpp` déjà lancé sur la machine. Il ne télécharge pas et ne démarre pas le modèle lui-même.

> **Principe :** regarder, écouter, lire, rechercher et analyser les contenus vidéo depuis une seule interface web locale.

---

## Sommaire

- [1. Vision](#1-vision)
- [2. Fonctionnalités de la première version](#2-fonctionnalités-de-la-première-version)
- [3. Expérience utilisateur](#3-expérience-utilisateur)
- [4. Architecture technique](#4-architecture-technique)
- [5. Intégration de Nemotron](#5-intégration-de-nemotron)
- [6. Sous-titres et synchronisation](#6-sous-titres-et-synchronisation)
- [7. Gestion des débats et des intervenants](#7-gestion-des-débats-et-des-intervenants)
- [8. Roadmap](#8-roadmap)
- [9. Structure du projet](#9-structure-du-projet)
- [10. Installation et configuration](#10-installation-et-configuration)
- [11. Format des données](#11-format-des-données)
- [12. Qualité et fiabilité](#12-qualité-et-fiabilité)
- [13. Critères de validation du MVP](#13-critères-de-validation-du-mvp)
- [14. Licence et respect des sources](#14-licence-et-respect-des-sources)

---

## 1. Vision

Les vidéos longues contiennent une quantité considérable d'informations difficiles à exploiter : conférences de trois heures, débats où plusieurs personnes se coupent la parole, interviews, tables rondes, émissions d'actualité ou discussions techniques.

AudioScope doit permettre de transformer ces contenus en documents audiovisuels navigables et interrogeables.

L'utilisateur colle une URL YouTube. AudioScope récupère les médias, transcrit l'audio à l'aide de Nemotron, prépare les sous-titres, puis ouvre un lecteur vidéo enrichi.

À terme, chaque vidéo devient une source de connaissances que l'on peut explorer sans devoir la regarder intégralement.

### Objectifs fondamentaux

- **Vidéo locale :** conserver une copie locale du média lorsque son téléchargement est autorisé.
- **Transcription fidèle :** préserver les hésitations, répétitions et formulations originales.
- **Sous-titres synchronisés :** suivre la vidéo avec des sous-titres générés automatiquement.
- **Intervenants :** distinguer les voix et suivre les prises de parole.
- **Traduction :** proposer une traduction française lorsque la langue originale est l'anglais.
- **Recherche :** retrouver un passage et revenir directement au moment correspondant.
- **Analyse :** identifier progressivement les thèmes, arguments, désaccords et interruptions.
- **Autonomie :** privilégier un fonctionnement local, avec un backend connecté au serveur `llama.cpp` existant.

## 2. Fonctionnalités de la première version

Le MVP doit être réellement utilisable, pas seulement une démonstration de modèle.

### Importation et traitement

- Champ de saisie pour une URL YouTube.
- Récupération des informations disponibles : titre, chaîne, durée, miniature et URL source.
- Téléchargement de la vidéo et de l'audio via `yt-dlp`, lorsque le téléchargement est autorisé et techniquement possible.
- Extraction ou conversion audio avec FFmpeg.
- Création d'un traitement en arrière-plan pour ne pas bloquer l'interface.
- Affichage des étapes : importation, préparation audio, transcription, génération des sous-titres et disponibilité du lecteur.
- Reprise ou relance d'un traitement interrompu, dans la mesure du possible.
- Historique persistant des vidéos importées.

### Transcription

- Utilisation du serveur Nemotron 3.5 Transcribe déjà démarré avec `llama.cpp`.
- Transcription dans la langue originale.
- Conservation des hésitations, répétitions et phrases inachevées lorsque le modèle les restitue.
- Identification des intervenants lorsque le modèle et le runtime fournissent ces informations.
- Traduction française des contenus en anglais, conservée séparément de l'original.
- Horodatages par mot si la sortie du runtime les prend en charge.
- Sinon, horodatages par segment et génération de sous-titres à partir des segments disponibles.
- Export des résultats en JSON, TXT, SRT et WebVTT lorsque les données nécessaires sont disponibles.

**Important :** l'application doit distinguer les capacités théoriques du modèle de celles effectivement exposées par la version de `llama.cpp` utilisée. Elle ne doit jamais inventer des horodatages ou des informations sur les intervenants pour remplir les champs manquants.

### Lecteur vidéo intégré

Le lecteur est une fonctionnalité centrale du MVP.

- Lecture et pause.
- Barre de progression et navigation dans la vidéo.
- Réglage du volume et de la vitesse de lecture.
- Affichage des sous-titres générés.
- Activation et désactivation des sous-titres.
- Choix entre les sous-titres originaux et la traduction française, si disponible.
- Synchronisation entre la vidéo et la transcription.
- Affichage du nom ou de l'identifiant de l'intervenant dans les sous-titres lorsque l'information est disponible.
- Navigation vers un passage en cliquant sur une ligne de transcription.
- Mise en évidence du segment actuellement prononcé lorsque la synchronisation le permet.

Le lecteur utilise le lecteur vidéo HTML5 du navigateur et des fichiers de sous-titres WebVTT. Les médias doivent être dans un format compatible avec le navigateur ; une conversion optionnelle pourra être proposée lorsque cela est nécessaire.

### Sous-titres incrustés dans la vidéo

En complément des sous-titres activables, AudioScope doit permettre de produire une nouvelle vidéo avec les sous-titres définitivement incrustés dans l'image.

- Choix de la langue des sous-titres.
- Possibilité d'inclure les noms des intervenants.
- Style lisible : taille, contour, position et contraste.
- Génération d'un fichier vidéo exportable via FFmpeg.
- Conservation de la vidéo originale.
- Possibilité de récupérer le fichier sous-titré et les fichiers SRT/VTT séparément.

L'incrustation est un traitement distinct : elle ne doit pas bloquer le lecteur ni la navigation dans la bibliothèque. Elle peut être ajoutée après la génération des sous-titres, sans relancer la transcription.

---

## 3. Expérience utilisateur

L'interface doit être moderne, sobre, rapide et adaptée aux vidéos longues. L'objectif est de privilégier l'information utile plutôt que de multiplier les panneaux décoratifs.

### Écran A — Bibliothèque

La page d'accueil affiche les vidéos importées sous forme de liste ou de grille.

Chaque élément présente :

- La miniature.
- Le titre et la chaîne.
- La durée.
- La date d'importation.
- L'état du traitement.
- La disponibilité de la transcription et de la traduction.
- Un accès direct au lecteur.

L'utilisateur peut rechercher une vidéo, filtrer les traitements en cours et supprimer les médias locaux dont il n'a plus besoin.

### Écran B — Importation

Une page ou une fenêtre permet de coller une URL YouTube.

L'utilisateur peut sélectionner les options disponibles :

- Télécharger la vidéo ou ne conserver que l'audio.
- Générer les sous-titres.
- Traduire en français si l'audio est en anglais.
- Conserver les horodatages détaillés si le runtime les fournit.

Les options avancées ne doivent pas compliquer le parcours par défaut.

Une fois l'importation lancée, un panneau affiche les étapes et les éventuelles erreurs. Une URL inaccessible ou une vidéo protégée ne doit pas provoquer un plantage de l'application.

### Écran C — Lecteur et transcription

<text>Disposition cible : lecteur vidéo à gauche, transcription consultable à droite, avec adaptation aux petits écrans.</text>

```text
┌─────────────────────────────────────────────────────────────┐
│ AudioScope     Bibliothèque     Recherche     Paramètres    │
├──────────────────────────────────────┬──────────────────────┤
│                                      │ TRANSCRIPTION        │
│                                      │                      │
│             LECTEUR VIDÉO            │ [00:12] Speaker 1    │
│                                      │ Bonjour à tous...    │
│       Sous-titres incrustés          │                      │
│                                      │ [00:18] Speaker 2    │
│                                      │ Je voudrais répondre │
│                                      │                      │
├──────────────────────────────────────┤ [00:24] Speaker 1    │
│ ▶  ━━━━━━━━━━━━━━━━  12:35           │ ...                  │
│ Sous-titres : FR ▼   Vitesse : 1x    │                      │
├──────────────────────────────────────┴──────────────────────┤
│ Rechercher dans cette vidéo...                              │
└─────────────────────────────────────────────────────────────┘
```

Cette représentation décrit l'interface souhaitée, pas une interface déjà implémentée.

Interactions principales :

- Cliquer sur un horodatage fait avancer le lecteur jusqu'au passage.
- La transcription suit la lecture et met en évidence le passage courant.
- Une recherche filtre les passages contenant les termes recherchés.
- Les intervenants peuvent être filtrés lorsque leur identification est disponible.
- L'utilisateur peut afficher l'original, la traduction ou les deux.
- Un bouton permet de lancer la génération d'une vidéo avec sous-titres incrustés.
- Les exports restent accessibles sans quitter le lecteur.

La synchronisation doit être précise autant que les horodatages fournis le permettent. Une précision au mot ne doit pas être simulée si seules des plages temporelles par segment sont disponibles.

### Écran D — Exports

L'utilisateur peut télécharger :

- La vidéo originale conservée localement.
- La transcription originale en TXT et JSON.
- Les sous-titres SRT et WebVTT.
- La traduction française, si disponible.
- Les données d'intervenants lorsqu'elles sont fournies.
- La vidéo avec sous-titres incrustés, une fois le rendu terminé.

---

## 4. Architecture technique

AudioScope sépare l'interface, les traitements multimédias, les données et l'inférence.

```text
                     NAVIGATEUR WEB
                           │
                           ▼
                  FRONTEND AUDIOSCOPE
              Bibliothèque / Lecteur / Recherche
                           │
                           ▼
                    API FASTAPI
                           │
                ┌──────────┼───────────┐
                ▼          ▼           ▼
             yt-dlp      FFmpeg     Gestionnaire
          Import média   Audio/vidéo  de tâches
                │          │           │
                └──────────┼───────────┘
                           ▼
                 ADAPTATEUR NEMOTRON
                           │
                           ▼
              SERVEUR LLAMA.CPP EXISTANT
                   API HTTP locale
                           │
                           ▼
                 TRANSCRIPTION STRUCTURÉE
                           │
                ┌──────────┼───────────┐
                ▼          ▼           ▼
              SQLite     SRT/VTT    JSON/TXT
                │          │
                └──────────┼───────────┐
                           ▼           ▼
                     LECTEUR WEB    EXPORT FFmpeg
                                  Sous-titres incrustés
```

### Stack proposée

| Composant | Technologie |
|---|---|
| Frontend | React + TypeScript |
| Interface | CSS moderne, responsive |
| Lecteur | HTML5 Video |
| Sous-titres | WebVTT, SRT |
| Backend | Python + FastAPI |
| Traitements longs | Tâches asynchrones persistées |
| Import vidéo | yt-dlp |
| Traitement audio/vidéo | FFmpeg |
| Base de données | SQLite |
| Recherche textuelle | SQLite FTS5 |
| Inférence | API HTTP compatible avec le serveur `llama.cpp` existant |
| Configuration | Variables d'environnement |
| Déploiement initial | Application locale |

Le frontend ne doit pas communiquer directement avec le serveur d'inférence. Toutes les requêtes passent par le backend, qui gère les tâches, la validation, les erreurs et les données persistantes.

### Principes d'architecture

- Ne jamais démarrer un second serveur de modèle automatiquement.
- Ne pas télécharger les poids du modèle.
- Permettre de configurer l'URL du serveur `llama.cpp`.
- Ne pas supposer que le modèle est accessible sur un port précis.
- Ne pas bloquer l'API pendant une transcription ou un rendu vidéo.
- Persister l'état des tâches afin de pouvoir retrouver les traitements après un redémarrage.
- Séparer le fichier vidéo original, l'audio de travail, la transcription et les fichiers dérivés.
- Permettre de reconstruire les sous-titres sans relancer l'inférence.
- Prévoir un adaptateur d'inférence isolé pour faciliter les évolutions futures.

---

## 5. Intégration de Nemotron

Le modèle ciblé est **NVIDIA Nemotron 3.5 Transcribe**, un modèle audio à poids ouverts annoncé avec environ 30 milliards de paramètres au total et environ 4 milliards de paramètres actifs.

Référence du modèle :

https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B

Le modèle est déjà lancé manuellement sur la machine de l'utilisateur avec `llama.cpp`. AudioScope doit donc se connecter au serveur existant.

### Configuration

Exemple de fichier `.env` :

```dotenv
APP_HOST=127.0.0.1
APP_PORT=8000

LLAMA_CPP_BASE_URL=http://127.0.0.1:8080/v1
LLAMA_CPP_MODEL=nemotron-transcribe

DATA_DIR=./data
DATABASE_URL=sqlite:///./data/audioscope.db

VIDEO_DOWNLOAD_ENABLED=true
MAX_VIDEO_SIZE_GB=10
```

Les valeurs sont des exemples. L'adresse, le port et l'identifiant du modèle doivent correspondre à la configuration réelle du serveur.

Le backend doit fournir une vérification de connexion permettant de distinguer :

- Serveur inaccessible.
- Serveur accessible, mais modèle non identifié.
- Requête de test réussie.
- Format de requête audio non pris en charge.
- Réponse reçue mais impossible à interpréter.

### Adaptateur d'inférence

L'intégration doit être centralisée dans un module dédié, par exemple :

```text
backend/app/services/inference/
├── base.py
├── llama_cpp.py
├── capabilities.py
└── output_parser.py
```

Responsabilités :

- Construire les requêtes compatibles avec le serveur effectivement utilisé.
- Envoyer l'audio selon le format attendu par ce runtime.
- Gérer les réponses, erreurs, délais d'attente et tentatives de reprise.
- Interpréter les sorties du modèle sans perdre les informations structurées disponibles.
- Détecter les capacités réellement utilisables.
- Fournir au reste de l'application un format de données stable.

Le fait qu'un serveur expose une API compatible avec OpenAI ne garantit pas à lui seul la prise en charge de toutes les entrées audio ou métadonnées propres au modèle. L'adaptateur doit être validé sur l'installation réelle de `llama.cpp`.

### Segmentation audio

Pour les vidéos longues, le backend doit prévoir une stratégie de segmentation configurable.

- Respecter les limites audio et de contexte du runtime.
- Conserver les offsets temporels des segments.
- Ajouter si nécessaire un chevauchement contrôlé entre segments.
- Éviter les répétitions et les pertes de mots aux frontières.
- Réassembler les résultats dans l'ordre chronologique.
- Conserver les métadonnées nécessaires à la synchronisation.

Le traitement d'un débat de deux heures ne doit pas dépendre d'une unique requête gigantesque.

---

## 6. Sous-titres et synchronisation

La synchronisation est un élément central du projet.

### Deux modes complémentaires

**Mode 1 — Sous-titres activables**

Le lecteur charge un fichier WebVTT associé à la vidéo. Les sous-titres peuvent être activés ou désactivés, et la langue peut être changée lorsque plusieurs pistes sont disponibles.

C'est le mode à implémenter en premier : il ne nécessite pas de réencoder la vidéo et permet de modifier les sous-titres indépendamment du média.

**Mode 2 — Sous-titres incrustés**

FFmpeg génère un nouveau fichier vidéo dont les sous-titres sont inscrits dans l'image. Ce rendu peut prendre du temps selon la durée de la vidéo et les performances de la machine.

L'original reste intact. Le rendu utilise un fichier de sous-titres validé et permet de configurer le style.

### Formats à prendre en charge

| Format | Utilisation |
|---|---|
| SRT | Export universel et compatibilité |
| WebVTT | Lecteur web et synchronisation |
| JSON | Données complètes, segments, intervenants et métadonnées |
| TXT | Lecture simple de la transcription |

### Précision temporelle

Le système privilégie, dans cet ordre :

1. Horodatages par mot fournis par le runtime.
2. Horodatages par segment fournis par le runtime.
3. Horodatages obtenus par un mécanisme d'alignement explicitement identifié, si celui-ci est ajouté et validé.

La durée d'une phrase ne doit pas être répartie artificiellement entre les mots puis présentée comme une précision réelle.

Lorsque la synchronisation est approximative, l'application doit le signaler. Les sous-titres peuvent être ajustés par l'utilisateur dans une future version.

### Traduction

La transcription originale et la traduction sont deux pistes distinctes.

- La piste originale conserve la langue parlée.
- La piste française contient la traduction.
- Les deux restent associées aux mêmes passages temporels lorsqu'une correspondance fiable est disponible.
- Les textes traduits ne remplacent jamais la transcription originale.

La traduction peut nécessiter une étape distincte si le runtime de transcription ne la fournit pas directement. Dans ce cas, l'architecture doit permettre d'ajouter un moteur de traduction séparé, sans coupler toute l'application à un second modèle.

---

## 7. Gestion des débats et des intervenants

La capacité à exploiter les discussions à plusieurs voix constitue l'une des orientations principales du projet.

Les débats présentent des difficultés particulières :

- Plusieurs personnes parlent simultanément.
- Une intervention peut être très courte.
- Les participants s'interrompent.
- Les noms propres et les termes techniques sont difficiles à reconnaître.
- Les changements de locuteur peuvent être ambigus.
- Une transcription linéaire peut masquer le chevauchement des voix.

### Première étape

Si les sorties du modèle le permettent, AudioScope conserve :

- L'identifiant de l'intervenant.
- Le début et la fin de chaque segment.
- Le texte prononcé.
- La langue.
- Les métadonnées de confiance lorsqu'elles sont réellement fournies.
- Les informations de chevauchement si elles sont disponibles.

L'interface permet alors de filtrer la transcription par intervenant et d'afficher les prises de parole dans l'ordre chronologique.

### Point essentiel : les interruptions

Une transcription classique représente souvent les paroles sous forme de séquence. Or, dans un débat, deux personnes peuvent parler en même temps.

AudioScope doit pouvoir évoluer vers une représentation temporelle permettant plusieurs segments simultanés. Il ne faut pas forcer artificiellement toutes les paroles sur une seule ligne chronologique si cela détruit l'information.

Si le modèle ou le runtime ne permet pas de reconstruire les chevauchements, l'application doit présenter cette limite plutôt que prétendre détecter toutes les interruptions.

### Évolutions possibles

- Timeline des prises de parole par intervenant.
- Détection des interruptions et des chevauchements, après validation.
- Temps de parole par personne.
- Recherche des questions et des réponses.
- Repérage des désaccords et des changements de sujet.
- Extraction des affirmations factuelles avec leurs citations temporelles.
- Génération d'un résumé par thème ou par participant.
- Navigation entre une affirmation et le passage vidéo qui la justifie.

Ces analyses doivent rester distinctes des données brutes de transcription. Une interprétation générée par l'IA ne doit jamais être présentée comme un fait établi par le modèle de transcription.

---

## 8. Roadmap

### v0.1 — MVP fonctionnel

Objectif : importer une vidéo, la transcrire et la regarder avec les sous-titres.

- [x] Initialiser le dépôt et la structure du projet.
- [x] Créer l'interface web.
- [x] Ajouter la bibliothèque vidéo.
- [x] Importer une URL YouTube.
- [x] Télécharger le média avec `yt-dlp`.
- [x] Extraire et préparer l'audio avec FFmpeg.
- [x] Se connecter au serveur `llama.cpp` existant.
- [x] Transcrire l'audio et conserver les métadonnées disponibles.
- [x] Générer SRT et WebVTT à partir des horodatages disponibles.
- [x] Lire la vidéo locale avec les sous-titres activables.
- [x] Synchroniser la transcription et le lecteur.
- [x] Ajouter l'export TXT, JSON, SRT et VTT.
- [x] Persister les tâches et les résultats dans SQLite.
- [x] Ajouter une page de configuration et un diagnostic du serveur d'inférence.

**Livrable :** une application locale utilisable de bout en bout.

### v0.2 — Traduction et sous-titres incrustés

- [ ] Générer une piste française lorsque l'audio est en anglais.
- [ ] Sélectionner la langue des sous-titres dans le lecteur.
- [ ] Personnaliser le style des sous-titres.
- [ ] Générer une vidéo avec sous-titres incrustés via FFmpeg.
- [ ] Afficher la progression des rendus.
- [ ] Permettre de relancer un rendu sans retranscrire l'audio.
- [ ] Ajouter la gestion des erreurs de conversion et des formats incompatibles.

**Livrable :** un outil complet pour regarder et exporter des vidéos sous-titrées.

### v0.3 — Transcription avancée des débats

- [ ] Afficher les intervenants dans la transcription.
- [ ] Filtrer les passages par intervenant.
- [ ] Améliorer la navigation temporelle.
- [ ] Afficher les métadonnées de diarisation disponibles.
- [ ] Ajouter une timeline des prises de parole.
- [ ] Préserver les segments qui se chevauchent lorsqu'ils sont fournis.
- [ ] Permettre de corriger manuellement les noms des intervenants.
- [ ] Ajouter un glossaire personnalisable pour les noms propres et les termes techniques.
- [ ] Signaler les passages incertains sans les corriger silencieusement.

**Livrable :** une interface réellement adaptée aux conférences et aux débats.

### v0.4 — Bibliothèque audiovisuelle intelligente

- [ ] Rechercher dans toutes les transcriptions.
- [ ] Utiliser SQLite FTS5 pour la recherche textuelle.
- [ ] Filtrer par vidéo, langue, date ou intervenant.
- [ ] Retrouver un passage et ouvrir directement la vidéo à cet instant.
- [ ] Ajouter des favoris et des marqueurs temporels.
- [ ] Organiser les vidéos en collections ou dossiers.
- [ ] Éviter de retranscrire un média déjà traité si ses fichiers et paramètres sont toujours valides.

**Livrable :** une bibliothèque personnelle consultable comme un moteur de recherche documentaire.

### v0.5 — Intelligence des débats

- [ ] Identifier les grands thèmes abordés.
- [ ] Regrouper les interventions par sujet.
- [ ] Repérer les questions et les réponses associées.
- [ ] Extraire les arguments avancés par chaque intervenant.
- [ ] Identifier les désaccords apparents et les réfutations.
- [ ] Repérer les affirmations factuelles à vérifier.
- [ ] Générer des résumés par thème et par intervenant.
- [ ] Associer chaque résultat à des passages horodatés de la vidéo.

Chaque analyse doit fournir des liens vers les passages sources. Le système doit distinguer ce qui a été explicitement dit de ce que l'IA en déduit.

### v0.6 — Analyse temporelle des interactions

- [ ] Détecter les interruptions à partir de données temporelles suffisantes.
- [ ] Visualiser les chevauchements de parole.
- [ ] Calculer les temps de parole avec des limites explicites.
- [ ] Explorer les changements de rythme et de sujet.
- [ ] Comparer la chronologie des interventions.
- [ ] Ajouter une interface de correction des segments et des intervenants.

Cette étape dépend des capacités réellement disponibles dans les sorties du modèle et, si nécessaire, de l'ajout de traitements audio spécialisés.

### v0.7 — Assistant de recherche vidéo

- [ ] Poser des questions sur une vidéo ou une collection.
- [ ] Retrouver les passages pertinents avant de produire une réponse.
- [ ] Citer les horodatages et les extraits à l'origine de chaque réponse.
- [ ] Comparer les positions de plusieurs intervenants.
- [ ] Construire des dossiers thématiques à partir de plusieurs vidéos.
- [ ] Exporter des notes de recherche structurées.

Exemple : « Quels arguments ont été avancés contre cette proposition, et à quels moments ? »

La réponse doit pointer vers les passages originaux, et non inventer des citations.

### v0.8 — Traitement par lots et automatisation

- [ ] Importer plusieurs URL en une fois.
- [ ] Mettre les traitements en file d'attente.
- [ ] Définir des priorités.
- [ ] Ajouter des limites de stockage et une politique de conservation.
- [ ] Reprendre les traitements interrompus.
- [ ] Proposer un mode audio uniquement pour économiser l'espace disque.
- [ ] Générer automatiquement des exports et des résumés.

### v1.0 — Système local de connaissance audiovisuelle

- [ ] Bibliothèque stable et persistante.
- [ ] Lecteur vidéo intégré fiable.
- [ ] Transcriptions et sous-titres exportables.
- [ ] Traductions et pistes multiples.
- [ ] Recherche plein texte rapide.
- [ ] Navigation par intervenant et par thème.
- [ ] Analyses sourcées par horodatages.
- [ ] Diagnostic des capacités du runtime.
- [ ] Documentation d'installation, de sauvegarde et de récupération.
- [ ] Tests automatisés des parcours principaux.

---

## 9. Structure du projet

Structure cible, à ajuster pendant l'implémentation si une meilleure organisation se justifie :

```text
audioscope/
├── README.md
├── .env.example
├── .gitignore
├── docker-compose.yml
│
├── frontend/
│   ├── package.json
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── features/
│   │   │   ├── library/
│   │   │   ├── importer/
│   │   │   ├── player/
│   │   │   ├── transcript/
│   │   │   └── subtitles/
│   │   └── services/
│   └── public/
│
├── backend/
│   ├── pyproject.toml
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── services/
│   │       ├── media/
│   │       │   ├── downloader.py
│   │       │   ├── audio.py
│   │       │   └── video.py
│   │       ├── inference/
│   │       │   ├── base.py
│   │       │   ├── llama_cpp.py
│   │       │   ├── capabilities.py
│   │       │   └── output_parser.py
│   │       ├── transcription.py
│   │       ├── subtitles.py
│   │       ├── translation.py
│   │       └── jobs.py
│   └── tests/
│
├── data/
│   ├── library/
│   ├── audio/
│   ├── subtitles/
│   ├── transcripts/
│   ├── exports/
│   ├── thumbnails/
│   └── audioscope.db
│
└── docs/
    ├── architecture.md
    └── development.md
```

Les fichiers générés, les médias téléchargés et les bases de données ne doivent pas être versionnés dans Git. Le dossier `data/` doit être ignoré par défaut, à l'exception éventuelle d'un fichier `.gitkeep`.

La structure doit rester proportionnée au MVP : pas de microservices, de Kubernetes ou d'infrastructure complexe sans nécessité démontrée.

---

## 10. Installation et configuration

### Prérequis

- Python 3.12 ou version compatible avec les dépendances retenues.
- Node.js LTS pour le frontend.
- FFmpeg accessible depuis le système.
- `yt-dlp` à jour.
- Un serveur `llama.cpp` déjà lancé avec le modèle Nemotron chargé.
- Un espace de stockage suffisant pour les vidéos et les fichiers générés.

### Étapes prévues

1. Cloner le dépôt.
2. Installer les dépendances du backend.
3. Installer les dépendances du frontend.
4. Copier `.env.example` vers `.env`.
5. Configurer l'URL du serveur `llama.cpp` existant.
6. Vérifier FFmpeg et yt-dlp.
7. Démarrer le backend et le frontend.
8. Ouvrir l'interface web locale.
9. Lancer un test de connexion à l'inférence avant le premier import.

Les commandes exactes seront documentées une fois le choix des dépendances et le squelette du projet stabilisés.

### Stockage

Le stockage doit être configurable. Les vidéos peuvent prendre beaucoup plus de place que les transcriptions, surtout si les rendus incrustés sont conservés.

Prévoir :

- Un emplacement configurable pour les médias.
- Une estimation de l'espace disponible.
- Une suppression contrôlée des médias locaux.
- La conservation des transcriptions si la vidéo est supprimée, selon le choix de l'utilisateur.
- La possibilité de nettoyer les fichiers temporaires.
- Des noms de fichiers générés par l'application plutôt que directement à partir de titres non fiables.

### Sécurité locale

L'application est conçue pour une utilisation locale. Elle ne doit pas exposer le lecteur, les fichiers ou l'API sur le réseau sans configuration explicite.

Les URL importées doivent être validées. Le backend ne doit pas accepter une URL arbitraire puis lire sans contrôle des ressources internes ou des services locaux. Les appels à `yt-dlp`, FFmpeg et aux autres programmes doivent être construits de manière sûre, sans concaténer directement des chaînes utilisateur dans une commande shell.

---

## 11. Format des données

Les données doivent être structurées pour pouvoir ajouter de nouvelles fonctionnalités sans migrer toute l'application à chaque étape.

### Exemple de transcription

```json
{
  "video_id": "local-video-id",
  "source_language": "en",
  "segments": [
    {
      "start": 12.4,
      "end": 16.8,
      "speaker_id": "speaker_1",
      "text": "I think we should examine the evidence.",
      "translation_fr": "Je pense que nous devrions examiner les preuves.",
      "timing_source": "runtime",
      "words": []
    }
  ],
  "speakers": [
    {
      "speaker_id": "speaker_1",
      "display_name": null
    }
  ]
}
```

C'est un exemple de schéma cible, pas une promesse sur la structure exacte des sorties de Nemotron. L'adaptateur doit convertir les réponses réelles vers ce format et conserver les informations utiles qui ne peuvent pas être normalisées.

### Principes de données

- Les temps sont exprimés en secondes à partir du début de la vidéo.
- Les segments sont ordonnés par temps de début.
- Des segments peuvent se chevaucher si les données sources le permettent.
- L'identifiant d'un intervenant ne constitue pas une identification réelle de la personne.
- `display_name` reste vide tant que l'utilisateur ne l'a pas renseigné ou qu'une identification fiable n'a pas été établie par un mécanisme explicite.
- `timing_source` indique l'origine de la temporalité.
- Les données brutes du modèle peuvent être conservées séparément pour le diagnostic.
- Les champs indisponibles restent absents ou vides ; ils ne sont pas complétés artificiellement.

### Entités principales

- `Video` : source, titre, durée, chemins locaux et métadonnées.
- `Job` : état, progression, erreurs et dates de traitement.
- `Transcript` : texte original, langue, segments et version du modèle.
- `Speaker` : identifiant local, nom modifiable et métadonnées disponibles.
- `SubtitleTrack` : langue, format et chemin du fichier.
- `Export` : fichier produit, options utilisées et état du rendu.

Les résultats doivent pouvoir être régénérés quand les paramètres de sous-titrage changent, sans relancer la transcription si elle reste valide.

---

## 12. Qualité et fiabilité

Le projet doit privilégier une transcription honnête et vérifiable.

### Règles impératives

1. Ne pas réécrire la transcription originale pour la rendre plus élégante.
2. Ne pas supprimer silencieusement les hésitations ou les répétitions.
3. Ne pas inventer les noms des intervenants.
4. Ne pas inventer des horodatages précis.
5. Ne pas présenter une traduction comme le texte original.
6. Ne pas prétendre détecter les chevauchements si les données ne le permettent pas.
7. Ne pas confondre un résumé généré par IA avec une transcription.
8. Ne pas perdre les offsets temporels lors de la segmentation audio.
9. Ne pas retranscrire une vidéo à chaque changement de style des sous-titres.
10. Ne pas masquer les erreurs du modèle ou les limites du runtime.

### Robustesse

- Gestion des URL invalides ou indisponibles.
- Gestion des échecs de téléchargement.
- Gestion des fichiers trop volumineux.
- Gestion des réponses incomplètes du modèle.
- Délais d'attente et reprise contrôlée des requêtes.
- Tâches persistées et erreurs consultables.
- Vérification des chemins de fichiers.
- Nettoyage des fichiers temporaires.
- Tests des conversions SRT/WebVTT.
- Tests de synchronisation du lecteur.
- Tests sur des vidéos courtes, longues et avec plusieurs intervenants.

---

## 13. Critères de validation du MVP

La version 0.1 est considérée comme fonctionnelle lorsque les scénarios suivants sont validés de bout en bout.

- [ ] L'utilisateur peut importer une URL YouTube accessible.
- [ ] Le média est téléchargé ou l'erreur est clairement expliquée.
- [ ] Le backend se connecte au serveur `llama.cpp` déjà démarré.
- [ ] L'audio est traité et la transcription est enregistrée.
- [ ] Les horodatages réellement disponibles sont conservés.
- [ ] Les fichiers de sous-titres sont générés sans inventer de précision.
- [ ] La vidéo se lit dans l'interface web locale.
- [ ] Les sous-titres peuvent être activés et désactivés.
- [ ] Cliquer sur un passage de transcription positionne le lecteur au bon endroit.
- [ ] La traduction française est proposée lorsqu'elle a été générée avec succès.
- [ ] La transcription et les sous-titres peuvent être exportés.
- [ ] Une vidéo peut être réouverte après redémarrage de l'application.
- [ ] Une tâche échouée affiche une erreur exploitable et peut être relancée.
- [ ] L'export vidéo avec sous-titres incrustés fonctionne sur un média de test, sans modifier l'original.

Les fonctionnalités avancées de diarisation, d'horodatage au mot et de détection des chevauchements doivent être validées séparément selon les sorties réellement disponibles dans le runtime.

---

## 14. Licence et respect des sources

AudioScope est conçu pour l'analyse et l'archivage personnel de contenus audiovisuels.

L'utilisateur doit respecter les droits d'auteur, les conditions de la plateforme source et les règles applicables aux contenus téléchargés. Le projet doit afficher clairement l'URL d'origine et ne doit pas contourner les restrictions d'accès ou de téléchargement.

La licence du projet, les licences des dépendances et les conditions d'utilisation du modèle doivent être documentées séparément avant une distribution publique.

---

## Conclusion

AudioScope commence par un problème concret : **transformer une URL YouTube en vidéo locale consultable avec une transcription et des sous-titres générés par Nemotron**.

Sa particularité est de ne pas s'arrêter à la transcription. Le lecteur, les sous-titres incrustés, la navigation par intervenant et la recherche dans les vidéos constituent le socle d'un outil de recherche audiovisuelle.

La priorité reste une première version fiable, qui exploite le serveur `llama.cpp` existant, gère correctement les fichiers et fournit une vraie interface web. Les fonctions d'analyse des débats viendront ensuite, en s'appuyant sur des transcriptions et des horodatages dont les limites sont clairement identifiées.
