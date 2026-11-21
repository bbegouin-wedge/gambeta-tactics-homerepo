# I25 — Questions

## Questions et réponses

### Q1 — Quel décor d'arène mettre en fond de la page d'accueil ?

*(designer UX)* La page d'accueil doit afficher un décor d'arène venu du jeu d'origine, sans préciser lequel, et le designer ne peut pas voir lesquels sont déjà disponibles dans le jeu. Si on ne choisit pas, l'accueil garde le simple dégradé de couleur de la maquette.

Choix de produit : c'est à toi de trancher.

Options :
- **Reprendre le décor de l'écran de match** : Le passage de l'accueil au match paraît naturel, sans ajouter d'image ; s'il n'y en a pas, on prend le premier décor disponible et on le note.
- **Choisir toi-même un décor précis** : Tu fixes l'ambiance de l'accueil, mais il faut vérifier que ce décor est déjà disponible.
- **Garder le dégradé pour l'instant** : La page est plus pauvre que prévu et le décor reste à faire plus tard.

Détail technique : Quel fond d'arène OpenDuelyst utiliser ? — I25-B3 demande un fond d'arène déjà importé par scripts/duelyst_import/, sans dire lequel. Je ne peux pas lire depuis le home repo les fonds que le client a vraiment importés. La maquette met un dégradé à la place.

**Recommandation :** Reprendre le décor de l'écran de match : l'enchaînement reste cohérent et on n'ajoute aucune image.
**Réponse :** propose moi trois alternatives de page d'accueil en utilisant les assets de duelyst

### Q2 — Que voit le joueur juste après avoir cliqué « Rejoindre un match » ?

*(designer UX)* Un seul match doit s'ouvrir, même si le joueur clique plusieurs fois, mais rien ne dit ce qu'il voit entre le clic et l'arrivée du match. La maquette grise le bouton dès le premier clic, sans message d'attente.

Choix de produit : c'est à toi de trancher.

Options :
- **Griser le bouton, sans message** : Simple et suffisant si le match s'affiche presque tout de suite, ce qui est attendu ici.
- **Griser le bouton et afficher « Chargement… »** : Le joueur est rassuré si l'attente dure, au prix d'un petit élément en plus.

Détail technique : Comment empêcher un double clic sur « Rejoindre un match » ? — I25-B13 exige qu'un seul écran de match s'ouvre si l'on clique plusieurs fois. Le grilling ne dit pas ce que le joueur voit entre le clic et l'affichage du match. La maquette (section 2) montre le bouton grisé dès le premier clic, sans texte d'attente.

**Recommandation :** Griser le bouton sans message : le passage au match se fait sur la machine du joueur et devrait être quasi immédiat.
**Réponse :** propose moi trois versions de pages d'accueil basé sur différents assets de duelyst, dispo sur ma machine

### Q3 — Le joueur peut-il lancer un match au clavier (Entrée ou Espace) ?

*(designer UX)* La page n'a qu'un bouton, « Rejoindre un match », et rien ne dit s'il répond au clavier. Par défaut dans le moteur du jeu, un bouton sélectionné réagit déjà à Entrée et Espace.

Choix de produit : c'est à toi de trancher.

Options :
- **Oui, bouton sélectionné à l'ouverture** : Le joueur peut appuyer sur Entrée pour jouer tout de suite ; c'est le comportement natif, rien à ajouter.
- **Non, souris seulement** : Il faut désactiver un comportement natif, et les joueurs au clavier sont gênés.

Détail technique : Le clavier peut-il activer le bouton (Entrée / Espace) ? — I25-B10 limite la page au seul élément interactif « Rejoindre un match », sans préciser s'il répond au clavier. Dans Godot, un bouton qui a le focus réagit par défaut à ui_accept (Entrée ou Espace). La maquette montre le bouton avec le focus à l'ouverture.

**Recommandation :** Oui : c'est gratuit, plus pratique, et cela n'ajoute aucun autre élément sur la page.
**Réponse :** D'accord avec la recommandation : Oui : c'est gratuit, plus pratique, et cela n'ajoute aucun autre élément sur la page.

### Q4 — Quelle police et quelle disposition pour le titre et le bouton ?

*(designer UX)* Aucune nouvelle image ni police ne doit être ajoutée, et la place du titre et du bouton n'est pas fixée. La maquette met le titre centré dans le haut de l'écran et le bouton centré un peu sous le milieu, par-dessus le décor.

