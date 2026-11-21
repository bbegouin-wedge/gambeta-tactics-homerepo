# I25 — Grilling

## Questions et réponses

### Q1 — « Rejoindre un match » ouvre-t-il directement l'écran de match existant (navigation locale), ou doit-il déjà contacter le serveur pour rejoindre une vraie partie ?

D'après la projection I17-E1-CL, le client a aujourd'hui un écran de match maquetté, `scenes/mockup/mockup.tscn`, qui se construit depuis `data/cards.json` sans logique de jeu. Le serveur, lui, n'expose encore rien : la relation `client-plays-on-backend` est `planned`, sans contrat (system/relations.yaml). Créer ou rejoindre une partie (`CreateMatch` / `JoinMatch`), le protocole et le `ServerLink` du client sont prévus dans I21 (runtime et lobby), I22 (protocole et gateway) et I23 (client Godot de la boucle), toutes au backlog. Si le bouton doit contacter le serveur, I25 dépend de ces trois initiatives et touche aussi le backend. S'il ne fait qu'ouvrir l'écran, I25 ne concerne que le client et peut être livrée tout de suite. La réponse décide des composants concernés, des cas d'erreur à couvrir (serveur injoignable, attente d'un adversaire) et des maquettes à faire.

**Recommandation :** La navigation locale : le bouton ouvre l'écran de match existant (`scenes/mockup/mockup.tscn`), sans appel au serveur. Brancher le vrai « rejoindre » (file d'attente, connexion, erreurs) reviendrait à I21, I22 et I23 quand le contrat existera. I25 resterait alors une initiative du seul client, petite et livrable sans attendre.
**Réponse :** D'accord avec la recommandation : La navigation locale : le bouton ouvre l'écran de match existant (`scenes/mockup/mockup.tscn`), sans appel au serveur. Brancher le vrai « rejoindre » (file d'attente, connexion, erreurs) reviendrait à I21, I22 et I23 quand le contrat existera. I25 resterait alors une initiative du seul client, petite et livrable sans attendre.

### Q2 — Une fois dans l'arène, le joueur peut-il revenir à la page d'accueil, ou le passage accueil → arène est-il à sens unique ?

La Q1 a tranché : le bouton « Rejoindre un match » ouvre l'écran de match existant, `scenes/mockup/mockup.tscn`, sans appel au serveur. Cet écran n'a aujourd'hui ni logique de jeu ni fin de match (projection I17-E1-CL, composant `client` : « maquette de l'écran de match, sans logique de jeu »). Il faut donc savoir si I25 ajoute aussi un chemin de retour (bouton ou touche « Quitter le match » dans l'arène, qui ramène à l'accueil). La réponse décide de deux choses. D'abord le périmètre : I25 touche-t-elle seulement une nouvelle scène, ou modifie-t-elle aussi l'écran de match ? Ensuite les cas limites : que devient l'état de l'arène au retour, et peut-on la rouvrir plusieurs fois ? Le vrai retour en fin de match (victoire, abandon, déconnexion) relève de la boucle de jeu prévue dans I21 à I23, qui sont au backlog.

**Recommandation :** Sens unique : I25 ne modifie pas l'écran de match, et quitter l'arène revient à fermer le jeu. Le retour à l'accueil prend son sens avec une vraie fin de match (abandon, victoire), qui appartient à la boucle de jeu (I21 à I23). L'ajouter maintenant obligerait à toucher la maquette de l'arène pour un parcours qui n'existe pas encore.
**Réponse :** navigation a sens unique pour le moment, de toutes façons on aura très vite plusieurs écrans qui s'intercalent entre la page d'accueil et la page de match

### Q3 — En plus du bouton « Rejoindre un match », la page d'accueil affiche-t-elle le nom du jeu sur un fond tiré d'OpenDuelyst, ou seulement le bouton sur un fond uni ?

Les Q1 et Q2 ont tranché le parcours : la page d'accueil se charge en premier, le bouton ouvre l'écran de match (`scenes/mockup/mockup.tscn`) sans appel au serveur, et on ne revient pas en arrière. Il reste à fixer ce que la page montre, parce que la maquette en dépend. L'idée parle d'« un seul bouton », ce qui n'exclut pas un titre ou un fond. Le composant `client` (system/components.yaml) génère déjà ses assets depuis OpenDuelyst, qui est sous licence CC0 : un fond d'arène est donc disponible sans rien produire. En revanche, le nom et le logo « Duelyst » ne sont pas couverts par cette licence, donc on ne peut pas reprendre leur logo. La réponse fixe la liste des éléments de la page, et donc les besoins à vérifier et la maquette à faire.

