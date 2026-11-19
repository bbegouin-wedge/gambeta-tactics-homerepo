# Boucle de gameplay — étapes techniques

Nov 15, 2026 · @Bertrand

Liste ordonnée des étapes que le moteur enchaîne pour un match en mode Escarmouche, d'après le document de game design v0.15. Chaque étape porte un identifiant pour la traçabilité.

## Vue d'ensemble

La boucle est faite de cinq niveaux imbriqués ; chaque niveau appelle le suivant et lui rend la main quand il a fini.

1. **Match** (M) : 2 manches gagnantes, 3 au plus.
2. **Manche** (R) : 5 tours au plus, se termine par un essai ou au départage.
3. **Tour** (T) : programmation simultanée, puis résolution alternée des ordres.
4. **Ordre** (O) : résolution d'une carte posée sur une unité.
5. **File d'effets** (F) : traitement en cascade des effets produits par un ordre, avec déclenchement des combos, jusqu'à épuisement.

Principes communs : aucune étape ne tire au hasard, sauf le mélange du deck et le tirage de l'initiative (graine enregistrée pour le replay) ; chaque étape émet des événements ; l'information cachée est filtrée par joueur au moment de la diffusion. Une vérification d'essai a lieu après chaque effet : un essai interrompt immédiatement tous les niveaux jusqu'à la fin de manche.

## Initialisation du match

1. **M-01 Charger la configuration** : mode, arène (13 × 7, obstacles fixes), équipes de 4 unités prédéfinies, liste des combos.
2. **M-02 Construire les decks** : 15 cartes génériques + 3 cartes par unité (2 de rôle, 1 propre) + 3 combos = 30 cartes par joueur.
3. **M-03 Mélanger les decks** avec une graine enregistrée.
4. **M-04 Piocher 7 cartes** par joueur.
5. **M-05 Initialiser le score** des manches à 0 – 0.
6. **M-06 Tirer au sort l'initiative** de la première manche (graine enregistrée).
7. **M-07 Lancer la manche 1** (R-01).

## Début de manche

1. **R-01 Réinitialiser l'arène** : obstacles fixes de l'arène, retrait des murs et creux créés, drapeau au centre (colonne 7, ligne 4), aucun porteur.
2. **R-02 Réinitialiser les unités** : toutes en jeu, PV au maximum, statuts effacés, gardes annulées.
3. **R-03 Retirer les combos actifs** des deux joueurs (défausse).
4. **R-04 Pioche entre manches** (manches 2 et 3 seulement : 3 cartes par joueur). Les mains sont conservées.
5. **R-05 Fixer l'initiative** : tirage pour la manche 1 (M-06) ; ensuite, le perdant de la manche précédente.
6. **R-06 Placement alterné** des 4 unités de chaque joueur dans sa zone de départ (colonnes 1-2 ou 12-13), unité par unité, en commençant par le joueur qui a l'initiative du premier tour. Saisie joueur à chaque placement.
7. **R-07 Remettre le compteur de tours à 1** et lancer le tour (T-01).

## Tour

