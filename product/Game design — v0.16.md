# Game design — v0.16

Nov 15, 2026 · @Bertrand

Deux équipes de 4 unités s'affrontent sur une grille de 13 × 7 pour s'emparer du drapeau placé au centre et le porter dans la zone de départ adverse ; chaque tour, les joueurs donnent à leurs unités des ordres face cachée sous forme de cartes. Ce document décrit le noyau à prototyper en premier ; les extensions attendent que le noyau ait fait ses preuves.

## Vision et piliers

La profondeur tactique se joue sur le plateau : les cartes sont des ordres donnés à des unités qui poursuivent un objectif clair. Le numérique est un atout : le serveur fait autorité sur l'information cachée.

| Pilier | Ce qui le porte dans le noyau |
| --- | --- |
| Stratégie | Capture de drapeau, économie de la main sur plusieurs manches, placement |
| Bluff | Ordres face cachée ; une carte posée peut n'être qu'un leurre |
| Mémoire et déduction | Suivre les cartes jouées par l'adversaire pour savoir ce qui lui reste |
| Combos | Synergie entre terrain, poussées et cartes de combo |

Règle de conception : le noyau ne contient aucun hasard en combat. L'incertitude vient des ordres cachés de l'adversaire.

## Matériel et mise en place

Une partie oppose deux équipes fixes de 4 unités sur une arène de 13 × 7 cases, avec un drapeau unique au centre.

- **Arène** : 13 colonnes × 7 lignes. Zones de départ sur les 2 colonnes de chaque extrémité (colonnes 1-2 et 12-13). Il y a 5 cases entre une zone de départ et le drapeau, puis 5 cases entre le drapeau et la zone d'essai.
- **Drapeau** : un seul, au centre du terrain (colonne 7, ligne 4).
- **Obstacles fixes** : chaque arène peut avoir ses propres murs et creux de départ ; plusieurs arènes sont prévues.
- **Équipes** : 4 unités par joueur, choisies parmi les rôles Striker, Tank, Coureur, Support et Caster. Pas de draft dans le noyau.
- **Deck** : cartes d'action génériques, 3 cartes par unité (2 cartes de rôle et 1 carte propre) et cartes de combo ; voir la section Cartes d'action.
- **Main de départ** : 7 cartes au début du match.
- **Placement** : les unités sont placées dans leur zone de départ au début de chaque manche.
- **Initiative** : tirée au sort pour la première manche.

## Unités, poussées et terrain

Chaque unité est une carte qui porte trois caractéristiques, un trait passif et la liste des cartes d'action qu'elle apporte au deck. Toute son identité tient dans son passif et ses cartes.

| Caractéristique | Rôle |
| --- | --- |
| Points de vie | À 0, l'unité est blessée et sort du terrain jusqu'à la fin de la manche |
| Mouvement | Nombre de cases parcourues avec une carte de déplacement |
| Masse | Légère, moyenne ou lourde : décide qui peut pousser qui |

**Combat.** Chaque carte d'attaque décrit un motif fixe : cases touchées, dégâts (1 à 3), poussée éventuelle. Les dégâts sont toujours ceux inscrits sur la carte.

**Poussées** (proposé) :

- une unité ne peut pousser qu'une cible de Masse inférieure ou égale à la sienne ;
- une unité poussée contre un mur ou une autre unité s'arrête et subit 1 dégât ; l'unité heurtée en subit 1 aussi.

**Terrain du noyau** : seulement deux types, créés par certaines cartes et retirés à la fin de la manche.

| Terrain | Règle |
| --- | --- |
| Mur | Bloque le mouvement et les tirs |
| Creux | Une unité poussée dedans perd son prochain ordre et lâche le drapeau |

**Drapeau.** Ramassage et transmission sont automatiques, sans test : une unité qui entre sur la case du drapeau le ramasse. Un porteur blessé lâche le drapeau sur sa case.

## Déroulé d'un tour

Les deux joueurs programment en même temps, puis résolvent leurs ordres un par un, en alternance.

1. **Programmation simultanée.** Chaque joueur pose au plus une carte face cachée sur chacune de ses unités. Il peut aussi utiliser une unité pour poser une carte de combo : cette unité n'agit pas ce tour-ci. Le serveur révèle la suite quand les deux joueurs ont validé.
2. **Révélation des combos.** Les combos posés ce tour-ci sont révélés, face visible.
3. **Résolution alternée.** Le joueur qui a l'initiative commence. À son tour, chaque joueur choisit une de ses unités, révèle sa carte et la résout. Quand un joueur n'a plus d'ordre, l'autre termine les siens.
4. **Déclenchements.** Après chaque résolution, les combos dont la condition est remplie se déclenchent.
5. **Fin de tour.** Chaque joueur pioche 3 cartes ; les cartes non jouées restent en main. L'initiative change de camp.

