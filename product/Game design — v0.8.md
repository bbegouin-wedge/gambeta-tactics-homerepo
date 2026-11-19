# Game design — v0.8

Nov 15, 2026 · @Bertrand

Deux équipes de 4 unités s'affrontent sur une grille de 11 × 7 pour s'emparer du drapeau placé au centre et le porter dans la zone de départ adverse ; chaque tour, les joueurs donnent à leurs unités des ordres face cachée sous forme de cartes. Ce document décrit le noyau à prototyper en premier ; les extensions attendent que le noyau ait fait ses preuves.

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

Une partie oppose deux équipes fixes de 4 unités sur une arène de 11 × 7 cases, avec un drapeau unique au centre.

- **Arène** : 11 colonnes × 7 lignes. Zones de départ sur les 2 colonnes de chaque extrémité (colonnes 1-2 et 10-11).
- **Drapeau** : un seul, au centre du terrain (colonne 6, ligne 4).
- **Obstacles fixes** : chaque arène peut avoir ses propres murs et creux de départ ; plusieurs arènes sont prévues.
- **Équipes** : 4 unités par joueur, choisies parmi les rôles Striker, Tank, Coureur, Support et Caster. Pas de draft dans le noyau.
- **Deck** : cartes d'action génériques, cartes propres à chaque unité (1 à 3 par unité) et cartes de combo. Taille à définir.
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
- **Durée** (proposé) : les combos restent en place jusqu'à la fin du match, à travers les manches.

Une carte de combo s'écrit « quand \[événement\], \[effet\] ». Événements reconnus dans le noyau : unité poussée, collision, chute dans un creux, unité blessée, drapeau ramassé, drapeau lâché.

Exemple : « Quand une unité adverse tombe dans un creux, pioche une carte. »

## Combat et sorts (propositions)

Ces règles sont proposées et restent à valider ; elles complètent la section Unités, poussées et terrain.

| Règle | Proposition |
| --- | --- |
| Choix de la cible | On programme la carte ; la cible ou la direction se choisit à la révélation. Une attaque sans cible valide devient un déplacement d'une case |
| Dégâts | Inscrits sur la carte, de 1 à 3, sans hasard ; une unité tombe en 2 ou 3 coups |
| Riposte | Pas de riposte automatique ; certains passifs en donnent (tanks) |
| Poussée sur plus lourd | L'attaque inflige ses dégâts mais ne pousse pas |
| Tir | Ligne de vue nécessaire : murs et unités bloquent, le premier touché encaisse |
| Sorts canalisés | Révélés comme les autres cartes, zone affichée sur le plateau, effet à la fin du tour. Plus puissants (zone, 3 dégâts, ignorent les obstacles). Annulés si le lanceur subit des dégâts ou est poussé avant la fin du tour |
| Sorts instantanés | Plus faibles et utilitaires : attirer, échanger de place, poser un mur adjacent |

Exemples de sorts : Pluie de braises (canalisé, 2 dégâts sur 2 × 2 à portée 4), Onde de choc (canalisé, repousse d'une case autour d'une case ciblée), Faille (canalisé, creux de 2 cases), Attraction (instantané, attire de 2 cases), Rempart (instantané, mur adjacent), Translocation (instantané, échange deux alliés).

## Fin de manche et fin de match

Une manche se joue en deux temps : un rush vers le drapeau central, puis une phase de score où le porteur doit traverser la défense adverse. Le premier joueur à 2 manches gagne le match (3 manches au plus).

- **Marquer** : porter le drapeau dans la zone de départ adverse (ses 2 colonnes), comme un essai au rugby. Cela termine la manche.
- **Durée d'une manche** : 5 tours au plus.
- **Départage** : sans essai au bout de 5 tours, l'équipe qui porte le drapeau gagne la manche ; si personne ne le porte, la manche est nulle.
- **Remise à zéro** : entre deux manches, le terrain, les positions, le drapeau et les unités blessées reviennent à l'état initial.
- **Main** (proposé) : conservée d'une manche à l'autre, comme au Gwynt. Dépenser beaucoup pour gagner une manche se paie dans la suivante.
- **Initiative** (proposé) : le perdant de la manche précédente a l'initiative au premier tour de la suivante.
- **Durée d'un match** : environ 3 min 30 par tour, soit 35 à 50 minutes pour 2 à 3 manches de 5 tours. À surveiller par rapport à la cible de 30 minutes.

**Pourquoi l'essai dans le camp adverse** : la phase de score devient un face-à-face attaque contre défense où chaque rôle a sa fonction (le tank bloque, le striker ouvre un passage en poussant, le support couvre avec un mur, le coureur reçoit la passe). L'équipe qui perd le rush est déjà en position de défendre.

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

## Questions ouvertes

- [ ] Valider le choix de la cible à la révélation.
- [ ] Valider les sorts canalisés et leur annulation.
- [ ] Durée de match : 5 tours par manche tiennent-ils dans la cible de 30 minutes ?
- [ ] Taille et composition du deck ; nombre de cartes piochées entre deux manches.
- [ ] Dessin des arènes : obstacles fixes de départ, symétrie, nombre d'arènes.
- [ ] Transmission du drapeau : une carte « Passe » générique, avec quelle portée ? Le porteur a-t-il des restrictions ?
- [ ] Rush : qui atteint le drapeau en premier à distance égale, et faut-il un équilibrage ?
- [ ] Conflits de résolution : deux unités visant la même case.
- [ ] Combien de terrains actifs par joueur au maximum ?
- [ ] Conception des 5 unités de test, une par rôle, avec passifs et cartes.
