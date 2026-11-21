# I17 — Questions

## Questions et réponses

### Q1 — Qui réécrit la note de client-shows-card-texts dans system/relations.yaml (S5) ?

*(architecte projet)* S5 exige qu'à la livraison, la note de la relation décrive data/cards.json devenu un dictionnaire structuré. Ce fichier est dans le home repo, que les composants ne modifient pas. J'ai mis S5 sur I17-E1-CL : le client livre la description du fichier tel qu'il est devenu, avec l'emplacement des fiches d'unités. La modification elle-même reste dans le home repo.

**Recommandation :** La réécriture se fait dans le home repo au moment où l'usine clôt l'epic projet, à partir de la description livrée par le client. Aucun ticket composant n'écrit dans relations.yaml.
**Réponse :** D'accord avec la recommandation : La réécriture se fait dans le home repo au moment où l'usine clôt l'epic projet, à partir de la description livrée par le client. Aucun ticket composant n'écrit dans relations.yaml.

### Q2 — À quoi comparer l'écran de match pour prouver que rien n'a changé ?

*(relecteur de client)* Le catalogue et le nouvel affichage des cartes sont déjà en place, et l'écran de match les utilise déjà. Pour vérifier que les joueurs voient les mêmes unités et les mêmes textes de cartes qu'avant (scénario S4, sans régression), il faut une version « d'avant » à laquelle comparer. Sans elle, le test ne prouve pas grand-chose.

Choix technique : tu peux le confier à l'analyste.

Options :
- **Confier à l'analyste la correction proposée** : La référence est la liste des unités et les textes des cartes juste avant la refonte. Le test vérifie que l'écran de match s'ouvre sans erreur et montre les mêmes unités. Si cette version n'existe pas, l'état actuel sert de référence.
- **Prendre directement l'état actuel comme référence** : C'est plus simple, mais une régression déjà introduite par la refonte passerait inaperçue.

Détail technique : Comment prouver la non-régression de S4 alors que la refonte est déjà faite ? — Le dictionnaire, CardCatalog, CardView et la planche existent déjà, et l'écran de match passe déjà par CardCatalog. Pour comparer à « avant », il faut une référence antérieure.

**Recommandation :** Confier la décision à l'analyste. Comparer à la version d'avant la refonte est la seule façon de repérer une carte ou une unité modifiée par erreur, et il n'y a pas de choix de produit à faire.
**Réponse :** D'accord avec la recommandation : Confier la décision à l'analyste. Comparer à la version d'avant la refonte est la seule façon de repérer une carte ou une unité modifiée par erreur, et il n'y a pas de choix de produit à faire.

### Q3 — Les combos doivent-ils avoir leur propre gemme de porteur ?

*(architecte projet)* Dans data/cards.json, les 4 combos portent `tier: generique`, donc CardView leur donne la gemme des cartes génériques. C'est conforme au grilling, qui ne connaît que trois porteurs (Générique / Rôle / Propre), et à l'epic, qui compte les combos par famille. Mais le game design v0.16 décrit trois familles distinctes dans le deck : le socle générique, les cartes d'unité et les combos. Sur la planche, un combo porte donc la même gemme qu'une carte générique. Le cadre de la famille combo le distingue quand même.

**Recommandation :** Garder la gemme générique pour les combos dans I17-E1. Le cadre de famille suffit à les distinguer, et la preuve S2 compare la gemme à la valeur résolue, donc elle tiendra si la valeur change. Si le game designer veut une gemme propre aux combos, l'ajouter plus tard en changeant les données (un nouveau tier ou une gemme par famille), dans un epic suivant ou au moment de valider la planche (I17-E2).
**Réponse :** D'accord avec la recommandation : Garder la gemme générique pour les combos dans I17-E1. Le cadre de famille suffit à les distinguer, et la preuve S2 compare la gemme à la valeur résolue, donc elle tiendra si la valeur change. Si le game designer veut une gemme propre aux combos, l'ajouter plus tard en changeant les données (un nouveau tier ou une gemme par famille), dans un epic suivant ou au moment de valider la planche (I17-E2).