Choix de produit : c'est à toi de trancher.

Options :
- **Police déjà présente dans le jeu, disposition de la maquette** : On respecte l'interdiction d'ajouter des éléments graphiques ; à défaut d'une police existante, on prend celle par défaut du moteur.
- **Ajouter une police dédiée au titre** : Titre plus marquant, mais cela contredit la règle de n'ajouter aucun élément graphique.

Détail technique : Quelle police et quelle disposition pour le titre ? — I25-B12 interdit tout nouvel asset graphique. Une police importée en serait un. Le grilling ne fixe pas non plus la place du titre ni celle du bouton. La maquette centre le titre dans le tiers haut et le bouton un peu sous le milieu de l'écran.

**Recommandation :** Reprendre une police déjà présente (sinon celle par défaut) et garder la disposition de la maquette : cela respecte le périmètre sans rien ajouter.
**Réponse :** D'accord avec la recommandation : Reprendre une police déjà présente (sinon celle par défaut) et garder la disposition de la maquette : cela respecte le périmètre sans rien ajouter.

### Q5 — Quel décor choisir pour la page d'accueil : A, B ou C ?

*(designer UX)* Le designer propose trois fonds pour l'accueil. A reprend le décor de l'écran de match sans la grille de jeu, et ce décor est sans doute déjà disponible dans le jeu. B utilise un fond de menu qu'il faudrait d'abord ajouter au jeu. C montre une arène avec deux unités qui attendent de chaque côté du bouton, ce qui ajoute un élément que le besoin initial ne prévoyait pas.

Choix de produit : c'est à toi de trancher.

Options :
- **Variante A (décor du match)** : Rien à changer dans le besoin, et l'accueil est prêt sans travail en plus.
- **Variante C (arène avec deux unités)** : L'accueil est plus vivant, mais il faut ajouter au besoin « deux unités décoratives, prises parmi celles déjà présentes dans le jeu ».
- **Variante B (fond de menu)** : Il faut d'abord ajouter ce fond au jeu, et deux exigences du besoin changent. L'initiative grossit d'autant.

Détail technique : Quelle variante de page d'accueil retenir : A, B ou C ? — La maquette I25-M1 montre les trois propositions demandées. A : le décor de l'écran de match, sans sa grille de jeu (maps/), a priori déjà importé. B : un fond de menu d'OpenDuelyst (play/) qui n'est probablement pas importé ; le retenir change I25-B3 et I25-B12, car il faudrait étendre l'import du client. C : un décor d'arène avec deux unités en attente de part et d'autre du bouton (units/) ; ces unités sont un élément décoratif en plus du fond, que le grilling ne prévoit pas (I25-B3 ne parle que du fond), donc un léger élargissement du besoin.

**Recommandation :** Prendre A : c'est la seule variante qui ne change rien au besoin, et cet accueil sera de toute façon revu quand d'autres écrans viendront avant lui. On peut garder B pour un futur menu principal.
**Réponse :** ou est ce que je peux voir les maquettes ?

### Q6 — Après le clic sur « Rejoindre un match », faut-il afficher « Chargement… » ?

*(designer UX)* Si le joueur clique plusieurs fois, un seul match doit s'ouvrir. Pour cela, la maquette grise le bouton dès le premier clic, sans texte d'attente. Ta réponse précédente ne tranchait pas ce point. Aujourd'hui, l'arrivée dans le match se fait sur l'ordinateur du joueur, sans serveur, donc elle devrait être presque immédiate.

Choix de produit : c'est à toi de trancher.

Options :
- **Griser le bouton seulement** : L'écran reste sobre. Si le passage au match prend un peu de temps, le joueur ne voit aucun message d'attente.
- **Griser le bouton et afficher « Chargement… »** : Le joueur sait que son clic a été pris en compte, mais le message ne s'affichera qu'une fraction de seconde tant qu'il n'y a pas de serveur.

Détail technique : Après le clic sur « Rejoindre un match », griser le bouton seul ou ajouter « Chargement… » ? — Ta réponse à cette question (Q2 de questions.md) demandait les trois variantes de page et ne tranchait pas ce point. I25-B13 impose qu'un seul match s'ouvre même si le joueur clique plusieurs fois. La maquette (section 2) montre le bouton grisé dès le premier clic, sans texte d'attente. Le passage au match se fait sur la machine du joueur, sans serveur (I25-B7).