1. **T-01 Début de tour** : émettre l'événement de début de tour (numéro, initiative).
2. **T-02 Programmation simultanée** : chaque joueur, pour chacune de ses unités en jeu et non étourdies (l'emplacement d'une unité étourdie est bloqué), choisit une option :
   - poser une carte face cachée (n'importe quelle carte de sa main : la légalité n'est vérifiée qu'à la résolution, pour permettre les leurres) ;
   - utiliser l'emplacement de l'unité pour poser une carte de combo (face cachée jusqu'à T-04) ;
   - ne rien poser.
3. **T-03 Barrière de validation** : attendre la validation des deux joueurs ; si la réserve de temps d'un joueur est épuisée, valider d'office ce qu'il a posé. Les cartes posées quittent la main.
4. **T-04 Révéler et installer les combos posés**, dans l'ordre de pose de chaque joueur. Si un joueur dépasse 3 combos actifs, il choisit le combo à défausser (saisie).
5. **T-05 Boucle de résolution alternée** :
   1. le joueur actif est celui qui a l'initiative ;
   2. s'il lui reste un ordre non résolu, il choisit une de ses unités porteuses d'un ordre (saisie) et résout cet ordre (O-01 à O-10) ;
   3. la main passe à l'adversaire s'il lui reste un ordre ; sinon le même joueur continue ;
   4. la boucle s'arrête quand plus aucun ordre n'est à résoudre. Les ordres des unités hors combat sont défaussés sans effet.
6. **T-06 Effets différés** : résoudre les sorts canalisés non annulés, dans l'ordre de leur révélation, chacun via la file d'effets (F-01 à F-08).
7. **T-07 Fin de tour** :
   1. expirer les statuts « ce tour-ci » (immobilisé) ;
   2. défausser les cartes résolues ;
   3. chaque joueur pioche 3 cartes, en remélangeant sa défausse si sa pioche est vide ;
   4. l'initiative change de camp ;
   5. réinitialiser les compteurs « une fois par tour » des combos.
8. **T-08 Suite** : si le tour 5 est terminé, aller en fin de manche par départage (E-01) ; sinon incrémenter le compteur et revenir à T-01.

Les gardes ne s'expirent pas en fin de tour : elles durent jusqu'à la prochaine activation de leur unité (O-03).

## Résolution d'un ordre

1. **O-01 Sélection** de l'unité par le joueur actif (saisie, faite en T-05).
2. **O-02 Étourdissement** : si l'unité est étourdie, l'ordre est perdu, la carte est défaussée sans être révélée, le statut est levé ; fin de l'ordre.
3. **O-03 Fin des effets « jusqu'à la prochaine activation »** de cette unité : garde, muet.
4. **O-04 Révéler la carte** à tous les joueurs.
5. **O-05 Légalité** : la carte est jouable pour son effet si elle est générique, de rôle avec le bon rôle, ou propre à cette unité ; si l'unité n'est pas muette pour une carte non générique ; si les restrictions sont respectées (le porteur ne peut pas jouer Sprint).
6. **O-06 Choix du mode** (saisie) : jouer l'effet, ou jouer la carte comme leurre (déplacement d'une case). Une carte illégale est forcément un leurre.
7. **O-07 Choix de la cible** (saisie) : cible, direction ou case, avec prévisualisation de l'effet sur le plateau. Sans cible valide, la carte devient un leurre.
8. **O-08 Exécution** : traduire la carte en effets et les placer dans la file d'effets. Cas particuliers :
   - **garde** : poser l'état de garde sur l'unité (zone de 8 cases), sans effet immédiat ;
   - **sort canalisé** : enregistrer un effet différé (zone affichée, lanceur en concentration), résolu en T-06 ;
   - **combo** : déjà installé en T-04, rien à exécuter.
9. **O-09 Traiter la file d'effets** (F-01 à F-08).
10. **O-10 Défausser la carte** et marquer l'ordre comme résolu.

## File d'effets et déclenchements

La file est traitée dans l'ordre d'arrivée (premier entré, premier sorti) jusqu'à ce qu'elle soit vide.

1. **F-01 Extraire** l'effet suivant de la file.
2. **F-02 Calculer les valeurs effectives** : Mouvement, portée, dégâts, en appliquant les combos de règle actifs dans leur ordre de pose (et le malus du porteur).
3. **F-03 Appliquer l'effet** selon son type :
   - **déplacement**, case par case : arrêt en entrant dans une case contrôlée par une garde adverse ; arrêt en ramassant le drapeau ; arrêt devant un obstacle (mur ou creux, infranchissables volontairement) ou une unité adverse ; traversée des alliés ;
   - **dégâts** : retrait de PV ; plaquage si la cible porte le drapeau (rebond sur une case adjacente choisie par l'attaquant, saisie) ; hors combat à 0 PV (le drapeau tombe sur sa case) ;
   - **poussée ou attraction** : contrôle de Masse ; déplacement forcé case par case ; collision (1 dégât à chaque unité, ou 1 contre un mur) ; chute dans un creux (perd son prochain ordre, lâche le drapeau) ; plaquage si la cible porte le drapeau (le drapeau reste sur la case de départ) ;
   - **passe** : trajectoire en ligne droite de 4 cases au plus ; interception par la première unité adverse ou une garde Interception ; sinon, le receveur devient porteur ;
   - **terrain** : création d'un mur ou d'un creux ;
   - **statut** : étourdi, immobilisé, muet ;
   - **soin** : PV rendus sans dépasser le maximum.
4. **F-04 Émettre les événements** produits par l'effet.
5. **F-05 Annuler les sorts canalisés** dont le lanceur vient de subir un dégât ou d'être poussé.
6. **F-06 Évaluer les combos déclencheurs** concernés par ces événements, chacun au plus une fois par tour : ceux du joueur actif d'abord, puis ceux de l'adversaire, chacun dans son ordre de pose. Leurs effets sont ajoutés en fin de file.
7. **F-07 Vérifier l'essai** : si un porteur entre dans une case de la zone de départ adverse, son déplacement s'arrête et la manche se termine immédiatement (E-01). La vérification se fait à chaque case parcourue.
8. **F-08 Boucler** sur F-01 tant que la file n'est pas vide.

La limite « une fois par tour » par combo garantit que la cascade se termine toujours.

## Fin de manche et fin de match

1. **E-01 Déterminer le vainqueur de la manche** :
   - essai (F-07) : l'équipe du porteur gagne ;
   - sinon, au départage après le tour 5 : l'équipe qui porte le drapeau gagne si le porteur est dans la moitié adverse ;
   - sinon, manche nulle.
2. **E-02 Mettre à jour le score** des manches et émettre l'événement de fin de manche.
3. **E-03 Fin de match ?** Si un joueur a 2 manches, il gagne le match ; si 3 manches ont été jouées, le match se termine (en cas d'égalité : match nul en Escarmouche ; en Compétitif, victoire à l'équipe qui a terminé le plus de tours avec le drapeau dans la moitié adverse).
4. **E-04 Sinon, préparer la manche suivante** : les cartes posées et non résolues sont défaussées, les mains sont conservées, puis retour à R-01.
5. **E-05 Fin de match** : résultat, enregistrement du flux d'événements complet pour le replay.

## Points d'attente et événements

Le moteur s'arrête pour attendre une saisie en sept points ; tous les autres enchaînements sont automatiques. Le temps est géré par une pendule d'échecs : une réserve par joueur et par manche (environ 6 minutes), plus quelques secondes par décision.

| Étape | Saisie attendue | Joueur | Réserve de temps épuisée |
| --- | --- | --- | --- |
| R-06 | Placement d'une unité | Celui dont c'est le tour de placer | Placement automatique |
| T-02 / T-03 | Programmation de toutes ses unités | Les deux, en parallèle | Validation de ce qui est posé |
| T-04 | Combo à défausser au-delà de 3 | Le joueur concerné | Le plus ancien est défaussé |
| T-05 / O-01 | Unité à résoudre | Joueur actif | Première unité dans l'ordre du plateau |
| O-06 | Effet ou leurre | Joueur actif | Effet si légal |
| O-07 | Cible, direction ou case | Joueur actif | La carte devient un leurre |
| F-03 | Case de rebond du drapeau après un dégât | L'attaquant | Première case libre dans l'ordre horaire |

Événements émis, par famille :

| Famille | Événements |
| --- | --- |
| Structure | Match commencé, manche commencée, tour commencé, programmation validée, tour terminé, manche terminée, match terminé |
| Cartes | Carte piochée, carte posée (cachée pour l'adversaire), carte révélée, carte jouée comme leurre, ordre perdu, combo installé, combo défaussé, combo déclenché, deck remélangé |
| Mouvement | Unité placée, unité déplacée, déplacement arrêté par une garde, unité poussée, unité attirée, collision, chute dans un creux |
| Combat | Dégâts subis, unité soignée, unité hors combat, statut appliqué, statut levé, garde activée, garde levée |
| Drapeau | Drapeau ramassé, lâché, passé, intercepté, essai marqué |
| Sorts et terrain | Sort canalisé lancé, résolu, annulé ; mur créé ; creux créé |

## Questions techniques ouvertes

Les huit questions relevées lors de la première rédaction sont tranchées et intégrées aux étapes ci-dessus :

| # | Question | Décision |
| --- | --- | --- |
| 1 | Ordre de placement sans draft (R-06) | Le joueur qui a l'initiative du premier tour place en premier |
| 2 | Pioche entre deux manches (R-04) | 3 cartes par joueur |
| 3 | Égalité après 3 manches (E-03) | Match nul en Escarmouche ; en Compétitif, départage par la possession (tours terminés avec le drapeau dans la moitié adverse) |
| 4 | Combos des deux joueurs sur le même événement (F-06) | Ceux du joueur actif d'abord, puis ceux de l'adversaire, chacun dans son ordre de pose |
| 5 | Entrer volontairement dans un creux | Interdit : le creux est infranchissable pour un déplacement volontaire, mais ne bloque ni tirs ni passes |
| 6 | Unité étourdie en programmation (T-02) | Emplacement bloqué ; une unité étourdie après avoir reçu une carte la perd à sa résolution (O-02) |
| 7 | Gestion du temps | Pendule d'échecs (réserve par manche + incrément) ; comportements par défaut du tableau des points d'attente |
| 8 | Moment de l'essai (F-07) | Dès l'entrée dans la zone de départ adverse ; le déplacement s'arrête et la manche se termine |

Aucune question technique ouverte à ce stade.
