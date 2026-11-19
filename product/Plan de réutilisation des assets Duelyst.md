# Plan de réutilisation des assets Duelyst

Nov 15, 2026 · @Bertrand

Les assets d'OpenDuelyst, publiés en CC0, servent à prototyper le jeu sous Godot sans attendre une direction artistique propre ; ils sont isolés derrière un manifeste pour pouvoir être remplacés plus tard.

## Cadre juridique

Le dépôt OpenDuelyst est sous licence CC0 1.0 (fichier LICENSE à la racine) : code et assets créés par Counterplay sont utilisables librement, y compris commercialement, sans attribution.

| Élément | Statut | Action |
| --- | --- | --- |
| Sprites d'unités, icônes, effets, décors, interface | Couverts par CC0 | Réutilisables |
| Nom « Duelyst », logo (ui/brand\_duelyst.png) | Marque, non couverte par CC0 | Ne jamais utiliser |
| Police Lato | Licence libre (OFL), indépendante de Duelyst | Réutilisable |
| Polices Trump Gothic Pro et Averta | Polices commerciales probablement sous licence tierce | Ne pas reprendre, remplacer par des polices libres |
| Font Awesome | Licence propre au projet Font Awesome | Vérifier la version et sa licence avant usage |
| Musiques et effets sonores | Origine non vérifiée | Vérifier avant tout usage au-delà du prototype local |
| Contenu de Duelyst II (Dream Sloth) | Hors CC0 | Ne rien reprendre |

## Inventaire des assets

Tout se trouve dans `app/resources/` ; six dossiers couvrent l'essentiel des besoins du prototype.

| Dossier | Fichiers | Contenu | Intérêt |
| --- | --- | --- | --- |
| `units/` | 1 392 | Planches de sprites animés (images de 100 × 100 px) + fichiers `.plist`, environ 700 créatures et généraux | Fort : les unités du jeu |
| `icons/` | 746 | Icônes animées des sorts et artefacts (48 × 48 px) | Fort : illustrations des cartes d'action et de combo |
| `fx/` et `particles/` | 568 | Effets visuels animés (impacts, sorts, explosions) | Fort : retour visuel des attaques et des poussées |
| `ui/` | 307 | Boutons, cadres, fonds de carte, barres, bouton de fin de tour | Fort : kit d'interface |
| `maps/` et `scenes/` | 207 | Décors de champ de bataille en couches (fond, plan moyen, avant-plan), en simple et double résolution | Fort : fond du plateau |
| `tiles/` | 72 | Grille, survol, case d'attaque, coffre au trésor | Moyen : états des cases |
| `card_backgrounds/` | 138 | Dos de cartes | Moyen : cartes face cachée |
| `generals/` | 124 | Portraits des généraux, double résolution | Moyen : portraits d'unités, écran de draft |
| `crests/` | 32 | Emblèmes des factions | Faible : bases ou équipes |
| `emotes/` | 520 | Émoticônes de joueurs | Plus tard : communication en ligne |
| `sfx/` et `music/` | 693 | Sons et musiques | En attente de vérification de licence |

La correspondance carte → sprite est déjà faite pour les 836 cartes jouables (colonne Sprite de la Sheet « Cartes Duelyst »).

## Correspondance avec les besoins du jeu

Le noyau des règles est couvert à 80 % par les assets existants ; les manques sont le drapeau, les bases, les murs et les creux.

| Besoin du jeu | Source Duelyst | Couverture |
| --- | --- | --- |
| Unités (5 rôles, une vingtaine au total) | `units/` : sprites animés attente, course, attaque, coup reçu, mort | Complète |
| Illustrations des cartes d'action et de combo | `icons/` | Complète |
| Cartes face cachée | `card_backgrounds/card_back*` | Complète |
| Cadres de cartes en main | `ui/card_background*` | Complète |
| Plateau et fond | `maps/`, `scenes/`, `tiles/tile_grid`, `tile_hover`, `tile_attack` | Complète pour une grille 9 × 5 |
| Effets d'attaque, de poussée, de soin | `fx/`, `particles/` | Large |
| Drapeau et bases | Aucun équivalent ; `tiles/item_treasurechest` ou `crests/` en substitut | À créer |
| Mur | Aucun obstacle de terrain dans Duelyst | À créer ou à prendre ailleurs (tuiles CC0) |
| Creux | Aucun équivalent | À créer |
| Animations de poussée et de chute | Absentes : seulement attente, course, attaque, coup reçu, mort | À simuler par déplacement interpolé + animation « coup reçu » |
| Slots de combo, marqueurs d'ordre | Pas d'équivalent direct ; cadres de `ui/` adaptables | À composer |

**Recommandation pour le prototype** : adopter la grille 9 × 5 de Duelyst plutôt que 8 × 6. Les décors sont dessinés pour ces dimensions ; les changer obligerait à retoucher chaque fond.

## Écrans du jeu

Le prototype a besoin de trois écrans ; seul l'écran de match se construit en grande partie avec les assets Duelyst, les autres sont à concevoir.

