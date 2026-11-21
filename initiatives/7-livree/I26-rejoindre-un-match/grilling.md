# I26 — Grilling

## État des composants au départ

- **backend** (`gambeta_server`, tête `e2907f0`) : moteur d'automate porté
  (`gambeta_automaton`) ; `gambeta_rules` vide ; dans `gambeta_engine`, un acteur tokio
  par match (`runtime/match_actor.rs`) qui exécute le moteur, et des enveloppes
  `ServerEnvelope { seq }` / `ClientEnvelope { command_id }` au format non choisi ; route
  `/ws` à faire ; `gambeta_meta` vide. Seule route : `GET /health`, sur `0.0.0.0:8080`.
- **client** (Godot 4.7, tête `f7495ff`) : page d'accueil (`scenes/home/`) avec un bouton
  « Rejoindre un match » qui ouvre la maquette de l'écran de match (`scenes/mockup/`) sans
  appeler le serveur ; aucun code réseau.
- **Système** : la relation `client-plays-on-backend` est `planned`, sans contrat.

## Questions et réponses

### Q1 — Où s'arrête « avoir rejoint un match » ?

Le moteur tourne côté serveur, mais `gambeta_rules` est vide : aucune étape de jeu
n'existe encore (M-01 à M-07, `product/Boucle de gameplay — étapes techniques.md`).
Deux bornes possibles : (A) les deux clients sont rattachés au même match côté serveur,
chacun sait qu'il est le joueur 1 ou 2 et voit l'arène ; (B) en plus, le serveur prépare
le match (decks, mélange, pioche de 7, tirage de l'initiative) et chaque client voit sa
main. B rend I26 dépendante des premières règles écrites dans `gambeta_rules`.

**Recommandation :** A. I26 prouve la chaîne de bout en bout (client → WebSocket →
acteur de match → les deux clients) sans attendre les règles ; la mise en place du match
(M-01 à M-07) devient l'initiative suivante, qui se branche sur ce canal.
**Réponse :** A, d'accord avec la recommandation.

### Q2 — Comment deux joueurs se retrouvent-ils dans le même match ?

Q1 a tranché : I26 s'arrête quand les deux clients sont rattachés au même match côté
serveur, chacun sachant s'il est le joueur 1 ou 2. Reste à dire comment le serveur forme
la paire. La page d'accueil du client n'a qu'un bouton, « Rejoindre un match »
(`scenes/home/`). Trois façons : (A) une seule place d'attente sur le serveur : le premier
qui clique attend, le suivant le rejoint et le match est créé ; (B) un code de match : l'un
crée un match et reçoit un code, l'autre le saisit pour le rejoindre ; (C) une liste des
matchs ouverts, où l'on choisit le sien. B et C demandent des écrans et des messages en
plus (créer, saisir ou choisir) ; le vrai matchmaking (file d'attente, appariement par
cote, `gambeta_meta`) demande des comptes.

**Recommandation :** A. Elle colle au bouton unique qui existe déjà, ne demande aucun
écran de plus qu'une attente de l'adversaire, et suffit pour deux clients lancés sur un
même poste ou sur un réseau local. Le code de match ou le matchmaking viendront quand on
voudra choisir son adversaire.
**Réponse :** A, pour le moment.

### Q3 — Qui est le joueur, et qui est le joueur 1 ?

Q2 a tranché : une seule place d'attente, le premier qui clique attend, le suivant le
rejoint. Sans comptes, il faut dire comment le serveur reconnaît un joueur et comment il
attribue les numéros 1 et 2. L'architecture du backend prévoit que l'authentification
relève de `gambeta_meta` et que le serveur passe au BC jeu l'identité du joueur
(`docs/architecture.md`) ; `gambeta_meta` est vide. Le numéro compte pour la suite : le
mode Initiation et la boucle désignent les camps (initiative, M-06), et le client doit
savoir de quel côté de l'arène il joue.

**Recommandation :** Joueur anonyme : le serveur le reconnaît à sa connexion WebSocket,
sans nom, sans compte, sans jeton. Le premier arrivé (celui qui attendait) est le
joueur 1, l'autre le joueur 2. Les comptes, les pseudos et l'authentification viendront
avec le méta ; la reconnaissance par connexion implique qu'une connexion perdue est un
joueur perdu (voir la question sur la déconnexion).
**Réponse :** D'accord avec la recommandation : joueur anonyme.

### Q4 — Que se passe-t-il quand une connexion se coupe ?

Q3 a tranché : le joueur est sa connexion WebSocket, sans compte ni jeton, donc il ne peut
pas revenir dans un match après une coupure. Deux moments sont à couvrir. Pendant
l'attente : le joueur qui attend ferme le client, ou perd le réseau ; s'il garde la place,
le suivant est apparié avec un absent. Après l'appariement : l'un des deux part, et
l'autre reste dans un match sans adversaire. La reconnexion (snapshot et événements
manquants, grâce au `seq` des enveloppes déjà esquissées dans `gambeta_engine`) suppose
une identité qui survit à la connexion.