**Recommandation :** Griser le bouton sans message : le passage au match est presque immédiat. On ajoutera « Chargement… » quand rejoindre un match passera par le serveur, avec les initiatives I21 à I23.
**Réponse :** D'accord avec la recommandation : Griser le bouton sans message : le passage au match est presque immédiat. On ajoutera « Chargement… » quand rejoindre un match passera par le serveur, avec les initiatives I21 à I23.

### Q7 — Quel décor choisir pour la page d'accueil : A, B ou C ?

*(designer UX)* La page d'accueil a besoin d'un décor de fond. Les trois propositions sont esquissées dans la section 1 de la maquette de la page d'accueil, et les vraies images sont dans les fichiers OpenDuelyst de ta machine. A reprend le décor de l'écran de match sans la grille de jeu, B est un fond de menu qui n'est pas encore dans le jeu, et C montre une arène avec deux unités qui attendent de chaque côté du bouton.

Choix de produit : c'est à toi de trancher.

Options :
- **A : le décor de l'écran de match, sans la grille** : Ce décor est a priori déjà dans le jeu : le besoin ne change pas et l'initiative ne grossit pas.
- **B : un nouveau fond de menu** : Il faut d'abord ajouter ce fond au jeu : deux tickets de l'initiative changent et le travail augmente.
- **C : une arène avec deux unités de chaque côté du bouton** : Il faut ajouter au besoin deux unités décoratives, prises parmi celles qui sont déjà dans le jeu.

Détail technique : Quel décor choisir pour la page d'accueil : A, B ou C ? — Pour voir les trois propositions, ouvre dans un navigateur initiatives/3-maquettes/I25-page-d-accueil-gambeta-tactics/maquettes/I25-M1-page-d-accueil.html (section 1). Les décors y sont seulement esquissés : pour les vraies images, regarde les assets OpenDuelyst de ta machine (maps/ pour A et C, play/ pour B, units/ pour les unités de C).

A reprend le décor de l'écran de match, sans la grille de jeu. Ce décor est a priori déjà dans le jeu, donc rien ne change dans le besoin.

B est un fond de menu qu'il faudrait d'abord ajouter au jeu. Ça change I25-B3 et I25-B12 (étendre scripts/duelyst_import/) et ça agrandit l'initiative.

C est une arène avec deux unités qui attendent de chaque côté du bouton. Il faut alors ajouter au besoin « deux unités décoratives, prises parmi celles déjà importées ».

**Recommandation :** Prendre A, comme le propose le designer : c'est le seul décor qui ne change rien au besoin, et l'accueil sera revu quand d'autres écrans viendront s'ajouter. On peut garder B pour un futur menu principal.
**Réponse :** ou est la maquette a valider ?

### Q8 — Quel décor choisir pour la page d'accueil : A, B ou C ?

*(designer UX)* La maquette propose trois décors de page d'accueil, tous tirés d'arènes qui existent déjà dans le jeu : A reprend l'arène du match (fond clair, avec un léger voile pour qu'on lise le titre), B est une arène de glace très claire où le titre se lit moins bien, et C est un crépuscule violet et bleu, sombre, où le titre ressort tout seul. Tant que tu n'as pas choisi, la page d'accueil reste bloquée sur trois versions ; les deux non retenues seront retirées.

Choix de produit : c'est à toi de trancher.

Options :
- **C, crépuscule violet et bleu** : Le titre est le plus lisible et l'écran fait le plus « écran de titre », mais le joueur change de décor en passant au match.
- **A, la même arène que le match** : Le joueur reste dans le même décor de l'accueil au match, mais il faut un léger voile pour lire le titre sur ce fond clair.
- **B, arène de glace** : Le décor est très clair et le titre est le moins lisible des trois.

