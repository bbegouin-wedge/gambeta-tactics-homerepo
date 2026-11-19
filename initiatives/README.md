# Initiatives du projet Gambeta Tactics

Toute évolution du produit naît ici, même si elle ne touche qu'un composant
(modèle multi-dépôts de la software factory, `spec/multi-depots/` de wedge-factory).
Quatre niveaux : **initiative projet** `I1` → **epic projet** `I1-E1` → **epic composant**
`I1-E1-BE` (sa part dans un composant ; `BE`, `CL` : codes courts des composants) →
**ticket composant** `I1-E1-BE-T3`.

Le déroulé et ses raisons : [`decisions/0002-processus-multi-depots.md`](../decisions/0002-processus-multi-depots.md).
Le dossier où se trouve une initiative est sa colonne :

| Colonne | Ce qui avance | Ce qui s'y produit | Pour passer |
|---|---|---|---|
| `1-backlog/` | l'initiative | une idée, avec son origine ; préfixe de priorité (`01-I2-…`) | priorité |
| `2-grilling/` | l'initiative | besoins numérotés `I<n>-B<k>` (`grilling.md`) : le périmètre | validation humaine |
| `3-maquettes/` | l'initiative | écrans `I<n>-M<k>` | validation humaine |
| `4-epics/` | l'initiative | epics projet (`I<n>-E<k>-…/epic.md`), étapes métier livrables, avec leurs scénarios de bout en bout | validation humaine |
| `5-realisation/` | chaque epic projet | projection (`projection.md` : epics composant, contrats, relectures des composants), puis réalisation dans les dépôts, intégration, promotion | validation humaine de la projection et de la promotion |
| `7-livree/` | l'initiative | tous ses epics projet promus | — |
| `8-abandonnee/` | l'initiative | archive | — |

`initiative.md` porte son origine, écrite une fois :

```yaml
origine:
  type: idee | report | remontee | reprise
  par: humain | chef d'usine
  le: 2026-11-19
  source: "product/Boucle de gameplay — étapes techniques.md"   # report : I0-B5 ; remontee : I0-E1-BE-T4 ; reprise : <dépôt>:<id>
```

Modèle : [`_modele/initiative.md`](_modele/initiative.md).
