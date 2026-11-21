---
epic: I26-E1
status: a_relire
---

# I26-E1 — Projection

## Composants

- **backend** (`I26-E1-BE`) : la route `/ws`, la place d'attente dans le méta, le port
  d'appariement et la salle de match dans le BC jeu, le branchement dans
  `gambeta_server`. Responsabilités de `system/components.yaml` : « mettre les joueurs en
  file d'attente et les apparier par cote » (ici sans cote, une seule place) ;
  « authentifier les joueurs, tenir leurs sessions et les router vers leur match » (ici
  sans authentification : le joueur est sa connexion) ; « pousser les événements […] sur
  le canal de chaque joueur ». Scénarios S1, S2, S4 (côté serveur), S5 ; besoins B2 à B4,
  B6, B15 à B17, B19.
- **client** (`I26-E1-CL`) : le lien vers le serveur, l'overlay de messages (I26-M1), le
  parcours accueil → attente → arène, le mode automatique du scénario. Responsabilités :
  « présenter les saisies qui lui sont demandées et remonter ses décisions » ; « de
  manière générale c'est le composant d'affichage de ce qui se présente au joueur ».
  Scénarios S1 à S4, S5 (côté client) ; besoins B1, B5, B11, B14, B18, B20.
- **home repo** (actions H1, H2 ci-dessous) : le contrat, la relation, l'étape de
  scénarios de `ci/integrate` et les portes du client. Scénarios S5, S6 ; besoins B16, B21.

Aucune responsabilité nouvelle : pas d'ADR.

### Décision d'architecture appliquée (backend)

Le schéma directeur du backend (`docs/architecture.md`) est respecté : la place
d'attente est un agrégat du BC méta (`gambeta_meta`), qui ignore le BC jeu. Le BC jeu
(`gambeta_engine`) reçoit `rejoindre_match` sur `/ws` et le transmet par un port
`Appariement` ; `gambeta_server` branche ce port sur le cas d'usage du méta, puis demande
au BC jeu d'ouvrir une salle de match pour la paire formée. Le match d'I26 ne lance pas
encore l'automate (`gambeta_rules` est vide) : la salle tient les deux connexions ; la
mise en place du match y branchera l'automate.

### Décision d'architecture appliquée (client)

Le client a désormais un schéma directeur, `docs/architecture.md` (grilling
d'architecture du 2026-11-21) : hexagone avec un port `ServerPort` qui transporte des
messages typés, des adaptateurs choisis au démarrage par l'autoload `App`
(`WebSocketServer` ; `FakeServer` et ses scénarios, `--server=fake:<scénario>`, pour
jouer le client sans serveur), `Session` (intentions) et `SessionStore` (état de
session), et un `Parcours` qui décide des écrans. Le « lien `ServerLink` dans
`scripts/net/` » cité par `I26-E1-CL` était un exemple : il est réalisé par ce port et
ses adaptateurs. `make arch` du client fait respecter les frontières.

## Contrats

### `contracts/canal-joueur.md` — nouveau, écrit à la main (action H1)

Porté par la relation `client-plays-on-backend` (client → backend, `consumes`), qui passe
de `planned` à `formal`, `contract: canal-joueur.md`. Compatible : aucun composant ne
parle encore sur ce canal. À livrer **en premier** : le backend et le client
l'implémentent en parallèle.

Contenu à écrire :

- **Transport** : WebSocket, route `/ws` du backend, trames texte, une trame = un
  message JSON (I26-B15).
- **Enveloppes** (celles de `gambeta_engine/src/io/web/protocol.rs`) :
  - client → serveur : `{"command_id": <entier ≥ 1>, "payload": <message>}` ; le client
    numérote ses messages à partir de 1 sur chaque connexion ;
  - serveur → client : `{"seq": <entier ≥ 1>, "payload": <message>}` ; `seq` part de 1
    et augmente de 1 à chaque message, par connexion.
- **Messages** (`payload`), distingués par leur champ `type` (I26-B17) :

  | Sens | `type` | Champs | Sens métier |
  |---|---|---|---|
  | client → serveur | `rejoindre_match` | — | le joueur demande un adversaire |
  | serveur → client | `en_attente` | — | le joueur occupe la place d'attente |
  | serveur → client | `match_trouve` | `joueur`: `1` ou `2` | la paire est formée ; numéro du joueur |
  | serveur → client | `adversaire_deconnecte` | — | le match est fini ; le serveur ferme ensuite la connexion |
  | serveur → client | `erreur` | `code`: chaîne, `message`: chaîne lisible | une demande est refusée ; l'état du joueur ne change pas |

- **Codes d'erreur** : `message_illisible` (trame qui n'est pas une enveloppe valide, ou
  `type` inconnu) ; `demande_en_double` (second `rejoindre_match` sur une connexion qui
  attend ou joue).
