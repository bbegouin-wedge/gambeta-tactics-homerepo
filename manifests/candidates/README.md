# Manifestes candidats

Un fichier par initiative en réalisation : `<id>.yaml`, du même nom que son
répertoire dans `initiatives/`. Il ne fixe que les composants que
l'initiative change ; les autres héritent de `../current.yaml`.

```yaml
manifest: candidate
initiative: I1-principes-generaux
components:
  backend:
    sha: <40 hexa>        # commit de main qui livre la part du backend
  client:
    sha: <40 hexa>
```

On met les SHA à jour au fil des fusions dans chaque composant, puis :

```bash
uv run ci/integrate manifests/candidates/<id>.yaml            # vérifier
uv run ci/integrate manifests/candidates/<id>.yaml --promote  # sur validation
```

La promotion réécrit `current.yaml` et supprime le candidat.
