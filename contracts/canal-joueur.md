# Contrat — canal du joueur

- Relation : `client-plays-on-backend` (`client` → `backend`, `consumes`),
  `system/relations.yaml`.
- Écrit à la main. Introduit par I26 (« Rejoindre un match »), epic I26-E1. Enrichi par
  I27 (« Traces du client et du serveur »), epic I27-E2 : ajouts compatibles.
- Version : 1.

Le canal par lequel un client parle au serveur pour le compte d'un joueur. Cette version
couvre **rejoindre un match** (se retrouver à deux dans le même match, sans état de jeu)
et les **traces techniques** du serveur, pour le développeur. Les commandes et les
événements de jeu s'ajouteront ici.

## Transport

- WebSocket, sur la route **`/ws`** du backend. Adresse par défaut côté client :
  `ws://localhost:8080/ws`.
- **Trames texte** uniquement. Une trame contient **un** message JSON (UTF-8).
- Pas de sous-protocole WebSocket, pas d'en-tête particulier.

## Identité

- Le joueur est **sa connexion** : pas de nom, pas de compte, pas de jeton.
- **Fermer la connexion vaut départ**, quelle qu'en soit la cause (« Annuler », client
  fermé, réseau perdu). Il n'y a pas de message de départ.
- Pas de reconnexion : une nouvelle connexion est un nouveau joueur, sans lien avec un
  match passé.

## Enveloppes

Chaque trame est une enveloppe dont `payload` porte le message.

**Client → serveur**

```json
{"command_id": 1, "payload": {"type": "rejoindre_match"}}
```

| Champ | Type | Règle |
|---|---|---|
| `command_id` | entier ≥ 1 | numéroté par le client à partir de 1 sur chaque connexion, +1 par message |
| `payload` | objet | un message client → serveur |

**Serveur → client**

```json
{"seq": 1, "heure": "2026-11-21T19:04:11.902Z", "payload": {"type": "en_attente"}}
```

| Champ | Type | Règle |
|---|---|---|
| `seq` | entier ≥ 1 | numéroté par le serveur à partir de 1 sur chaque connexion, +1 par message |
| `heure` | chaîne | heure UTC du serveur à l'émission du message, RFC 3339 à la milliseconde (`…T19:04:11.902Z`). Ajouté par I27 ; seul le serveur date, le client ne date pas ses enveloppes |
| `payload` | objet | un message serveur → client |

Un champ inconnu dans une enveloppe ou un message est ignoré par celui qui le reçoit.

## Messages

Le champ **`type`** de `payload` désigne le message. Les noms sont en `snake_case`.

### Client → serveur

| `type` | Champs | Sens |
|---|---|---|
| `rejoindre_match` | — | Le joueur demande un adversaire. Une seule fois par connexion. |
| `suivre_traces` | — | La connexion s'abonne aux traces du serveur qui la concernent (voir [Traces](#traces)). Envoyé une fois, avant toute autre demande ; un second envoi est sans effet. |

### Serveur → client

