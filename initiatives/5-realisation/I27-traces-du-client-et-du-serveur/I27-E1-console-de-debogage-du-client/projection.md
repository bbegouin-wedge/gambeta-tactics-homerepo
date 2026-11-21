---
epic: I27-E1
status: a_relire
---

# I27-E1 — Projection

## Composants

- **client** (`I27-E1-CL`) : fonction de trace commune, recopie dans la sortie de Godot,
  option `--traces`, journal tenu dès le démarrage, console de débogage ouverte par
  `lll`. Responsabilité : « de manière générale c'est le composant d'affichage de ce qui
  se présente au joueur » (ici, au développeur qui joue). Scénarios S1 à S6 ; besoins B1 à
  B7, B16.
- **backend** : rien.
- **hors dépôt** : `make run-client TRACES=1` (I27-B7) touche le `Makefile` de la racine
  `03-gamebeta_tactics`, qui n'appartient à aucun composant ni au home repo. Fait à la
  main, avec la réalisation du client.
- **home repo** : rien. Les scénarios d'E1 sont prouvés par les tests du client ; le
  scénario de bout en bout s'étend avec I27-E2.

Aucune responsabilité nouvelle : pas d'ADR.

## Contrats

`contracts/canal-joueur.md` : **inchangé** pour cet epic. Les traces du client ne passent
pas sur le canal.

## Couverture

| Besoin | Porté par |
|---|---|
| B1 à B6 | CL |
| B7 | hors dépôt (`Makefile` racine), avec CL |
| B16 | CL |

| Scénario | Porté par |
|---|---|
| S1 à S4, S6 | CL |
| S5 | `Makefile` racine |

## Relectures

- **client** : faite et réalisée le 2026-11-21, branche `I27-E1-CL` de
  `gambeta_tactics_client` (commit `a9595b7`). Ajouts validés par l'humain : délai de
  500 ms pour les trois `L`, texte de la console en 18 points. `Makefile` racine :
  `TRACES=1` fait.
