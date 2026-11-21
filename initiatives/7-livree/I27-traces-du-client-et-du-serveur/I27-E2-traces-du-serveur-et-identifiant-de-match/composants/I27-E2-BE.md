---
id: I27-E2-BE
parent: I27-E2
depot: backend
needs: [I27-B8, I27-B9, I27-B11, I27-B12, I27-B13, I27-B15]
scenarios: [I27-E2-S1, I27-E2-S2, I27-E2-S3, I27-E2-S4, I27-E2-S5]
contracts: [canal-joueur.md]
depends_on: []
verdict: a_faire
kind: realisation
---
# I27-E2-BE — Traces du serveur et identifiant de match

À la fin de cet epic, chaque match a un ULID, transmis aux deux joueurs dans
`match_trouve`. Le serveur trace les étapes du parcours dans son terminal, visibles par
défaut, et les envoie, en messages `trace`, aux seules connexions abonnées par
`suivre_traces`. Le format est celui de `contracts/canal-joueur.md` (sections Messages,
Traces, Déroulés).

## Ce que le backend livre

1. **Identifiant de match** : un ULID attribué à la formation de la paire, porté par la
   salle, envoyé dans `match_trouve { joueur, match }` aux deux joueurs (I27-B11, B12).
   Crate `ulid`, validée : `[workspace.dependencies]` du `Cargo.toml` racine. L'horloge et
   l'aléa qui le fabriquent sont injectés (ports), pour des tests déterministes.
2. **Traces d'étape** : `connexion_acceptee`, `en_attente`, `apparie` (`joueur`,
   `match`), `demande_refusee` (`code`), `adversaire_parti` (`match`), chacune écrite dans
   le terminal par `tracing` au niveau `info` (le niveau par défaut du filtre la rend
   visible sans `RUST_LOG`), avec `quoi` et ses champs. Les traces `debug` existantes
   (salle fermée, appariement avec un absent…) sont reprises ou gardées en `debug`
   (I27-B8).
3. **Abonnement** : `suivre_traces` abonne la connexion ; un second envoi est sans effet.
   Une connexion abonnée reçoit ensuite, en `trace { niveau, quoi, message, champs }`,
   les traces qui la concernent, jamais celles d'une autre connexion. Sans
   abonnement, rien. `connexion_acceptee` ne part jamais sur le canal. `adversaire_parti`
   part avant la fermeture de la connexion par le serveur (I27-B9).
4. **Heure** : **toute** enveloppe serveur → client porte `heure` à côté de `seq`
   (`ServerEnvelope { seq, heure, payload }`), heure de son émission : UTC du serveur,
   RFC 3339 à la milliseconde ; une trace prend l'heure de son enveloppe. Lire l'heure est une IO : le
   cœur ne la lit jamais lui-même, il la reçoit par un **port `Horloge`** (dans
   `ports.rs`), branché sur l'horloge système par `gambeta_server` et sur une horloge
   fixe ou pas à pas dans les tests. Ce même port date les traces et fournit le temps de
   l'ULID ; l'aléa de l'ULID passe par `RngCore` injecté. Les tests vérifient donc des
   heures et des ULID exacts. Pas d'autre nouvelle dépendance que `ulid` ; si une autre
   semble nécessaire, la demander.

## Preuve attendue

Tests d'intégration dans `crates/gambeta_server/tests/`, sur de vrais WebSocket, avec les
aides de test d'I26 (I27-B15) :
- A et B appariés : leurs `match_trouve` portent le même `match`, un ULID valide (S3) ;
- A abonné, B non : A reçoit `trace` `en_attente` puis `apparie` (`joueur` 1, même
  `match`), B ne reçoit aucune `trace` (S1, S3) ;
- A non abonné : aucune `trace` (S3) ;
- A abonné, B part : A reçoit `adversaire_deconnecte` et la `trace` `adversaire_parti`,
  puis sa connexion est fermée (S4) ;
- A abonné envoie un second `rejoindre_match` : `trace` `demande_refusee`
  (`code: demande_en_double`) ;
- un second `suivre_traces` ne double pas les traces ;
- avec une horloge de test, chaque enveloppe reçue (`en_attente`, `match_trouve`,
  `trace`, `erreur`, `adversaire_deconnecte`) porte l'`heure` exacte attendue.

Et, pour le terminal (S2), un test que les traces d'étape sont émises au niveau `info`
(abonné `tracing` de test, sans horloge réelle). Pas de sleep : un test attend un message.
`make check` passe.
