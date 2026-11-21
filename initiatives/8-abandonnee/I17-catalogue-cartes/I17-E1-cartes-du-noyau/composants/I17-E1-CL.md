---
id: I17-E1-CL
parent: I17-E1
depot: client
needs: [I17-B1, I17-B2, I17-B3, I17-B4]
scenarios: [I17-E1-S1, I17-E1-S2, I17-E1-S3, I17-E1-S4, I17-E1-S5]
contracts: []
depends_on: []
verdict: a_faire
kind: realisation
---
# I17-E1-CL — Un composant de carte : on lui donne l'identifiant, il va chercher le reste dans le dictionnaire

Le cadrage de l'humain (décision Q5, `questions.md`) : à la fin de cet epic, le client a
**un composant Godot de carte** à qui l'on donne **l'identifiant d'une carte**, et qui va
chercher toutes ses parties graphiques dans **un dictionnaire JSON** (`data/cards.json`).
Les définitions sont centralisées là, et nulle part ailleurs.

Ce que le client livre :

- **le dictionnaire** `data/cards.json` : les 33 cartes du noyau (5 génériques, 19 de rôle,
  5 propres, 4 combos), chacune définie une seule fois ; les valeurs communes (familles et
  leur cadre, types et leur couleur, porteurs et leur gemme, stats, motifs) définies une
  fois et référencées par les cartes ;
- **le composant de carte** (`CardView`, avec `CardCatalog` pour lire le dictionnaire) :
  on lui passe un identifiant de carte, il dessine cadre de famille, gemme du porteur,
  icône, nom, ligne « type · porteur », pastilles chiffrées, motif des cases et texte.
  Aujourd'hui, `CardView.make()` prend une carte déjà résolue par `CardCatalog` ; il doit
  aussi s'utiliser **directement avec un identifiant** (par exemple
  `CardView.make_by_id(id)` ou une propriété `card_id`, au choix du client), le composant
  faisant lui-même la résolution dans le dictionnaire. L'entrée par identifiant accepte
  **un catalogue fourni en option** (décision Q7) : sans rien fournir, le composant
  utilise le catalogue du jeu (`data/cards.json`), lu une seule fois au premier besoin et
  partagé par toutes les cartes ; un test peut lui passer un catalogue préparé. Rien ne
  change pour le joueur ;
- **la légende des motifs suit le catalogue utilisé** (relecture du client) : aujourd'hui
  elle est rangée dans une variable statique de `CardView` (`pattern_colors`) que seul
  `load_default` remplit. Après l'epic, une carte créée par identifiant dessine son motif
  avec la légende du catalogue dans lequel elle a été résolue : le catalogue du jeu chargé
  au premier besoin apporte sa légende, même si personne n'a appelé `load_default`
  avant ; un catalogue préparé pour un test ne change pas la légende des autres cartes.
  Comment la ranger (dans le catalogue, ou fixée une seule fois) est au choix du client ;