**Recommandation :** Pendant l'attente, une connexion coupée libère la place. Après
l'appariement, une connexion coupée met fin au match : le serveur prévient l'autre joueur
(« adversaire déconnecté »), dont le client revient à la page d'accueil. Pas de
reconnexion dans I26 : elle viendra avec l'identité des joueurs.
**Réponse :** D'accord avec la recommandation.

### Q5 — Que voit le joueur, de l'accueil à l'arène ?

Q1 à Q4 fixent le parcours côté serveur : attente, appariement, numéro 1 ou 2, fin du match
si l'un part. Côté client existent la page d'accueil (`scenes/home/`, bouton
« Rejoindre un match ») et la maquette de l'arène (`scenes/mockup/`, une composition figée :
manche 1, tour 3, le bleu programme ses ordres). Il manque l'écran d'attente, le cas
« serveur injoignable », la façon de montrer au joueur son numéro, et le retour à
l'accueil décidé en Q4.

**Recommandation :**
- Un clic sur « Rejoindre un match » ouvre un écran d'attente, « En attente d'un
  adversaire… », avec un bouton « Annuler » qui coupe la connexion (la place se libère,
  Q4) et revient à l'accueil.
- Si le serveur est injoignable, le joueur reste sur l'accueil avec un message d'erreur,
  et le bouton reste utilisable pour réessayer.
- Une fois apparié, le joueur arrive sur l'arène existante, telle quelle, avec en plus
  l'indication « Joueur 1 » ou « Joueur 2 ». I26 ne touche pas à la composition figée :
  la mise en place réelle du match la remplacera.
- Si l'adversaire se déconnecte, un message « Adversaire déconnecté » s'affiche, puis le
  client revient à l'accueil.
**Réponse :** D'accord. Les messages sont portés par un overlay sur tout l'écran, opaque à
80 %, message plein centre : maquette `maquettes/I26-M1-overlay-de-messages.html`,
validée. Chaque overlay apparaît et disparaît en fondu de 0,5 s. L'overlay « Adversaire
trouvé » s'efface seul au bout de 2 s et laisse un
repère « Joueur 1 » / « Joueur 2 » dans l'arène ; l'overlay « Adversaire déconnecté »
ramène à l'accueil après un compte à rebours de 5 s, ou tout de suite par un bouton.

### Q6 — Sous quelle forme passent les messages, et comment écrit-on le contrat ?

Le canal d'un joueur est la relation `client-plays-on-backend` (`system/relations.yaml`),
`planned`, sans contrat : I26 est la première à la faire exister. Côté backend, les
enveloppes `ServerEnvelope { seq, payload }` et `ClientEnvelope { command_id, payload }`
existent (`gambeta_engine/src/io/web/protocol.rs`), au format non choisi (postcard,
MessagePack...). Côté client, Godot lit le JSON nativement (`JSON.parse_string`) et
`WebSocketPeer` envoie des trames texte ; un format binaire demanderait un décodeur écrit
à la main en GDScript. Le contrat peut être écrit à la main dans `contracts/`, ou généré
depuis les types Rust (schéma JSON), ce qui suppose un outillage à mettre en place.

**Recommandation :** JSON en trames texte WebSocket, sur la route `/ws` du serveur, dans
les enveloppes existantes. Le contrat est écrit à la main, en Markdown, dans
`contracts/canal-joueur.md` : il liste chaque message, son sens et ses champs, et la
relation passe en `formal`. Un format binaire ou un contrat généré pourront venir quand
le volume de messages le justifiera.
**Réponse :** D'accord avec la recommandation.

### Q7 — Quels messages passent sur le canal ?

Q6 a tranché : JSON sur `/ws`, contrat écrit à la main dans `contracts/canal-joueur.md`.
Il faut maintenant la liste des messages, qui couvre le parcours de Q1 à Q5. Une question
de fond : ouvrir la connexion vaut-il demande de rejoindre, ou le client l'envoie-t-il
explicitement ? Le même canal portera ensuite les commandes de jeu, la reconnexion
(`seq`) et peut-être les spectateurs : une connexion ne voudra pas toujours dire
« je cherche un adversaire ».