Détail technique : Quelle page d'accueil retenir : A (Lyonar), B (Vanar) ou C (Abyssienne) ? — Les trois propositions sont dans la section 1 de initiatives/3-maquettes/I25-page-d-accueil-gambeta-tactics/maquettes/I25-M1-page-d-accueil.html (à ouvrir dans un navigateur, sur ta machine). Elles utilisent toutes une arène déjà présente dans le client, donc aucune ne change le besoin. A : la même arène que l'écran de match, le passage au match se fait dans le même décor ; c'est un fond clair, avec un léger voile pour lire le titre. B : glace, fond très clair, le titre est le moins lisible des trois. C : crépuscule violet et bleu, fond sombre, le titre ressort sans voile, c'est la plus « écran de titre ». Une fois ton choix fait, les deux autres variantes seront retirées de la maquette.

**Recommandation :** Je prendrais C, comme le propose le designer : c'est la plus lisible et la plus marquante pour un premier écran, sans rien ajouter au jeu. Choisis A si tu tiens à ce que l'accueil et le match se passent dans le même décor.
**Réponse :** améliore la B avec les boutons de l'application, tels qu'ils sont utilisés dans la maquette de l'arène

### Q9 — Comment montrer le survol et le grisé de « Rejoindre un match » ?

*(designer UX)* Sur l'accueil, « Rejoindre un match » reprend l'image du bouton « VALIDER » de l'écran de match, qui n'a ni version survolée ni version grisée. Le bouton doit pourtant réagir quand la souris passe dessus et se griser dès le premier clic pour qu'un seul match s'ouvre, alors que la règle de l'initiative interdit d'ajouter toute nouvelle image.

Choix de produit : c'est à toi de trancher.

Options :
- **Retoucher l'image existante dans le jeu** : Le bouton s'éclaircit un peu au survol, puis se grise et s'assombrit après le clic. On ne crée aucune image et l'écran de match ne change pas.
- **Créer deux nouvelles images (survol et grisé)** : Le rendu est plus soigné, mais il faut lever l'interdiction d'ajouter de nouveaux éléments graphiques.
- **Ne marquer que l'état grisé, sans effet au survol** : C'est plus simple, mais le joueur ne voit pas que le bouton est cliquable avant de cliquer.

Détail technique : Comment montrer que « Rejoindre un match » est survolé, puis grisé après le clic ? — Le bouton reprend l'image du bouton « VALIDER » de l'écran de match. Là-bas, il est seulement affiché : il ne réagit pas au clic et n'a pas d'autre image pour le survol ou l'état grisé. Sur l'accueil, il doit réagir à la souris et se griser dès le premier clic, pour qu'un seul match s'ouvre (I25-B13). Créer de nouvelles images irait contre I25-B12, qui interdit tout nouvel élément graphique. Voir la section 2 de I25-M1-page-d-accueil.html.

**Recommandation :** Retoucher l'image existante dans le jeu : le joueur voit bien les deux états et on respecte la règle « aucun nouvel élément graphique ». Inutile d'ajouter un cadre de sélection, puisque c'est le seul bouton de la page.
**Réponse :** dans les assets tu dois avoir une version "non highlighté" du bouton. Par ailleurs cherche une auter police pour le texte, celle ci est trop commune

### Q10 — Quelle police libre pour le titre et le bouton de l'accueil ?

*(designer UX)* Tu trouves la police actuelle (Lato) trop banale, mais les polices du jeu d'origine sont payantes, donc on ne peut pas les reprendre. Il faut ajouter au jeu une police gratuite, ce qui revient sur deux décisions déjà prises : « utiliser une police déjà présente » et « aucun nouvel élément graphique sur l'accueil ».

Choix de produit : c'est à toi de trancher.

Options :
- **Teko (étroite, en capitales), en version épaisse** : C'est la plus proche du style de la maquette. On ajoute à la règle « sauf une police libre pour le titre et le bouton » et tu télécharges la police.
- **Oswald (étroite aussi), ou une police d'un autre style : Cinzel, aux allures « fantasy », ou Orbitron, plus « science-fiction »** : Même modification de la règle et même téléchargement. Le style s'éloigne plus ou moins de la maquette selon la police choisie.
- **Garder Lato** : Rien n'est ajouté et les décisions déjà prises restent telles quelles, mais le titre garde l'aspect que tu trouves trop banal.