- **la planche** I17-M1 (`scenes/cards/card_gallery.tscn`) qui montre les 33 cartes par ce
  composant (ses filtres et sa légende relèvent d'I17-E2) ;
- **les fiches d'unités** conservées, contenu identique, et les écrans qui lisaient
  `data/cards.json` (dont l'écran de match) qui s'affichent comme avant.

## Preuve attendue

Des tests GUT headless, courts, un par scénario :

- **S1** : le dictionnaire contient 33 cartes, sans doublon ; la planche en montre 33.
  Les combos se comptent par famille `combo`, les autres par porteur. **L'absence de
  doublon se prouve sur le texte brut du fichier** (relecture du client) : une clé en
  double dans un objet JSON est écrasée en silence au chargement, donc le test relève les
  identifiants de la section `cards` dans le texte de `data/cards.json` (et non dans le
  dictionnaire chargé), vérifie qu'il y en a 33 et qu'aucun n'apparaît deux fois.
- **S2** : on crée le composant avec l'identifiant d'une carte d'ordre, d'un sort et d'un
  combo ; ce qu'il affiche correspond à la définition résolue par `CardCatalog`. Lire les
  parties dans les nœuds enfants du composant est accepté, même si ce test devra suivre
  les changements de mise en page (décision Q4 : on avance).
- **S3** : on modifie **une** valeur commune dans un catalogue préparé pour le test (passé
  au composant par l'entrée par identifiant, décision Q7), sans toucher aux cartes, et
  toutes les cartes qui la référencent l'affichent changée. Les
  valeurs à utiliser sont celles qui se voient sur toutes leurs cartes : le **cadre d'une
  famille** (`families.<f>.frame`) ou la **gemme d'un porteur** (`tiers.<t>.gem`). L'epic
  cite « la couleur d'une famille » et « le libellé d'un porteur » à titre d'exemple : une
  famille n'a pas de couleur (la couleur est celle du type, `types.<t>.color`), et le
  libellé de porteur n'est affiché que sur les 5 génériques hors combos ; ces exemples ne
  sont donc pas ceux de la preuve (le cadre est une donnée de famille, la couleur une
  donnée de type ; `types.<t>.color` est aussi acceptable, sur les cartes de ce type).
- **S4** : l'écran de match (`scenes/mockup/mockup.tscn`) et la planche s'ouvrent sans
  erreur ; leurs unités, fiches et textes de cartes sont comparés à une référence figée en
  fixture de test. La référence est la version de `data/cards.json` d'avant la refonte :
  la relecture désigne le commit 84bb030 (parent de la refonte 7919dd9) sans avoir pu
  lancer git ; ce point reste ouvert et c'est voulu. **Première étape du ticket qui écrit
  cette preuve** : vérifier avec git que
  ce commit existe et qu'il est bien le parent de la refonte ; sinon prendre le parent
  réel de la refonte, et si aucune version d'avant la refonte n'est retrouvable, l'état
  actuel sert de référence (décision Q2). Le test nomme le commit retenu.
- **Légende des motifs** (avec S2/S3) : une carte créée par identifiant sans chargement
  préalable du catalogue a ses motifs en couleur ; créer une carte avec un catalogue
  préparé ne change pas les couleurs de motif d'une carte créée avec le catalogue du jeu.
- **S5** : le client livre, dans son rendu, une description courte de `data/cards.json`
  (dictionnaire structuré, valeurs communes référencées, rendu par `CardCatalog` /
  `CardView`, fiches d'unités dans la section `units`), tirée du champ `_doc` et des
  en-têtes des scripts. L'usine s'en sert pour réécrire la note de
  `client-shows-card-texts` dans `system/relations.yaml` à la clôture (décision Q1) ;
  aucun ticket du client n'écrit dans le home repo.

Les combos gardent la gemme des génériques (décision Q3) ; la preuve compare la gemme à la
valeur résolue, sans l'écrire en dur.

N'en fait pas partie : filtres et légende de la planche (I17-E2) ; l'usage des cartes en
match ; la refonte des fiches d'unités ; la publication du catalogue par le backend.

## Responsabilités
- afficher le match à un joueur (arène, plateau, unités, cartes, événements)
- de manière générale c'est le composant d'affichage de ce qui se présente au joueur

## Relecture du composant

Verdict : **à faire**

Ce qu'il y aura à faire :
- Créer une carte à partir de son identifiant : ajouter à CardView (le composant de carte) une entrée par identifiant, par exemple make_by_id(id, catalogue = null). Sans catalogue fourni, elle utilise le catalogue du jeu (data/cards.json), lu une seule fois au premier besoin et partagé par toutes les cartes (par exemple une fonction CardCatalog.shared()). La création à partir d'une carte déjà résolue (CardView.make) est conservée pour la planche et pour l'écran de match.
- Faire suivre la légende des motifs au catalogue utilisé : la carte résolue porte les couleurs de motif de son catalogue, ou CardView garde une référence à ce catalogue. Supprimer la variable statique partagée CardView.pattern_colors et la ligne de CardCatalog.load_default qui la remplit. CardPattern reçoit alors les couleurs de la carte elle-même. Ainsi, une carte créée par identifiant sans chargement préalable du catalogue a ses motifs en couleur, et un catalogue préparé pour un test ne change pas la légende des autres cartes.
- Permettre aux tests de préparer un catalogue : ajouter un constructeur depuis un dictionnaire ou un texte JSON (par exemple CardCatalog.from_dict), qui valide le contenu comme le fait load_default.
- Planche des cartes (scenes/cards/card_gallery.gd) : la faire passer, si possible, par l'entrée par identifiant pour les vignettes et le zoom. Ses filtres et sa légende restent tels quels (ils relèvent d'I17-E2).
- Tests GUT headless, un par scénario. S1 : relever les identifiants de la section cards dans le texte brut de data/cards.json et vérifier qu'il y en a 33, sans doublon ; vérifier la répartition 5 génériques, 19 de rôle, 5 propres, 4 combos ; vérifier que la planche instancie 33 cartes. S2 : créer par identifiant une carte d'ordre, un sort et un combo, et comparer ce qu'affichent leurs nœuds enfants (images du cadre et de la gemme, textes, pastilles, motif) à CardCatalog.resolve. S3 : dans un catalogue préparé, changer le cadre d'une famille (families.<f>.frame) ou la gemme d'un porteur (tiers.<t>.gem), puis vérifier que toutes les cartes concernées l'affichent changé. Légende des motifs : les deux vérifications décrites dans la part. S4 : ouvrir l'écran de match et la planche sans erreur, et comparer leurs unités, leurs fiches et les textes de cartes à une référence figée en fixture (data/cards.json au commit retenu, après vérification avec git).
- Livrer dans le rendu une description courte de data/cards.json pour S5 (dictionnaire structuré, valeurs communes référencées, rendu par CardCatalog / CardView, fiches d'unités dans la section units), tirée du champ _doc et des en-têtes des scripts.

Où c'est déjà fait :
- Le dictionnaire existe déjà. data/cards.json contient les sections _doc, families, types, tiers, pattern_legend, cards et units. Le test test/unit/test_card_catalog.gd vérifie qu'il compte 33 cartes et ne contient aucune référence inconnue, mais il compte sur le dictionnaire chargé : ce comptage ne prouve donc pas l'absence de doublon.
- scripts/cards/card_catalog.gd : load_default() lit le fichier à chaque appel, sans le garder en mémoire, et remplit au passage la variable statique CardView.pattern_colors (ligne 23). resolve(id) renvoie le cadre de la famille, la gemme et le libellé du porteur, le type, les pastilles, le motif et le texte. Il n'existe aucun moyen de construire un catalogue depuis un dictionnaire préparé.
- scripts/ui/card_view.gd : seule existe make(card), qui prend une carte déjà résolue. La légende des motifs est la variable statique pattern_colors (ligne 37), utilisée par _pattern (ligne 122). Une carte créée sans appel préalable à load_default dessine donc ses motifs sans couleur.
- La planche existe déjà : scenes/cards/card_gallery.gd appelle load_default, puis resolve_all, puis CardView.make pour chaque carte et pour le zoom.
- L'écran de match (scenes/mockup/mockup.gd, lignes 28 à 40) lit le dictionnaire avec load_default, resolve_all et units(), et transmet les cartes et les unités au HUD (hud.build). Il n'utilise pas CardView directement.

Objections :
- Le dictionnaire, ses 33 cartes et la planche existent déjà. Le travail porte donc sur l'entrée par identifiant, la légende des motifs propre à chaque catalogue, et les preuves S1 à S4 (aucun test ne couvre aujourd'hui CardView, la planche ou l'écran de match). Ce n'est pas une refonte des données.
- S4 : je n'ai pas pu lancer git pendant cette relecture. Je ne sais donc ni si le commit 84bb030 existe, ni s'il est le parent de la refonte 7919dd9. Le ticket qui écrit cette preuve le vérifiera en premier, comme la part le prévoit.
- S4 côté écran de match : il transmet les cartes et les unités au HUD sans passer par CardView. Le plus simple est de comparer ce que le HUD reçoit (cartes résolues et fiches d'unités) à la référence figée, plutôt que de lire des nœuds affichés.
