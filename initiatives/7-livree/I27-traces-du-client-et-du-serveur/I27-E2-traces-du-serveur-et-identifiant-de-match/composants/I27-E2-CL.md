---
id: I27-E2-CL
parent: I27-E2
depot: client
needs: [I27-B10, I27-B12, I27-B13]
scenarios: [I27-E2-S1, I27-E2-S3, I27-E2-S4]
contracts: [canal-joueur.md]
depends_on: [I27-E1-CL]
verdict: a_faire
kind: realisation
---
# I27-E2-CL — Traces du serveur dans la console et identifiant de match

À la fin de cet epic, un client lancé avec `--traces` s'abonne aux traces du serveur et
les mêle aux siennes dans le journal, et la trace `match_rejoint` porte l'identifiant du
match. Le format est celui de `contracts/canal-joueur.md`.

## Ce que le client livre

1. **Abonnement** : avec `--traces`, `suivre_traces` part dès l'ouverture de la
   connexion, avant `rejoindre_match` (I27-B10).
2. **Réception** : `Protocol` lit le champ `heure` de toute enveloppe serveur → client, et
   le message `trace { niveau, quoi, message, champs? }` ; la trace entre au journal avec
   l'origine `serveur` et l'heure de son enveloppe, et elle est recopiée dans
   la sortie de Godot comme les autres (I27-B13).
3. **Identifiant** : `Protocol` lit le champ `match` de `match_trouve` ; `match_rejoint`
   le porte dans ses champs (`joueur`, `match`). Le mode automatique peut l'écrire dans son
   rapport (I27-B12).
4. **Faux serveur** : les scénarios du `FakeServer` datent leurs enveloppes, envoient un `match` et, pour une
   connexion abonnée, les `trace` du contrat.

## Preuve attendue

Tests GUT, sans réseau (faux serveur) :
- avec `--traces`, `suivre_traces` est le premier message envoyé ; sans, il n'est jamais
  envoyé ;
- une `trace` reçue entre au journal avec l'origine `serveur`, son `quoi`, ses champs et
  son heure ;
- `match_trouve { joueur, match }` produit `match_rejoint` avec les deux champs ;
- `adversaire_deconnecte` après une `trace` `adversaire_parti` : les deux sont au
  journal, dans l'ordre d'arrivée.

`make check` passe.