**Recommandation :** Le nom « Gambeta Tactics » en texte, pas de logo, sur un fond d'arène tiré des assets OpenDuelyst que le client importe déjà, avec le bouton unique « Rejoindre un match ». Le joueur reconnaît ainsi le jeu dès le premier écran, sans créer d'asset, sans risque de licence et sans ajouter d'autre bouton (pas de « Quitter » ni d'« Options »).
**Réponse :** D'accord avec la recommandation : Le nom « Gambeta Tactics » en texte, pas de logo, sur un fond d'arène tiré des assets OpenDuelyst que le client importe déjà, avec le bouton unique « Rejoindre un match ». Le joueur reconnaît ainsi le jeu dès le premier écran, sans créer d'asset, sans risque de licence et sans ajouter d'autre bouton (pas de « Quitter » ni d'« Options »).

## Synthèse

I25 ajoute au composant `client` (Godot) une page d'accueil qui s'ouvre en premier au lancement du jeu. Elle affiche le nom « Gambeta Tactics » en texte sur un fond d'arène tiré d'OpenDuelyst, avec un seul bouton « Rejoindre un match ». Ce bouton ouvre l'écran de match existant (`scenes/mockup/mockup.tscn`) sans appeler le serveur, et on ne peut pas revenir à l'accueil. Seul le client est concerné : aucun contrat et aucune relation ne changent. Deux points sont à vérifier dans le dépôt du client, que je n'ai pas pu lire depuis ce dépôt : quelle scène se lance aujourd'hui au démarrage (probablement `mockup.tscn`), et quels fonds d'arène sont déjà importés par `scripts/duelyst_import/`.

## Besoins
- **I25-B1** — Au lancement du jeu, le client ouvre la page d'accueil, avant tout autre écran.
- **I25-B2** — La page d'accueil affiche le nom « Gambeta Tactics » en texte, sans logo.
- **I25-B3** — Le fond de la page d'accueil est un fond d'arène tiré des assets OpenDuelyst que le client importe déjà (`scripts/duelyst_import/`).
- **I25-B4** — La page d'accueil a un seul bouton, « Rejoindre un match ».
- **I25-B5** — Un clic sur « Rejoindre un match » remplace la page d'accueil par l'écran de match existant (`scenes/mockup/mockup.tscn`).
- **I25-B6** — L'écran de match ouvert depuis l'accueil s'affiche comme quand on le lance directement, construit depuis `data/cards.json`.

## Règles et cas d'erreur
- **I25-B7** — « Rejoindre un match » n'appelle pas le serveur : c'est une navigation locale dans le client (Q1).
- **I25-B8** — Le passage de l'accueil à l'écran de match est à sens unique : l'écran de match n'a ni bouton ni touche pour revenir à l'accueil (Q2).
- **I25-B9** — I25 ne modifie pas l'écran de match (`scenes/mockup/mockup.tscn`) (Q2).
- **I25-B10** — La page d'accueil n'a pas d'autre élément interactif que « Rejoindre un match » : pas de « Quitter » ni d'« Options » (Q3).
- **I25-B11** — Aucun nom ni logo « Duelyst » n'apparaît sur la page d'accueil, car la licence CC0 d'OpenDuelyst ne les couvre pas (system/components.yaml, open-duelyst).
- **I25-B12** — Aucun nouvel asset graphique n'est créé : le fond vient des assets OpenDuelyst déjà importés (Q3).
- **I25-B13** — Si on clique plusieurs fois de suite sur « Rejoindre un match », un seul écran de match s'ouvre.

## Hors périmètre
- Rejoindre une vraie partie (file d'attente, `CreateMatch` / `JoinMatch`, connexion au serveur, attente d'un adversaire, serveur injoignable) : initiatives I21, I22 et I23.
- Revenir à l'accueil depuis l'arène et gérer la fin de match (victoire, abandon, déconnexion) : boucle de jeu, I21 à I23.
- Les écrans qui viendront entre l'accueil et le match (Q2) : initiatives à venir.
- Tout changement côté `backend`, côté contrats (`contracts/`) ou dans `system/relations.yaml`.
- Le logo du jeu, les options, le bouton « Quitter », les comptes et l'authentification.
