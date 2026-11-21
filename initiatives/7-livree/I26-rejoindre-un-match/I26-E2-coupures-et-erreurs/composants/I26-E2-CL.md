---
id: I26-E2-CL
parent: I26-E2
depot: client
needs: [I26-B7, I26-B10, I26-B13, I26-B20]
scenarios: [I26-E2-S1, I26-E2-S3, I26-E2-S4, I26-E2-S6]
contracts: [canal-joueur.md]
depends_on: [I26-E1-CL]
verdict: a_faire
kind: realisation
---
# I26-E2-CL — Annuler, adversaire déconnecté, retour à l'accueil

À la fin de cet epic, le joueur qui attend peut renoncer, et le joueur dont l'adversaire
part est prévenu puis ramené à l'accueil, d'où il peut rejoindre un autre match. Les
écrans suivent la maquette I26-M1 (états 1 et 4).

## Ce que le client livre

1. **Annuler** : le bouton « Annuler » de l'overlay d'attente ferme la connexion (sans
   message : c'est la fermeture qui vaut départ, d'après le contrat), retire l'overlay en
   fondu, et l'accueil redevient utilisable (I26-B7).
2. **Adversaire déconnecté** : à la réception de `adversaire_deconnecte`, l'overlay
   « Adversaire déconnecté » s'affiche sur l'arène, titre en rouge, avec « Le match est
   terminé. Retour à l'accueil dans N s. », un compte à rebours de 5 s, puis le retour à
   la page d'accueil ; le bouton « Retour à l'accueil » y ramène tout de suite (I26-B10).
   Le repère « Joueur N » disparaît avec l'arène.
3. **Nouvelle demande** : après un retour à l'accueil (Annuler, fin de match), le lien
   repart de zéro : nouvelle connexion, `command_id` et `seq` remis à 1 au prochain clic.
   Le client ne tente aucune reconnexion à l'ancien match (I26-B13).
4. **Mode automatique** (`--rejoindre`, I26-E1-CL) : la réception de
   `adversaire_deconnecte` est écrite dans le rapport, et le client quitte avec un code
   non nul.

## Preuve attendue

Tests GUT headless dans `test/unit/`, sans réseau, avec la doublure du lien d'I26-E1-CL
(I26-B20) :
- attente → « Annuler » : la connexion est fermée, l'overlay retiré, l'accueil
  utilisable (S1) ;
- arène → `adversaire_deconnecte` : overlay « Adversaire déconnecté », retour à
  l'accueil au bout de 5 s (S3) ;
- même situation, clic sur « Retour à l'accueil » : retour immédiat (S4) ;
- après un retour à l'accueil, un nouveau clic ouvre une nouvelle connexion avec
  `command_id` 1 (S6).

Et, à la main, S1, S3 et S6 avec `make run-server` et deux `make run-client`.
`make lint`, `make typecheck` et `make test` passent.
