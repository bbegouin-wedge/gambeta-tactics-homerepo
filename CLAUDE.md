# CLAUDE.md — home repo du système Gambeta Tactics

## Rôle du repo

Ce dépôt ne contient **aucun code de composant**. Il décrit le système formé
par plusieurs dépôts et garde ce qui n'appartient à aucun d'eux :

- **qui** compose le système et de quoi chacun répond (`system/components.yaml`) ;
- **qui dépend de qui, via quel contrat** (`system/relations.yaml`) ;
- **les contrats** entre composants (`contracts/`) ;
- **quelles versions marchent ensemble** (`manifests/current.yaml`), et celles
  qu'une initiative propose (`manifests/candidates/`) ;
- **le game design** (`product/`), la référence des grillings ;
- **les initiatives du projet** (`initiatives/`), conduites par la software
  factory, et les **décisions transverses** (`decisions/`).

Les composants, leurs dépôts voisins :

| Composant | Code | Dépôt local | Rôle | Reçoit ses epics composant dans |
|---|---|---|---|---|
| `backend` | `BE` | `../gambeta_server` | service de jeu Rust : matchs (seul détenteur de leur état), canal des joueurs, méta (ADR 0003) | `specs/` |
| `client` | `CL` | `../gambeta_tactics_client` | client Godot d'un joueur | `specs/` |
| `open-duelyst` | — | `../../duelyst` | assets CC0 lus par le client (données, non monté) | — |

Chaque composant garde son `CLAUDE.md`, ses règles et son kanban : ils
s'appliquent quand on travaille dans ce composant. Ce fichier ne régit que
le niveau système.

## Vocabulaire

Celui de `product/` : **joueur** (une personne, qui commande une équipe),
**unité**, **carte** (d'action, de rôle, propre, de combo), **ordre** (une carte
posée sur une unité), **leurre**, **match**, **manche**, **tour**, **file
d'effets**, **drapeau**, **essai**, **garde**, **point d'attente** (une saisie
attendue d'un joueur), **événement**. Les étapes de la boucle gardent leur
identifiant (`M-01`, `R-06`, `T-05`, `O-07`, `F-03`, `E-01`).

Modes : **Initiation** (une manche, 3 unités, six règles) d'abord, puis
**Escarmouche** (le noyau de `product/Game design — v0.16.md`).

## L'ordre du flux

Toute évolution du produit naît ici, même si elle ne touche qu'un composant
(`decisions/0002`). La software factory la conduit, étape par étape, et chaque
étape est validée par l'utilisateur :

1. **Grilling** — les besoins métier, le périmètre (`initiatives/2-grilling/`).
2. **Maquettes**, s'il y a de l'écran.
3. **Epics projet** — les étapes métier livrables, avec leurs scénarios de bout
   en bout vus du joueur (`initiatives/4-epics/`).
4. **Projection**, epic projet par epic projet — ses epics composant et les
   changements de contrat entre composants, relus par chaque composant
   (`initiatives/5-realisation/`). Les responsabilités de `system/components.yaml`
   sont figées : elles ne changent que par un ADR (processus d'architecture).
5. **Dans les composants** — chaque epic composant devient des tickets dans le
   kanban **du composant**, selon ses propres règles. Le home repo ne porte pas
   de tickets.
6. **Intégration et promotion, par epic projet** — manifeste candidat,
   `ci/integrate` (portes, dérive des contrats, scénarios de bout en bout),
   puis `--promote` sur validation de l'utilisateur.

## Règles

- **Validation humaine** : chaque livrable (initiative, contrat, ADR,
  manifeste, promotion) est présenté et discuté avant d'être écrit ou commité.
- **La baseline ne change que par promotion** : ne jamais éditer les SHA de
  `manifests/current.yaml` à la main.
- **Toute dépendance est déclarée** : une relation entre composants absente
  de `system/relations.yaml` n'existe pas. Un contrat dans `contracts/` est
  porté par au moins une relation.
- **Contrats** : aucun n'existe encore. Le protocole du canal d'un joueur, et
  la règle qui dit quels contrats sont générés depuis le code et lesquels sont
  écrits à la main, sont fixés par l'initiative I1 et son ADR.
- **`product/` est la référence du game design.**
- **Les composants se lisent au SHA du manifeste**, dans `workspace/`
  (`make workspace`), jamais dans leur clone de travail quand on raisonne sur
  le système. `workspace/` est jetable et ignoré par git ; on n'y commite rien.
- **Ne jamais modifier un dépôt de composant depuis ici** sans le demander :
  ses fichiers relèvent de ses propres règles.
- `make check` (structure + dérive) passe avant tout commit du home repo.
- **La software factory commite les étapes que l'utilisateur valide** : chaque
  initiative avance sur sa branche `flux/I<n>`, et chaque étape validée entre
  sur `main` par la gestion de configuration de l'usine, après `make check`.
  Ne pas déplacer à la main une initiative que l'usine conduit.
- Échanger en français, avec le vocabulaire ci-dessus.
- Hors de l'usine : ne commiter et ne pousser que sur demande ; sur `main`,
  créer une branche.

## Outils

| Commande | Effet |
|---|---|
| `make workspace [MANIFEST=…]` | monte `workspace/` aux SHA du manifeste |
| `make status` | ce qui est monté, et à quel SHA |
| `make contracts` | régénère les contrats issus du code, depuis `workspace/` |
| `make check` | validations croisées + dérive (contrats et SHA) |
| `make integrate MANIFEST=…` | intégration complète d'un manifeste |
| `uv run ci/integrate <candidat> --promote` | promotion d'un candidat |
