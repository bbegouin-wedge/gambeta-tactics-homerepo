---
id: I27-E1
parent: I27
needs: [I27-B1, I27-B2, I27-B3, I27-B4, I27-B5, I27-B6, I27-B7, I27-B16]
screens: []
depends_on: []
---
# I27-E1 — Console de débogage du client

À la fin de cet epic, un client lancé avec `--traces` trace son propre parcours et
l'affiche dans une console de débogage, ouverte en tapant trois fois `l`, par-dessus tous
les écrans. Sans l'option, le joueur ne voit rien, mais chaque trace est recopiée dans la
sortie de Godot. La trace `match_rejoint` porte le numéro du joueur ; l'identifiant de
match la rejoint avec I27-E2.

## Effet sur l'existant

Client seul. Une fonction de trace commune remplace le `push_warning` de la trame
illisible (`scripts/adapters/websocket_server.gd`). Le parcours (`scenes/parcours/`) et
l'overlay ne changent pas : la console se pose au-dessus. `make run-client` (racine de
`03-gamebeta_tactics`) gagne `TRACES=1`. Aucun changement de contrat, rien côté serveur.

N'en fait pas partie : les traces du serveur et l'identifiant de match (I27-E2) ; filtre,
recherche ou copie dans la console.

## Scénarios de bout en bout

- **I27-E1-S1** — Étant donné un client lancé avec `--traces` et un serveur démarré, quand
  le joueur rejoint un match puis tape `lll`, alors la console montre, dans l'ordre,
  `connexion_ouverte`, `rejoindre_demande` et `match_rejoint` (joueur N), chacune avec
  son heure et l'origine `client`. (I27-B1, B3, B4, B5, B6)
- **I27-E1-S2** — Étant donné la console ouverte, quand le joueur tape `lll` ou `Échap`,
  alors elle se ferme ; quand il tape « lll » dans la saisie du chat de l'arène, alors
  elle ne s'ouvre pas. (I27-B5)
- **I27-E1-S3** — Étant donné un client lancé avec `--traces` et le serveur arrêté, quand
  le joueur clique sur « Rejoindre un match », alors la console, ouverte par-dessus
  l'overlay « Serveur injoignable », montre `serveur_injoignable` en rouge.
  (I27-B3, B6)
- **I27-E1-S4** — Étant donné un client lancé sans `--traces`, quand le joueur rejoint un
  match et tape `lll`, alors rien ne s'ouvre ; la sortie de Godot contient pourtant la
  ligne `[trace] client info match_rejoint joueur=N — …`. (I27-B2, B4, B5)
- **I27-E1-S5** — `make run-client TRACES=1` lance le client avec la console disponible.
  (I27-B7)
- **I27-E1-S6** — Les tests GUT du client vérifient le journal (ordre, origine, limite de
  500), le raccourci `lll`, ignoré pendant une saisie, et l'absence de console et de
  journal sans `--traces`. (I27-B16)