Détail technique : Quelle police libre pour le titre et le bouton ? — Tu trouves Lato trop commune (Q9). Le jeu d'origine n'a que deux autres polices, Trump Gothic Pro et Averta, et elles sont commerciales : le plan de réutilisation des assets interdit de les reprendre. La maquette (section 3 de I25-M1-page-d-accueil.html) montre le style visé, étroit et en capitales, avec Trump Gothic Pro comme simple aperçu. Je n'ai trouvé aucune police libre de ce genre sur ta machine. Il faut donc en ajouter une au client. Ça change la décision de la Q4 (« police déjà présente ») et la règle I25-B12 (« aucun nouvel élément graphique »), puisqu'une police ajoutée en est un. Candidates libres (licence OFL) : Teko et Oswald, étroites, les plus proches des titres du jeu d'origine ; Cinzel, à empattements, plus « fantasy » ; Orbitron, plus « science-fiction ».

**Recommandation :** Prendre Teko : c'est la plus fidèle au style voulu et elle est gratuite. Il faut accepter la petite exception à la règle « aucun nouvel élément graphique ».
**Réponse :** les polices ne se chargent pas

### Q11 — Quelle couleur pour « Rejoindre un match » au repos, au survol, après le clic ?

*(designer UX)* Le bouton reprend celui du jeu d'origine, qui existe en jaune, en jaune lumineux et en gris. La maquette le montre jaune au repos, lumineux au survol de la souris et gris après le clic, mais tu avais peut-être en tête l'inverse : gris au repos et jaune au survol.

Choix de produit : c'est à toi de trancher.

Options :
- **Comme la maquette : jaune, puis lumineux, puis gris** : Le bouton ressemble à « VALIDER » sur l'écran de match, et le gris montre au joueur que son clic a été pris en compte.
- **L'inverse : gris au repos, jaune au survol** : Le bouton est plus discret tant qu'on ne le survole pas, mais il ne ressemble plus à « VALIDER » sur l'écran de match.

