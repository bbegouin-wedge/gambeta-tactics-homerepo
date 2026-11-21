---
id: I26-E1-CL
parent: I26-E1
depot: client
needs: [I26-B1, I26-B3, I26-B5, I26-B11, I26-B14, I26-B15, I26-B17, I26-B18, I26-B20]
scenarios: [I26-E1-S1, I26-E1-S3, I26-E1-S4, I26-E1-S5, I26-E1-S6]
contracts: [canal-joueur.md]
depends_on: [H1]
verdict: a_faire
kind: realisation
---
# I26-E1-CL — Rejoindre un match depuis l'accueil

À la fin de cet epic, « Rejoindre un match » contacte le serveur. Le joueur attend sous un
overlay, puis arrive sur l'arène en sachant s'il est le joueur 1 ou le joueur 2. Si le
serveur ne répond pas, il le voit et peut réessayer. Les messages suivent
`contracts/canal-joueur.md` (home repo) ; les écrans suivent la maquette I26-M1
(`initiatives/5-realisation/I26-rejoindre-un-match/maquettes/`).

## Ce que le client livre

1. **Lien vers le serveur** : un autoload (par exemple `ServerLink`, dans
   `scripts/net/`) qui ouvre la connexion avec `WebSocketPeer`, la fait vivre, envoie
   `rejoindre_match` dans son enveloppe (`command_id` à partir de 1), lit les enveloppes
   reçues et émet un signal par message : `en_attente`, `match_trouve(joueur)`, `erreur`,
   ainsi qu'un signal d'échec de connexion. La lecture d'une trame (texte JSON → message)
   est une fonction pure, testable sans réseau.
2. **Adresse du serveur** : `ws://localhost:8080/ws` par défaut, remplacée par l'argument
   `--server=ws://hôte:port/ws` placé après `--`, lu comme `--screenshot=` dans
   `scenes/home/` (I26-B18).
3. **Overlay de messages** : une scène réutilisable, au-dessus de tout écran, conforme à
   I26-M1 : voile sur tout l'écran, couleur d'encre du jeu (`06040f`) à 80 % d'opacité,
   titre en Michroma, or (`ffd15a`) ou rouge pour une erreur, texte, un bouton
   facultatif ; il apparaît et disparaît en fondu de 0,5 s (I26-B14). Il survit au
   changement de scène accueil → arène.
4. **Parcours** :
   - le bouton « Rejoindre un match » de l'accueil n'ouvre plus l'arène : il demande au
     lien de rejoindre et affiche « En attente d'un adversaire… » (roue qui tourne) ;
     un double clic n'envoie qu'une demande (I26-B1) ;
   - `match_trouve` ouvre l'arène existante (`scenes/mockup/`, composition inchangée)
     sous l'overlay « Adversaire trouvé — Vous êtes le Joueur N », qui s'efface seul au
     bout de 2 s ; un repère « Joueur N » reste affiché dans l'arène, en bas à gauche
     (I26-B5) ;
   - l'échec de la connexion affiche « Serveur injoignable » avec « OK », qui ferme
     l'overlay ; le bouton de l'accueil redevient utilisable (I26-B11).
   Le bouton « Annuler » de l'attente est posé, mais son effet relève d'I26-E2.
5. **Mode automatique, pour le scénario de bout en bout** (S6) : avec les arguments
   `--rejoindre` et `--rapport=<fichier>`, le client clique de lui-même sur « Rejoindre
   un match », écrit dans le fichier le numéro reçu (`{"joueur": 1}`) à la réception de
   `match_trouve`, puis quitte. Il doit marcher en `--headless`. Il quitte avec un code
   non nul s'il n'a pas reçu `match_trouve` au bout de 30 s.

Hors de cet epic (I26-E2) : l'effet d'« Annuler », « Adversaire déconnecté », le retour à
l'accueil.

## Preuve attendue

Des tests GUT headless dans `test/unit/`, sans réseau (I26-B20) :
- la lecture des trames : chaque message du contrat est reconnu avec ses champs ; une
  trame illisible est signalée sans planter ; l'enveloppe envoyée pour
  `rejoindre_match` est celle du contrat ;
- l'argument `--server=` remplace l'adresse par défaut ;
- le parcours, piloté par une doublure du lien écrite à la main (signaux émis à la
  main) : clic → overlay d'attente ; `match_trouve(2)` → arène, overlay « Vous êtes le
  Joueur 2 », repère « Joueur 2 » ; échec de connexion → overlay « Serveur injoignable »,
  puis « OK » → accueil utilisable ;
- l'overlay : opacité 80 %, fondu de 0,5 s, effacement automatique au bout de 2 s.

Et, à la main, S1, S3 et S4 avec `make run-server` et deux `make run-client`.
`make lint`, `make typecheck` et `make test` passent.