- **Identité** : le joueur est sa connexion ; aucun nom, compte ni jeton (I26-B6).
  Fermer la connexion vaut départ (« Annuler », coupure) : pas de message de départ.
- **Séquence nominale** : A `rejoindre_match` → A `en_attente` ; B `rejoindre_match` →
  A `match_trouve {joueur: 1}` et B `match_trouve {joueur: 2}`.
- **Reconnexion** : non prise en charge (I26-B13) ; `seq` et `command_id` la
  prépareront.

Avec H1 : `contracts/README.md` dit que le canal du joueur est écrit à la main, en
Markdown ; `CLAUDE.md` (règle « Contrats ») ne renvoie plus à l'ancienne I1.

### Autres relations

- `client-shows-card-texts`, `client-imports-duelyst-assets` : non concernées.

## Actions du home repo

- **H1 — Contrat** : écrire `contracts/canal-joueur.md` (ci-dessus), passer la relation en
  `formal`, mettre à jour `contracts/README.md` et `CLAUDE.md`. `make check` passe.
  Débloque `I26-E1-BE` et `I26-E1-CL`. **Fait le 2026-11-21.**
- **H2 — Scénario de bout en bout** (S6) : ajouter à `ci/integrate` une étape
  « scénarios », après les portes, qui joue chaque scénario de `ci/scenarios/` contre le
  workspace monté. Premier scénario `ci/scenarios/deux-joueurs-se-retrouvent` : il
  démarre le serveur du workspace sur un port libre (`GAMBETA_ADDR`), attend `/health`,
  lance deux clients Godot `--headless` en mode automatique (`I26-E1-CL`, point 5) à
  1 s d'écart, et vérifie que leurs rapports disent `1` et `2`. Déclarer aussi les portes
  du client dans `system/components.yaml` (`install: make install`, `test: make test`).
  Dépend de `I26-E1-BE` et `I26-E1-CL` livrés.
- **Racine** (hors dépôts) : `make run-client SERVER=…` transmet `--server=…` au client
  (I26-B18, S4). À faire avec `I26-E1-CL`.

## Couverture

| Besoin | Porté par |
|---|---|
| B1 | CL |
| B2, B3, B4 | BE (serveur), CL (affichage de B3) |
| B5 | CL |
| B6 | BE, contrat |
| B11 | CL |
| B14 | CL |
| B15, B17 | contrat (H1), BE, CL |
| B16 | H1 |
| B18 | CL, racine |
| B19 | BE |
| B20 | CL |
| B21 | H2 |

| Scénario | Porté par |
|---|---|
| S1 | BE + CL, prouvé par H2 (numéros) et les tests GUT (overlays) |
| S2 | BE (tests d'intégration) |
| S3 | CL |
| S4 | CL, racine |
| S5 | H1, BE, CL |
| S6 | H2 |

## Relectures

- **backend** : faite et réalisée le 2026-11-21, branche `I26-E2-BE` de `gambeta_server` (commit `3f6a6ba`). Écart : la porte `test-quality` de l’usine n’a pas tourné (usine en pause) ; la forme `given_` / `when_` / `then_` est suivie à la main.
- **client** : faite et réalisée le 2026-11-21, branche `I26-E1-CL` de `gambeta_tactics_client` (commit `4063ea8`). Vérifié à la main : deux clients `--headless` en mode automatique contre le serveur de `I26-E2-BE` écrivent `{"joueur":1}` et `{"joueur":2}` ; un serveur injoignable fait sortir avec 1.
