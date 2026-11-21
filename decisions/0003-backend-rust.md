# 0003 — Le backend devient un serveur Rust, et répond aussi du méta

- Statut : acceptée
- Date : 2026-11-21

## Contexte

Le composant `backend` a été déclaré à l'amorçage (0001) sur le dépôt Python
`gambeta_tactics_backend`, vide de code : seulement les docs de game design, dont
`product/` est désormais la référence. Ses responsabilités ne couvraient que le
match lui-même.

Un nouveau dépôt, `gambeta_server` (git@github.com:bbegouin-wedge/gambeta-server.git),
pose un workspace Rust pensé pour l'ensemble du service : passerelle WebSocket, un
acteur par match, un moteur de règles pur, le méta des joueurs (comptes, rosters,
matchmaking, classement), et PostgreSQL comme event store des matchs et stockage
du méta. Il
est déjà outillé pour la software factory (portes `make`, `.factory.toml`), et
son schéma directeur est vérifié par sa porte `arch` (`docs/architecture.md` du
dépôt).

Les responsabilités des composants étant figées (0002), changer de dépôt et
élargir le périmètre du backend passe par cet ADR.

## Décision

**Le composant `backend` garde son identifiant et son code `BE`**, et change de
dépôt : `gambeta_server`, Rust. Les relations, les manifestes et les identifiants
d'epics composant (`I<n>-E<m>-BE`) restent valables.

**Ses responsabilités s'élargissent** du match au service de jeu entier :

| Domaine | Responsabilités |
|---|---|
| Match (inchangé) | seul détenteur de l'état d'un match et de son flux d'événements ; seul composant qui applique les règles, étape par étape ; mélange des decks et tirage de l'initiative, graine enregistrée pour le replay ; filtrage de l'information cachée par joueur ; attente des saisies aux points d'attente et pendule |
| Match (précisé) | gestion des déconnexions et reconnexions ; journal des événements de chaque match en PostgreSQL, d'où un match se rejoue à l'identique |
| Canal des joueurs | point d'entrée réseau unique (WebSocket) ; authentification des joueurs et sessions ; routage d'un joueur vers son match ; numérotation des messages |
| Spectateurs (nouveau) | diffusion d'un match aux spectateurs, en différé |
| Méta (nouveau) | comptes et rosters des joueurs ; file d'attente et appariement par cote ; classement (Glicko-2) ; historique des matchs |
| Hors ligne (nouveau) | bots et simulations d'équilibrage ; analyse anti-triche des matchs enregistrés |

**L'ancien dépôt est retiré** : aucun epic composant n'y est plus projeté. Son
kanban est vide ; il n'y a rien à reprendre. La copie du game design qu'il porte
disparaît avec lui.

**L'architecture interne reste au composant** : le découpage en crates et les
dépendances autorisées sont décrits et vérifiés dans `gambeta_server`
(`docs/architecture.md`, `make arch`). Le home repo ne s'en sert que pour
rattacher un epic composant à une responsabilité.

Le protocole du canal d'un joueur n'est pas fixé ici : le transport est WebSocket,
le contrat reste à l'initiative I1 (relation `client-plays-on-backend`).

## Conséquences

- `system/components.yaml` : dépôt, chemin local, pile et responsabilités du
  backend mis à jour ; `CLAUDE.md` du home repo aussi.
- **La baseline change avec cette décision.** `manifests/current.yaml` fixe le backend à
  un commit de l'ancien dépôt (`35199e1`), absent de `gambeta_server`. Laisser les deux
  fichiers se contredire est pire qu'un échec : un `workspace/backend/` déjà monté
  contient ce commit, donc `make workspace` continue de monter l'ancien backend sans
  rien signaler ; seul un workspace neuf (CI, autre poste) échoue. La décision s'applique
  donc par un **candidat d'adoption**, `manifests/candidates/adr-0003.yaml`, qui fixe le
  backend à un commit de `gambeta_server` : intégré, puis promu dès l'acceptation de la
  décision. Le clone `workspace/backend/` de l'ancien dépôt est à supprimer pour être
  recréé depuis le nouveau.
- **Un candidat peut naître d'une décision**, et non seulement d'une initiative : il nomme
  `decision: "NNNN"`, s'appelle `adr-NNNN.yaml`, n'est promu que si la décision est
  acceptée, et `current.yaml` en garde l'origine (`from_decision`). Le contrôle de
  structure et `ci/integrate` l'acceptent.
- Les portes du backend existent désormais (`make check` dans le dépôt) ;
  `gates` du composant reste vide jusqu'à ce que `ci/integrate` les appelle.
- Une initiative qui touche comptes, matchmaking ou classement se projette sur
  `BE` ; aucun nouveau composant n'est nécessaire pour le méta.
- Le backend ne dépend d'aucun dépôt de l'univers kreek : le méta est écrit pour
  Gambeta, sur PostgreSQL.
- Le backend porte plus de responsabilités : une projection qui en touche
  plusieurs domaines reste un seul epic composant, découpé en tickets par le dépôt.
