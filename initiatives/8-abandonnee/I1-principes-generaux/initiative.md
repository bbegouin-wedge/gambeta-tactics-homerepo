---
id: I1
title: Principes généraux
origine:
  type: idee
  par: humain
  le: 2026-11-19
  source: "product/Boucle de gameplay — étapes techniques.md"
---

# I1 — Principes généraux

Les principes que toutes les autres initiatives supposent, à fixer avant tout code :
le serveur fait autorité sur l'état et sur l'information cachée ; chaque étape émet
des événements, filtrés par joueur à la diffusion ; aucun hasard hors du mélange des
decks et du tirage de l'initiative (graine enregistrée, pour le replay) ; le moteur
s'arrête aux points d'attente pour une saisie. Le grilling fixe le protocole du canal
d'un joueur (relation `client-plays-on-backend`, aujourd'hui `planned`), la nature
de ses contrats (générés ou écrits, par un ADR), et la stack du backend.

Références : `product/Boucle de gameplay — étapes techniques.md` (principes communs, points d'attente et événements), `product/Game design — v0.16.md`
(vision et piliers). Côté client, la maquette de l'écran de match existe déjà.
