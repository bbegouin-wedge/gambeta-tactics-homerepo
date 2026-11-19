---
name: initiative-systeme
description: Ouvrir, cadrer et faire avancer une initiative du projet Gambeta Tactics dans le kanban du home repo (backlog, grilling, maquettes, epics projet, projection sur backend et client). À utiliser quand l'utilisateur veut lancer une évolution du jeu, modifier un contrat entre le client et le backend, ou ajouter une dépendance entre composants.
---

# Mener une initiative du projet

Suivre l'ordre du flux de `CLAUDE.md` et `decisions/0002`. Chaque étape produit
un livrable **présenté et validé avant d'être écrit**. Quand la software factory
conduit l'initiative, la laisser faire : ne pas déplacer l'initiative à la main.

## 1. Ouvrir

Toute évolution naît ici, même si elle ne touche qu'un composant.
- Id : `I<n>`, `n` = le plus grand existant + 1, toutes colonnes confondues.
- Dossier `initiatives/1-backlog/<nn>-I<n>-<slug>/` (`nn` : priorité), d'après
  `initiatives/_modele/initiative.md`, avec son origine.

## 2. Grilling

Dans `initiatives/2-grilling/I<n>-<slug>/grilling.md` : une question à la fois,
chacune avec son contexte (sections de `product/`, étapes `M-`/`R-`/`T-`/`O-`/`F-`/`E-`,
état des composants lu dans `workspace/`), une recommandation et la réponse de
l'utilisateur. En sortent des besoins numérotés `I<n>-B<k>`, vérifiables.
Un changement de règle met aussi à jour le document de `product/` concerné.

## 3. Maquettes

S'il y a de l'écran : `I<n>-M<k>`, validées. La maquette du client
(`scenes/mockup/`) est le point de départ.

## 4. Epics projet

`initiatives/4-epics/I<n>-<slug>/I<n>-E<k>-<slug>/epic.md` : étapes métier
livrables, chacune avec ses scénarios de bout en bout vus du joueur. Découpage
validé en bloc.

## 5. Projection (par epic projet)

`projection.md` dans `initiatives/5-realisation/…` :
- les epics composant `I<n>-E<k>-BE` et `I<n>-E<k>-CL`, chacun rattaché à une
  responsabilité écrite de `system/components.yaml` ; sinon, escalade
  « architecture » (ADR), l'epic s'arrête ;
- chaque contrat touché (`contracts/`) : changement décrit, compatible ou non,
  ordre de livraison ; nouvelle dépendance → `system/relations.yaml` ;
- chaque besoin et chaque scénario couverts ;
- relecture de sa part par chaque composant, dans son dépôt (à faire, déjà
  fait, hors responsabilités).

Les tickets s'écrivent ensuite **dans le kanban du composant**, selon ses
propres règles (lire son `CLAUDE.md`). Ne pas les créer d'ici sans le demander.

## 6. Candidat

`manifests/candidates/<id>.yaml` (voir son README), SHA reportés au fil des
fusions. Puis skill `integration`.

`make structure` doit passer après chaque étape.
