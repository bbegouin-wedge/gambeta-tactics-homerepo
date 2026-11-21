# I27 — Grilling

## État des composants au départ

- **backend** (`gambeta_server`, tête `56844e3`) : `tracing` et `tracing-subscriber`
  (filtre par `RUST_LOG`) sont en place dans `gambeta_server/src/main.rs` ; quelques
  traces `debug`/`warn` dans `gambeta_engine` (connexion fermée, salle, appariement avec un
  absent, match terminé). Elles ne sortent que sur la sortie standard du serveur ; rien ne
  part vers le client.
- **client** (Godot 4.7, tête `b521249`) : aucune fonction de log ; quelques `push_error`
  et `push_warning` épars (manifeste, catalogue de cartes, trame illisible). La maquette de
  l'arène porte un fil du match (`scripts/ui/match_feed.gd`) à onglets Tout, Chat,
  Journal : le journal **de jeu**, destiné au joueur, lu dans l'état figé, sans réseau.
- **Système** : le contrat `contracts/canal-joueur.md` (v1) n'a aucun message de trace.

## Questions et réponses

### Q1 — À qui s'adresse ce log ?

« Log » peut désigner deux choses : (A) des traces techniques, pour le développeur, qui
montrent que la chaîne marche — celles du serveur rapatriées et affichées à côté de celles
du client, invisibles du joueur ; (B) le journal de jeu, pour le joueur (« Vous avez
rejoint le match, vous êtes le joueur 1 »), dans l'onglet Journal du fil du match : du
produit, qui relève de `product/` et des événements de match.

**Recommandation :** A. Le but est de vérifier l'epic. Des traces du serveur montrées au
joueur exposeraient l'interne, et le serveur filtre l'information cachée par joueur : ses
traces brutes ne peuvent pas partir telles quelles. Le journal de jeu (B) viendra avec les
événements de la boucle.
**Réponse :** A.

### Q2 — Où les traces s'affichent-elles dans le client ?

Q1 a tranché : des traces techniques, invisibles du joueur. Le parcours du client va de
l'accueil à l'attente (overlay), puis à l'arène (`scenes/parcours/`) : la connexion,
`en_attente` et `match_trouve` arrivent avant l'arène. Deux places : (A) un onglet « Tech »
dans le fil du match de l'arène, présent seulement avec une option de lancement ; (B) une
console de débogage par-dessus tous les écrans, ouverte au clavier.