Détail technique : Quelle image pour chaque état de « Rejoindre un match » ? — Dans le jeu d'origine, le bouton de l'écran de match existe en trois versions : jaune (celle de « VALIDER » aujourd'hui), jaune lumineuse (`button_end_turn_mine_glow@2x.png`) et grise non éclairée (`button_end_turn_enemy@2x.png`). La maquette (section 2) utilise le jaune au repos, le jaune lumineux au survol et le gris après le clic. Tu as peut-être pensé à l'inverse : le gris au repos et le jaune au survol. Dans les deux cas, les deux images qui manquent sont à importer dans le client depuis le jeu d'origine.

**Recommandation :** Garder la maquette : le bouton reste cohérent avec l'écran de match et le joueur voit clairement que son clic est pris en compte. Dans les deux cas, il faut reprendre deux images du jeu d'origine.
**Réponse :** les polices ne se chargent pas

### Q12 — Quelle police libre pour le titre et le bouton de l'accueil ?

*(designer UX)* La police que tu as vue dans la maquette n'était pas celle proposée, parce que la maquette n'affiche pas les polices (un défaut de l'usine à corriger) : pour la voir, ouvre d'un double-clic le fichier Barlow Condensed Bold indiqué par le designer, déjà sur ta machine, et compare avec Trump Gothic, le style visé mais payant. Toutes les options demandent d'ajouter une police au jeu, ce qui revient sur deux décisions déjà prises : « utiliser une police déjà présente » et « aucun nouvel élément graphique ».

Choix de produit : c'est à toi de trancher.

Options :
- **Barlow Condensed Bold** : Gratuite, étroite et proche du style visé ; tu peux la vérifier tout de suite, et on ajoute une exception à la règle « aucun nouvel élément graphique ».
- **Teko ou Oswald** : Également étroites et gratuites, mais tu ne peux pas les voir sur ta machine avant de choisir.
- **Cinzel ou Orbitron** : Changent l'ambiance de l'accueil : plus « fantasy » avec Cinzel, plus « science-fiction » avec Orbitron.

Détail technique : Quelle police libre pour le titre et le bouton de l'accueil ? — Les polices ne s'affichent pas quand tu ouvres la maquette : ce que tu as vu n'était pas la police proposée. Pour les voir quand même, ouvre directement ces fichiers d'un double-clic (Livre des polices) : le style visé, duelyst/app/resources/fonts/TrumpGothicPro-Bold-webfont.ttf (payante, donc exclue), et une police libre de ce style qui se trouve déjà sur ta machine, 01-bbtrainer/bloodbowltrainer/app/io/client/assets/fonts/BarlowCondensed-Bold.ttf. Quel que soit le choix, il faut ajouter une police au jeu. Ça revient sur deux décisions : « police déjà présente » (Q4) et « aucun nouvel élément graphique » (I25-B12). Autres polices libres possibles, que tu n'as pas sur ta machine : Teko, Oswald (étroites aussi), Cinzel (plus « fantasy »), Orbitron (plus « science-fiction »). Côté usine : les polices citées dans une maquette ne sont pas transmises au navigateur, alors que les images le sont. C'est à corriger pour qu'on puisse voir les polices directement dans les maquettes.

**Recommandation :** Je prendrais Barlow Condensed Bold : elle est gratuite, proche du style visé et tu peux la vérifier tout de suite ; il faut accepter l'exception « sauf une police libre pour le titre et le bouton ».
**Réponse :** propose autre chose

### Q13 — Quelles couleurs pour « Rejoindre un match » : au repos, au survol, après le clic ?

*(designer UX)* Ta réponse précédente portait sur les polices et ne tranchait pas ce point. Le bouton reprend celui du jeu d'origine, qui existe en jaune, jaune lumineux et gris (la version « non éclairée » dont tu parlais) : la maquette le montre jaune au repos, comme « VALIDER » sur l'écran de match, puis lumineux au survol et gris après le clic.

Choix de produit : c'est à toi de trancher.

Options :
- **Garder la maquette : jaune, puis lumineux, puis gris** : Le bouton ressemble à « VALIDER » sur l'écran de match, et le joueur voit que son clic a été pris en compte.
- **L'inverse : gris au repos, jaune au survol** : Le bouton paraît éteint tant qu'on ne le survole pas, donc il attire moins l'œil sur l'accueil.

Détail technique : Quelle couleur pour « Rejoindre un match » au repos, au survol, après le clic ? — Ta réponse précédente portait sur les polices et ne tranchait pas ce point. Le bouton reprend celui du jeu d'origine, qui existe en jaune, en jaune lumineux et en gris. La maquette (section 2) le montre jaune au repos, comme « VALIDER » sur l'écran de match, lumineux au survol et gris après le clic. La version grise est la version « non éclairée » dont tu parlais. L'inverse est possible : gris au repos, jaune au survol. Dans les deux cas, il faut reprendre deux images du jeu d'origine.

**Recommandation :** Je garderais la maquette : le bouton est cohérent avec « VALIDER » et le gris confirme le clic. Dans les deux cas, il faut reprendre deux images du jeu d'origine.
**Réponse :** propose autre chose

### Q14 — Quelle police pour le titre et le bouton de la page d'accueil ?

*(designer UX)* Les trois pistes s'affichent dans leur vraie police dans la section 2 de la maquette de la page d'accueil. Deux d'entre elles demandent d'ajouter une police au jeu, alors que tu avais validé « aucun nouvel élément graphique » et « police déjà présente ».

Choix de produit : c'est à toi de trancher.

Options :
- **P1 : la police actuelle du jeu, en capitales, penchée et serrée** : Le titre donne une impression d'élan, rien n'est ajouté au jeu et les règles déjà validées restent intactes.
- **P2 : « GAMBETA » massif, « TACTICS » fin et très espacé dessous, façon affiche** : Le rendu est plus travaillé, mais il faut ajouter la version fine de la même police (gratuite), ce qui fait une petite exception à tes règles.
- **P3 : une cursive épaisse au style rétro « écusson de club »** : Le ton est plus marqué mais s'éloigne de l'univers d'origine du jeu, et il faut copier cette police dans le jeu, ce qui fait une exception à tes règles.

Détail technique : Quelle police pour le titre et le bouton : P1, P2 ou P3 ? — Ouvre la section 2 de I25-M1-page-d-accueil.html : les trois pistes s'y affichent dans leur vraie police, tirée de fichiers déjà sur ta machine. P1 : Lato Black, la police actuelle du jeu, en capitales, penchée vers l'avant et serrée. Le moteur du jeu fait cette transformation, donc rien n'est ajouté et les règles « police déjà présente » (Q4) et « aucun nouvel élément graphique » (I25-B12) restent intactes. P2 : « GAMBETA » en Lato Black massif, avec « TACTICS » dessous en Lato Light, fin et très espacé, façon affiche. Il faut importer Lato Light depuis OpenDuelyst : c'est la même famille, gratuite, mais c'est une petite exception à I25-B12. P3 : Lobster Two Bold, une cursive épaisse au style rétro « écusson de club ». Elle est déjà dans le dépôt du client, mais seulement dans l'outil de tests : il faut la copier dans les polices du jeu. Exception à I25-B12, et le ton s'éloigne d'OpenDuelyst.

**Recommandation :** P1 : elle donne du caractère au titre sans rien ajouter et sans revenir sur les règles déjà validées.
**Réponse :** essaye une police un peu plus sci-fi

### Q15 — Quel habillage pour le bouton « Rejoindre un match » ?

*(designer UX)* La section 3 de la maquette montre chaque piste au repos, au survol (version plus lumineuse, comme tu l'as demandé) et après le clic. Quelle que soit la piste, on reprend deux ou trois images existantes du jeu d'origine, sans en dessiner ni en retoucher aucune.

Choix de produit : c'est à toi de trancher.

Options :
- **B1 : la plaque bleue** : Elle s'accorde avec le décor de glace et se distingue des boutons de l'écran de match. Après le clic, le jeu assombrit simplement l'image, faute de version grise.
- **B2 : la flèche verte, de la même forme que « VALIDER » en match** : Le bouton rappelle « VALIDER » de l'écran de match et il a une vraie version grise après le clic.
- **B3 : la plaque verte** : C'est un habillage plus neutre. Comme pour B1, le jeu assombrit l'image après le clic.

Détail technique : Quel habillage pour « Rejoindre un match » : B1, B2 ou B3 ? — Ouvre la section 3 de la maquette : chaque piste y est montrée au repos, au survol et après le clic. Comme tu l'as indiqué, la version normale sert au repos et la version lumineuse au survol (Q9). B1 : la plaque bleue d'OpenDuelyst (button_primary). Elle s'accorde avec la glace de Vanar. Comme elle n'a pas de version grise, le moteur assombrit l'image après le clic. B2 : la flèche verte (button_end_turn_finished), de la même forme que « VALIDER » sur l'écran de match. Elle a une vraie version grise (button_end_turn_enemy). B3 : la plaque verte (button_confirm) ; comme pour B1, le moteur l'assombrit après le clic. Quelle que soit la piste, il faut importer deux ou trois images d'OpenDuelyst dans le client, sans en dessiner ni en retoucher aucune.

**Recommandation :** B1 : la plaque bleue va avec le décor de glace et ne se confond pas avec les boutons de match. Choisis B2 si tu préfères que le bouton rappelle « VALIDER ».
**Réponse :** les chose dont tu me parle ne sont pas sur la maquette

### Q16 — Faut-il réparer la maquette pour afficher trois des boutons proposés ?

*(designer UX)* Trois des quatre boutons proposés pour « Rejoindre un match » (B1, B2, B3) viennent d'OpenDuelyst, le jeu libre dont on réutilise les images. Ils ne s'affichent pas dans la maquette parce que celle-ci cherche ces images au mauvais endroit : tu ne vois qu'un cadre orange en pointillé, et tu devrais choisir sans les voir.

Choix technique : tu peux le confier à l'analyste.

Options :
- **Confier à l'analyste la correction proposée** : Le bon emplacement des images est corrigé, et B1, B2 et B3 apparaissent dès que tu rouvres la maquette.
- **Laisser en l'état** : Tu choisis le bouton en ne voyant que B0, le bouton « VALIDER » déjà présent sur l'écran de match.

Détail technique : Peux-tu corriger l'adresse d'OpenDuelyst pour que les boutons s'affichent dans la maquette ? — Les boutons B1, B2 et B3 de la section 3 sont des images d'OpenDuelyst. Elles ne s'affichent pas parce que system/components.yaml déclare le dossier d'OpenDuelyst à ../../duelyst (01-code_projects/duelyst/), qui n'existe pas. Le vrai dossier est 03-gamebeta_tactics/duelyst/. Tant que ce n'est pas corrigé, ces boutons restent des cadres en pointillé orange et tu ne peux choisir qu'en les imaginant. Le bouton B0 (« VALIDER » de l'écran de match) s'affiche déjà.

**Recommandation :** Confier la correction : c'est une simple erreur d'emplacement, sans choix de produit, et elle conditionne le point 3. Le designer ne peut pas la faire, il ne travaille que sur les maquettes.
**Réponse :**

### Q17 — Quelle police sci-fi pour le titre et le bouton d'accueil ?

*(designer UX)* La maquette montre S1 et S2 dans leur vraie police. S1 reprend la police déjà utilisée par le jeu, élargie, espacée et avec un contour cyan lumineux, sans rien ajouter. S2 (police de style terminal, déjà chez le client mais hors du jeu) et S3 (police sci-fi à télécharger, pas encore visible) font chacune une exception aux règles déjà fixées : pas de nouvel élément graphique dans le jeu, et pour S3, utiliser une police déjà présente.

Choix de produit : c'est à toi de trancher.

Options :
- **S1 : police actuelle du jeu, habillée sci-fi** : Rien n'est ajouté au jeu, les règles fixées restent respectées et le titre est cohérent avec les textes de l'écran de match.
- **S2 : police de style terminal** : Il faut la copier dans le jeu, ce qui fait une exception à la règle « aucun nouvel élément graphique ».
- **S3 : police sci-fi à télécharger** : Tu dois d'abord la télécharger pour la voir dans la prochaine version, et elle fait une exception aux deux règles.

Détail technique : Quelle police sci-fi pour le titre et le bouton : S1, S2 ou S3 ? — La section 2 de la maquette montre S1 et S2 dans leur vraie police. S1 : la police actuelle du jeu (Lato Black), élargie et très espacée, avec un contour cyan lumineux. Rien n'est ajouté au jeu, et les règles « police déjà présente » (Q4) et « aucun nouvel élément graphique » (I25-B12) restent intactes. S2 : Anonymous Pro Bold, une police libre de style terminal, déjà dans le dépôt du client mais seulement dans l'outil de tests. Il faudrait la copier dans les polices du jeu, ce qui fait une exception à I25-B12. S3 : une police sci-fi libre à télécharger (Orbitron, Audiowide, Exo 2 ou Rajdhani). Je ne peux pas la montrer tant qu'elle n'est pas sur ta machine, et elle fait une exception à Q4 et à I25-B12.

**Recommandation :** S1 : elle donne l'allure sci-fi sans rien ajouter au jeu et reste cohérente avec l'écran de match.
**Réponse :**

### Q18 — Quel habillage pour le bouton « Rejoindre un match » ?

*(designer UX)* La maquette montre chaque bouton au repos, au survol et après le clic. B0 est le bouton « VALIDER » de l'écran de match, visible tout de suite ; B1 (plaque bleue), B2 (flèche verte) et B3 (plaque verte) n'apparaîtront qu'après la correction du point 1. Quel que soit le choix, on reprend deux ou trois images d'OpenDuelyst telles quelles, sans en dessiner ni en retoucher.

Choix de produit : c'est à toi de trancher.

Options :
- **B0 : le bouton de l'écran de match** : L'accueil reprend exactement le bouton de l'écran de match, comme tu l'avais demandé (Q8). Il faut importer ses vraies images de survol et d'état grisé, simulées dans la maquette.
- **B1 : plaque bleue** : Le bouton s'accorde avec le thème glacé de Vanar et ne se confond pas avec les boutons de l'écran de match.
- **B2 ou B3 : flèche ou plaque verte** : Autre habillage d'OpenDuelyst, à juger une fois les images affichées.

Détail technique : Quel habillage pour « Rejoindre un match » : B0, B1, B2 ou B3 ? — La section 3 montre chaque bouton au repos, au survol et après le clic. B0 est le bouton « VALIDER » de l'écran de match, déjà dans le jeu et visible tout de suite. Son survol et son état grisé sont simulés dans la maquette ; dans le jeu, il faudrait importer les vraies versions depuis OpenDuelyst. B1 (plaque bleue), B2 (flèche verte) et B3 (plaque verte) viennent d'OpenDuelyst et ne s'afficheront qu'une fois l'adresse corrigée (question précédente). Quel que soit le choix, il faut importer deux ou trois images d'OpenDuelyst, sans en dessiner ni en retoucher aucune.

**Recommandation :** Corriger d'abord le point 1 pour voir les quatre boutons, puis prendre B1 comme le conseille le designer, ou B0 si tu tiens à ce que l'accueil reprenne le bouton de l'écran de match (Q8).
**Réponse :**
