# 0002 — Une initiative se pense au niveau du projet, se projette sur les composants, se réalise dans chacun

- Statut : acceptée
- Date : 2026-11-19

## Contexte

Gambeta Tactics est une application faite de composants (backend, client), et
chaque composant est un dépôt, avec ses responsabilités (`system/components.yaml`).
Une initiative ne peut donc pas être cassée directement en tickets : il faut
d'abord dire comment elle se répartit entre les composants.

Le système bbTrainer a appris à ses dépens qu'une évolution décidée dans un seul
dépôt se perd entre eux (un changement du canal du coach décidé côté serveur,
que ni le contrat, ni la doublure, ni le client n'avaient suivi). Il a adopté ce
processus (son ADR 0003) ; Gambeta Tactics le reprend dès l'amorçage.

Le détail du processus est dans wedge-factory, `spec/multi-depots/lot3-processus.md`.

## Décision

**Toute initiative naît ici**, au niveau du projet, même si elle ne touche qu'un
composant. Elle porte son origine (idée, report, remontée d'un ticket, reprise).

**Quatre niveaux :** initiative projet `I1` → epic projet `I1-E1` → epic composant
`I1-E1-BE` → ticket composant `I1-E1-BE-T3`, où `BE` et `CL` sont les codes
courts du backend et du client. Les besoins gardent
leur identifiant de projet (`I1-B2`) jusque dans les tickets.

**Le déroulé :**

1. **Grilling** : les besoins métier, le périmètre. Validé par l'humain.
2. **Maquettes**, s'il y a de l'écran. Validées par l'humain.
3. **Epics projet** : les grandes étapes métier ; chacune est un incrément
   autocontenu et livrable, avec ses scénarios de bout en bout vus du joueur.
   Le découpage est validé en bloc par l'humain.
4. **Projection**, epic projet par epic projet : la jointure entre le projet et
   les composants. Un architecte projet propose les epics composant et les
   changements de contrat entre composants ; chaque composant touché relit sa
   part dans son dépôt (à faire, déjà fait, hors responsabilités) ;
   l'architecte consolide. Des contrôles vérifient la couverture des besoins
   et des scénarios, chaque contrat changé couvert chez son fournisseur et ses
   consommateurs, et le rattachement de chaque epic
   composant à une responsabilité écrite de son composant. Puis l'humain valide.
5. **Réalisation dans les dépôts**, comme avant et en parallèle : chaque epic
   composant est cassé en tickets composant, validés automatiquement, puis
   réalisés.
6. **Intégration et promotion par epic projet** : ses scénarios de bout en bout
   sont joués sur les composants assemblés ; la promotion est validée par
   l'humain. L'initiative est livrée quand tous ses epics projet sont promus.

**Les contrats** sont fixés pendant la projection, avant tout code. **Une part
« déjà faite »** est gardée, réduite à une preuve : un test d'acceptation. **Aucun
ordre imposé** entre epics projet : seules les dépendances déclarées bloquent.

**Les responsabilités des composants sont figées.** Leur valeur initiale est
proposée à l'onboarding ; elles ne changent que par un processus d'architecture,
hors du flux d'un développement, par un ADR. Une projection qui sort de ce cadre
arrête son epic projet (escalade « architecture ») : on le reformule, ou on ouvre
le processus d'architecture ; les autres epics continuent.

## Conséquences

- Les dépôts n'ont pas de backlog, de grilling, de maquettes ni d'epics propres :
  ils reçoivent des epics composant et en écrivent les tickets. Le backlog initial
  est tiré de `product/Boucle de gameplay — étapes techniques.md`.
- Le kanban d'`initiatives/` suit ces étapes : `1-backlog`, `2-grilling`,
  `3-maquettes`, `4-epics`, `5-realisation`, `7-livree`, `8-abandonnee`.
- Un manifeste candidat et une promotion par epic projet, et non plus par
  initiative.
- Les livrables restent validés par l'humain ; les composants gardent leur
  `CLAUDE.md`, leurs portes et leur production.
- Restent ouverts : la promotion d'un epic projet quand un autre, inachevé, a déjà
  livré du code dans le même dépôt ; l'outil qui joue les scénarios de bout en
  bout ; le déroulé du processus d'architecture.