### Q4 — Le découpage en projection de I17-E1 n'aboutit pas après 3 essais

*(usine)* Remarques restantes du dernier contrôle :
- **Quel exemple garder pour prouver qu'un changement de famille se voit sur les cartes ?** — L'epic donne comme exemple « changer la couleur d'une famille », mais dans le catalogue une famille n'a pas de couleur : elle n'a qu'un nom et un cadre. La couleur vient du type de carte. Si on ne fait rien, la vérification prévue s'appuie sur une donnée qui n'existe pas et ne peut pas être écrite.
- **Quel repère utiliser pour toucher toutes les cartes d'un même niveau ?** — La vérification prévoit de changer le nom d'un niveau de porteur et de voir toutes ses cartes changer. Or ce nom n'apparaît que sur 5 cartes génériques : les cartes de rôle, les cartes propres à une unité et les combos affichent leur porteur autrement. Pour atteindre toutes les cartes d'un niveau, il faut se servir de la gemme du niveau.
- **Une version du catalogue d'avant la refonte existe-t-elle vraiment ?** — Le scénario S4 compare sans doute le catalogue d'avant la refonte avec celui d'après. Faute d'accès à l'historique du projet, le relecteur n'a pas pu vérifier que cette ancienne version existe. Si elle n'existe pas, la vérification prévue ne pourra pas être faite comme décrit.
- **Accepter une vérification sensible aux changements de mise en page de la carte ?** — Pour vérifier ce qu'affiche une carte (image, textes, badges de statistiques, motif), le test devra fouiller les éléments graphiques de la carte un par un, car la carte n'expose pas ses parties autrement. Ce n'est pas bloquant, mais si on réorganise un jour la mise en page de la carte, ces tests casseront même si l'affichage reste juste.

Détail technique :
* I17-E1-CL (client) : S3 : les familles n'ont pas de couleur dans data/cards.json. `families` ne porte que label et frame, et la couleur est portée par `types.<t>.color`. L'exemple « couleur d'une famille » de l'epic ne correspond donc à aucune donnée. La preuve doit utiliser `families.<f>.frame` ou `types.<t>.color`. C'est à l'architecte de corriger l'exemple, si besoin.
* I17-E1-CL (client) : S3 : `tiers.<t>.label` n'est visible que pour les 5 cartes génériques hors combos. Pour les cartes de rôle et propres, le porteur affiché vient de `roles` ou de l'unité, et pour les combos il vient de `scope`. Pour toucher toutes les cartes d'un porteur, il faut prendre `tiers.<t>.gem`.
* I17-E1-CL (client) : S4 : je n'ai pas pu consulter l'historique git (lecture seule, sans shell). Je n'ai donc pas vérifié qu'une version de data/cards.json antérieure à la refonte existe. Celui qui écrit la preuve doit le faire, comme le prévoit la part.
* I17-E1-CL (client) : CardView n'expose pas ses parties autrement que par ses nœuds enfants. La preuve S2/S3 devra parcourir l'arbre (TextureRect, Label, CardStatBadge, CardPattern) une fois le nœud entré dans l'arbre, car tout est construit dans `_ready`. Ce n'est pas bloquant, mais un test fragile si la mise en page change.

**Recommandation :** Si ces remarques te semblent secondaires, valide le découpage en l'état. Sinon, réponds en disant quoi faire (par exemple « applique les corrections proposées ») : l'analyste reprend avec ta réponse (3 nouveaux essais).
**Réponse :** on avance sans tenir compte de ces remarques. j'essentiel est de pouvoir afficher les cartes dans le client, avec une mécanique de composant valide pour le moment

### Q5 — Le découpage en projection de I17-E1 n'aboutit pas après 3 essais