**Recommandation :** une demande explicite, et cinq messages en tout.
- Client → serveur : `rejoindre_match` (sans champ). « Annuler » ferme la connexion,
  sans message (Q4).
- Serveur → client : `en_attente` (le joueur occupe la place d'attente) ;
  `match_trouve { joueur: 1 | 2 }` ; `adversaire_deconnecte` (le match est fini, le
  serveur ferme ensuite la connexion) ; `erreur { code, message }` pour une demande
  refusée (par exemple un second `rejoindre_match` sur la même connexion).
- « Serveur injoignable » n'est pas un message : c'est l'échec de la connexion, constaté
  par le client.
**Réponse :** D'accord avec la recommandation.

### Q8 — Comment le client trouve-t-il le serveur ?

Le serveur écoute sur `0.0.0.0:8080` par défaut, adresse changeable par la variable
`GAMBETA_ADDR` (`gambeta_server/src/main.rs`). Le client n'a aucune configuration réseau.
Il lit déjà des arguments de ligne de commande (`--screenshot=` dans `scenes/home/`), et
le `Makefile` racine lance client et serveur (`make run-client`, `make run-server`). Pour
jouer à deux sur un même poste, il suffit de lancer deux clients ; sur un réseau local,
le second poste doit viser l'adresse du premier.

**Recommandation :** Adresse par défaut `ws://localhost:8080/ws`, remplaçable au
lancement par un argument `--server=ws://hôte:port/ws` (après `--`), que
`make run-client SERVER=…` transmet. Pas d'écran de réglage dans I26.
**Réponse :** D'accord avec la recommandation.

### Q9 — Comment prouve-t-on que « rejoindre un match » marche ?

Chaque composant a ses portes (`make test`, `lint`, `arch`…) : tests Rust du backend,
tests GUT du client (`test/unit/`). Le flux du home repo prévoit en plus des scénarios de
bout en bout, joués par `ci/integrate` contre les composants montés au SHA d'un
manifeste ; aucun n'existe encore. Le parcours d'I26 traverse les deux composants : un
test qui ne regarde qu'un côté ne prouve pas que les deux s'entendent sur le contrat.

**Recommandation :** trois niveaux.
- Backend : tests d'intégration qui ouvrent de vrais WebSocket sur le serveur lancé en
  test : deux clients appariés reçoivent `match_trouve` avec 1 et 2 ; un départ pendant
  l'attente libère la place ; un départ après l'appariement envoie
  `adversaire_deconnecte` ; un second `rejoindre_match` reçoit une `erreur` ; un
  troisième client attend une nouvelle paire.
- Client : tests GUT de la correspondance message reçu → overlay affiché, sans réseau.
- Bout en bout : un scénario du home repo lance le serveur et deux clients Godot sans
  fenêtre (`--headless`), et vérifie que les deux arrivent sur l'arène, l'un joueur 1,
  l'autre joueur 2. C'est le premier scénario de `ci/integrate`.
**Réponse :** D'accord avec la recommandation, « c'est exactement ce qu'il faut ».

## Synthèse

I26 fait exister le canal du joueur, de bout en bout, pour une seule chose : se retrouver à
deux dans le même match. Sur la page d'accueil du client, « Rejoindre un match » ouvre une
connexion WebSocket vers le serveur et envoie `rejoindre_match`. Le serveur garde une seule
place d'attente : le premier joueur l'occupe, le suivant forme la paire avec lui. Le premier
est le joueur 1, le second le joueur 2. Les joueurs sont anonymes, reconnus à leur
connexion ; une connexion coupée libère la place pendant l'attente, et met fin au match
après l'appariement, l'autre joueur étant prévenu. Côté client, chaque étape est portée par
un overlay plein écran (maquette I26-M1). Le match ne contient encore aucun état de jeu :
l'arène affichée reste la maquette figée, et la mise en place réelle (M-01 à M-07) est
l'initiative suivante. Les messages sont du JSON sur `/ws`, décrits à la main dans un
premier contrat, `contracts/canal-joueur.md`. Le tout est prouvé par des tests de chaque
composant et par un premier scénario de bout en bout.

## Besoins

- **I26-B1** — Un clic sur « Rejoindre un match » ouvre une connexion WebSocket vers le
  serveur, envoie `rejoindre_match` et affiche l'overlay « En attente d'un adversaire… »
  avec un bouton « Annuler » (Q2, Q5, Q7).
- **I26-B2** — Le serveur a une seule place d'attente. Si elle est libre, le joueur qui
  envoie `rejoindre_match` l'occupe et reçoit `en_attente` (Q2, Q7).
- **I26-B3** — Si la place est occupée, le serveur forme un match avec les deux joueurs et
  libère la place : celui qui attendait est le joueur 1, le nouvel arrivant le joueur 2.
  Chacun reçoit `match_trouve { joueur }` avec son numéro (Q2, Q3, Q7).
- **I26-B4** — Plusieurs matchs coexistent : après un appariement, le joueur suivant occupe
  de nouveau la place d'attente (Q2).
- **I26-B5** — À la réception de `match_trouve`, le client ouvre l'arène existante, sans en
  changer la composition, sous l'overlay « Adversaire trouvé — Vous êtes le Joueur N ».
  L'overlay s'efface seul au bout de 2 s, et un repère « Joueur N » reste affiché dans
  l'arène (Q5, I26-M1).
- **I26-B6** — Un joueur est anonyme : le serveur le reconnaît à sa connexion, sans nom,
  sans compte, sans jeton (Q3).

## Règles et cas d'erreur

- **I26-B7** — « Annuler » ferme la connexion, sans message ; le client retire l'overlay et
  l'accueil redevient utilisable (Q4, Q7).
- **I26-B8** — Une connexion coupée pendant l'attente, quelle qu'en soit la cause, libère
  la place d'attente (Q4).
- **I26-B9** — Une connexion coupée après l'appariement met fin au match : le serveur
  envoie `adversaire_deconnecte` à l'autre joueur, puis ferme sa connexion (Q4, Q7).
- **I26-B10** — À la réception de `adversaire_deconnecte`, le client affiche l'overlay
  « Adversaire déconnecté » avec un compte à rebours de 5 s, puis revient à l'accueil ; un
  bouton « Retour à l'accueil » y ramène tout de suite (Q5, I26-M1).
- **I26-B11** — Si la connexion au serveur échoue, le client affiche l'overlay « Serveur
  injoignable » ; « OK » le ferme, le joueur reste sur l'accueil et peut réessayer (Q5, Q7).
- **I26-B12** — Un second `rejoindre_match` sur une même connexion reçoit
  `erreur { code, message }` et ne change rien à l'état du joueur (Q7).
- **I26-B13** — Pas de reconnexion : un joueur dont la connexion s'est coupée ne revient
  pas dans son match (Q4).
- **I26-B14** — Les overlays couvrent tout l'écran, opaques à 80 %, message plein centre,
  et apparaissent et disparaissent en fondu de 0,5 s (Q5, I26-M1).

## Canal et contrat

- **I26-B15** — Les messages sont du JSON en trames texte WebSocket, sur la route `/ws` du
  serveur, dans les enveloppes `ServerEnvelope { seq, payload }` et
  `ClientEnvelope { command_id, payload }` (Q6).
- **I26-B16** — Le contrat du canal est écrit à la main dans `contracts/canal-joueur.md` :
  chaque message, son sens et ses champs. La relation `client-plays-on-backend` passe en
  `formal` et pointe vers lui (Q6).
- **I26-B17** — Le canal porte cinq messages : `rejoindre_match` (client → serveur) ;
  `en_attente`, `match_trouve { joueur: 1 | 2 }`, `adversaire_deconnecte`,
  `erreur { code, message }` (serveur → client) (Q7).
- **I26-B18** — Le client vise `ws://localhost:8080/ws` par défaut, ou l'adresse donnée au
  lancement par `--server=ws://hôte:port/ws` ; `make run-client SERVER=…` la transmet (Q8).

## Preuves

- **I26-B19** — Des tests d'intégration du backend, sur de vrais WebSocket, couvrent
  I26-B2 à B4, B8, B9 et B12 (Q9).
- **I26-B20** — Des tests GUT du client vérifient, sans réseau, l'overlay affiché pour
  chaque message reçu et pour l'échec de connexion (Q9).
- **I26-B21** — Un scénario de bout en bout du home repo lance le serveur et deux clients
  Godot `--headless`, et vérifie que les deux arrivent sur l'arène, l'un joueur 1, l'autre
  joueur 2 ; c'est le premier scénario de `ci/integrate` (Q9).

## Hors périmètre

- La mise en place du match (M-01 à M-07 : decks, mélange, pioche, initiative) et tout
  état de jeu : initiative suivante (Q1).
- Choisir son adversaire : code de match, liste des matchs ouverts, matchmaking par cote
  (Q2).
- Comptes, pseudos, authentification, et la reconnexion qu'ils permettraient (Q3, Q4).
- Quitter volontairement un match en cours ; les spectateurs.
- Un format binaire ou un contrat généré depuis le code (Q6).
- Un écran de réglage de l'adresse du serveur (Q8).
- La persistance des matchs (event store) et tout changement de `gambeta_meta`.
