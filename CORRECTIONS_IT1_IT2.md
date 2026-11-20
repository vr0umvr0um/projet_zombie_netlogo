# Corrections des itérations 1 et 2 (branche `correction-iteration1-iteration2`)

**Rôles** : corrections et tests d'harmonisation par **Vanessa**. La relecture prévue pour **Soumia** (fichiers `it1_A`, `it2_A`) et **Amandine** (fichiers `it1_B`, `it2_B`) a été faite à leur place, à la demande de Vanessa (voir « Relecture » plus bas) ; elles peuvent toujours relire et réagir avant la fusion dans `main`.

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
| 11 | Une sortie pouvait rapporter moins qu'elle ne consomme : la règle « stock > 2 × longueur du trajet » ignorait la capacité de transport (au-delà de 24 pas, perte assurée même sur un point plein), et un point pouvait être vidé par un humain d'une autre colonie avant l'arrivée. | Bilan d'une sortie de *n* pas : gain net = *q* − 2*n*. Sortie lancée seulement si la quantité collectable (stock non réservé, au plus `capacite-transport` − 1) est > 2*n* (`sortie-rentable?`). Indicateurs `nb-sorties-terminees`, `nb-sorties-deficitaires`, `gain-moyen-sortie`. | `it1_B`, `it1_C` |
| 12 | Pas de réservation du stock. | Au départ, l'humain réserve sur son point la quantité qu'il pourra collecter (`stock-reserve` des patches, `reservation` des humains) ; à l'arrivée il prend au moins sa réservation. Réservation rendue s'il meurt ou se transforme en route (`liberer-reservation`, appelée par `mourir` et `transformer`). Invariants : réservation entre 0 et le stock, cohérente avec les humains à l'aller, aucune sortie déficitaire. | `it1_B`, `it1_A`, `it2_B`, `it1_C`, fichier principal |
| 13 | `proba-defense` à revalider avec la prédation. | Expérience `it2-calibration-defense` et `analyse/calibration_defense.py` : **0,125 conservée** (voir plus bas, refait après la correction 14). | fichier principal, `analyse/`, `results/`, `figures/` |
| 14 | 99 % des attaques visaient des humains **cachés dans leur colonie** (mesure sur 100 graines, avec et sans obstacles), alors que le TP5 prévoit la défense « pendant le déplacement de l'humain ». Le risque ne dépendait donc presque pas des sorties, ce qui vidait la question (stratégie de ravitaillement) de son sens, et aucune valeur de `proba-defense` ne remplissait le critère de calibrage. | **La colonie protège ses habitants** : un zombie ne voit, ne poursuit et n'attaque que les humains en sortie (`proies-visibles`, mission « aller » ou « retour »). Un infecté qui rentre peut toujours se transformer à la colonie : le zombie apparaît sur place, puis ne s'en prend qu'aux humains qui sortent. `zombie-attaquer` ne fait rien sans proie visible. Nouveau scénario dans `tester-it2` : un humain à la colonie n'est jamais attaqué. | `it2_A`, `it2_C` |
| 15 | `choisir-point` n'était appelée nulle part. | Supprimée. | `it1_B` |
| 16 | Les réglages par défaut (20 zombies, 30 obstacles) n'avaient jamais été validés ensemble. | `analyse/validation_reglages.py` : chaque curseur balayé seul autour de sa valeur par défaut, 100 graines par valeur, avec et sans zombie (voir « Validation des réglages »). | `analyse/`, `results/` |

## Tests d'harmonisation (NetLogo 7.0.4, sans interface)

Résultats après toutes les corrections (1 à 16).

- **`tester-it1`** : critères 1 à 4 vrais ; les 20 lignes sont identiques à la référence régénérée sur la base corrigée (graines 8 et 14 sans famine depuis la réservation du stock, correction 12). Survie moyenne 1,007, 20 simulations sur 20 dans [0,9 ; 1,1]. La correction 14 ne change rien sans zombie.
- **`tester-it2`** : critères 1 à 4 vrais. Scénarios d'attaque (humain en sortie) inchangés : cas mixte 0,285 / 0,128 / 0,288 pour 0,3 / 0,14 / 0,28 attendus ; âge du zombie 100 → 52. Nouveau scénario : un humain à la colonie n'est jamais attaqué (1000 sur 1000 indemnes, avec mort et infection certaines). Sur les 20 simulations : **90 humains** restants en moyenne (22 avant la correction 14), minimum 61, aucune extinction, zombies présents à la fin dans 19 sur 20, 3,4 morts par attaque en moyenne (36 avant). Deux lancements donnent une sortie identique.
- **Courbes refaites** : `results/it2_courbes.csv` et `figures/it2_courbes.png`. Au jour 30 : 90 humains et 2,6 zombies en moyenne ; humains présents dans 20 simulations sur 20, zombies dans 19 sur 20. Les zombies restent autour de 19 jusqu'au jour 20, puis tombent à 5 : les 20 zombies du départ ont tous l'âge 0 et meurent de vieillesse ensemble à 480 ticks (voir « Reste à faire »).
- **Sorties** : 0 sortie déficitaire dans toutes les simulations de la validation des réglages (8 700, avec et sans zombie).
- **Affichage** (3 simulations de 720 ticks, réglages par défaut) : à chaque tick, un humain est caché si et seulement s'il est à la colonie ; aucun zombie caché ; tous les humains et zombies de taille 1 ; aucune étiquette sur les humains et les zombies.

