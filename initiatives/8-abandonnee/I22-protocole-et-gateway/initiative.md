---
id: I22
title: Protocole et gateway
status: in_progress
origine:
  type: idee
  par: chef d'usine
  le: 2026-11-21
  source: 
---

# I22 — Protocole et gateway

## Idée de l'humain

Idée de l'humain, issue de son plan « première boucle jouable » (numéro I3 dans son plan).

Contenu : « Enveloppes client/serveur, choix du format de sérialisation, route WebSocket, projection par joueur, reconnexion (snapshot + événements manquants). »

Crates citées par l'humain : `gambeta-protocol`, `gambeta-gateway` (« WebSocket »).
Dépendance explicite : « I3 dépend du contrat, pas de l'implémentation des règles » — c'est-à-dire des enums `Command` / `Event` et de l'API `decide` / `apply` / `legal_actions` / `view_for` figés en première tâche du Moteur (I1 du plan).
Jalons : J2 — « Deux clients Godot jouent une vraie partie via le serveur (résolution affichée en journal, sans animation) » ; J3 — « Partie lisible et robuste : animations via le `Director`, timers visibles, reconnexion, spectateur basique ».
Attendu : objectif, périmètre, hors périmètre, crates concernées, dépendances, critères d'acceptation vérifiables, tâches de 0,5 à 2 jours rattachées à un jalon.

*Déposée par le chef d'usine le 2026-11-21.*
