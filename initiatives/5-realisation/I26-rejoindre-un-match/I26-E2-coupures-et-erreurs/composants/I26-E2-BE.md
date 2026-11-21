---
id: I26-E2-BE
parent: I26-E2
depot: backend
needs: [I26-B8, I26-B9, I26-B12, I26-B13, I26-B19]
scenarios: [I26-E2-S1, I26-E2-S2, I26-E2-S3, I26-E2-S5, I26-E2-S6]
contracts: [canal-joueur.md]
depends_on: [I26-E1-BE]
verdict: a_faire
kind: realisation
---
# I26-E2-BE — Coupures de connexion et demande en double

À la fin de cet epic, une connexion coupée ne laisse jamais de trace : elle libère la place
d'attente si elle l'occupait, et elle met fin à son match si elle était appariée, l'autre
joueur étant prévenu. Une seconde demande sur la même connexion est refusée sans rien
changer. Le format est celui de `contracts/canal-joueur.md`, inchangé.

## Ce que le backend livre

1. **Départ pendant l'attente** : quand la connexion qui occupe la place d'attente se
   ferme, quelle qu'en soit la cause (fermeture propre, réseau perdu), le BC jeu le
   signale par le port `Appariement` et le méta libère la place (`quitter(participant)`
   sur l'agrégat). Le joueur suivant attend au lieu d'être apparié avec un absent
   (I26-B8).
2. **Départ après l'appariement** : quand l'une des deux connexions d'une salle de match
   se ferme, la salle envoie `adversaire_deconnecte` à l'autre, ferme sa connexion, et
   s'arrête : le match est fini (I26-B9).
3. **Demande en double** : un `rejoindre_match` reçu d'une connexion qui attend ou qui
   est dans un match reçoit `erreur {code: "demande_en_double"}` ; rien ne change, ni la
   place d'attente, ni la salle (I26-B12).
4. **Pas de reconnexion** : une nouvelle connexion est toujours un nouveau participant ;
   rien ne la rattache à un match passé (I26-B13).

## Preuve attendue

Tests d'intégration dans `crates/gambeta_server/tests/`, sur de vrais WebSocket, avec
l'aide de test d'I26-E1-BE (I26-B19) :
- A attend puis ferme sa connexion ; B rejoint et reçoit `en_attente` (S1, S2) ;
- A et B appariés ; B ferme sa connexion ; A reçoit `adversaire_deconnecte`, puis sa
  connexion est fermée par le serveur (S3) ;
- après S3, A rejoint sur une nouvelle connexion et reçoit `en_attente` ; B, sur une
  nouvelle connexion, est apparié avec A comme un nouveau joueur, sans retour dans le
  match quitté (S6) ;
- A attend et envoie un second `rejoindre_match` : il reçoit
  `erreur {code: "demande_en_double"}`, puis B rejoint et A reçoit
  `match_trouve {joueur: 1}` (S5) ;
- un joueur apparié qui renvoie `rejoindre_match` reçoit la même erreur, et son
  adversaire ne reçoit rien.

Et les tests de `quitter` sur l'agrégat de la place d'attente (`crates/gambeta_meta/tests/`).
Pas d'horloge réelle : un test attend un message, il ne dort pas. `make check` passe.
