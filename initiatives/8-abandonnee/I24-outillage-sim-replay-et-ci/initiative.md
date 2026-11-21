---
id: I24
title: Outillage sim, replay et CI
status: in_progress
origine:
  type: idee
  par: chef d'usine
  le: 2026-11-21
  source: 
---

# I24 — Outillage sim, replay et CI

## Idée de l'humain

Idée de l'humain, issue de son plan « première boucle jouable » (numéro I5 dans son plan).

Contenu : « Bot aléatoire et hot-seat en ligne de commande dans `gambeta-sim`, export de logs d'événements, lecteur de replay en ligne de commande, `check-arch.sh` et lints en CI. »

Dépend de : Moteur (I1 du plan). Ses logs d'événements alimentent le client Godot (I4 du plan), qui démarre en les rejouant.
Jalon : J1 — « Un tour complet joué en local, sans réseau (bots ou hot-seat en ligne de commande) ».
Attendu : objectif, périmètre, hors périmètre, crates concernées, dépendances, critères d'acceptation vérifiables (par exemple « `check-arch.sh` est vert »), tâches de 0,5 à 2 jours rattachées à un jalon.

*Déposée par le chef d'usine le 2026-11-21.*
