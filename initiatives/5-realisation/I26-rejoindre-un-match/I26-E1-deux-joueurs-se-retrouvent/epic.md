---
id: I26-E1
parent: I26
needs: [I26-B1, I26-B2, I26-B3, I26-B4, I26-B5, I26-B6, I26-B11, I26-B14, I26-B15, I26-B16, I26-B17, I26-B18, I26-B19, I26-B20, I26-B21]
screens: [I26-M1]
depends_on: []
---
# I26-E1 — Deux joueurs se retrouvent dans le même match

À la fin de cet epic, deux joueurs qui cliquent chacun sur « Rejoindre un match » se
retrouvent dans le même match, sur l'arène : celui qui attendait est le joueur 1, l'autre
le joueur 2, et chacun le lit à l'écran. Le premier qui clique voit l'overlay « En attente
d'un adversaire… » jusqu'à l'arrivée du second. Si le serveur ne répond pas, le joueur le
voit et peut réessayer. Plusieurs paires peuvent jouer en même temps. Le canal du joueur
existe, décrit par le premier contrat du système (`contracts/canal-joueur.md`), et un
scénario de bout en bout le prouve à chaque intégration.

## Effet sur l'existant

- **Client** : « Rejoindre un match » ouvre aujourd'hui la maquette de l'arène
  (`scenes/mockup/`) directement, sans serveur. Après l'epic, le bouton contacte le
  serveur, et l'arène ne s'ouvre qu'à la réception de `match_trouve`. La composition figée
  de l'arène ne change pas ; seul s'y ajoute le repère « Joueur N ».
- **Backend** : seule la route `GET /health` existe. S'ajoutent la route `/ws`, la place
  d'attente dans le méta et la salle de match dans le BC jeu.
- **Système** : la relation `client-plays-on-backend` passe de `planned` à `formal`, avec
  son contrat. `contracts/README.md` et `CLAUDE.md` renvoient encore à l'ancienne
  initiative I1 pour fixer le protocole : ils sont mis à jour. `ci/integrate` gagne une
  étape de scénarios, et le client déclare ses portes dans `system/components.yaml`
  (`gates: {}` aujourd'hui).

N'en fait pas partie : Annuler, les coupures de connexion, l'adversaire déconnecté et la
double demande (I26-E2) ; tout état de jeu (mise en place du match, M-01 à M-07).

## Scénarios de bout en bout

- **I26-E1-S1** — Étant donné le serveur lancé et deux clients sur la page d'accueil,
  quand le joueur A clique sur « Rejoindre un match », alors il voit l'overlay « En
  attente d'un adversaire… » ; quand le joueur B clique à son tour, alors les deux clients
  ouvrent l'arène sous l'overlay « Adversaire trouvé », A avec « Vous êtes le Joueur 1 »,
  B avec « Vous êtes le Joueur 2 », et au bout de 2 s l'overlay s'efface et laisse le
  repère « Joueur 1 » chez A, « Joueur 2 » chez B. (I26-B1 à B3, B5, B14)
- **I26-E1-S2** — Étant donné le serveur lancé, quand quatre joueurs cliquent l'un après
  l'autre sur « Rejoindre un match », alors ils forment deux matchs : le premier et le
  deuxième ensemble (joueurs 1 et 2), le troisième et le quatrième ensemble (joueurs 1
  et 2). (I26-B4)
- **I26-E1-S3** — Étant donné le serveur arrêté, quand un joueur clique sur « Rejoindre
  un match », alors il voit l'overlay « Serveur injoignable » ; quand il clique sur « OK »,
  alors il est sur la page d'accueil ; quand le serveur est lancé et qu'il clique de
  nouveau, alors il voit « En attente d'un adversaire… ». (I26-B11)
- **I26-E1-S4** — Étant donné le serveur lancé sur un autre port
  (`GAMBETA_ADDR=127.0.0.1:9000 make run-server`), quand deux clients lancés par
  `make run-client SERVER=ws://127.0.0.1:9000/ws` cliquent sur « Rejoindre un match »,
  alors ils se retrouvent dans le même match. (I26-B18)
- **I26-E1-S5** — Étant donné l'epic livré, quand on compare les messages échangés en S1
  à `contracts/canal-joueur.md`, alors chacun y est décrit (enveloppe, type, champs), et
  la relation `client-plays-on-backend` est `formal` et pointe vers ce contrat. Aucun
  joueur ne porte de nom ni de jeton. (I26-B6, B15 à B17)
- **I26-E1-S6** — Étant donné un manifeste candidat qui monte le backend et le client de
  l'epic, quand on lance `ci/integrate`, alors l'étape des scénarios démarre le serveur et
  deux clients sans fenêtre, et constate que l'un a reçu le numéro 1 et l'autre le
  numéro 2. (I26-B19 à B21)