**Règle de bluff.** Une carte posée sur une unité peut être jouée pour son effet ou non. Si elle ne l'est pas, ou si elle ne peut pas l'être (carte d'une autre unité, carte d'une unité blessée), elle donne un déplacement d'une case, puis est défaussée. L'adversaire ne distingue jamais un vrai ordre d'une défausse. Une unité sans carte reste sur place.

**Économie de la main.** Avec 4 unités, 7 cartes de départ et 3 piochées par tour, on ne peut pas donner un vrai ordre à chaque unité à chaque tour : il faut choisir qui agit.

## Combos

Une carte de combo reste posée face visible et se déclenche automatiquement chaque fois que sa condition est remplie.

- **Coût** : poser un combo occupe une unité, qui n'agit pas ce tour-ci.
- **Limite** : 3 combos actifs au plus par joueur. Pour en poser un 4e, on défausse un combo actif.
- **Ordre** : quand plusieurs combos se déclenchent sur le même événement, ils s'appliquent dans l'ordre où ils ont été posés.
- **Visibilité** : face visible ; ils annoncent une stratégie, qui peut être un leurre.
- **Durée** (décidé) : les combos sont retirés à la fin de chaque manche, avec la remise à zéro du terrain ; poser un combo est un choix renouvelé à chaque manche.

Une carte de combo s'écrit « quand \[événement\], \[effet\] ». Événements reconnus dans le noyau : unité poussée, collision, chute dans un creux, unité blessée, drapeau ramassé, drapeau lâché.

Exemple : « Quand une unité adverse tombe dans un creux, pioche une carte. »

**Deux types de combos** (décidé sur le principe, détail à concevoir) :

- **Déclencheur** : « quand \[événement\], \[effet\] », comme ci-dessus.
- **Règle** : « tant que ce combo est actif, \[règle ajoutée ou modifiée\] ». Portée : ton équipe, un rôle de ton équipe, ou tout le monde (les deux joueurs). Exemples : ton porteur n'est plus ralenti par le drapeau ; tes Frappes rendent la cible muette ; pour tout le monde, les poussées font glisser d'une case de plus.

