# Contrats entre composants

| Contrat | Relation | Forme |
|---|---|---|
| [`canal-joueur.md`](canal-joueur.md) | `client-plays-on-backend` | écrit à la main, Markdown (I26) |

Un contrat est **écrit** à la main tant qu'aucun outillage ne le **génère** depuis le code
d'un composant. Un contrat généré porterait l'en-tête `# GÉNÉRÉ` et serait produit par
`scripts/extract-contracts` avec un extracteur de `scripts/extractors/` (aucun encore) ;
`scripts/checks/drift` compare alors le code et `contracts/`.

Le passage à un format machine (AsyncAPI, JSON Schema) se décidera quand le nombre de
messages le justifiera (I26, Q6). Arborescence prévue alors :

```
api/<composant>/       API HTTP (OpenAPI)
events/<domaine>/      canaux et messages (AsyncAPI, JSON Schema)
```

Tout fichier ici est porté par au moins une relation de `system/relations.yaml`.
