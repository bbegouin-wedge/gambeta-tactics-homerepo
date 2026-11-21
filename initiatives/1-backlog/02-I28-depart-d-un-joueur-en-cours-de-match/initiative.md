---
id: I28
title: Départ d'un joueur en cours de match
origine:
  type: remontee
  par: humain
  le: 2026-11-21
  source: "vérification d'I27 avant promotion (deux clients Godot contre le vrai serveur)"
---

# I28 — Départ d'un joueur en cours de match

## Constat (défaut présent depuis I26)

Quand un joueur quitte un match, l'autre voit « Impossible de rejoindre le serveur de jeu »
au lieu de « Adversaire déconnecté » (I26-B9, B10 non tenus avec de vrais clients).

- Le serveur est conforme au contrat : il envoie `adversaire_deconnecte` (et la trace
  `adversaire_parti`), **puis** ferme la connexion aussitôt. Vérifié avec un client
  WebSocket Python : tout arrive.
- Le `WebSocketPeer` de Godot **jette les paquets reçus dans le même lot que la trame de
  fermeture** : à l'image suivante, état `CLOSED`, 0 paquet disponible. Le client ne voit
  qu'une connexion perdue (`PERDUE` → état `INJOIGNABLE`).
- Non détecté par I26 : côté client, ce départ n'est testé qu'avec le faux serveur ; côté
  serveur, avec tungstenite. Aucun test ne le fait passer par de vrais clients Godot.
- Reproduction : deux clients `make run-client TRACES=1` contre `make run-server`, rejoindre,
  fermer un client ; la console de l'autre montre `connexion_fermee cause=serveur` sans
  `adversaire_deconnecte`.

## Piste de correction (à grillier)

Après `adversaire_deconnecte`, le serveur laisse le client fermer lui-même la connexion, et
ne la ferme qu'au bout d'un délai de grâce (par exemple 2 s). Changement de contrat
(« le serveur ferme ensuite la connexion »), compatible. Le client n'a rien à changer : il
lit le message à l'image suivante, et ignore déjà la fermeture une fois l'adversaire parti.

## Idée de l'humain

Le bon message serait : « Adversaire déconnecté, vous gagnez la partie dans 30 secondes ».
C'est une règle nouvelle — **victoire par forfait** — qui touche `product/`. Le grilling
devra dire à quoi servent ces 30 s : simple compte à rebours, ou délai laissé au partant
pour revenir (reconnexion, écartée par I26 faute d'identité des joueurs).

## À ajouter aux preuves

Le départ de l'adversaire avec de vrais clients Godot, dans un scénario de bout en bout
(`ci/scenarios/`) : le restant doit recevoir `adversaire_deconnecte`.
