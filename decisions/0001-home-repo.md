# 0001 — Un home repo pour le système

- Statut : acceptée
- Date : 2026-11-19

## Contexte

Gambeta Tactics est fait de deux dépôts qui évolueront ensemble : le
`backend` (le serveur de jeu, vide à ce jour) et le `client` (Godot, une
maquette de l'écran de match). Le game design vit dans `docs/` du backend,
alors qu'il décrit le produit entier. Le client recopie à la main les textes
des cartes de ces docs (`data/cards.json`) et génère ses assets depuis un
clone d'OpenDuelyst dont rien ne fixe la version.

Le système bbTrainer a déjà un home repo (`bbtrainer-homerepo`) ; on en
reprend l'organisation et l'outillage.

## Décision

Un dépôt dédié, sans code de composant, porte :

- le modèle du système (composants, codes courts, responsabilités, relations) ;
- les contrats entre composants ;
- des manifestes : la baseline (SHA intégrés) et les candidats par initiative ;
- le game design (`product/`), copié depuis le backend ;
- les initiatives et les décisions transverses ;
- l'outillage pour monter les composants à un manifeste et vérifier la dérive.

Les composants gardent leur autonomie : leur `CLAUDE.md`, leur kanban, leurs
portes. Le home repo ne fait que les appeler.

Pas de doublure du serveur pour l'instant : si le client a besoin de jouer
sans le vrai backend, elle viendra comme composant par un ADR.

OpenDuelyst est un composant `data`, fixé par le manifeste mais non monté
dans `workspace/` (`mount: false`) : il ne sert qu'à régénérer les assets,
commités dans le client.

## Conséquences

- Une évolution a un seul endroit où commencer et un seul endroit où dire
  qu'elle est intégrée.
- La baseline n'avance que par intégration réussie d'un candidat.
- Aucun contrat à l'amorçage : la relation client → backend est `planned`,
  l'initiative I1 la formalise.
- Aucun composant n'a encore de portes (`gates`) : l'intégration ne vérifie
  pour l'instant que la structure et la dérive.
- Coût : tenir les relations et les contrats à jour. Les checks de dérive
  sont là pour que l'oubli se voie.
