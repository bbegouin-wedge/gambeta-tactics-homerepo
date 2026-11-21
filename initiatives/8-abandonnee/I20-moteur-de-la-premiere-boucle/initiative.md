---
id: I20
title: Moteur de la première boucle
status: in_progress
origine:
  type: idee
  par: chef d'usine
  le: 2026-11-21
  source: 
---

# I20 — Moteur de la première boucle

## Idée de l'humain

Idée de l'humain, issue de son plan « première boucle jouable » (numéro I1 dans son plan, à ne pas confondre avec l'ancienne I1 « Principes généraux » qu'elle remplace avec le reste du backlog).

Contenu : « Portage d'`automaton` (brief de portage existant), puis les étapes `Setup` → `Planning` → `Reveal` → `Resolution` → `EndOfTurn` ; les 5 ordres ; `legal_actions` ; `view_for` (information cachée) ; tests de propriétés. »

Contrainte transverse « le contrat d'abord » : « La première tâche de I1 est de figer les enums `Command` et `Event` de la boucle, ainsi que l'API `decide` / `apply` / `legal_actions` / `view_for`, même si les règles derrière restent provisoires. » Ce contrat débloque le client Godot (I4 du plan) et le protocole (I3 du plan).

Dépend de : Règles v0 (I0 du plan).
Crates concernées citées par l'humain : `automaton` (« cœur générique de la machine à états, pur »), `gambeta-engine` (« étapes et règles, pur »).
Jalon : J1 — « Un tour complet joué en local, sans réseau (bots ou hot-seat en ligne de commande) ».
Attendu : objectif, périmètre, hors périmètre, crates concernées, dépendances, critères d'acceptation vérifiables, tâches de 0,5 à 2 jours rattachées à un jalon.

*Déposée par le chef d'usine le 2026-11-21.*
