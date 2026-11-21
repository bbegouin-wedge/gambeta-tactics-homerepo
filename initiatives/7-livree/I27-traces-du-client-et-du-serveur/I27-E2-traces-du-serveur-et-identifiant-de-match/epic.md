---
id: I27-E2
parent: I27
needs: [I27-B8, I27-B9, I27-B10, I27-B11, I27-B12, I27-B13, I27-B14, I27-B15]
screens: []
depends_on: [I27-E1]
---
# I27-E2 — Traces du serveur et identifiant de match

À la fin de cet epic, le serveur attribue un ULID à chaque match et le transmet dans
`match_trouve`. Il écrit ses traces d'étape dans son terminal, visibles par défaut, et les
envoie aux clients abonnés par `suivre_traces`. Dans la console, les traces du serveur se
mêlent à celles du client, et les deux joueurs d'un match y lisent le même identifiant.

## Effet sur l'existant

S'appuie sur I27-E1 (journal, console, recopie dans la sortie de Godot). Côté serveur, la
salle (`runtime/salle.rs`) reçoit un identifiant ; les traces `debug` actuelles sont
reprises dans les traces d'étape. Nouvelle dépendance pour générer l'ULID, à demander
(`Cargo.toml` racine protégé).

Le contrat `contracts/canal-joueur.md` s'enrichit en restant en version 1 (ajouts
compatibles) : `suivre_traces` (client → serveur), `trace` (serveur → client), champ
`match` de `match_trouve`, liste des `quoi` du serveur. Le scénario
`ci/scenarios/deux-joueurs-se-retrouvent` est étendu.

N'en fait pas partie : un canal de débogage global, les trames brutes, la reconnexion.

## Scénarios de bout en bout

- **I27-E2-S1** — Étant donné deux clients lancés avec `--traces`, quand ils se
  retrouvent dans un match, alors la console de chacun montre la trace serveur `apparie`
  (joueur N, match X) et la trace client `match_rejoint` (joueur N, match X), avec le même
  X chez les deux. (I27-B8, B9, B10, B11, B12)
- **I27-E2-S2** — Étant donné ce même parcours, alors le terminal du serveur montre, sans
  réglage de `RUST_LOG`, `connexion_acceptee` pour chacun, `en_attente` pour le premier et
  `apparie` avec le même ULID. (I27-B8, B11)
- **I27-E2-S3** — Étant donné A lancé avec `--traces` et B sans, quand ils se retrouvent,
  alors A reçoit ses traces serveur, B n'en reçoit aucune, et le `match_trouve` de B porte
  le même ULID que celui de A. (I27-B9, B12)
- **I27-E2-S4** — Étant donné A et B dans un match, A abonné, quand B ferme son client,
  alors la console de A montre `adversaire_parti` (serveur) puis `adversaire_deconnecte`
  (client). (I27-B8)
- **I27-E2-S5** — `ci/integrate` passe avec le scénario étendu
  `deux-joueurs-se-retrouvent` : pour chaque client, `apparie` et `match_rejoint` avec le
  bon numéro de joueur et le même identifiant de match chez les deux, lus par `quoi` et
  les champs, jamais par `message`. Les tests d'intégration du backend, sur de vrais
  WebSocket, couvrent l'abonnement, l'étanchéité entre connexions et l'ULID partagé.
  (I27-B13, B14, B15)