| Écran | Phase | Reprise depuis Duelyst | À concevoir |
| --- | --- | --- | --- |
| Match (plateau) | Prototype noyau | Fond de carte, grille, sprites, effets, cadres de cartes, bouton de fin de tour (devient « Valider la programmation ») | Cartes face cachée posées sur les unités, 3 slots de combo, indicateur d'initiative, compteur de tours et de manches, drapeau et bases |
| Fin de manche et de match | Prototype noyau | Cadres et fonds de `ui/` | Score des manches, main conservée, bouton « Manche suivante » |
| Choix des équipes | Prototype noyau (équipes fixes) | Portraits de `generals/`, cadres de collection | Sélection simple de 4 unités |
| Draft et ban | Extension 1 | Mise en page de la collection comme référence, portraits, emblèmes | Séquence de bans et de choix en serpent, minuteur, zone titulaires / remplaçants |
| Codex des unités | Plus tard | Structure de `codex/` | Fiche d'unité (PV, Mouvement, Masse, passif, cartes) |
| Menu principal | Plus tard | Fonds de `play/` | Identité propre, sans le nom ni le logo Duelyst |

Les écrans propres à l'économie de Duelyst (boutique, coffres, boosters, quêtes, récompenses de saison) ne sont pas repris.

## Pipeline d'import dans Godot

Un script convertit une fois pour toutes les planches Duelyst en ressources Godot ; le jeu ne référence jamais un fichier Duelyst directement, seulement un identifiant de manifeste.

1. **Extraction ciblée** : ne copier dans le projet que les assets retenus (une vingtaine d'unités, les icônes des cartes, un décor, le kit d'interface), pas les 4 000 fichiers.
2. **Conversion des planches** : un script Python lit chaque `.plist` (format Cocos2d / TexturePacker) et génère une ressource `SpriteFrames` Godot, une animation par préfixe (attente, course, attaque, coup reçu, mort).
3. **Rendu pixel art** : filtre de texture « Nearest », agrandissement par facteur entier (×2 ou ×3), jamais de lissage.
4. **Orientation** : les sprites regardent dans un seul sens ; l'équipe adverse est retournée horizontalement.
5. **Manifeste** : un fichier (JSON ou ressource Godot) associe chaque identifiant de jeu (`unit.striker_01`, `card.charge`, `terrain.wall`) à ses assets. Remplacer la direction artistique revient à changer ce fichier.
6. **Audio** (si la licence est confirmée) : conversion des `.m4a` en `.ogg`, format que Godot importe nativement.

Le serveur MCP Funplay permet de faire tester l'import par Claude Code : charger une unité, lancer la scène, prendre une capture.

## Plan par étapes

Les assets Duelyst servent jusqu'à la validation du gameplay ; la direction artistique propre arrive ensuite, sans toucher au code grâce au manifeste.

1. **Vérifications** : statut des polices, des musiques et des sons ; choix d'une police libre en remplacement de Trump Gothic et Averta.
2. **Sélection** : une vingtaine d'unités (4 par rôle) choisies dans la Sheet « Cartes Duelyst » pour leur lisibilité à l'écran, les icônes des cartes du noyau, un décor, le kit d'interface.
3. **Pipeline** : script de conversion `.plist` → `SpriteFrames`, manifeste, scène de test avec une unité animée sur une case.
4. **Comblement des manques** : drapeau, bases, mur et creux en placeholders simples ou en tuiles CC0 d'autres sources (Kenney, Dungeon Crawl Stone Soup), à harmoniser avec le pixel art.
5. **Prototype du noyau** : écran de match complet, écran de fin de manche, sélection simple des équipes.
6. **Sortie de la direction artistique Duelyst** : une fois le gameplay validé, définition d'une identité visuelle propre, puis remplacement progressif via le manifeste (interface d'abord, unités ensuite).

## Risques

Le principal risque n'est pas juridique : c'est que le prototype soit perçu comme un clone de Duelyst.

| Risque | Effet | Parade |
| --- | --- | --- |
| Effet clone | Les testeurs jugent le jeu par rapport à Duelyst plutôt que sur ses règles | Le garder en tête en lisant les retours ; changer la DA avant toute diffusion publique |
| Résolution des sprites (100 px) | Inadaptée à de grandes illustrations | Garder les sprites sur le plateau, pas en grand format |
| Décors liés à la grille 9 × 5 | Une autre taille de grille demande de retoucher les fonds | Prototyper en 9 × 5 |
| Animations manquantes (poussée, chute) | Retour visuel pauvre sur la mécanique centrale | Interpolation de position + effets de `fx/` |
| Éléments tiers (polices, audio) | Usage non couvert par CC0 | Exclus tant qu'ils ne sont pas vérifiés |
| Marque Duelyst | Risque de confusion | Aucun nom, logo ni mention dans le jeu |

## Sources

- [Dépôt OpenDuelyst sur GitHub](https://github.com/open-duelyst/duelyst) (licence CC0 1.0, fichier LICENSE)
- [Funplay MCP pour Godot](https://github.com/FunplayAI/funplay-godot-mcp)
