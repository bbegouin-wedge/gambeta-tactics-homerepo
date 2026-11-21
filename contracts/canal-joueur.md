# Contrat — canal du joueur

- Relation : `client-plays-on-backend` (`client` → `backend`, `consumes`),
  `system/relations.yaml`.
- Écrit à la main. Introduit par I26 (« Rejoindre un match »), epic I26-E1.
- Version : 1.

Le canal par lequel un client parle au serveur pour le compte d'un joueur. Cette version
ne couvre que **rejoindre un match** : se retrouver à deux dans le même match, sans état de
jeu. Les commandes et les événements de jeu s'ajouteront ici.

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
{"seq": 1, "payload": {"type": "en_attente"}}
```

| Champ | Type | Règle |
|---|---|---|
| `seq` | entier ≥ 1 | numéroté par le serveur à partir de 1 sur chaque connexion, +1 par message |
| `payload` | objet | un message serveur → client |

Un champ inconnu dans une enveloppe ou un message est ignoré par celui qui le reçoit.

## Messages

Le champ **`type`** de `payload` désigne le message. Les noms sont en `snake_case`.

### Client → serveur

| `type` | Champs | Sens |
|---|---|---|
| `rejoindre_match` | — | Le joueur demande un adversaire. Une seule fois par connexion. |

### Serveur → client

| `type` | Champs | Sens |
|---|---|---|
| `en_attente` | — | Le joueur occupe la place d'attente ; il recevra `match_trouve` à l'arrivée d'un adversaire. |
| `match_trouve` | `joueur` : `1` ou `2` | La paire est formée. `1` pour celui qui attendait, `2` pour celui qui vient d'arriver. |
| `adversaire_deconnecte` | — | L'adversaire est parti : le match est fini. Le serveur ferme ensuite la connexion. |
| `erreur` | `code` : chaîne ; `message` : chaîne lisible | Une demande est refusée. L'état du joueur ne change pas, et la connexion reste ouverte. |

```json
{"seq": 2, "payload": {"type": "match_trouve", "joueur": 1}}
{"seq": 2, "payload": {"type": "erreur", "code": "demande_en_double", "message": "Une demande est déjà en cours sur cette connexion."}}
```

### Codes d'erreur

| `code` | Quand |
|---|---|
| `message_illisible` | La trame n'est pas une enveloppe valide (JSON invalide, champ manquant, `type` inconnu), ou c'est une trame binaire. |
| `demande_en_double` | `rejoindre_match` reçu d'une connexion qui attend déjà ou qui est dans un match. |

Le texte de `message` est destiné à un humain (journal, débogage) ; le client se fonde sur
`code`.

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

**Serveur injoignable** : ce n'est pas un message. C'est l'échec de l'ouverture de la
connexion, constaté par le client.

## Évolution

Un changement compatible (nouveau message, nouveau champ facultatif, nouveau code
d'erreur) ajoute à ce contrat sans changer sa version. Tout autre changement augmente la
version, se décrit dans la projection de l'initiative qui le porte, et se livre côté
serveur et côté client dans le même manifeste candidat.
