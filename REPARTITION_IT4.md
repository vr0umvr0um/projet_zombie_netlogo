# Répartition de l'itération 4 (stratégies de groupe)

**Branche** : `iteration4`, créée à partir de `iteration3`. Elle contient la partie C de l'itération 3 et celle de l'itération 4 ; les parties A et B des deux itérations sont à écrire. Quand la branche `iteration3` avancera, la reporter ici (`git merge iteration3`).

**État** : partie C (Vanessa) **faite** ; parties A (Soumia) et B (Amandine) : squelettes commentés à remplir.

Question du projet (TP5) : quelle stratégie de ravitaillement (individuelle, groupe fixe, groupe adaptatif) influence la proportion de survivants après 30 jours ?
- **Groupe fixe** : « un groupe de taille fixe est sélectionné aléatoirement parmi les humains disponibles pour partir ravitailler la colonie. Le groupe part ensemble, collecte ensemble et retourne ensemble. Le groupe se défendra ensemble si un zombie est détecté. »
- **Groupe adaptatif** : « un groupe ajuste sa taille en fonction du nombre de zombies repérés autour de la colonie. »

## Qui fait quoi

| Personne | Partie | Fichier | Contenu |
|---|---|---|---|
| Soumia | **A** | `it4_A_groupe_fixe.nls` | groupe fixe : formation aléatoire, trajet, collecte et retour communs, dissolution au retour |
| Amandine | **B** | `it4_B_groupe_adaptatif.nls` | groupe adaptatif : zombies repérés autour de la colonie, règle de taille ; branchements dans ses fichiers `it1_B` et `it2_B` (voir plus bas) |
| Vanessa | **C** | `it4_C_comparaison_tests.nls` | défense collective, plafond de sorties, indicateurs de comparaison, invariants des groupes, `tester-it4`, expérience et script de comparaison : **fait** |

## Partie C (faite)

- **Défense collective** : `proba-defense-effective`. Chaque membre du groupe au contact de l'humain attaqué (lui compris) tente sa défense ; elle échoue seulement si tous échouent : `1 - (1 - proba-defense)^k`. Seul, c'est exactement `proba-defense`. Vérifié sur une copie où `detecter-et-defendre` l'appelle : 0,646 de défenses pour un groupe de 3 avec `proba-defense = 0,3` (0,657 attendu), et résultats de la stratégie individuelle inchangés.
- **Plafond de sorties** : `sortie-autorisee? [ colonie ]`, au plus `plafond-sorties-colonie` (1) sortie simultanée par colonie ; un groupe compte pour une seule sortie (`nb-sorties-en-cours`).
- **Indicateurs de comparaison**, mesurés à chaque tick sans tirage aléatoire (`mesurer-humains-it4`) : `nb-departs`, `nb-departs-groupes`, `nb-retours`, `nb-retours-infectes` (infections introduites dans la colonie), `part-retours-infectes`, `nourriture-par-sortie`, `taille-max-groupe-observee`. Moniteurs « Sorties de groupe » et « Retours infectés ».
- **Invariants des groupes** (branchés dans `liste-invariants-violes`) : aucun groupe en stratégie individuelle ; aucun groupe à la colonie (dissous au retour) ; membres d'un même groupe avec la même colonie, la même mission et le même point ; membres d'un groupe sur la même case.
- **`tester-it4`** et **`tester-it4-pas`** (bouton « Test it4 ») : les trois stratégies sur 20 graines (taille 5), puis individuelle et groupe fixe avec `taille-groupe = 1`, le scénario de défense collective, la non-régression de `tester-it1`. Il dit explicitement ce qui manque (« groupes NON IMPLÉMENTÉS », « défense collective NON BRANCHÉE »).
- **Expérience `it4-comparaison`** (3 stratégies × 100 graines, mêmes graines pour les trois) et **`analyse/comparaison_strategies_it4.py`** : moyennes, intervalle de confiance, **écart apparié** à la stratégie individuelle (graine par graine), figure `figures/it4_comparaison.png`.
- Les tests des itérations 1 à 3 remettent le sélecteur `strategie` sur « individuelle » (leurs références portent sur elle).

**Résultat de départ (stratégie individuelle, 100 graines)** : 88,9 % de survivants (intervalle de confiance ± 1,7 point), 3,6 morts par attaque, **un retour sur trois (33 %) ramène un infecté dans la colonie**, 32,7 unités nettes rapportées par humain parti. C'est la référence à laquelle comparer les groupes.

## À faire : partie A (Soumia), `it4_A_groupe_fixe.nls`

Les contrats sont écrits en tête du fichier et vérifiés par les invariants de `tester-it4`.
1. `decider-sortie-groupe` : vérifier `sortie-autorisee?` et le stock ; trajet commun (`chemin-vers-ravitaillement`) ; rentabilité pour tout le groupe ; tirer les membres au hasard parmi les humains disponibles ; ration, réservation, même `groupe-id`, même trajet.
2. `deplacer-groupe` : le groupe avance sur la même case ; chacun consomme 1 unité par pas.
3. `collecter-en-groupe`, `dissoudre-groupe` (groupe-id -1 au retour, bilan des sorties).
4. Avec `taille-groupe = 1`, résultats identiques à la stratégie individuelle (critère 1) : ne pas tirer de hasard en plus dans ce cas.

## À faire : partie B (Amandine), `it4_B_groupe_adaptatif.nls` et branchements

1. `zombies-reperes`, `rayon-reperage`, `taille-groupe-adaptative` : règle à choisir, mesurer (100 graines par variante) et justifier.
2. Dans `detecter-et-defendre` (`it2_B`) : remplacer `proba-defense` par `proba-defense-effective`. **Une ligne** ; aucun résultat ne change en stratégie individuelle (vérifié).
3. Dans `decider-sortie` (`it1_B`) : remplacer le plafond écrit en dur par `sortie-autorisee? origine`, et appeler `decider-sortie-groupe` (A) quand `strategie` n'est pas « individuelle ». À faire ensemble avec Soumia.

## Dépendances

| Ce qu'une partie fournit | À qui | Quand |
|---|---|---|
| `proba-defense-effective`, `sortie-autorisee?`, invariants, `tester-it4` (C) | A et B | disponible |
| Branchements dans `it1_B` et `it2_B` (B) | A (son groupe ne part pas sans eux) | en premier |
| `decider-sortie-groupe`, `deplacer-groupe` (A) | B (même mécanique, autre taille) | milieu d'itération |

## Critères de sortie (`PLAN_ITERATIONS.md`)

1. Avec `taille-groupe = 1`, le groupe fixe donne les mêmes résultats que la stratégie individuelle (20 graines).
2. Le groupe se déplace et se défend ensemble.
3. Invariants vrais pour les trois stratégies.

État actuel de `tester-it4` : critères 1, 3 et non-régression vrais ; critère 2 en attente des parties A et B.

## Pièges

- Toute mesure appelée à chaque tick dans `go` ne doit consommer aucun tirage aléatoire (`foreach sort`, `ask` sur un seul agent).
- `n-of` et `one-of` consomment du hasard : pour le critère 1, ne pas les appeler quand la taille vaut 1.
- Un membre qui disparaît passe par `mourir` ou `transformer` (stock réservé rendu, compteurs tenus).
- Les curseurs `strategie` et `taille-groupe` sont lus pendant `go` : un test qui les change doit les remettre ensuite (`tester-it4` le fait).
- Le nom `plafond-sorties` est déjà une variable locale de `decider-sortie` : le reporter de C s'appelle `plafond-sorties-colonie`.
