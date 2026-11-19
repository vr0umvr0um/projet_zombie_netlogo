# Corrections des itérations 1 et 2 (branche `correction-iteration1-iteration2`)

**Rôles** : corrections et tests d'harmonisation par **Vanessa** ; vérification et retours par **Soumia** (fichiers `it1_A`, `it2_A`) et **Amandine** (fichiers `it1_B`, `it2_B`). La branche n'est fusionnée dans `main` qu'après leurs retours.

## Ce qui change

| # | Problème | Correction | Fichiers |
|---|---|---|---|
| 1 | Le nombre d'humains affichés ne correspondait pas à l'effectif : humains créés par `hatch` depuis la colonie, donc de taille 2 et bleus comme la maison, et entassés sur ses 4 cases voisines. | Humains de taille 1 (comme les zombies), bleu ciel ; cachés quand ils sont à la colonie, visibles en sortie. La maison porte une étiquette « habitants (infectés) / stock ». | `it1_B` (`initialiser-humain`, `decider-sortie`, `rentrer-a-la-colonie`), `it1_A` (`actualiser-affichage-colonies`), fichier principal |
| 2 | Deux initialisations d'humain différentes (`setup-humains` et `reproduire`) : taille 2 et `date-infection` 0 d'un côté, taille 1 et -1 de l'autre. | Une seule procédure `initialiser-humain [ maison ]`, utilisée par les deux. | `it1_A`, `it1_B` |
| 3 | Un zombie issu d'un humain caché aurait été caché lui aussi (`hatch` copie `hidden?`). | `initialiser-zombie` fixe `hidden? false`, la taille 1 et une étiquette vide. | `it2_A` |
| 4 | La défense détruisait le zombie le plus proche au contact, pas forcément celui qui attaque. | `detecter-et-defendre [ attaquant ]` : le zombie se passe en argument et c'est lui qui est détruit. | `it2_A` (`zombie-attaquer`), `it2_B` |
| 5 | Points de ravitaillement pleins affichés en blanc (`scale-color` donne du blanc à la borne haute). | Borne à 2 × le stock maximal : plein = vert, vide = noir. Couleur des maisons : bleu (stock ≥ `s-min`), bleu foncé (en dessous), noir (vide), gris (sans habitant). | `it1_A` |
| 6 | Tant qu'aucun point n'est rentable, chaque humain présent refait le même parcours en largeur à chaque tick. | Cache, pour le tick en cours, des cases de départ sans trajet. Aucun résultat ne change (les stocks ne font que baisser pendant la phase des humains). | `it1_B` (`decider-sortie`, globals du fichier) |
| 7 | La sortie des tests ne disait pas ce qui était testé. | `annoncer-test-it1` et `annoncer-test-it2` : un message distinct au début de chaque test (bouton ou ligne de commande) liste les critères vérifiés, avec les seuils, et ceux qui restent à vérifier à la main. | `it1_C`, `it2_C` |
| 8 | `nb-morts-attaque` valait toujours 0 : une attaque n'avait aucun effet prédateur. | Prédation activée : si la défense échoue, l'humain est tué avec `proba-mort-attaque` (0,1) et le zombie se nourrit, son âge recule de `gain-attaque-zombie` (48 ticks), comme le loup de *Wolf Sheep Predation* ; sinon, infection avec `proba-infection`. Deux nouveaux curseurs. | `it2_B` (`detecter-et-defendre`), `it2_A` (`zombie-se-nourrir`), fichier principal |
| 9 | Résultats non reproductibles : scénarios de `tester-it2` sans graine, expériences BehaviorSpace avec une graine différente à chaque lancement. | Graine fixe pour chaque scénario (`graine-scenarios`) ; `random-seed behaviorspace-run-number` dans les trois expériences. | `it2_C`, fichier principal |
| 10 | Lisibilité | `ifelse` imbriqués remplacés par `(ifelse …)` dans `humain-agir` et `zombie-agir` ; courbe des infectés ajoutée ; en-tête « SQUELETTE » remplacé ; responsable des fichiers C renseigné ; contrats mis à jour dans `PLAN_ITERATIONS.md` ; lecture de la carte dans le README et l'onglet Info. | divers |

## Tests d'harmonisation (NetLogo 7.0.4, sans interface)

- **`tester-it1`** : les 20 lignes sont **identiques** à la référence (`results/reference_tester_it1.txt` de la branche `iteration3`). Critères 1 à 4 vrais. Les corrections 1, 2, 5 et 6 ne changent donc rien au modèle sans zombie.
- **`tester-it2`** : critères 1 à 4 vrais, y compris les nouveaux scénarios de prédation (tué à chaque contact avec `proba-mort-attaque = 1` ; âge du zombie 100 → 52 avec un gain de 48 ; cas mixte 0,285 / 0,128 / 0,288 pour 0,3 / 0,14 / 0,28 attendus). **Deux lancements donnent une sortie identique.** Sur les 20 simulations : 22 humains restants en moyenne, aucune extinction humaine, zombies présents à la fin dans 7 sur 20, 36 morts par attaque en moyenne.
- **Courbes refaites** : `results/it2_courbes.csv` (graine = numéro de simulation) et `figures/it2_courbes.png`. Au jour 30 : 22 humains et 0,4 zombie en moyenne ; humains présents dans 20 simulations sur 20, zombies dans 7 sur 20. Toujours une décroissance sans oscillation.
- **Affichage** (3 simulations de 720 ticks, réglages par défaut) : à chaque tick, un humain est caché si et seulement s'il est à la colonie ; aucun zombie caché ; tous les humains et zombies de taille 1 ; aucune étiquette sur les humains et les zombies.

## À vérifier par Soumia et Amandine

- [ ] **Soumia** : `actualiser-affichage-colonies` et la couleur des points (`regenerer-points`) dans `it1_A` ; `initialiser-zombie`, `zombie-attaquer` et `zombie-se-nourrir` dans `it2_A`.
- [ ] **Amandine** : `initialiser-humain`, le cache de `decider-sortie` et le passage visible / caché dans `it1_B` ; la nouvelle signature et la prédation de `detecter-et-defendre` dans `it2_B`.
- [ ] **Les deux** : ouvrir le modèle, `setup` puis `go` avec 20 et 100 humains ; le total des étiquettes plus les humains visibles doit correspondre au moniteur « Humains vivants ».
- [ ] **Les deux** : relancer « Test it1 » et « Test it2 » et comparer aux résultats ci-dessus.

## Reste à faire ou à décider

- **Décision d'équipe : recalibrer `proba-defense`.** Avec la prédation, le critère retenu pour `proba-defense` (zombies encore présents dans au moins la moitié des simulations, humains éteints dans au plus 10 %) n'est plus rempli à 0,125 : zombies présents dans 7 simulations sur 20. Balayage (20 graines par case, 0 obstacle) : seule la case `proba-defense` 0,12 / `proba-mort-attaque` 0,1 remplit les deux conditions (10 sur 20 et 1 sur 20), et de justesse ; entre 0,1 et 0,125, le résultat bascule d'une case à l'autre. `gain-attaque-zombie` (48 ou 240) ne change presque rien, car les zombies meurent par la défense bien avant 480 ticks.
- **Décision d'équipe** : les curseurs par défaut combinent 20 zombies et 30 obstacles, une configuration de l'itération 3 pas encore validée.
- **Fusion avec `iteration3`** : les modifications des en-têtes « Responsable » sont les mêmes des deux côtés. Il faudra simplement reporter dans les squelettes de l'itération 3 la nouvelle signature de `detecter-et-defendre`, si on y fait appel.
