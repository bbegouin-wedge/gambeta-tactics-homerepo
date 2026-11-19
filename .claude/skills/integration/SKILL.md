---
name: integration
description: Monter le workspace aux SHA d'un manifeste, intégrer un manifeste (baseline ou candidat), lire la dérive des contrats et des SHA, et promouvoir un candidat en baseline. À utiliser quand l'utilisateur demande si les composants marchent ensemble, d'intégrer ou promouvoir une initiative, de vérifier la dérive, ou de mettre à jour la baseline.
---

# Intégrer un manifeste

## Lire l'état

```bash
make status                 # ce qui est monté, et à quel SHA
uv run scripts/checks/drift # dérive des contrats (workspace) et des SHA (clones locaux)
```

Une dérive de SHA n'est pas une faute : ce sont des commits pas encore
intégrés. La signaler, avec le nombre de commits, sans rien changer.

Une dérive de contrat est une faute : le code au SHA monté ne fournit plus
ce que `contracts/` déclare. Deux issues, à proposer à l'utilisateur :
- le changement est voulu → il appartient à une initiative ; régénérer
  (`make contracts`) dans le cadre de son candidat ;
- il ne l'est pas → c'est un bug du composant, à corriger dans son dépôt.

## Intégrer

```bash
uv run ci/integrate manifests/candidates/<id>.yaml
```

Étapes : structure → workspace → portes de chaque composant
(`gates` de `system/components.yaml` ; aucune déclarée à l'amorçage) →
dérive des contrats. `open-duelyst` est fixé mais jamais monté (`mount: false`).
`--skip-gates` pour un essai rapide, jamais pour promouvoir.

Si une porte échoue, rapporter la sortie telle quelle et le composant en
cause. Ne pas corriger un composant depuis le workspace : le workspace est
jetable, le correctif va dans le dépôt du composant, puis nouveau SHA dans
le candidat.

## Promouvoir

Seulement après une intégration complète réussie **et** la validation
explicite de l'utilisateur :

```bash
make contracts   # si l'initiative change un contrat généré
uv run ci/integrate manifests/candidates/<id>.yaml --promote
```

Puis passer l'initiative en `livrée`, et proposer un commit unique :
`current.yaml`, contrats régénérés, suppression du candidat, initiative.
