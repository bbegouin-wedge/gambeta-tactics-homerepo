---
epic: I26-E2
status: a_relire
---

# I26-E2 — Projection

## Composants

- **backend** (`I26-E2-BE`) : libérer la place d'attente quand la connexion qui l'occupe se
  coupe ; mettre fin au match quand l'un des deux part (`adversaire_deconnecte`, puis
  fermeture) ; refuser un second `rejoindre_match`. Responsabilités : « gérer les
  déconnexions et reconnexions des joueurs en cours de match » (ici, déconnexion seule) ;
  « mettre les joueurs en file d'attente […] ». Scénarios S1, S2, S3, S5, S6 (côté
  serveur) ; besoins B8, B9, B12, B13, B19.
- **client** (`I26-E2-CL`) : « Annuler », l'overlay « Adversaire déconnecté » avec son
  compte à rebours et le retour à l'accueil ; un lien qui peut rejoindre de nouveau après
  une fin de match. Responsabilités : « présenter les saisies qui lui sont demandées et
  remonter ses décisions » ; « composant d'affichage de ce qui se présente au joueur ».
  Scénarios S1, S3, S4, S6 (côté client) ; besoins B7, B10, B13, B20.
- **home repo** : rien. Le scénario de bout en bout d'I26-E1 suffit (I26-B21) ; les
  scénarios d'E2 sont prouvés par les tests de chaque composant.

Aucune responsabilité nouvelle : pas d'ADR.

## Contrats

`contracts/canal-joueur.md` : **inchangé**. Il décrit depuis I26-E1 (action H1)
`adversaire_deconnecte`, le code `demande_en_double` et la règle « fermer la connexion
vaut départ ». Cet epic les fait exister des deux côtés.

## Couverture

| Besoin | Porté par |
|---|---|
| B7 | CL (Annuler ferme la connexion), BE (la place se libère : B8) |
| B8 | BE |
| B9 | BE |
| B10 | CL |
| B12 | BE |
| B13 | BE (une nouvelle connexion est un nouveau joueur), CL (le lien repart de zéro) |
| B19 | BE |
| B20 | CL |

| Scénario | Porté par |
|---|---|
| S1 | CL (Annuler) + BE (place libérée) |
| S2 | BE |
| S3 | BE (`adversaire_deconnecte`) + CL (overlay, retour, nouvelle demande) |
| S4 | CL |
| S5 | BE |
| S6 | BE + CL |

## Relectures

- **backend** : faite et réalisée le 2026-11-21, branche `I26-E2-BE` de `gambeta_server` (commit `56844e3`).
- **client** : faite et réalisée le 2026-11-21, branche `I26-E2-CL` de `gambeta_tactics_client` (commit `f91b9ab`). Écart : le point 4 (mode automatique et `adversaire_deconnecte`) est sans objet, le mode automatique quittant dès `match_trouve` (I26-E1-CL) ; il n'a pas de test.
