---
id: I17-E2
parent: I17
needs: [I17-B4]
screens: [I17-M1]
depends_on: [I17-E1]
---
# I17-E2 — Planche de validation : filtres et légende

À la fin de cet epic, celui qui valide les cartes peut, sur la planche I17-M1, ne garder
que les cartes d'une famille (ordres, sorts, combos) et/ou d'un porteur (Générique /
Rôle / Propre), et lire la légende des pastilles chiffrées et des motifs des cases, pour
valider le catalogue sans connaître le dictionnaire.

N'en fait pas partie : la définition et le rendu des cartes (I17-E1) ; toute recherche
ou tri au-delà des filtres par famille et par porteur ; un écran de collection pour le
joueur en jeu.

## Scénarios de bout en bout

- **I17-E2-S1** — Étant donné la planche affichant les 33 cartes, quand on filtre sur la
  famille « sorts », alors seules les cartes de sorts restent affichées ; quand on retire
  le filtre, les 33 cartes reviennent. (I17-B4)
- **I17-E2-S2** — Étant donné la planche, quand on filtre sur le porteur « Rôle » puis
  qu'on ajoute la famille « ordres », alors seules les cartes d'ordre de rôle restent
  affichées, et aucune carte générique, propre ou combo. (I17-B4)
- **I17-E2-S3** — Étant donné la planche, quand on consulte la légende, alors chaque
  pastille chiffrée et chaque motif des cases présents sur les cartes y sont expliqués,
  sans qu'aucune pastille ni aucun motif d'une carte affichée en soit absent. (I17-B4)