*(usine)* Remarques restantes du dernier contrôle :
- **Quel réglage du catalogue utiliser pour prouver qu'une modification se voit sur la carte ?** — L'epic prend pour exemple « changer la couleur d'une famille », mais dans le catalogue une famille n'a qu'un nom et un cadre : la couleur appartient au type de carte. La vérification prévue ne pourrait donc pas s'écrire en l'état.
- **Quel réglage modifier pour changer toutes les cartes d'un même porteur ?** — Le nom du porteur défini au niveau du palier ne s'affiche que sur 5 cartes génériques. Sur les cartes de rôle, les cartes propres à une unité et les combos, le nom affiché vient d'ailleurs. Une vérification fondée sur ce nom ne toucherait donc presque aucune carte, alors que la gemme du palier, elle, apparaît sur toutes.
- **Existe-t-il bien une version du catalogue antérieure à la refonte ?** — Le relecteur n'a pas pu consulter l'historique des versions. Il ne sait donc pas si l'ancien catalogue, celui d'avant la refonte, est encore disponible. Si je comprends bien, la vérification S4 en a besoin, sans doute pour comparer avant et après. Si cette version n'existe pas, la vérification ne pourra pas s'écrire comme prévu.
- **Faut-il rendre les éléments d'une carte plus faciles à vérifier ?** — Pour contrôler ce qu'affiche une carte (image, textes, pastilles de statistiques, motif), les tests doivent fouiller ses éléments internes, et ceux-ci n'existent qu'une fois la carte affichée. Rien ne bloque aujourd'hui, mais ces tests casseront dès qu'on modifiera la mise en page de la carte.

Détail technique :
* I17-E1-CL (client) : S3 : les familles n'ont pas de couleur dans data/cards.json. `families` ne porte que label et frame, et la couleur est portée par `types.<t>.color`. L'exemple « couleur d'une famille » de l'epic ne correspond donc à aucune donnée. La preuve doit utiliser `families.<f>.frame` ou `types.<t>.color`. C'est à l'architecte de corriger l'exemple, si besoin.
* I17-E1-CL (client) : S3 : `tiers.<t>.label` n'est visible que pour les 5 cartes génériques hors combos. Pour les cartes de rôle et propres, le porteur affiché vient de `roles` ou de l'unité, et pour les combos il vient de `scope`. Pour toucher toutes les cartes d'un porteur, il faut prendre `tiers.<t>.gem`.
* I17-E1-CL (client) : S4 : je n'ai pas pu consulter l'historique git (lecture seule, sans shell). Je n'ai donc pas vérifié qu'une version de data/cards.json antérieure à la refonte existe. Celui qui écrit la preuve doit le faire, comme le prévoit la part.
* I17-E1-CL (client) : CardView n'expose pas ses parties autrement que par ses nœuds enfants. La preuve S2/S3 devra parcourir l'arbre (TextureRect, Label, CardStatBadge, CardPattern) une fois le nœud entré dans l'arbre, car tout est construit dans `_ready`. Ce n'est pas bloquant, mais un test fragile si la mise en page change.

**Recommandation :** Si ces remarques te semblent secondaires, valide le découpage en l'état. Sinon, réponds en disant quoi faire (par exemple « applique les corrections proposées ») : l'analyste reprend avec ta réponse (3 nouveaux essais).
**Réponse :** je ne comprends pas ce que tu essaye de faire. C'est quand même pas compliqué à l'issu de cette carte on doit avoir un composant godot auquel on donne une référence de carte et il va chercher ses composants graphique dans un dictionnaire json, ainsi les définitions sont centralisées. point

### Q6 — Comment S4 lit-il la référence d'avant la refonte ?

*(relecteur de client)* Le test GUT peut appeler `git show 84bb030:data/cards.json` par OS.execute, ce qui dépend de git et de l'historique au moment du test. Il peut aussi comparer à une copie figée du fichier en fixture.

**Recommandation :** Figer la version de 84bb030 en fixture (test/fixtures/cards_84bb030.json), avec le commit nommé dans le test et dans la fixture. Le test reste ainsi headless et déterministe.
**Réponse :** c'est quoi S4 ? de quoi tu me parle ?

### Q7 — Une carte affichée à partir de son identifiant peut-elle venir d'un autre catalogue que celui du jeu ?

