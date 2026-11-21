---
epic: I17-E1
status: in_progress
---

# I17-E1 — Projection

## Composants

- **client** (`I17-E1-CL`) : porte tous les besoins (I17-B1 à B4) et tous les scénarios
  (S1 à S5). Le dictionnaire `data/cards.json`, `CardCatalog`, `CardView` et la planche
  I17-M1 sont tous dans le client.
- **backend** : non touché. L'epic exclut explicitement la publication du catalogue par
  le serveur ; la relation `client-shows-card-texts` reste une copie d'affichage côté
  client, sans contrat.

Part recentrée sur le cadrage de l'humain (décision Q5) : un composant de carte Godot à qui
l'on donne l'identifiant d'une carte et qui va chercher ses parties graphiques dans le
dictionnaire `data/cards.json`. Seul changement de code demandé : `CardView` doit pouvoir se
créer directement à partir d'un identifiant (aujourd'hui il prend une carte déjà résolue).
Le reste est la preuve, en tests courts.

Objections du client traitées dans `I17-E1-CL` :
- S3 : la preuve modifie le cadre d'une famille (`families.<f>.frame`) ou la gemme d'un
  porteur (`tiers.<t>.gem`), visibles sur toutes leurs cartes ; les exemples de l'epic
  (« couleur d'une famille », « libellé d'un porteur ») ne sont pas retenus ;
- S4 : la référence est la version d'avant la refonte (84bb030 d'après la relecture,
  figée en fixture), sinon l'état actuel, avec le commit nommé ; vérifier avec git que ce
  commit existe et qu'il est le parent de la refonte est la première étape du ticket qui
  écrit la preuve (décision Q2 si ce n'est pas le cas) ;
- légende des motifs : elle suit le catalogue dans lequel la carte est résolue. Le
  catalogue du jeu, chargé au premier besoin, apporte sa légende, et un catalogue de test
  ne la change pas pour les autres cartes. La preuve est rattachée à S2/S3 ;
- S2/S3 : lire les parties dans les nœuds enfants du composant est accepté (décision Q4) ;
- S1, doublons : un identifiant en double dans l'objet JSON serait écrasé au chargement ;
  le test compte donc les identifiants de `cards` dans le texte brut de `data/cards.json` ;
- S4, commit de référence : la vérification git de 84bb030 / 7919dd9 reste la première
  étape du ticket qui écrit S4, comme prévu (pas de changement de la part).

Décision Q7 appliquée : l'entrée par identifiant de `CardView` accepte un catalogue fourni
en option ; par défaut, le catalogue du jeu, lu une fois et partagé. S3 passe un catalogue
préparé pour le test.

## Contrats

Aucun contrat n'est touché, donc aucune cible sous `contrats/`.

- `client-shows-card-texts` (client → backend, `reads`) : `contract: null`, statut
  `informal`. La refonte change la structure de `data/cards.json`, mais ce fichier est
  interne au client : le backend ne le lit pas et ne le publie pas. Seule la **note** de la
  relation dans `system/relations.yaml` est réécrite à la livraison (S5) pour décrire le
  dictionnaire structuré et l'emplacement des fiches d'unités ; statut (`informal`) et
  cible (`backend`) inchangés. Compatible : aucune partie autre que le client n'en dépend.
  Cette réécriture est faite dans le home repo par l'usine à la clôture de l'epic projet,
  à partir de la description livrée par le client (décision Q1, `questions.md`) ; aucun
  ticket composant n'écrit dans `system/relations.yaml`.
- `client-plays-on-backend` : non concernée (l'usage des cartes en match est hors epic).
