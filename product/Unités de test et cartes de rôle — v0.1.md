# Unités de test et cartes de rôle — v0.1

Nov 15, 2026 · @Bertrand

Cinq unités de test, une par rôle, pour le prototype du mode Escarmouche ; chacune apporte au deck 2 cartes de son rôle et 1 carte propre. Règles de référence : document de game design v0.16 (variante A des caractéristiques : PV, Mouvement, Masse).

## Listes de cartes de rôle

Chaque rôle a une liste commune de 4 cartes ; une unité en apporte 2 au deck, jouables par n'importe quelle unité de ce rôle dans l'équipe.

| Rôle | Carte | Type | Effet |
| --- | --- | --- | --- |
| Striker | Charge | Attaque | Avance en ligne jusqu'à 3 cases, puis 2 dégâts et pousse d'une case la première unité rencontrée |
| Striker | Percée | Attaque | Case adjacente, sans dégât, pousse de 2 cases |
| Striker | Coup de balayage | Attaque | Cône de 3 cases devant l'unité, 1 dégât |
| Striker | Riposte | Garde | L'unité qui entre dans la zone s'arrête et subit 1 dégât |
| Tank | Bastion | Garde | Zone de 2 cases de rayon ; l'unité qui y entre s'arrête |
| Tank | Repousser | Garde | L'unité qui entre dans la zone s'arrête et recule d'une case |
| Tank | Immobiliser | Attaque | Case adjacente, la cible est immobilisée |
| Tank | Bouclier | Soutien | Jusqu'à sa prochaine activation, un allié adjacent subit 1 dégât de moins |
| Coureur | Esquive | Mouvement | Déplacement qui ignore les gardes |
| Coureur | Interception | Garde | Zone en ligne de 4 cases : intercepte une passe qui la traverse |
| Coureur | Échange | Mouvement | Échange sa place avec un allié à 3 cases ou moins |
| Coureur | Appel | Mouvement | Déplacement de 2 cases, puis le porteur allié peut lui passer le drapeau sans dépenser son propre ordre |
| Support | Ériger un mur | Sort instantané | Mur de 2 cases à portée 3 |
| Support | Creuser | Sort instantané | Creux à portée 3 |
| Support | Soin | Soutien | +2 PV à un allié à portée 2 |
| Support | Harpon | Attaque | Attire une unité de 2 cases, portée 4, ligne de vue |
| Caster | Tir précis | Attaque | Portée 4, ligne de vue, 2 dégâts |
| Caster | Pluie de braises | Sort canalisé | Zone 2 × 2 à portée 4, 2 dégâts |
| Caster | Onde de choc | Sort canalisé | Repousse d'une case les unités autour d'une case ciblée |
| Caster | Harpon | Attaque | Attire une unité de 2 cases, portée 4, ligne de vue |

## Les 5 unités

| Unité | Rôle | PV | Mouvement | Masse | Passif | Cartes de rôle | Carte propre |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Brise-Ligne | Striker | 4 | 3 | Lourde | Élan | Charge, Percée | Bélier |
| Gardien de Pierre | Tank | 6 | 2 | Lourde | Ancré | Bastion, Repousser | Muraille |
| Feu-Follet | Coureur | 3 | 5 | Légère | Insaisissable | Interception, Échange | Appel de balle |
| Veilleuse | Support | 3 | 3 | Légère | Halo | Ériger un mur, Creuser | Translocation |
| Conjuratrice | Caster | 3 | 2 | Moyenne | Focalisation | Pluie de braises, Harpon | Entrave |

### Brise-Ligne · Striker

- **Passif, Élan** : quand elle provoque une collision, la collision inflige 2 dégâts au lieu de 1.
- **Carte propre, Bélier** : case adjacente, 1 dégât, pousse de 2 cases.
- **Identité** : elle transforme les murs et les creux en armes ; faite pour ouvrir un couloir en pleine défense.

### Gardien de Pierre · Tank

- **Passif, Ancré** : ne peut être ni poussé ni attiré.
- **Carte propre, Muraille** : garde dont la zone bloque aussi les tirs et les passes qui la traversent.
- **Identité** : un point fixe qu'on ne déplace pas ; il faut le contourner ou passer le drapeau ailleurs.

### Feu-Follet · Coureur

- **Passif, Insaisissable** : la première fois par tour qu'il entre dans une zone de garde, il ne s'arrête pas.
- **Carte propre, Appel de balle** : se déplace de sa valeur de Mouvement ; à l'arrivée, si le porteur allié est en ligne droite à 4 cases ou moins, le drapeau lui est passé, avec les règles d'interception habituelles.
- **Identité** : le finisseur ; il crée une passe sans coûter l'ordre du porteur, mais il est fragile.

### Veilleuse · Support

- **Passif, Halo** : les alliés adjacents subissent 1 dégât de moins.
- **Carte propre, Translocation** : échange la position de deux alliés à portée 3.
- **Identité** : elle sculpte le terrain et repositionne les alliés ; ses creux sont le terrain de jeu de Brise-Ligne.

### Conjuratrice · Caster

- **Passif, Focalisation** : ses sorts canalisés ne sont pas annulés par une poussée, seulement par des dégâts.
- **Carte propre, Entrave** : sort instantané, portée 4, ligne de vue ; la cible est muette et immobilisée ce tour-ci, sans dégât.
- **Identité** : le contrôle à distance, et la meilleure réponse à une barricade autour du porteur.

## Synergies et contres

Les unités sont conçues par paires : chaque synergie a un contre identifiable dans le même pool.

| Synergie | Comment elle joue | Contre |
| --- | --- | --- |
| Veilleuse + Brise-Ligne | Creux et mur posés, puis poussée dedans avec Élan : le combo de base du jeu | Gardien de Pierre, impossible à pousser |
| Feu-Follet + porteur | Appel de balle et Insaisissable font de la passe une arme de percée | Muraille, qui coupe les passes ; Interception adverse |
| Gardien de Pierre + Conjuratrice | Le premier fixe la défense, la seconde neutralise l'attaquant le plus dangereux avec Entrave | Tir précis ou Frappe sur Conjuratrice, qui annule sa Pluie de braises |

## Protocole des premiers tests

Les premiers matchs se jouent en miroir, pour tester les règles sans biais de composition.

1. **Matchs miroir** : les deux joueurs avec la même équipe (Brise-Ligne, Gardien de Pierre, Feu-Follet, Veilleuse) ; seules les décisions diffèrent.
2. **Entrée des sorts** : Conjuratrice remplace l'une des quatre unités dans une équipe, pour mesurer l'effet des sorts canalisés.
3. **Mesures à relever** (priorités du document de game design) : économie de la main, durée de la garde, taux d'essai.

Points de vigilance spécifiques à ces unités :

- [ ] Appel de balle et Appel (rôle Coureur) rendent-ils les passes trop faciles ?
- [ ] Ancré rend-il Gardien de Pierre trop dominant face aux strikers ?
- [ ] Élan + Creuser : la paire Veilleuse et Brise-Ligne est-elle trop forte en combo ?
- [ ] Les unités à 3 PV (Feu-Follet, Veilleuse, Conjuratrice) survivent-elles assez longtemps pour jouer leur rôle ?
