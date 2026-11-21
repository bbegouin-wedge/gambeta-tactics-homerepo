---
id: I26-E1-BE
parent: I26-E1
depot: backend
needs: [I26-B2, I26-B3, I26-B4, I26-B6, I26-B15, I26-B17, I26-B19]
scenarios: [I26-E1-S1, I26-E1-S2, I26-E1-S4, I26-E1-S5]
contracts: [canal-joueur.md]
depends_on: [H1]
verdict: a_faire
kind: realisation
---
# I26-E1-BE — Le canal `/ws` et l'appariement de deux joueurs

À la fin de cet epic, le serveur accepte des connexions WebSocket sur `/ws`. Il reçoit
`rejoindre_match`, met le joueur sur une place d'attente unique, et quand un second joueur
arrive, forme la paire : le premier reçoit `match_trouve {joueur: 1}`, le second
`match_trouve {joueur: 2}`. Le format des messages est celui de
`contracts/canal-joueur.md` (home repo).

Le schéma directeur (`docs/architecture.md`) est respecté : les deux BC s'ignorent et
`gambeta_server` les relie.

## Ce que le backend livre

1. **Canal** (`gambeta_engine`, `io/web`) : la route `/ws` (passage en WebSocket, axum
   `ws`), les messages du contrat comme types serde (`payload` étiqueté par `type`, en
   `snake_case`) dans les enveloppes existantes de `protocol.rs`, JSON en trames texte.
   `seq` part de 1 et augmente à chaque message, par connexion. Une trame illisible ou un
   `type` inconnu reçoit `erreur {code: "message_illisible"}`, et la connexion reste
   ouverte. Chaque connexion reçoit un identifiant de participant anonyme, attribué par
   le BC jeu : c'est l'identité du joueur (I26-B6).
2. **Place d'attente** (`gambeta_meta`, `domain/` et `use_cases/`) : un agrégat à une
   seule place. `rejoindre(participant)` rend « en attente » si la place était libre, ou
   « apparié (joueur 1 = celui qui attendait, joueur 2 = le nouveau) » en libérant la
   place. Pur, sans async ni framework.
3. **Port d'appariement** (`gambeta_engine`, `ports.rs` et `use_cases/`) : sur
   `rejoindre_match`, le BC jeu appelle le port `Appariement`. S'il rend « en attente »,
   il envoie `en_attente` ; s'il rend une paire, il ouvre une **salle de match** dans
   `runtime/`, qui tient les deux connexions et envoie à chacune son `match_trouve`.
   La salle ne lance pas encore l'automate.
4. **Branchement** (`gambeta_server`) : le port `Appariement` du BC jeu branché sur le cas
   d'usage de la place d'attente du méta, en traduisant les types de chaque BC. Le routeur
   et le lancement sont exposés par une bibliothèque (`src/lib.rs`), pour que les tests
   démarrent le serveur sur un port libre ; `main.rs` ne fait que l'appeler.

Plusieurs matchs coexistent : la place se libère à chaque appariement (I26-B4).

Hors de cet epic (I26-E2) : départ pendant l'attente, `adversaire_deconnecte`,
`demande_en_double`.

## Dépendances à demander

Le `Cargo.toml` racine est protégé : ces ajouts se demandent.
- `tokio-tungstenite` en dépendance de workspace, pour les tests seulement (le client
  WebSocket des tests d'intégration).
- `serde_json` (déjà déclaré dans le workspace) dans les `[dependencies]` de
  `gambeta_engine`, pour coder et décoder les trames.

## Preuve attendue

Des tests d'intégration dans `crates/gambeta_server/tests/` (I26-B19). Ils démarrent le
vrai serveur sur un port libre et parlent JSON sur de vrais WebSocket, avec une aide de
test (`tests/<support>/mod.rs`) qui ouvre des clients et lit leurs messages. Les
scénarios suivent la forme `given_` / `when_` / `then_`, sans mock :

- un joueur qui envoie `rejoindre_match` reçoit `en_attente` (seq 1) ;
- deux joueurs à la suite : le premier reçoit `match_trouve {joueur: 1}`, le second
  `match_trouve {joueur: 2}` (S1) ;
- quatre joueurs à la suite forment deux matchs, avec 1 et 2 dans chacun (S2) ;
- une trame illisible reçoit `erreur {code: "message_illisible"}`, et la connexion peut
  ensuite rejoindre normalement (S5) ;
- le serveur écoute à l'adresse de `GAMBETA_ADDR` (S4).

Et des tests de l'agrégat de la place d'attente dans `crates/gambeta_meta/tests/`.
`make check` passe, `make arch` compris.