| `type` | Champs | Sens |
|---|---|---|
| `en_attente` | — | Le joueur occupe la place d'attente ; il recevra `match_trouve` à l'arrivée d'un adversaire. |
| `match_trouve` | `joueur` : `1` ou `2` ; `match` : chaîne, ULID | La paire est formée. `1` pour celui qui attendait, `2` pour celui qui vient d'arriver. `match` identifie le match, le même pour les deux joueurs (I27). |
| `trace` | `niveau`, `quoi`, `message`, `champs` (facultatif) | Une trace technique du serveur, envoyée seulement à une connexion abonnée par `suivre_traces` (voir [Traces](#traces)). |
| `adversaire_deconnecte` | — | L'adversaire est parti : le match est fini. Le serveur ferme ensuite la connexion. |
| `erreur` | `code` : chaîne ; `message` : chaîne lisible | Une demande est refusée. L'état du joueur ne change pas, et la connexion reste ouverte. |

```json
{"seq": 2, "heure": "2026-11-21T19:04:12.318Z", "payload": {"type": "match_trouve", "joueur": 1, "match": "01JDGQ8V4Z3K9M2N6P7R8S9T0V"}}
{"seq": 2, "heure": "2026-11-21T19:04:12.318Z", "payload": {"type": "erreur", "code": "demande_en_double", "message": "Une demande est déjà en cours sur cette connexion."}}
```

### Codes d'erreur

| `code` | Quand |
|---|---|
| `message_illisible` | La trame n'est pas une enveloppe valide (JSON invalide, champ manquant, `type` inconnu), ou c'est une trame binaire. |
| `demande_en_double` | `rejoindre_match` reçu d'une connexion qui attend déjà ou qui est dans un match. |

Le texte de `message` est destiné à un humain (journal, débogage) ; le client se fonde sur
`code`.

### Traces

Des traces techniques, pour le développeur (I27). Une connexion qui a envoyé
`suivre_traces` reçoit ensuite, en messages `trace`, les traces du serveur qui la
concernent, et **jamais** celles d'une autre connexion. Une connexion non abonnée n'en
reçoit aucune. Les traces émises avant l'abonnement ne sont pas renvoyées.

```json
{"seq": 3, "heure": "2026-11-21T19:04:12.318Z", "payload": {"type": "trace",
  "niveau": "info", "quoi": "apparie",
  "message": "Apparié avec un adversaire : joueur 1, match 01JDGQ8V4Z3K9M2N6P7R8S9T0V",
  "champs": {"joueur": 1, "match": "01JDGQ8V4Z3K9M2N6P7R8S9T0V"}}}
```

| Champ | Type | Règle |
|---|---|---|
| `niveau` | chaîne | `info`, `warn` ou `erreur` |
| `quoi` | chaîne | nom stable de l'étape, en `snake_case` (tableau ci-dessous) |
| `message` | chaîne | texte lisible ; il peut changer, on ne s'y fie pas |
| `champs` | objet, facultatif | valeurs structurées de la trace ; clés en `snake_case`, valeurs chaîne ou entier |

L'heure de la trace est celle de son enveloppe (`heure`).

Les `quoi` du serveur :

| `quoi` | `niveau` | `champs` | Quand |
|---|---|---|---|
| `connexion_acceptee` | `info` | — | La connexion est ouverte (précède tout abonnement : n'est jamais envoyée sur le canal). |
| `en_attente` | `info` | — | La connexion occupe la place d'attente. |
| `apparie` | `info` | `joueur`, `match` | La paire est formée ; même `match` que dans `match_trouve`. |
| `demande_refusee` | `warn` | `code` | Une demande reçoit `erreur` ; même `code`. |
| `adversaire_parti` | `info` | `match` | L'adversaire de cette connexion est parti ; le match est fini. |

Un nouveau `quoi`, un nouveau champ dans `champs` : ajouts compatibles. Un `quoi` inconnu
s'affiche comme les autres.

## Déroulés

**Nominal** : le serveur n'a qu'une place d'attente.

```
A → rejoindre_match
A ← en_attente
B → rejoindre_match
A ← match_trouve {joueur: 1}
B ← match_trouve {joueur: 2}
```

Après l'appariement, la place est de nouveau libre : le joueur suivant l'occupe.
Plusieurs matchs coexistent.

**Départ pendant l'attente** : A attend, puis sa connexion se ferme. La place est
libérée ; le joueur suivant reçoit `en_attente`.

**Départ après l'appariement** : A et B sont appariés, puis la connexion de B se ferme.

```
A ← adversaire_deconnecte
    (le serveur ferme la connexion de A)
```

**Demande en double** :

```
A → rejoindre_match
A ← en_attente
A → rejoindre_match
A ← erreur {code: "demande_en_double"}      (A reste en attente)
```

**Avec les traces** : A s'abonne, B non.

```
A → suivre_traces
A → rejoindre_match
A ← en_attente
A ← trace {quoi: "en_attente"}
B → rejoindre_match
A ← match_trouve {joueur: 1, match: X}
A ← trace {quoi: "apparie", champs: {joueur: 1, match: X}}
B ← match_trouve {joueur: 2, match: X}      (aucune trace pour B)
```

L'ordre entre un message et la trace qui le double n'est pas garanti ; les `seq` le
disent. Le client affiche les traces dans leur ordre d'arrivée, sans les réordonner.

**Serveur injoignable** : ce n'est pas un message. C'est l'échec de l'ouverture de la
connexion, constaté par le client.

## Évolution

Un changement compatible (nouveau message, nouveau champ facultatif, nouveau code
d'erreur) ajoute à ce contrat sans changer sa version. Tout autre changement augmente la
version, se décrit dans la projection de l'initiative qui le porte, et se livre côté
serveur et côté client dans le même manifeste candidat.