## Calibrage de `proba-defense` (correction 13, refait après la correction 14)

Expérience `it2-calibration-defense` : `proba-defense` de 0 à 0,5 par pas de 0,025, sans obstacle et avec 30 obstacles, 100 graines par valeur ; `analyse/calibration_defense.py`, `figures/it2_calibration_defense.png`.

- Le critère (zombies présents à 720 ticks dans au moins 50 % des simulations, humains éteints dans au plus 10 %) est **rempli pour toutes les valeurs** : aucune extinction humaine, zombies présents dans 58 % (à 0,5) à 100 % (à 0) des simulations. Avant la correction 14, aucune valeur ne le remplissait.
- **0,125 conservée** : zombies présents dans 97 % (sans obstacle) et 91 % (30 obstacles) des simulations, 88 à 89 humains sur 100 à 720 ticks. Au-delà de 0,15, la part avec zombies passe sous 90 % ; la survie monte vers 96 % à 0,5, ce qui laisserait peu d'écart entre les stratégies de ravitaillement.

## Validation des réglages (correction 16)

`analyse/validation_reglages.py --lancer` : chaque curseur est balayé seul autour de sa valeur par défaut, 100 graines par valeur, invariants vérifiés à chaque tick ; synthèse dans `results/validation_reglages.csv`. Deux séries : modèle complet (20 zombies, 30 obstacles, 19 curseurs) et sans zombie (30 obstacles, 10 curseurs de l'itération 1). 8 700 simulations au total.

**Résultat global** : dans toutes les simulations, invariants vrais à chaque tick, aucune erreur, aucune sortie déficitaire, aucune extinction humaine.

**Réglages par défaut (20 zombies, 30 obstacles)** : 88,9 humains à 720 ticks (minimum 53), zombies présents dans 91 % des simulations, 1,2 mort de famine et 3,6 morts par attaque en moyenne. Sans zombie : 101,1 humains (minimum 100), aucune famine. **La configuration par défaut est validée.**

Effet de chaque curseur sur les humains à 720 ticks (modèle complet, valeur par défaut en gras) :

| Curseur | Valeurs testées | Humains à 720 ticks | À retenir |
|---|---|---|---|
| `capacite-transport` | 25 / **50** / 75 | 46 / 89 / 95 | **falaise sous 50** : à 25, une sortie n'est rentable qu'à moins de 12 pas ; famine (14 morts même sans zombie) |
| `consommation-jour` | 0,125 / **0,25** / 0,5 | 95 / 89 / 67 | sensible ; à 0,5, famine même sans zombie (minimum 65) |
| `proba-mort-attaque` | 0 / **0,1** / 0,3 | 94 / 89 / 68 | sensible : c'est le paramètre de prédation qui compte |
| `nb-zombies` | 0 / 10 / **20** / 40 | 101 / 95 / 89 / 76 | effet régulier ; 20 est fixé par le TP5 |
| `nb-points-ravitaillement` | 8 / 12 / **16** / 24 | 74 / 83 / 89 / 92 | sous 16, famine (sans zombie : minimum 51 à 8 points) |
| `duree-vie-zombie` | 240 / **480** / 720 | 95 / 89 / 86 | **décide si des zombies restent** : 7 % / 91 % / 100 % des simulations ; à régler à l'itération 3 (B) |
| `portee-detection` | 2 / **3** / 5 | 93 / 89 / 82 | modéré ; à revoir à l'itération 3 (B) |
| `proba-defense` | 0 / **0,125** / 0,3 | 81 / 89 / 94 | voir le calibrage |
| `gain-attaque-zombie` | 0 / **48** / 96 | 89 / 89 / 89 | **sans effet** : les proies sont trop rares pour qu'un repas compte |
| `seuil-naissance` | 40 / **80** / 120 | 88 / 89 / 88 | à 120, aucune naissance : le seuil dépasse le stock de départ des colonies (100) |
| `taux-naissance` | 0,005 / **0,01** / 0,02 | 88 / 89 / 89 | sans zombie, 0,02 provoque de la famine (minimum 77) : 0,01 confirmé |
| `nb-obstacles`, `stock-initial-point`, `regeneration-point`, `s-min`, `stock-initial-colonie`, `delai-transformation`, `proba-infection`, `proba-mort-infection` | autour du défaut | 83 à 93 | peu sensibles autour du défaut |

## Relecture (faite à la place de Soumia et Amandine)

Chaque point de l'ancienne liste « À vérifier » a été relu dans le code, puis contrôlé par les tests ci-dessus.

**Partie de Soumia (`it1_A`, `it2_A`)**
- [x] `actualiser-affichage-colonies` : correct. L'étiquette compte **tous** les habitants (présents et en sortie). L'ancienne consigne « total des étiquettes plus les humains visibles = moniteur » comptait deux fois les humains en sortie : la bonne vérification est **total des étiquettes = moniteur « Humains vivants »** (vrai par construction : chaque humain a une colonie d'origine).
- [x] `regenerer-points` (couleur) : correct, plein = vert, vide = noir. La couleur est mise à jour au début du tick qui suit une collecte (décalage d'un tick, affichage seulement).
- [x] `initialiser-zombie` : correct (visible, taille 1, sans étiquette, âge 0).
- [x] `zombie-attaquer` : l'attaquant est bien passé en argument. **Problème trouvé** : les zombies attaquaient les humains cachés dans la colonie (99 % des attaques) → correction 14. `zombie-attaquer` ne plante plus s'il n'y a pas de proie au contact.
- [x] `zombie-se-nourrir` : correct (l'âge ne descend pas sous 0), mais sans effet mesurable aujourd'hui (voir la validation). Pour le rapport : il nuance l'hypothèse du TP5 « le zombie n'a pas besoin de nourriture ».
- [x] `avancer-zombie` : `patch-ahead vitesse-zombie` est la case d'arrivée, donc aucun zombie n'entre dans un obstacle (vérifié dans toutes les simulations).

**Partie d'Amandine (`it1_B`, `it2_B`)**
- [x] `initialiser-humain` et passage visible / caché : correct ; une seule initialisation pour `setup-humains` et `reproduire`.
- [x] Cache de `decider-sortie` : le raisonnement tient (le stock libre ne fait que baisser pendant la phase des humains ; une réservation rendue vide le cache). Preuve : `tester-it1` est identique à la référence.
- [x] Rentabilité (`sortie-rentable?`, `quantite-collectable`), réservation (`decider-sortie`, `collecter`, `liberer-reservation`) et bilan des sorties : corrects ; aucune sortie déficitaire et invariant des réservations vrai dans toutes les simulations. Écart au TP5 à justifier dans le rapport : le point choisi est le plus proche **rentable**, pas le plus proche dont le stock est positif.
- [x] `choisir-point` : jamais appelée → supprimée (correction 15).
- [x] `detecter-et-defendre [ attaquant ]` : signature, ordre des trois tirages et probabilités globales conformes au commentaire (vérifiés par le cas mixte de `tester-it2`).
- [x] `transformer` : `liberer-reservation` est bien appelée avant `die`.

**Les deux**
- [x] Total des étiquettes = moniteur « Humains vivants » (voir plus haut).
- [x] « Test it1 » et « Test it2 » relancés (sans interface) : résultats ci-dessus.
- [ ] Ouvrir le modèle dans l'interface, `setup` puis `go` avec 20 et 100 humains, et regarder la carte : **à faire par l'équipe** (impossible à vérifier sans interface).

## Reste à faire ou à décider

- **Itération 3, partie B** : `duree-vie-zombie` décide presque à elle seule si des zombies restent à 30 jours (7 % des simulations à 240 ticks, 91 % à 480, 100 % à 720). De plus, les 20 zombies du départ ont tous l'âge 0 et meurent ensemble au jour 20 (chute visible sur `figures/it2_courbes.png`). Leur donner un âge initial au hasard (entre 0 et `duree-vie-zombie`) supprimerait cet artefact. À décider avec la partie B : cela changerait les courbes et le calibrage.
- **`gain-attaque-zombie`** n'a aucun effet mesurable : le garder pour le cadre proie-prédateur en le présentant comme tel dans le rapport, ou le retirer.
- **Branche de l'itération 3** : les anciennes branches `iteration3` et `iteration3-corrigee` ont été supprimées (sauvegarde locale dans les tags `sauvegarde/iteration3` et `sauvegarde/iteration3-corrigee`). À recréer depuis `main` une fois cette branche fusionnée. La référence `results/reference_tester_it1.txt` de `sauvegarde/iteration3-corrigee` reste valable (lignes identiques).