*(relecteur de client)* Pour afficher une carte à partir de son seul identifiant, il faut aller chercher sa description dans le catalogue des cartes, aujourd'hui lu depuis les fichiers du jeu. Un test prévu doit changer une valeur commune à toutes les cartes dans un catalogue préparé pour l'occasion. Si l'affichage lit toujours le catalogue du jeu, ce test ne peut pas vérifier que la carte affichée suit le changement.

Choix technique : tu peux le confier à l'analyste.

Options :
- **Confier à l'analyste la correction proposée** : On peut fournir un autre catalogue au moment d'afficher une carte. Sans rien fournir, le jeu utilise son catalogue habituel, lu une seule fois au premier besoin et partagé par toutes les cartes.
- **Garder un seul catalogue, celui des fichiers du jeu** : Le test prévu ne peut pas être écrit tel quel : il faudra le revoir ou modifier les fichiers du jeu pour tester.

Détail technique : Quel catalogue utilise make_by_id ? — S3 doit modifier une valeur commune « dans le dictionnaire chargé en test » : l'entrée par identifiant doit donc pouvoir utiliser un catalogue autre que celui lu sur disque.

**Recommandation :** Confier la correction à l'analyste : le comportement ne change pas pour le joueur, et le test devient possible.
**Réponse :** D'accord avec la recommandation : Confier la correction à l'analyste : le comportement ne change pas pour le joueur, et le test devient possible.

### Q8 — Le découpage en projection de I17-E1 n'aboutit pas après 3 essais

*(usine)* Remarques restantes du dernier contrôle :
- **Le travail porte-t-il sur les compléments plutôt que sur une refonte du catalogue ?** — Le catalogue des cartes (ses 33 cartes et la planche qui les présente) existe déjà. Selon le relecteur, il reste trois choses à faire : ouvrir une carte à partir de son identifiant, donner à chaque catalogue sa propre légende des motifs, et ajouter les preuves S1 à S4, puisqu'aucun test ne vérifie aujourd'hui l'affichage d'une carte, la planche ou l'écran de match. Sans cette précision, on risque de refaire des données qui fonctionnent déjà.
- **La version de référence d'avant la refonte existe-t-elle bien ?** — D'après ce que je comprends, la preuve S4 compare l'affichage actuel à une version enregistrée juste avant la refonte des cartes. Le relecteur n'a pas pu vérifier que cette version existe, ni qu'elle précède directement la refonte. Si elle est absente ou mal choisie, la comparaison ne prouverait rien.
- **Comment vérifier que l'écran de match montre les bonnes cartes ?** — L'écran de match n'affiche pas les cartes avec le même composant que la planche. Il transmet directement les cartes et les fiches d'unités au bandeau de jeu. Le relecteur propose de comparer ces données transmises à la référence d'avant la refonte, plutôt que d'inspecter ce qui est dessiné à l'écran.

Détail technique :
* I17-E1-CL (client) : Le dictionnaire, ses 33 cartes et la planche existent déjà. Le travail porte donc sur l'entrée par identifiant, la légende des motifs propre à chaque catalogue, et les preuves S1 à S4 (aucun test ne couvre aujourd'hui CardView, la planche ou l'écran de match). Ce n'est pas une refonte des données.
* I17-E1-CL (client) : S4 : je n'ai pas pu lancer git pendant cette relecture. Je ne sais donc ni si le commit 84bb030 existe, ni s'il est le parent de la refonte 7919dd9. Le ticket qui écrit cette preuve le vérifiera en premier, comme la part le prévoit.
* I17-E1-CL (client) : S4 côté écran de match : il transmet les cartes et les unités au HUD sans passer par CardView. Le plus simple est de comparer ce que le HUD reçoit (cartes résolues et fiches d'unités) à la référence figée, plutôt que de lire des nœuds affichés.

**Recommandation :** Tranche chaque remarque dans ta réponse (par exemple « applique les corrections proposées », ou quel choix retenir) : l'architecte projet reprend la projection avec ta réponse (3 nouveaux essais).
**Réponse :**
