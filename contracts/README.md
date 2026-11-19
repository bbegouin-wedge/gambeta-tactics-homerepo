# Contrats entre composants

Aucun encore. Le canal d'un joueur (relation `client-plays-on-backend`,
`planned`) est fixé par l'initiative I1, qui dira aussi par un ADR quels
contrats sont **générés** depuis le code d'un composant (en-tête `# GÉNÉRÉ`,
`scripts/extract-contracts` et un extracteur dans `scripts/extractors/`) et
lesquels sont **écrits** à la main.

Arborescence prévue, comme dans bbtrainer-homerepo :

```
api/<composant>/       API HTTP (OpenAPI)
events/<domaine>/      canaux et messages (AsyncAPI, JSON Schema)
```

Tout fichier ici est porté par au moins une relation de `system/relations.yaml`.
