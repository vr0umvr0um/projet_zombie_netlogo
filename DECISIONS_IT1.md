# Décisions proposées pour l'itération 1 (environnement / humain)

Document de travail pour la séance d'assemblage. Il propose des décisions et dit, pour chacune, sur quoi elle repose et avec quel niveau de certitude.

## Constat de départ

Avec les parties A, B et C fusionnées et les curseurs par défaut, `tester-it1` échoue sur les 20 graines : proportion de survivants à 0 et famine à 100 % (critères 3 et 4 de `PLAN_ITERATIONS.md`). Les invariants restent vrais et le modèle ne plante pas : le problème vient des réglages et de la logique des sorties, pas de l'assemblage.

Dynamique observée avec les valeurs par défaut : 100 humains consomment 100 unités par jour pour 400 de stock initial dans les colonies. Avec `capacite-transport = 10`, un trajet aller coûte plus que la capacité, donc presque aucune sortie n'a lieu. Les colonies sont vides au jour 5.

## Comment les chiffres ont été obtenus

- Copie jetable du projet avec quelques curseurs supplémentaires pour tester des variantes (aucune modification du dépôt).
- `nb-zombies = 0`, 720 ticks, graines non fixées, de 5 à 20 simulations par configuration.
- Chaque ligne citée ci-dessous repose sur des tableaux **complets** (3 à 6 simulations par configuration, 20 pour la configuration finale). Deux balayages intermédiaires ont été interrompus avant la fin et ne sont pas utilisés.
- Les variances sont fortes : à 3 ou 5 répétitions, un écart de moins de 0,15 sur la survie ne prouve rien.

## Décisions

### D1. Changer le régime de fonctionnement par défaut

| Curseur | Actuel | Proposé |
|---|---|---|
| `nb-points-ravitaillement` | 8 | **16** |
| `capacite-transport` | 10 | **50** |
| `consommation-jour` | 1 | **0,25** |
| `regeneration-point` | 0,05 | **0,5** |
| `s-min` | 40 | **80** |

Justification :
- **Capacité.** Un trajet ne rapporte que `capacité − 2 × distance`. Sur une carte de 33 × 33, la distance vers un point atteint souvent 10 à 20 patchs. Avec 10, l'agent ne part même pas ; avec 30, la survie est de 0,78 contre 0,99 avec 50 (16 points, consommation 0,25).
- **Nombre de points.** À capacité 50 et consommation 0,25, la survie passe de 0,74 (8 points) à 0,99 (16) et 1,0 (24). Plus de points rapproche les colonies de leur ravitaillement.
- **Consommation.** À 1 unité par humain et par jour, aucun réglage testé ne tient. À 0,5, la survie varie de 0,54 à 0,86 selon le nombre de points (16 à 24, capacité 50) ; à 0,25 elle atteint 0,99 avec 16 points.
- **Régénération.** La valeur de 0,05 fournit environ 10 unités par jour pour toute la carte, contre 100 de consommation.
- **`s-min` à 80.** Avec 25 humains à 0,25 par jour, la colonie consomme 6 à 7 unités par jour : 80 représente donc environ 12 jours de réserve, assez pour qu'une sortie lente arrive à temps.

Certitude : bonne pour la capacité, le nombre de points et la consommation (écarts nets sur des tableaux complets). Plus faible pour `regeneration-point` et `s-min`, que j'ai surtout fixés par cohérence d'ordre de grandeur plutôt que par un balayage dédié.

### D2. Ajouter un contrôle de rentabilité avant de partir (partie B)

Dans `chemin-vers-ravitaillement`, n'accepter un point que si `stock-point > 2 × (nombre de pas)`, au lieu de `> 0`.

Justification : l'humain prend `distance + 1` unités à la colonie, collecte au plus ce que contient le point, puis rentre en payant `distance`. Si le point contient peu, la sortie coûte plus qu'elle ne rapporte, même quand l'humain survit.

| Contrôle avant départ | 8 points | 16 points |
|---|---|---|
| point avec `stock > distance` (retour possible) | 0,17 | 0,54 |
| point avec `stock > 2 × distance` (sortie rentable) | **0,41** | **0,81** |

(16 points, consommation 0,5, plafond de 1 sortie, 6 simulations par case.)

Constat annexe : peu d'humains meurent en route (2 sur 26 dans la simulation instrumentée). Le gain vient d'abord de l'abandon des sorties déficitaires, pas de la survie sur le trajet.

Certitude : moyenne à bonne.

### D3. Garder le plafond provisoire à 1 sortie par colonie

Le plafond de la partie B (1 par colonie) est le meilleur testé, contrairement à l'intuition. Avec 16 points, capacité 50, consommation 0,25 et contrôle D2 :

| Plafond | 1 | 2 | 4 |
|---|---|---|---|
| Survie moyenne | **0,99** | 0,70 | 0,30 |

