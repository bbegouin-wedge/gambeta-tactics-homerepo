---
id: I23
title: Client Godot de la boucle
status: in_progress
origine:
  type: idee
  par: chef d'usine
  le: 2026-11-21
  source: 
---

# I23 — Client Godot de la boucle

## Idée de l'humain

Idée de l'humain, issue de son plan « première boucle jouable » (numéro I4 dans son plan).

Contenu : « `ServerLink`, `MatchStore`, `Director`, grille, main en glisser-déposer d'une carte sur l'icône d'un minion, révélation, journal de résolution. »
Architecture client citée par l'humain : « un client Godot séparé : `ServerLink` → `MatchStore` (read model) → `Director` (file de présentation) → vues. »

Dépendance explicite : « I4 démarre dès ce contrat figé, en rejouant des logs d'événements produits par I5, sans attendre le serveur » — contrat = enums `Command` / `Event` et API figés en première tâche du Moteur (I1 du plan) ; logs = export de l'Outillage (I5 du plan).
Jalons : J2 — « Deux clients Godot jouent une vraie partie via le serveur (résolution affichée en journal, sans animation) » ; J3 — « Partie lisible et robuste : animations via le `Director`, timers visibles, reconnexion, spectateur basique ».
Contexte : I17 (catalogue et rendu des cartes), conservée par l'humain, est en réalisation ; le rendu des cartes de la main peut la recouper.
Attendu : objectif, périmètre, hors périmètre, dossiers concernés, dépendances, critères d'acceptation vérifiables, tâches de 0,5 à 2 jours rattachées à un jalon.

*Déposée par le chef d'usine le 2026-11-21.*
