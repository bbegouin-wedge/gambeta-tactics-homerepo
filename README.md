# gambeta-tactics-homerepo

Le home repo du système Gambeta Tactics : ce qui relie le `backend` (serveur
de jeu) et le `client` (Godot), sans le code d'aucun d'eux.

```
system/components.yaml       composants, dépôts, codes courts, responsabilités
system/relations.yaml        dépendances déclarées, via quels contrats
manifests/current.yaml       la baseline : les SHA qui marchent ensemble
manifests/candidates/        les SHA proposés par une initiative
contracts/                   contrats entre composants (aucun encore, voir I1)
product/                     game design : la référence des grillings
initiatives/<colonne>/<id>/  le kanban des initiatives du projet
decisions/                   ADR transverses
.claude/skills/              skills de niveau système
scripts/workspace            monte workspace/ aux SHA d'un manifeste
scripts/extract-contracts    régénère les contrats depuis le code
scripts/checks/              validations croisées, dérive
ci/                          validation (PR) et intégration d'un manifeste
```

## Démarrer

Prérequis : `uv`, `git`, et les dépôts clonés à côté de celui-ci
(`../gambeta_server`, `../gambeta_tactics_client`), plus OpenDuelyst
en `../../duelyst` pour régénérer les assets du client.

```bash
make workspace     # clone chaque composant dans workspace/, au SHA de la baseline
make check         # structure + dérive
make integrate     # portes de chaque composant, contrats
```

Le flux d'une évolution et les règles : [`CLAUDE.md`](CLAUDE.md).
