---
epic: I27-E2
status: a_relire
---

# I27-E2 — Projection

## Composants

- **backend** (`I27-E2-BE`) : un ULID par match, transmis dans `match_trouve` ; traces
  d'étape écrites dans le terminal au niveau `info` et envoyées aux connexions abonnées
  par `suivre_traces`. Responsabilités : « pousser les événements et les saisies attendues
  sur le canal de chaque joueur » (les traces sont poussées sur ce canal) ; « seul
  détenteur de l'état d'un match » (l'identifiant du match). Scénarios S1 à S5 (côté
  serveur) ; besoins B8, B9, B11, B12, B13, B15. **Ne dépend pas d'I27-E1** : peut se
  réaliser en parallèle.
- **client** (`I27-E2-CL`) : `suivre_traces` avec `--traces`, réception des `trace` dans
  le journal (origine `serveur`), champ `match` de `match_trouve` repris par
  `match_rejoint`, faux serveur aligné. Responsabilité : « composant d'affichage de ce
  qui se présente au joueur ». Scénarios S1, S3, S4 (côté client) ; besoins B10, B12, B13.
  **Dépend d'I27-E1-CL.**
- **home repo** : contrat (fait, ci-dessous) ; scénario `ci/scenarios/deux-joueurs-se-retrouvent`
  étendu (S5, B14), après les deux epics composant.

Aucune responsabilité nouvelle : pas d'ADR.

## Contrats

`contracts/canal-joueur.md` : **enrichi, version 1 inchangée** (ajouts compatibles :
nouveaux messages, nouveau champ). Écrit avec cette projection :
- client → serveur `suivre_traces` ;
- serveur → client `trace { niveau, quoi, message, champs? }`, section « Traces »
  avec la liste des `quoi` du serveur ;
- champ `heure` (UTC du serveur, RFC 3339 à la milliseconde) dans **toute** enveloppe
  serveur → client, à côté de `seq` : décidé à la relecture de la projection, pour que
  les enveloppes soient stables dès le début ; la trace n'a plus d'heure propre ;
- champ `match` (ULID) de `match_trouve` ;
- déroulé « avec les traces ».

Ordre de livraison : indifférent pour la compatibilité (un champ inconnu est ignoré), mais
un client récent face à un serveur d'I26 recevrait `erreur { message_illisible }` en
réponse à `suivre_traces` (type inconnu). Backend et client se livrent donc dans le même
manifeste candidat.

Pas de nouvelle relation : `client-plays-on-backend` porte déjà ce contrat.

**Nouvelle dépendance du backend** : la crate `ulid` dans `[workspace.dependencies]` du
`Cargo.toml` racine, validée par l'humain le 2026-11-21.

## Couverture

| Besoin | Porté par |
|---|---|
| B8 | BE |
| B9 | BE |
| B10 | CL |
| B11 | BE |
| B12 | BE (champ `match`, trace `apparie`), CL (`match_rejoint`) |
| B13 | home repo (contrat) ; BE et CL s'y conforment |
| B14 | home repo (scénario) |
| B15 | BE |

| Scénario | Porté par |
|---|---|
| S1 | BE (traces, ULID) + CL (abonnement, journal) |
| S2 | BE |
| S3 | BE (étanchéité, ULID partagé) + CL |
| S4 | BE (`adversaire_parti`) + CL (`adversaire_deconnecte`) |
| S5 | home repo (scénario) + BE (tests) |

## Relectures

- **backend** : faite et réalisée le 2026-11-21, branche `I27-E2-BE` de `gambeta_server`
  (commits `561f41d`, `9844b73`), par un agent, relue. Choix validés par l'humain :
  `demande_refusee` en `warn` (le contrat, contre l'epic qui disait `info` en bloc) ; traces
  construites dans l'adaptateur `io/web` (une connexion ne trace que ses étapes) ; graine
  de l'aléa de production tirée de `RandomState` mêlé à l'heure, sans `getrandom`. Non
  lancé : `make test-quality` (outil de l'usine absent).
- **client** : faite et réalisée le 2026-11-21, branche `I27-E2-CL` de
  `gambeta_tactics_client`. Ajout : le mode automatique attend la trace serveur `apparie`
  avant de quitter, sans quoi le scénario de bout en bout dépendrait d'une course.
- **home repo** : scénario `deux-joueurs-se-retrouvent` étendu (I27-E2-S5), passé contre
  les branches `I27-E2-BE` et `I27-E2-CL`.
