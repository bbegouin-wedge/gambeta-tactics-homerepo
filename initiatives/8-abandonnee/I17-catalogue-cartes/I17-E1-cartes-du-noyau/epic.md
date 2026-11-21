---
id: I17-E1
parent: I17
needs: [I17-B1, I17-B2, I17-B3, I17-B4]
screens: [I17-M1]
depends_on: []
---
# I17-E1 — Les 33 cartes du noyau, définies une fois et rendues par un même composant

À la fin de cet epic, chaque carte du noyau (5 génériques, 19 de rôle, 5 propres, 4
exemples de combos) existe une seule fois dans le dictionnaire de cartes du client
(`data/cards.json`), et le joueur — ici le game designer qui valide — la voit rendue par
un composant unique à parties variables : cadre de sa famille (ordres, sorts, combos),
gemme de son porteur, icône, nom, type et porteur (Générique / Rôle / Propre), pastilles
chiffrées, motif des cases, texte. Les valeurs communes (types, familles, porteurs,
motifs, couleurs) sont définies une fois dans le dictionnaire et référencées par les
cartes. La planche I17-M1 montre toutes les cartes, sans filtre ni légende.

## Effet sur l'existant

`data/cards.json` existe déjà dans le client : d'après la relation
`client-shows-card-texts` (`system/relations.yaml`), il recopie à la main les textes des
cartes **et les fiches d'unités** tirées des docs de game design (`product/`), pour
l'affichage, notamment l'écran de match (qui affiche unités et cartes, d'après
`system/components.yaml`). La refonte en dictionnaire ne retire rien de cet existant :

- **les fiches d'unités sont conservées**, avec le même contenu, et restent lisibles par
  ceux qui les lisent aujourd'hui. Les garder dans `data/cards.json` ou les déplacer
  dans un fichier voisin est un choix de la projection sur le client ; ce qui compte ici,
  c'est qu'aucune donnée d'unité ne soit perdue ni modifiée ;
- **chaque écran du client qui lit aujourd'hui `data/cards.json`** (cartes ou unités)
  continue d'afficher la même chose après la refonte : il passe par le nouveau
  dictionnaire (valeurs communes résolues) ou est adapté à sa structure, sans régression
  visible.

À vérifier dans le code du client, à la projection : qui lit `data/cards.json`
aujourd'hui (scènes, scripts, autoloads), avec quelle structure, et la liste exacte des
fiches d'unités qu'il contient.

**Mise à jour de l'état décrit du système** : la note de la relation
`client-shows-card-texts` dans `system/relations.yaml` est réécrite à la livraison pour
décrire `data/cards.json` tel qu'il est devenu — un dictionnaire structuré (cartes du
noyau définies une fois, valeurs communes référencées, rendu par `CardCatalog` /
`CardView`), qui porte toujours les fiches d'unités ou dit où elles sont allées. Le
statut reste `informal` et la cible reste le backend : copie d'affichage, à remplacer par
ce que le serveur publiera.

N'en fait pas partie : filtrer la planche, sa légende (I17-E2) ; l'usage des cartes en
match (main du joueur, jeu d'une carte) ; la refonte des fiches d'unités elles-mêmes ; la
publication du catalogue par le backend — le dictionnaire reste une copie d'affichage
côté client (relation `client-shows-card-texts`, informelle) tant que le backend ne le
publie pas.

## Scénarios de bout en bout

- **I17-E1-S1** — Étant donné le dictionnaire de cartes du client, quand on ouvre la
  planche des cartes, alors les 33 cartes du noyau y sont, chacune une seule fois :
  5 génériques, 19 de rôle, 5 propres et 4 combos. (I17-B1, I17-B4)
- **I17-E1-S2** — Étant donné une carte d'ordre, un sort et un combo affichés sur la
  planche, quand on les compare, alors chacun porte le cadre de sa famille, la gemme et
  la marque de son porteur, son icône, son nom, son type, ses pastilles chiffrées, son
  motif des cases et son texte, conformes à sa définition. (I17-B3)
- **I17-E1-S3** — Étant donné une valeur commune du dictionnaire (par exemple la couleur
  d'une famille ou le libellé d'un porteur), quand on la modifie une fois puis qu'on
  rouvre la planche, alors toutes les cartes qui la référencent l'affichent changée, sans
  qu'aucune définition de carte n'ait été touchée. (I17-B2, I17-B3)
- **I17-E1-S4** — Étant donné les écrans du client qui lisaient `data/cards.json` avant
  la refonte (dont l'écran de match) et les fiches d'unités qu'il contenait, quand on
  ouvre ces écrans après la refonte, alors ils s'affichent sans erreur et montrent les
  mêmes unités, avec les mêmes fiches, et les mêmes textes de cartes qu'avant. (I17-B1,
  I17-B2)
- **I17-E1-S5** — Étant donné l'epic livré, quand on lit la relation
  `client-shows-card-texts` dans `system/relations.yaml`, alors sa note décrit
  `data/cards.json` comme un dictionnaire structuré (valeurs communes référencées, rendu
  par `CardCatalog` / `CardView`) et dit où sont les fiches d'unités, son statut est
  toujours `informal` et sa cible toujours le backend. (I17-B1, I17-B2)