**Recommandation :** A, avec un journal des traces tenu dès le lancement du client (pour
ne pas perdre ce qui précède l'arène) et chaque trace recopiée dans la sortie de Godot.
**Réponse :** B : une console de débogage, plus efficace, qui apparaît en tapant trois
fois `l` de suite. Restent valables : le journal tenu dès le lancement, les traces locales
et celles du serveur dans l'ordre d'arrivée et marquées par leur origine, et la recopie
dans la sortie de Godot. La combinaison est ignorée quand une saisie de texte a le focus
(le chat du fil du match), sans quoi taper « lll » dans un message ouvrirait la console.

### Q3 — Comment les traces du serveur arrivent-elles au client ?

Les traces `tracing` du serveur ne sortent que sur sa sortie standard. Trois voies : (A) un
message `trace` ajouté au canal du joueur (`contracts/canal-joueur.md`), le serveur
n'envoyant à une connexion que les traces qui la concernent ; (B) un canal de débogage à
part (`/traces`) qui diffuse toutes les traces du serveur, second contrat et seconde
connexion ; (C) aucun transport : la console ne montre que les traces du client.

**Recommandation :** A, à la demande du client : un message `suivre_traces`, puis le
serveur ne renvoie que les traces de cette connexion — jamais celles de l'autre joueur, ce
qui comptera avec l'information cachée. Sans abonnement, le trafic reste celui d'I26.
Ajout compatible : le contrat reste en version 1.
**Réponse :** A. Le client s'abonne quand il est lancé avec l'option `--traces` (dès
l'ouverture de la connexion, pour ne rien perdre de ce qui la suit).

### Q4 — Quelles traces dans I27 ?

Le but est de vérifier I26-E1 (deux joueurs se retrouvent). Deux partis : tracer les
étapes du parcours, une ligne chacune, ou recopier toutes les trames échangées.

**Recommandation :** les étapes du parcours, une ligne par étape, avec origine et niveau
(`info`, `warn`, `erreur`) :
- client : connexion ouverte à `<adresse>` ; serveur injoignable ; rejoindre un match
  demandé ; **match rejoint : joueur N** ; adversaire déconnecté ; connexion fermée ; trame
  illisible (l'actuel `push_warning`) ;
- serveur : connexion acceptée ; joueur en attente ; **apparié avec un adversaire : joueur
  N, match `<id>`** ; demande refusée (`<code>`) ; adversaire parti, match terminé.

La ligne « match rejoint » existe des deux côtés : le client la trace à la réception de
`match_trouve`, le serveur à la formation de la paire, avec l'identifiant du match. Pas de
recopie des trames brutes (elle noierait les étapes ; un niveau `debug` pourra venir). Les
traces existantes du serveur sont reprises dans cette liste.
**Réponse :** D'accord avec la recommandation.

### Q5 — Que fait la console sans `--traces`, et que montre-t-elle ?

Q3 a lié l'abonnement aux traces du serveur à l'option `--traces`. Reste le comportement
sans l'option, et la forme de la console.

**Recommandation :** sans `--traces`, pas de console : `lll` ne fait rien et le client ne
tient aucun journal ; la recopie dans la sortie de Godot reste toujours active. Avec
`--traces`, une console minimale : panneau semi-transparent en haut de l'écran, au-dessus
de tout (overlay compris) ; une ligne par trace — heure, origine (`client` ou `serveur`),
niveau, message — `warn` en orange, `erreur` en rouge ; défilement sur la dernière ligne ;
`lll` ouvre et ferme, `Échap` ferme ; les 500 dernières traces gardées. Ni filtre, ni
recherche, ni copie dans I27.
**Réponse :** D'accord avec la recommandation.

### Q6 — Comment prouve-t-on que les traces marchent ?

`ci/integrate` lance déjà `ci/scenarios/deux-joueurs-se-retrouvent` : serveur et deux
clients Godot sans fenêtre en mode automatique, rapports `{"joueur": 1}` et
`{"joueur": 2}`. Deux voies : (A) étendre ce scénario ; (B) un scénario à part, qui refait
le même parcours.

**Recommandation :** A. Les deux clients sont lancés en plus avec `--traces` ; le scénario
lit leur sortie Godot (où chaque trace est recopiée) et y trouve, pour chacun, la trace
client « match rejoint : joueur N » et la trace serveur « apparié avec un adversaire :
joueur N, match `<id>` » reçue par le canal, avec le même identifiant de match chez les
deux. Il prouve ainsi ce que le scénario d'I26 ne prouve pas : les deux joueurs sont dans
le même match. Le reste se teste dans chaque composant (serveur : quelles traces partent
sur quelle connexion, seulement après `suivre_traces` ; client : journal, raccourci `lll`,
pas de console sans `--traces`).
**Réponse :** A.

### Q7 — Quelle forme prend le message `trace` ?

Le scénario de Q6 doit retrouver des traces précises : chercher un texte libre casserait à
la première reformulation. Le contrat suit déjà ce principe pour `erreur` (`message` pour
l'humain, `code` pour la machine).

**Recommandation :** un nom stable pour la machine, une phrase pour l'humain :

```json
{"seq": 3, "payload": {"type": "trace", "niveau": "info", "quoi": "apparie",
  "message": "Apparié avec un adversaire : joueur 1, match <id>",
  "champs": {"joueur": 1, "match": "<id>"}, "heure": "2026-11-21T19:04:12.318Z"}}
```

`niveau` : `info`, `warn` ou `erreur` ; `quoi` : nom stable de l'étape en `snake_case`
(`connexion_acceptee`, `en_attente`, `apparie`, `demande_refusee`, `adversaire_parti`) ;
`message` : texte lisible, libre de changer ; `champs` : valeurs structurées, facultatif ;
`heure` : heure UTC du serveur. Les traces du client prennent la même forme (`quoi` :
`connexion_ouverte`, `match_rejoint`…). La recopie dans la sortie de Godot tient sur une
ligne repérable (`[trace] serveur info apparie joueur=1 match=<id> — Apparié avec…`) ; le
scénario s'appuie sur `quoi` et `champs`, jamais sur `message`.
**Réponse :** D'accord avec la recommandation.

### Q8 — Quel identifiant pour un match ?

Le serveur n'a aucun identifiant de match : la salle (`runtime/salle.rs`) ne connaît que
ses deux participants. La trace `apparie` en demande un.

**Réponse (de l'humain) :** un ULID, attribué par le serveur à la formation de la paire.
Il demande une dépendance au serveur (aucune crate ULID dans `Cargo.lock`) : le
`Cargo.toml` racine est protégé, son ajout est à demander dans la projection.

### Q9 — L'identifiant du match va-t-il aussi dans `match_trouve` ?

Avec Q8, l'ULID ne paraît que dans la trace serveur `apparie`, donc seulement chez un
client lancé avec `--traces`. (A) trace seulement ; (B) un champ `match` ajouté à
`match_trouve` (`{"type": "match_trouve", "joueur": 1, "match": "01JD…"}`).

**Recommandation :** B. Ajout compatible (nouveau champ ; un champ inconnu est ignoré) :
le contrat reste en version 1. La trace client `match_rejoint` le reprend (« match
rejoint : joueur 1, match 01JD… ») et vérifie seule le rattachement, même sans les traces
du serveur. La reconnexion, plus tard, en aura besoin.
**Réponse :** B.

### Q10 — Faut-il une maquette, et que montre le terminal du serveur ?

(a) Le seul écran nouveau est la console de débogage, outil de développeur invisible du
joueur, dont Q5 a fixé la forme. (b) Les traces actuelles du serveur sont en `debug`,
masquées par défaut par le filtre `RUST_LOG`.

**Recommandation :** (a) pas de maquette : l'initiative passe du grilling aux epics, la
console se valide sur le client lancé avec `--traces`. (b) Chaque trace d'étape du serveur
est une seule trace, écrite au niveau `info` dans son terminal (visible par défaut, mêmes
`quoi`, champs et ULID) et envoyée sur le canal de la connexion concernée si elle est
abonnée : on recoupe un match entre le terminal du serveur et la console des deux clients.
**Réponse :** D'accord avec les deux.

## Synthèse

I27 donne au système une fonction de traces techniques, pour le développeur, et s'en sert
d'abord pour vérifier qu'un client a effectivement rejoint un match (I26-E1). Lancé avec
`--traces`, le client tient dès son démarrage un journal où se mêlent, dans l'ordre
d'arrivée, ses propres traces et celles que le serveur lui envoie ; une console de
débogage, ouverte en tapant trois fois `l`, l'affiche par-dessus tous les écrans. Sans
l'option, le joueur ne voit rien. Les traces du serveur passent par le canal du joueur :
un nouveau message `trace`, envoyé seulement à la connexion concernée et seulement si elle
s'y est abonnée par `suivre_traces`. Une trace a un nom stable (`quoi`) pour les machines
et une phrase (`message`) pour les humains. Le serveur attribue à chaque match un ULID,
transmis aux deux joueurs dans `match_trouve`, repris par les traces des deux côtés et
dans le terminal du serveur. Le contrat reste en version 1 : tout est ajout compatible. Le
scénario de bout en bout d'I26 est étendu pour prouver que les deux clients sont dans le
même match.

## Besoins

### Traces du client

- **I27-B1** — Le client a une fonction de trace commune : chaque trace porte une heure,
  une origine (`client` ou `serveur`), un niveau (`info`, `warn`, `erreur`), un nom
  d'étape `quoi`, un `message` lisible et des `champs` facultatifs (Q4, Q7).
- **I27-B2** — Chaque trace, locale ou reçue du serveur, est recopiée dans la sortie de
  Godot, avec ou sans `--traces`, sur une ligne repérable :
  `[trace] <origine> <niveau> <quoi> <clé=valeur…> — <message>` (Q5, Q7).
- **I27-B3** — Le client trace les étapes du parcours : `connexion_ouverte` (adresse),
  `serveur_injoignable`, `rejoindre_demande`, `match_rejoint` (joueur, match),
  `adversaire_deconnecte`, `connexion_fermee`, `trame_illisible` (qui remplace l'actuel
  `push_warning`) (Q4, Q9).

### Option `--traces` et console

- **I27-B4** — Lancé avec `--traces`, le client tient un journal des traces dès son
  démarrage, locales et du serveur mêlées dans l'ordre d'arrivée, limité aux 500
  dernières. Sans l'option, il ne tient aucun journal (Q2, Q5).
- **I27-B5** — Avec `--traces`, taper trois fois `l` de suite ouvre la console de
  débogage, et la ferme ; `Échap` la ferme aussi. Le raccourci est ignoré quand une saisie
  de texte a le focus. Sans `--traces`, il ne fait rien (Q2, Q5).
- **I27-B6** — La console est un panneau semi-transparent en haut de l'écran, au-dessus de
  tout, overlays compris, sur tous les écrans. Une ligne par trace : heure, origine,
  niveau, message ; `warn` en orange, `erreur` en rouge ; elle défile sur la dernière
  ligne. Ni filtre, ni recherche, ni copie (Q2, Q5, Q10).
- **I27-B7** — `make run-client TRACES=1` lance le client avec `--traces` (Q3).

### Traces du serveur

- **I27-B8** — Le serveur trace les étapes du parcours : `connexion_acceptee`,
  `en_attente`, `apparie` (joueur, match), `demande_refusee` (code), `adversaire_parti`
  (match). Chacune est écrite dans son terminal au niveau `info`, visible par défaut, avec
  ses champs (Q4, Q10).
- **I27-B9** — Une connexion qui a envoyé `suivre_traces` reçoit ensuite, en messages
  `trace`, les traces du serveur qui la concernent, et jamais celles d'une autre
  connexion. Une connexion non abonnée n'en reçoit aucune. Les traces émises avant
  l'abonnement (`connexion_acceptee`) ne vont qu'au terminal (Q3).
- **I27-B10** — Lancé avec `--traces`, le client envoie `suivre_traces` dès l'ouverture de
  la connexion, avant toute autre demande (Q3).

### Identifiant de match

- **I27-B11** — Le serveur attribue un ULID à chaque match, à la formation de la paire
  (Q8).
- **I27-B12** — `match_trouve` porte l'identifiant : `{type: match_trouve, joueur, match}`.
  La trace client `match_rejoint` et la trace serveur `apparie` le reprennent (Q9).

### Contrat

- **I27-B13** — `contracts/canal-joueur.md` s'enrichit, en restant en version 1 (ajouts
  compatibles) : message client → serveur `suivre_traces` ; message serveur → client
  `trace { niveau, quoi, message, champs? }` ; champ `heure` (UTC du serveur) dans toute
  enveloppe serveur → client, que la trace reprend (précisé à la projection) ; champ
  `match` de `match_trouve` ; liste des `quoi` du serveur (Q3, Q7, Q9).

### Preuves

- **I27-B14** — Le scénario `ci/scenarios/deux-joueurs-se-retrouvent` lance en plus les
  deux clients avec `--traces` et vérifie dans leur sortie, pour chacun, la trace client
  `match_rejoint` et la trace serveur `apparie`, avec le bon numéro de joueur et le même
  identifiant de match chez les deux. Il s'appuie sur `quoi` et les champs, jamais sur
  `message` (Q6, Q7).
- **I27-B15** — Des tests d'intégration du backend, sur de vrais WebSocket, vérifient
  qu'une connexion reçoit ses traces après `suivre_traces`, aucune sans, jamais celles de
  l'autre joueur, et que `match_trouve` porte le même ULID chez les deux joueurs (Q6).
- **I27-B16** — Des tests GUT du client vérifient le journal (ordre, origine, limite de
  500), le raccourci `lll` (y compris ignoré pendant une saisie) et l'absence de console
  et de journal sans `--traces` (Q6).

## Hors périmètre

- Le journal de jeu destiné au joueur (onglet Journal du fil du match) : il viendra avec
  les événements de la boucle (Q1).
- Un canal de débogage global, toutes connexions confondues (Q3).
- La recopie des trames brutes, un niveau `debug` sur le canal (Q4).
- Filtre, recherche, copie ou export dans la console (Q5).
- Une maquette de la console (Q10).
- La reconnexion, qui se servira de l'identifiant de match.
