---
id: I19
title: Règles v0 de la boucle
status: in_progress
origine:
  type: idee
  par: chef d'usine
  le: 2026-11-21
  source: 
---

# I19 — Règles v0 de la boucle

## Idée de l'humain

Idée de l'humain, issue de son plan « première boucle jouable » (numéro I0 dans son plan ; remplace, avec les cinq autres idées du plan, les anciennes initiatives du backlog I1 à I16 et I18).

Objectif : « Document de règles servant de spec : plateau, stats des minions, les 5 ordres, main et pioche, initiative, alternance, drapeau. Valeurs numériques dans un `Ruleset` paramétrable. »

Première boucle jouable, selon l'humain : « la création et la jonction d'une partie, le tirage de la main, le tirage de l'initiative, puis un tour complet : assignation face cachée, révélation et résolution alternée des 5 ordres de base (Mouvement, Sprint, Attaque, Garde, Passe du drapeau). »

Décidé :
- « les ordres et leur cible sont choisis à l'assignation, face cachée » ;
- « le geste est un glisser-déposer d'une carte de la main sur l'icône du minion ».

Hypothèses provisoires, « à marquer comme telles » :
- « en résolution, le joueur dont c'est l'alternance choisit lequel de ses minions agit » ;
- « 0 ou 1 ordre par minion, avec une main plus petite que le roster » ;
- « l'attaque est déterministe : l'aléa vient seulement de la pioche et de l'initiative » ;
- « l'alternance commence par le joueur qui a l'initiative ; un camp sans ordre restant laisse l'autre terminer ».

Questions ouvertes, « à lister sans les trancher » :
- « comment désigner la case de destination ou le receveur d'une passe lors du glisser-déposer » ;
- « taille de grille, stats des minions, composition de la pioche » ;
- « règles du drapeau (prise, perte, condition de victoire) » ;
- « effet exact de la Garde » ;
- « conflits de déplacement (deux minions vers la même case) » ;
- « gestion des ordres devenus caducs, puisque la cible est fixée avant que le plateau bouge ».

Consigne de l'humain : « N'invente aucune règle de jeu : tout point non tranché devient une question ouverte. »

Jalon : J1 — « Un tour complet joué en local, sans réseau (bots ou hot-seat en ligne de commande) » (I0, I1, I5 du plan).
Attendu pour chaque initiative du plan : objectif, périmètre, hors périmètre, crates ou dossiers concernés, dépendances, critères d'acceptation vérifiables (« le test X passe », « `check-arch.sh` est vert »), tâches de 0,5 à 2 jours rattachées chacune à un jalon.

*Déposée par le chef d'usine le 2026-11-21.*
