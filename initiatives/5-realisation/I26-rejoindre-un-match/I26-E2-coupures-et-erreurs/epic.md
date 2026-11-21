---
id: I26-E2
parent: I26
needs: [I26-B7, I26-B8, I26-B9, I26-B10, I26-B12, I26-B13, I26-B19, I26-B20]
screens: [I26-M1]
depends_on: [I26-E1]
---
# I26-E2 — Coupures et erreurs

À la fin de cet epic, un joueur peut renoncer à attendre (« Annuler »), une place
d'attente n'est jamais tenue par un absent, et un joueur dont l'adversaire part est
prévenu puis ramené à l'accueil, d'où il peut rejoindre un autre match. Une demande en
double est refusée sans rien casser. Il n'y a pas de reconnexion : un joueur parti ne
revient pas dans son match.

## Effet sur l'existant

S'appuie sur I26-E1 : même canal, même overlay, même contrat. Le contrat
`contracts/canal-joueur.md` décrit déjà `adversaire_deconnecte` et `erreur` depuis
I26-E1 ; cet epic les fait exister. Aucun changement de contrat.

N'en fait pas partie : la reconnexion, quitter volontairement un match en cours.

## Scénarios de bout en bout

- **I26-E2-S1** — Étant donné le joueur A dans l'overlay « En attente d'un
  adversaire… », quand il clique sur « Annuler », alors l'overlay disparaît et il est sur
  la page d'accueil ; quand le joueur B clique ensuite sur « Rejoindre un match », alors B
  attend à son tour et ne se retrouve pas dans un match avec A. (I26-B7, B8)
- **I26-E2-S2** — Étant donné le joueur A en attente, quand on ferme son client (ou qu'il
  perd le réseau), puis que le joueur B clique sur « Rejoindre un match », alors B attend :
  il n'est pas apparié avec A. (I26-B8)
- **I26-E2-S3** — Étant donné A et B dans le même match, quand on ferme le client de B,
  alors A voit l'overlay « Adversaire déconnecté » avec un compte à rebours de 5 s, puis
  arrive sur la page d'accueil ; quand A clique de nouveau sur « Rejoindre un match »,
  alors il attend un nouvel adversaire. (I26-B9, B10)
- **I26-E2-S4** — Étant donné A dans l'overlay « Adversaire déconnecté », quand il clique
  sur « Retour à l'accueil » avant la fin du compte à rebours, alors il arrive tout de
  suite sur la page d'accueil. (I26-B10)
- **I26-E2-S5** — Étant donné une connexion qui a envoyé `rejoindre_match` et attend,
  quand elle envoie un second `rejoindre_match`, alors elle reçoit
  `erreur { code: "demande_en_double" }` et reste en attente : le joueur suivant est
  apparié avec elle normalement. (I26-B12)
- **I26-E2-S6** — Étant donné A et B dans le même match, quand B ferme son client puis le
  relance et clique sur « Rejoindre un match », alors B attend un nouvel adversaire : il ne
  revient pas dans le match qu'il a quitté. (I26-B13)
