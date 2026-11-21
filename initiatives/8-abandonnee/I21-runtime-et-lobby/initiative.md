---
id: I21
title: Runtime et lobby
status: in_progress
origine:
  type: idee
  par: chef d'usine
  le: 2026-11-21
  source: 
---

# I21 — Runtime et lobby

## Idée de l'humain

Idée de l'humain, issue de son plan « première boucle jouable » (numéro I2 dans son plan ; remplace notamment l'ancienne I2 « Créer et rejoindre un match Initiation »).

Contenu : « `CreateMatch` / `JoinMatch` hors moteur ; l'acteur instancie le moteur une fois la partie pleine ; timers d'étape portés en données par les étapes ; journal d'événements ; numéros de séquence. »

Crates citées par l'humain : `gambeta-match` (« un acteur tokio par partie »), `gambeta-server`, `gambeta-matchmaking`, `gambeta-meta` selon le besoin.
Dépend de : Moteur (I1 du plan).
Jalons : J2 — « Deux clients Godot jouent une vraie partie via le serveur (résolution affichée en journal, sans animation) » ; J3 — « Partie lisible et robuste : animations via le `Director`, timers visibles, reconnexion, spectateur basique ». « Une initiative peut s'étaler sur plusieurs jalons. »
Attendu : objectif, périmètre, hors périmètre, crates concernées, dépendances, critères d'acceptation vérifiables, tâches de 0,5 à 2 jours rattachées à un jalon.

*Déposée par le chef d'usine le 2026-11-21.*