Même sens dans tous les balayages : dans l'un d'eux, le plafond de 1 fait mieux que celui de 2 dans 11 paires de configurations sur 12 (l'exception, 8 points, capacité 50, consommation 0,5, est dans le bruit : 0,21 contre 0,24).

**Ce que je n'ai pas réussi à expliquer.** J'ai testé deux hypothèses, sans les confirmer :
- une course aux points (plusieurs humains visent le même stock) : réserver le stock au départ améliore le plafond 2 (0,70 → 0,81) et le plafond 4 (0,30 → 0,66), sans atteindre le plafond 1 ;
- l'avance de nourriture prélevée sur la colonie : une marge de sécurité avant départ n'apporte rien de net (plafond 4 : 0,38 → 0,50 puis 0,55 ; plafond 1 : 0,76 → 0,79 puis 0,62, donc sans effet lisible).

Décision : ne pas relever le plafond pour l'itération 1. Reprendre la question à l'itération 4, où les groupes imposent des départs simultanés.

### D4. Ne pas implémenter la réservation de stock maintenant

Au plafond de 1, la réservation ne change rien (0,99 → 1,0 à consommation 0,25 ; 0,83 → 0,78 à 0,5, dans le bruit). Elle ajoute une variable (`reservation`) et du code de coordination pour aucun gain mesuré. À reconsidérer à l'itération 4.

### D5. Laisser la règle de famine de la partie A inchangée

Aujourd'hui chaque humain non nourri meurt le jour même, donc quand le stock d'une colonie tombe à zéro, tous ses habitants meurent d'un coup (19 morts le même jour dans une simulation avec les anciens réglages). C'est cohérent avec un stock partagé et sans état de « faim » à gérer. Avec D1 et D2, la famine moyenne est de 2 %. Ajouter un délai de grâce demanderait une variable de plus dans `humains-own` ; à n'envisager que si le critère 4 résiste après D1 et D2.

Certitude : décision de modélisation, non testée ; à valider avec Soumia (partie A).

### D6. Ne pas figer les naissances avant d'avoir appliqué D1 et D2

Dans le régime proposé, la moyenne des naissances sur 20 simulations est de 0 : le stock par colonie reste autour de 100, sous `seuil-naissance = 120`. De plus, à 0,01 par jour et par colonie, il y aurait au plus environ 1 naissance en 30 jours. Le critère 3 (population entre 0,9 et 1,1) est donc atteint sans reproduction.

Décision : lancer `it1-reglage-taux-naissance` une fois D1 et D2 appliqués, avec `seuil-naissance` entre 60 et 120, et choisir la valeur qui garde la population dans l'intervalle. Je ne propose pas de valeur sans cette expérience.

### D7. Reformuler le critère 3 en tenant compte du hasard

Configuration D1 + D2, 20 simulations : survie moyenne 0,98 (min 0,77, max 1,0), famine moyenne 2,1 %, invariants vrais à la fin, **1 simulation sur 20 hors de [0,9 ; 1,1]** (survie 0,77, famine 23 %).

Le critère actuel (« toutes les graines dans l'intervalle ») échoue donc d'un seul cas. Deux options :
1. exiger au moins 18 simulations sur 20 dans l'intervalle **et** une moyenne dans l'intervalle ;
2. garder le critère strict et chercher la cause de la simulation aberrante.

Je recommande la première, avec une mention dans le rapport, et un examen de la graine aberrante si le temps le permet.

### D8. Surveiller le temps de calcul

Une simulation complète prend plus de 20 secondes avec le vrai code (un balayage de 24 simulations n'a pas fini en 9 minutes en séquentiel), contre quelques secondes avec une version simplifiée. Cause probable, non mesurée : chaque humain d'une colonie recalcule un plus court chemin sur toute la carte à chaque tick quand le stock est sous `s-min`, même si aucune sortie n'est possible. Piste : ne décider qu'une fois par colonie et par tick. Priorité basse tant que les expériences de l'itération 5 ne sont pas lancées, mais 240 simulations de plus seront lentes.

## Récapitulatif

| # | Décision | Qui | Certitude |
|---|---|---|---|
| D1 | Nouveaux curseurs par défaut | tous | bonne (capacité, points, consommation) |
| D2 | Contrôle de rentabilité avant sortie | B | moyenne à bonne |
| D3 | Plafond de sorties à 1 | B et C | bonne pour le constat, cause inconnue |
| D4 | Pas de réservation de stock | B | moyenne |
| D5 | Famine inchangée | A | décision de modélisation |
| D6 | Naissances : expérience avant décision | A et C | à faire |
| D7 | Critère 3 reformulé | C | choix de méthode |
| D8 | Temps de calcul : à surveiller | B | hypothèse |

## À faire pendant la séance d'assemblage

1. Appliquer D1 et D2, puis relancer `tester-it1` (la durée est de quelques minutes avec le vrai code).
2. Lancer `it1-reglage-taux-naissance` (D6).
3. Valider la reformulation du critère 3 (D7) et le principe de la famine de la partie A (D5).
4. Vérifier à la main les critères 5 et 6 (sortie complète sans traverser d'obstacle, deux consommations documentées).
5. Relancer ensuite `tester-it2` : ses simulations complètes n'ont de sens que si les humains survivent à l'itération 1.
