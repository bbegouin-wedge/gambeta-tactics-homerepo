---
id: I29
title: Portes de qualité
origine:
  type: idee
  par: humain
  le: 2026-11-21
  source: "conversation du 2026-11-21, pendant I27 : que vérifient vraiment les make check ?"
---

# I29 — Portes de qualité

## Idée de l'humain

Les portes lancées à chaque run doivent vérifier : la couverture de test (100 % attendu),
les tests eux-mêmes, la qualité des tests, les règles d'architecture, les tests
d'intégration globaux. « L'essentiel est déjà là, on améliorera ça. »

## État constaté (2026-11-21)

| Attendu | `make check` serveur | `make check` client | Ailleurs |
|---|---|---|---|
| Couverture 100 % | non mesurée | non mesurée | — |
| Tests | `cargo test` | GUT | — |
| Qualité des tests | non | non | serveur : `make test-quality` (hors `check`, outil de l'usine absent du poste), `make mutation` (cargo-mutants, jamais lancé) ; client : rien |
| Architecture | `check-arch.sh`, `check-contexts.sh` | `tools/arch.sh` (motifs) | — |
| Intégration globale | non | non | home repo : `ci/integrate` (scénarios), au candidat seulement |

## Manques relevés en plus

- **Mutation** : seule mesure réelle de la qualité des tests (100 % de couverture
  s'obtient avec des assertions vides). Cible serveur existante, jamais lancée.
- **Conformité au contrat** : `canal-joueur.md` est écrit à la main ; rien ne vérifie le
  code contre lui hors du scénario de bout en bout, ni le faux serveur du client contre le
  vrai (I28 en est un exemple).
- **Duplication** : `make dup` (jscpd) existe dans les deux composants, hors de `check`,
  non bloquant.
- **Dépendances** : ni `cargo audit` ni `cargo deny` (failles, licences).
- **Exécution** : aucune CI ni hook ne lance les portes ; elles tournent quand on les lance.

## Points pour le grilling

- Couverture : faisable côté serveur (`cargo llvm-cov --fail-under-lines`, hors
  `gambeta_automaton` porté et `main.rs`) ; côté client, GUT ne mesure pas la couverture et
  aucun outil GDScript n'est mûr — viser `scripts/core` et `scripts/adapters`.
- Mutation : dans `check`, ou de nuit.
- Tests de contrat : lire les exemples JSON du contrat des deux côtés.
- Où tournent les portes : CI GitHub, hook git.
