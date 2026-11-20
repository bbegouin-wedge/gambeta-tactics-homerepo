# I17 — Grilling

### Q1 — Quelles cartes la planche couvre-t-elle ?

**Recommandation :** tout le noyau : génériques, cartes de rôle, cartes propres, combos et sorts.
**Réponse :** tout le noyau.

### Q2 — Quelles parties variables ajoute-t-on au cadre neutre validé dans la maquette ?

**Recommandation :** le motif des cases et les pastilles chiffrées.
**Réponse :** motif des cases, pastilles chiffrées, marque du porteur (Générique / Rôle / Propre), et un cadre par famille (ordres, sorts, combos).

### Q3 — Où vit la définition des cartes ?

**Recommandation :** dans le client, un fichier par carte.
**Réponse :** dans le client, sous forme d'un dictionnaire de cartes en JSON (`data/cards.json`), avec les définitions mutualisées. Le catalogue reste une copie d'affichage (relation `client-shows-card-texts`) jusqu'à ce que le backend le publie.

### Q4 — Comment trace-t-on ce travail ?

**Réponse :** une initiative du homerepo ; la planche Godot du client en est la maquette I17-M1.

## Besoins

- **I17-B1** — Chaque carte du noyau (33 : 5 génériques, 19 de rôle, 5 propres, 4 exemples de combos) est définie une fois, dans un dictionnaire JSON.
- **I17-B2** — Ce qui est commun à plusieurs cartes (type, famille, porteur, motif, couleurs) est défini une seule fois et référencé.
- **I17-B3** — Une carte se rend par un composant unique, à parties variables : cadre de sa famille, gemme de son porteur, icône, nom, type et porteur, pastilles chiffrées, motif des cases, texte.
- **I17-B4** — Une planche montre toutes les cartes, filtrables par famille et par porteur, avec la légende des pastilles et des motifs, pour validation.