Statuts que les combos peuvent appliquer (proposé, liste volontairement courte) : **étourdi** (perd son prochain ordre), **immobilisé** (pas de déplacement ce tour-ci), **muet** (ne peut jouer que des cartes génériques jusqu'à sa prochaine activation).

Garde-fous (proposé) : un combo se déclenche au plus une fois par tour ; un combo de règle modifie un seul paramètre ; aucun combo ne fait marquer directement ni n'annule entièrement le plaquage ; quand deux combos modifient la même règle, l'ordre de pose décide ; l'interface affiche les valeurs modifiées sur le plateau.

## Cartes d'action

Le deck mélange trois familles : un socle de cartes génériques identique pour les deux joueurs, les cartes apportées par les unités, et des combos.

### Cartes de rôle et cartes propres (décidé)

Chaque unité apporte 3 cartes au deck :

- **2 cartes de rôle**, prises dans la liste commune de son rôle. Elles sont jouables par **n'importe quelle unité de ce rôle** dans l'équipe.
- **1 carte propre**, jouable **uniquement par cette unité**. Avec le passif, elle fait l'identité de l'unité.

Règles associées :

- Avoir une unité d'un rôle donne accès aux cartes de ce rôle, mais en quantité liée au nombre d'unités : 2 cartes de rôle par unité, pas davantage.
- Si une unité est hors combat, sa carte propre ne peut plus servir que de leurre (déplacement d'une case) ; ses cartes de rôle restent jouables par une autre unité du même rôle.
- L'adversaire connaît les rôles de l'équipe et les listes de rôle : il sait ce qui est possible, pas ce qui a été choisi.
- **Noyau** : chaque unité arrive avec ses 2 cartes de rôle prédéfinies.
- **Extension** : choix des cartes de rôle de chaque unité en 30 secondes après le draft.

Exemple, rôle Striker. Liste de rôle : Charge (avance jusqu'à 3 cases, 2 dégâts, pousse d'une case), Coup de balayage (cône de 3 cases, 1 dégât), Riposte (garde qui inflige 1 dégât), Percée (avance d'une case, pousse de 2 cases sans dégât). Cartes propres : Bélier pour Brise-Ligne (Charge qui traverse la première unité poussée), Morsure pour Mâchoire (case adjacente, 2 dégâts, cible immobilisée).

### Une carte, une action (proposé)

Chaque unité reçoit au plus une carte par tour : se déplacer et attaquer sont deux ordres différents. Les cartes qui combinent les deux (Charge) sont réservées aux cartes de rôle et aux cartes propres. Le déplacement passe donc aussi par une carte.

### Cartes génériques (proposé)

Socle identique pour les deux joueurs.

| Carte | Type | Effet | Exemplaires |
| --- | --- | --- | --- |
| Avancer | Mouvement | Se déplace jusqu'à sa valeur de Mouvement, case par case, sans diagonale ; traverse ses alliés, pas ses adversaires | 4 |
| Sprint | Mouvement | Mouvement + 2 cases ; interdit au porteur du drapeau | 2 |
| Passe | Soutien | Le porteur transmet le drapeau à un allié à 4 cases ou moins, en ligne droite ; la première unité adverse sur la trajectoire l'intercepte. Le receveur garde son propre ordre du tour | 3 |
| Frappe | Attaque | Case adjacente, 1 dégât, pousse d'une case : le plaquage minimal, accessible à toutes les unités | 3 (proposé, reprend la place du Harpon) |
| Garde | Garde | Contrôle les 8 cases autour, jusqu'à la prochaine activation | 3 |

**Porteur du drapeau** (décidé) :

- Ramasser le drapeau (en entrant sur sa case) arrête le déplacement : le rush et la phase de score restent deux temps distincts.
- Le porteur a 1 de Mouvement en moins et ne peut pas jouer Sprint.
- La passe se fait uniquement en ligne droite ; pas de passe vers une case vide dans le noyau.
- Le Harpon (attire une unité de 2 cases, portée 4) devient une carte de rôle Support ou Caster.

Conséquence voulue : marquer dans le camp adverse demande une action coordonnée. Un porteur seul est lent et vulnérable ; l'essai se construit avec des passes, des écrans contre les intercepteurs et des poussées pour ouvrir le passage, en choisissant l'ordre de résolution des unités.

### Composition du deck (proposé)

15 génériques + 12 cartes d'unité (4 unités × 3) + 3 combos = 30 cartes. Un match de 3 manches peut faire voir jusqu'à 52 cartes : la défausse est remélangée quand la pioche est vide.

## Combat, garde et sorts

Le combat est entièrement déterministe ; la défense passe par un ordre de garde, qui donne aux cartes d'action leur poids défensif.

### Garde et engagement (décidé)

- **La garde est un ordre** : une carte jouée sur une unité, qui ne fait rien d'autre ce tour-là.
- **Activation** : la garde s'active quand on la résout, dans l'ordre alterné, comme n'importe quel ordre. Tant qu'elle n'est pas résolue, l'unité ne défend pas.
- **Zone de contrôle** : version forte, les 8 cases autour de l'unité, diagonales comprises.
- **Effet** : une unité adverse qui **entre** dans une case contrôlée arrête son déplacement. Être déjà au contact ne paralyse pas : l'unité peut attaquer, lancer un sort, poser un combo ou sortir de la zone ; seul un pas vers une autre case contrôlée l'arrête.
- **Sans garde, aucun engagement** : on circule librement à côté des adversaires.
- **Durée** (à tester) : la garde dure jusqu'à la prochaine activation de l'unité, c'est-à-dire jusqu'à la résolution de son ordre du tour suivant. Une garde jouée tard couvre ainsi le début du tour suivant.
- **Interruption** : un mouvement arrêté par une garde s'arrête vraiment ; une Charge interrompue n'inflige ses dégâts que si sa cible est adjacente à la case d'arrêt.

Conséquence voulue : le timing devient un duel. L'attaquant veut passer avant que la garde soit résolue, le défenseur veut la résoudre tôt.

Variantes par rôle (proposé) :

| Carte | Porteur | Effet quand un adversaire entre dans la zone |
| --- | --- | --- |
| Garde | Générique | L'adversaire s'arrête |
| Bastion | Tank | Zone de 2 cases de rayon ; l'adversaire s'arrête |
| Repousser | Tank, Striker | L'adversaire s'arrête et est repoussé d'une case |
| Interception | Coureur | Zone en ligne : intercepte une passe qui la traverse |
| Riposte | Striker | L'adversaire s'arrête et subit 1 dégât |

### Attaques (proposé)

| Règle | Proposition |
| --- | --- |
| Choix de la cible | Décidé : on programme la carte ; la cible ou la direction se choisit à la révélation. Une attaque sans cible valide devient un déplacement d'une case |
| Dégâts | Inscrits sur la carte, de 1 à 3 ; points de vie de 3 à 6 : une unité tombe en 2 ou 3 coups |
| Riposte automatique | Aucune ; seuls certains passifs ou la carte Riposte en donnent |
| Poussée sur plus lourd | L'attaque inflige ses dégâts mais ne pousse pas |
| Tir | Ligne de vue nécessaire : murs et unités bloquent, le premier touché encaisse |
| Plaquage | Décidé : le porteur lâche le drapeau dès qu'il subit au moins 1 dégât ou qu'il est poussé, y compris à distance (tir, sort). Après un dégât, le drapeau rebondit sur une case adjacente choisie par l'attaquant ; après une poussée, il reste sur la case de départ du porteur |
| Conflits de résolution | Inexistants : les ordres se résolvent un par un, et la cible est choisie à la révélation |

**Grammaire des cartes** (proposé) : chaque carte d'attaque se décrit par sa forme (case adjacente, ligne, cône, zone 2 × 2, croix, case ciblée), sa portée, ses dégâts (0 à 3) et son effet (pousser, attirer, statut). Deux statuts seulement dans le noyau : « perd son prochain ordre » et « immobilisé » (pas de déplacement ce tour-ci).

### Sorts (proposé)

- **Sorts canalisés** : révélés comme les autres cartes, zone affichée sur le plateau, effet à la fin du tour. Plus puissants (zone, 3 dégâts, ignorent les obstacles). Annulés si le lanceur subit des dégâts ou est poussé avant la fin du tour.
- **Sorts instantanés** : plus faibles et utilitaires (attirer, échanger de place, poser un mur adjacent).

Exemples : Pluie de braises (canalisé, 2 dégâts sur 2 × 2 à portée 4), Onde de choc (canalisé, repousse d'une case autour d'une case ciblée), Faille (canalisé, creux de 2 cases), Attraction (instantané, attire de 2 cases), Rempart (instantané, mur adjacent), Translocation (instantané, échange deux alliés).

### Effets de zone (décidé : ils font partie du noyau)

Les effets de zone sont la réponse naturelle aux groupes serrés : une unité en garde ne peut pas esquiver, et un porteur entouré de défenseurs devient une cible idéale. Avec le plaquage, un seul dégât ou une seule poussée suffit à faire tomber le drapeau.

| Carte (proposé) | Type | Effet |
| --- | --- | --- |
| Onde de choc | Sort canalisé | Repousse d'une case toutes les unités autour d'une case ciblée |
| Pluie de braises | Sort canalisé | 2 dégâts sur une zone de 2 × 2 à portée 4 |
| Coup de balayage | Attaque de striker | Cône de 3 cases devant l'unité, 1 dégât |
| Harpon | Carte de rôle (Support ou Caster) | Attire une unité de 2 cases, portée 4 : une poussée à distance, donc un plaquage |

**Contre le repli défensif** (décidé) : le départage n'est gagné que dans la moitié adverse ; la garde coûte une carte et l'action de l'unité ; elle n'arrête que les déplacements, pas les tirs, sorts ni poussées lancés de l'extérieur de la zone.

## Fin de manche et fin de match

Une manche se joue en deux temps : un rush vers le drapeau central, puis une phase de score où le porteur doit traverser la défense adverse. Le premier joueur à 2 manches gagne le match (3 manches au plus).

- **Marquer** : porter le drapeau dans la zone de départ adverse (ses 2 colonnes), comme un essai au rugby. Cela termine la manche.
- **Durée d'une manche** : 5 tours au plus.
- **Départage** : sans essai au bout de 5 tours, l'équipe qui porte le drapeau gagne la manche, à condition que le porteur soit dans la moitié adverse du terrain ; sinon, la manche est nulle. Reculer chez soi avec le drapeau ne rapporte rien.
- **Remise à zéro** : entre deux manches, le terrain, les positions, le drapeau et les unités blessées reviennent à l'état initial.
- **Main** (proposé) : conservée d'une manche à l'autre, comme au Gwynt. Dépenser beaucoup pour gagner une manche se paie dans la suivante.
- **Initiative** (proposé) : le perdant de la manche précédente a l'initiative au premier tour de la suivante.
- **Durée d'un match** : environ 3 min 30 par tour, soit 35 à 50 minutes pour 2 à 3 manches de 5 tours. À surveiller par rapport à la cible de 30 minutes.

**Pourquoi l'essai dans le camp adverse** : la phase de score devient un face-à-face attaque contre défense où chaque rôle a sa fonction (le tank bloque, le striker ouvre un passage en poussant, le support couvre avec un mur, le coureur reçoit la passe). L'équipe qui perd le rush est déjà en position de défendre.

## Modes de jeu (envisagé)

Tous les modes partagent les mêmes règles de base ; chacun ajoute des couches, pour limiter la complexité et rendre l'apprentissage progressif.

| Mode | Contenu | Durée visée |
| --- | --- | --- |
| Initiation | Arène réduite, 3 unités prédéfinies, une seule manche, sans combos ni sorts canalisés | 10 min |
| Escarmouche | Le noyau décrit dans ce document : 13 × 7, 4 unités prédéfinies, combos, sorts, 2 manches gagnantes. C'est le mode du prototype | 30 à 45 min |
| Compétitif | Escarmouche plus draft et ban, remplaçants dans le deck, choix des cartes de rôle | 40 à 50 min |
| Défis tactiques (solo) | Situations figées à résoudre en un tour, façon puzzle ; utiles aussi pour tester le combat sans adversaire | 2 à 5 min |
| Modes d'objectif (plus tard) | Ballon, protection d'un VIP | — |

Les paramètres d'économie de la main (cartes de départ, pioche par tour) restent à régler en test ; avec 5 tours par manche, 7 cartes et 3 piochées par tour donnent 19 cartes pour 20 emplacements d'ordre, une pénurie presque nulle.

## Extensions

Les extensions s'ajoutent une par une, une fois le noyau validé par des parties test.

| Niveau | Mécanique | Résumé |
| --- | --- | --- |
| Extension 1 | Draft et ban | Pool commun d'unités, chaque unité unique par match. Ban simultané de 2 unités chacun, puis choix en serpent (A, B, B, A…) de 4 titulaires et 3 remplaçants. Monétisation par cosmétiques uniquement |
| Extension 1 | Titulaires et remplaçants | Les remplaçants sont mélangés dans le deck ; les faire entrer coûte un ordre. Les cartes d'une unité n'entrent dans le deck qu'avec elle |
| Extension 2 | Deck de modificateurs | Seulement si les combats du noyau sont trop prévisibles. Un paquet par joueur (par exemple 4 × +0, 2 × +1, 2 × −1, 1 critique, 1 raté), mélangé au tirage du critique ou du raté |
| Extension 2 | Destin | Bénédictions et malédictions qui ajoutent des cartes aux decks de modificateurs ; dépend du précédent |
| Extension 2 | Information | Capacités qui révèlent un ordre caché adverse, ou qui en protègent |
| Extension 2 | Terrains supplémentaires | Ronces (2 points de mouvement par case), sanctuaire (+1 PV en fin de tour), glace (poussée d'une case de plus) |

Cadre des capacités spéciales : elles vivent dans le passif d'une unité, dans ses cartes ou dans les combos, et agissent sur cinq leviers (dégâts, mouvement forcé, terrain, destin, information), jamais directement sur une caractéristique.

## En attente et modes ultérieurs

- **Changement de titulaires entre les manches** : à reconsidérer avec l'extension 1.
- **Variante B des caractéristiques** (Mouvement, Force, Précision, Volonté, Points de vie, chacune définissant aussi une distance sur la grille) : seulement si la variante A manque de relief.
- **Format 45 minutes** : découpage à définir.
- **Modes de jeu** : ballon et protection d'un VIP, après la capture de drapeau.

## Précisions de déroulement (décidé)

Points tranchés lors de l'écriture de la boucle technique (document « Boucle de gameplay — étapes techniques »).

- **Placement** : sans draft, le joueur qui a l'initiative du premier tour place en premier.
- **Pioche entre deux manches** : 3 cartes par joueur.
- **Égalité après 3 manches** : match nul en Escarmouche ; en Compétitif, victoire à l'équipe qui a terminé le plus de tours avec le drapeau dans la moitié adverse.
- **Combos déclenchés par le même événement** : ceux du joueur actif d'abord, puis ceux de l'adversaire, chacun dans son ordre de pose.
- **Creux** : infranchissable pour un déplacement volontaire ; on n'y tombe qu'en étant poussé ou attiré. Il ne bloque ni tirs ni passes.
- **Unité étourdie** : son emplacement est bloqué en programmation ; étourdie après avoir reçu une carte, elle la perd à sa résolution.
- **Temps** : pendule d'échecs, avec une réserve par joueur et par manche (environ 6 minutes) plus quelques secondes par décision.
- **Essai** : il compte dès l'entrée dans une case de la zone de départ adverse ; le déplacement s'arrête et la manche se termine.

## Questions ouvertes

- [ ] Tester la durée de la garde (jusqu'à la prochaine activation de l'unité).
- [ ] Effets de zone : valider la liste de cartes (Onde de choc, Pluie de braises, Coup de balayage, Harpon) et leurs valeurs.
- [ ] Valider la grammaire des cartes.
- [ ] Valider les variantes de garde par rôle.
- [ ] Valider les sorts canalisés et leur annulation.
- [ ] Durée de match : 5 tours par manche tiennent-ils dans la cible de 30 minutes ?
- [ ] Taille et composition du deck ; nombre de cartes piochées entre deux manches.
- [ ] Dessin des arènes : obstacles fixes de départ, symétrie, nombre d'arènes.
- [ ] Transmission du drapeau : une carte « Passe » générique, avec quelle portée ? Le porteur a-t-il des restrictions ?
- [ ] Rush : qui atteint le drapeau en premier à distance égale, et faut-il un équilibrage ?
- [ ] Combien de terrains actifs par joueur au maximum ?
- [ ] Conception des 5 unités de test, une par rôle, avec passifs et cartes.

## Conclusion : objectifs et risques

Le jeu vise quatre objectifs : simple d'accès, tactiquement profond, streamable, avec un potentiel compétitif. Le cadre de règles est complet ; le contenu (unités, combos, arènes, valeurs) reste à produire et à régler en test.

Le jeu en une phrase : donne des ordres cachés à 4 unités pour porter le drapeau dans le camp adverse. Cinq verbes : se déplacer, attaquer, garder, passer, lancer un sort.

| Objectif | Évaluation | Points d'appui |
| --- | --- | --- |
| Profondeur tactique | Très bien servi | Ordres cachés, duel de timing sur la garde, ordre de résolution à planifier, deux phases par manche (rush puis score), poussées et terrain, combos visibles |
| Potentiel compétitif | Bien servi | Aucun hasard, pool commun et socle générique identique, draft et ban, manches au meilleur des trois, serveur qui fait autorité, replays gratuits grâce au flux d'événements |
| Streamable | Bien servi, sous condition | Objectif lisible et moments forts naturels (leurre révélé, plaquage, interception, essai au dernier tour) ; la phase de programmation silencieuse est à traiter |
| Simple d'accès | À surveiller | Une vingtaine de règles en mode Escarmouche, chacune simple mais lourdes ensemble |

### Risques et parades

| Risque | Parade |
| --- | --- |
| Accessibilité : trop de règles cumulées | Mode Initiation limité à six règles (se déplacer, frapper, passer, plaquer, garder, marquer) ; le moteur applique les règles ; chaque effet est prévisualisé sur le plateau (zones de garde, trajectoires de passe, zones de sort, valeurs modifiées par les combos) |
| Temps mort à l'écran pendant la programmation | Mode spectateur omniscient en différé (le public voit les mains et les ordres pendant la réflexion) ; résolution rapide et spectaculaire ; pendule de jeu |
| Avantage de l'initiative, surtout au rush | Initiative alternée ; à mesurer en test |
| Accès au drapeau à distance égale | Question ouverte ; à mesurer en test |
| Ouvertures « résolues » sur une arène unique | Plusieurs arènes ; draft en mode Compétitif |

### Priorités du premier prototype (mode Escarmouche)

1. **Économie de la main** : faut-il passer à 2 cartes piochées par tour pour retrouver la pénurie d'ordres ?
2. **Durée de la garde** : jusqu'à la prochaine activation, est-ce trop fort ou trop faible ?
3. **Taux d'essai** : quelle part des manches se termine par un essai plutôt qu'au départage ? Moins de la moitié signalerait une attaque trop faible.
