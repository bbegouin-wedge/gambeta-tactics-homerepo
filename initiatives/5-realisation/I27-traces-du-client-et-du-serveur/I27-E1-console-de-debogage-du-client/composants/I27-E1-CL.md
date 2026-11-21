---
id: I27-E1-CL
parent: I27-E1
depot: client
needs: [I27-B1, I27-B2, I27-B3, I27-B4, I27-B5, I27-B6, I27-B16]
scenarios: [I27-E1-S1, I27-E1-S2, I27-E1-S3, I27-E1-S4, I27-E1-S6]
contracts: []
depends_on: []
verdict: a_faire
kind: realisation
---
# I27-E1-CL — Console de débogage du client

À la fin de cet epic, le client trace son parcours par une fonction commune, recopie
chaque trace dans la sortie de Godot et, lancé avec `--traces`, tient un journal qu'une
console de débogage affiche par-dessus tous les écrans.

## Ce que le client livre

1. **Trace** : une valeur avec heure, origine (`client` ou `serveur`), niveau (`info`,
   `warn`, `erreur`), `quoi`, `message`, `champs` facultatifs. Une fonction commune pour
   tracer, utilisable du cœur et des adaptateurs, sans dépendre des vues (I27-B1).
2. **Recopie** : toute trace, avec ou sans `--traces`, est écrite dans la sortie de Godot
   sur une ligne `[trace] <origine> <niveau> <quoi> <clé=valeur…> — <message>`. Le format
   est stable : le scénario de bout en bout d'I27-E2 la lira (I27-B2).
3. **Étapes tracées** : `connexion_ouverte` (`adresse`), `serveur_injoignable`
   (`erreur`), `rejoindre_demande`, `match_rejoint` (`joueur`), `adversaire_deconnecte`
   (`info`), `connexion_fermee`, `trame_illisible` (`warn`, remplace le `push_warning` de
   `WebSocketServer`). `match_rejoint` gagnera le champ `match` avec I27-E2 (I27-B3).
4. **Option `--traces`** (lue par `Arguments`) : le client tient dès son démarrage un
   journal des traces, dans l'ordre d'arrivée, limité aux 500 dernières. Sans l'option,
   aucun journal (I27-B4).
5. **Console** : avec `--traces`, trois `l` de suite l'ouvrent et la ferment, `Échap` la
   ferme ; raccourci ignoré quand une saisie de texte a le focus, sans effet sans
   `--traces`. Panneau semi-transparent en haut de l'écran, au-dessus de tout (overlays
   compris), sur tous les écrans ; une ligne par trace (heure, origine, niveau, message),
   `warn` en orange, `erreur` en rouge ; défile sur la dernière ligne (I27-B5, B6).

Les frontières de l'hexagone (`docs/architecture.md`) tiennent : le journal ne dépend pas
des vues ; la console lit le journal.

## Preuve attendue

Tests GUT (`given_` / `when_` / `then_`, sans réseau, sans sleep) (I27-B16) :
- le journal garde l'ordre d'arrivée et l'origine, et ne garde que les 500 dernières ;
- sans `--traces`, pas de journal et pas de console ; la recopie a lieu quand même ;
- trois `l` ouvrent puis ferment la console, `Échap` la ferme ; trois `l` tapés dans une
  saisie de texte ne l'ouvrent pas ;
- avec le faux serveur (`adversaire`), les traces `connexion_ouverte`,
  `rejoindre_demande`, `match_rejoint` (`joueur`) arrivent dans cet ordre ; avec
  `injoignable`, `serveur_injoignable` au niveau `erreur`.

`make check` passe.
