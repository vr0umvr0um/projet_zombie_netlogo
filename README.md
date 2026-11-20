# Colonies et zombies : projet NetLogo (SMASE)

Simulation multi-agents d'une infection zombie dans plusieurs colonies. Les humains vivent en colonies, sortent chercher de la nourriture et sont exposés aux zombies. L'infection est inspirée d'une épidémie réelle (cas et décès Covid-19 en France, partie données à venir).

**Question :** quelle stratégie de ravitaillement (individuelle, groupe fixe, groupe adaptatif) influence la proportion de survivants après 30 jours (720 ticks) ?

Cadre proie-prédateur : la nourriture joue le rôle de l'herbe, les humains celui des proies, les zombies celui des prédateurs.

Ce README explique comment utiliser le dépôt. Le raisonnement scientifique (question, données, modèle, vérification, sensibilité, calibration, validation, limites) est à rédiger par l'équipe dans le rapport et l'onglet Info du modèle.

## État d'avancement

| Itération | Contenu | État |
|---|---|---|
| 1 | environnement / humain (colonies, nourriture, sorties individuelles, reproduction) | terminée : critères 1 à 6 vérifiés |
| 2 | humain / zombie (attaque, défense, infection, transformation) | terminée : critères 1 à 4 vérifiés, courbes tracées |
| 3 | environnement / zombie (obstacles et bords) | à démarrer |
| 4 | stratégies de groupe (groupe fixe, groupe adaptatif) | à faire |
| 5 | sensibilité, calibration, validation, rapport | à faire |

## Prérequis

- NetLogo 7.0.4.
- Python 3 pour les figures : `pip install -r requirements.txt` (pandas, matplotlib).

## Lancer le modèle

1. Ouvrir `Projet_zombies_base.nlogox` dans NetLogo (les fichiers `.nls` doivent rester dans le même dossier).
2. Cliquer sur `setup`, puis sur `go` : la simulation s'arrête à 720 ticks (30 jours, 1 tick = 1 heure).
3. Le curseur `delai-tick` règle la vitesse : pause en secondes après chaque tick (0,05 par défaut, soit environ 40 secondes pour les 30 jours ; 0 pour la vitesse maximale). Le curseur de vitesse de NetLogo, en haut de la fenêtre, agit aussi sur l'affichage. Le moniteur « Temps simulé » indique le jour et l'heure.
4. Les autres curseurs règlent les paramètres ; le sélecteur `strategie` est prévu pour l'itération 4.

Lecture de la carte : les humains présents à la colonie sont cachés et comptés dans l'étiquette de la maison (« 25 h (2 inf.) / 72 » : habitants, présents et en sortie, infectés, stock) ; la somme des étiquettes est donc égale au moniteur « Humains vivants ». Seuls les humains en sortie sont visibles (bleu ciel, orange s'ils sont infectés). Les zombies sont violets, de la même taille que les humains. La maison est bleue si son stock atteint `s-min`, bleu foncé en dessous, noire à zéro et grise sans habitant ; un point de ravitaillement passe du vert (plein) au noir (vide).

La colonie protège ses habitants : un zombie ne voit, ne poursuit et n'attaque que les humains en sortie (TP5 : l'humain se défend « pendant le déplacement »). Un infecté qui rentre peut se transformer à la colonie ; le zombie qui apparaît n'attaque ensuite que les humains qui sortent.

Réglages par défaut retenus :

| Paramètre | Valeur | Paramètre | Valeur |
|---|---|---|---|
| `nb-humains` / `nb-zombies` / `nb-colonies` | 100 / 20 / 4 | `capacite-transport` | 50 |
| `nb-points-ravitaillement` | 16 | `consommation-jour` | 0,25 |
| `stock-initial-point` | 150 | `s-min` | 80 |
| `regeneration-point` | 0,5 | `seuil-naissance` / `taux-naissance` | 80 / 0,01 |
| `proba-defense` | 0,125 | `proba-infection` | 0,5 |
| `proba-mort-attaque` | 0,1 | `gain-attaque-zombie` | 48 ticks |

## Organisation du code

Un fichier par partie (A, B, C) et par itération, inclus dans le fichier principal.

| Fichier | Rôle |
|---|---|
| `Projet_zombies_base.nlogox` | interface, variables communes, `setup`, `go`, expériences BehaviorSpace |
| `it1_A_environnement_colonies.nls` | carte, points de ravitaillement, colonies, consommation, famine, naissances, mort |
| `it1_B_humains_sorties.nls` | humains, sorties individuelles de ravitaillement |
| `it1_C_indicateurs_verification.nls` | indicateurs, invariants, `tester-it1` |
| `it2_A_zombies.nls` | création et comportement des zombies |
| `it2_B_infection_defense.nls` | défense, infection, transformation (côté humain) |
| `it2_C_indicateurs_tests.nls` | indicateurs d'infection, scénarios unitaires, `tester-it2` |
| `analyse/` | scripts Python d'analyse |
| `results/` | CSV produits par BehaviorSpace |
| `figures/` | figures produites par les scripts |

Les variables communes (`globals`, `*-own`) sont dans le fichier principal : toute modification doit être annoncée à l'équipe.

## Tests et expériences

- **Boutons « Test it1 » et « Test it2 »** (procédures `tester-it1-pas` et `tester-it2-pas`) : lancent 20 graines et affichent les critères de sortie dans le Centre de commandes (comptez quelques minutes chacun). Ce sont des boutons « forever » : **recliquer dessus arrête le test**, le relancer le reprend, et « setup » l'annule. Le moniteur « Test en cours » indique la graine et le jour. Les procédures `tester-it1` et `tester-it2` font la même chose d'un seul bloc, sans interruption possible : elles servent à la ligne de commande.
- **`invariants-ok?`** : vrai si les stocks sont positifs, les états valides, les humains et les zombies conservés, et aucune infection n'apparaît sans zombie. `liste-invariants-violes` dit lequel échoue.
- **Expériences BehaviorSpace** : `it1-stabilite`, `it1-reglage-taux-naissance`, `it2-courbes`, `it2-calibration-defense` (`proba-defense` de 0 à 0,5, sans obstacle et avec 30 obstacles, 100 graines par valeur ; analyse : `python analyse/calibration_defense.py`, figure `figures/it2_calibration_defense.png`).
- **Validation des réglages** : `python analyse/validation_reglages.py --lancer` balaie chaque curseur seul autour de sa valeur par défaut (100 graines par valeur, modèle complet et sans zombie, invariants vérifiés à chaque tick), puis écrit la synthèse dans `results/validation_reglages.csv`. Sans `--lancer`, il refait seulement la synthèse à partir des tables de `results/validation_reglages/` (non versionnées).
- **Non-régression** : sans zombie, `tester-it1` doit redonner exactement les 20 lignes de `results/reference_tester_it1.txt`.
- **Reproductibilité** : chaque test et chaque expérience fixe sa graine. `tester-it1` et les simulations de `tester-it2` utilisent les graines 1 à 20, les scénarios d'attaque et d'infection de `tester-it2` repartent de `graine-scenarios` (1), et les expériences BehaviorSpace utilisent le numéro de simulation (`random-seed behaviorspace-run-number`). Deux lancements donnent exactement la même sortie.

Lancer une expérience sans interface (exemple pour `it2-courbes`, depuis ce dossier) :

```bash
"C:/Program Files/NetLogo 7.0.4/runtime/bin/java" -cp "C:/Program Files/NetLogo 7.0.4/app/*" org.nlogo.headless.Main --model Projet_zombies_base.nlogox --experiment it2-courbes --threads 8 --table results/it2_courbes.csv
```

Tracer les courbes de l'itération 2 :

```bash
python analyse/courbes_it2.py
```

La figure obtenue est `figures/it2_courbes.png`.

## Limites connues

- Les données Covid-19 ne sont pas encore intégrées : calibration et validation restent à faire (itération 5).
- Les courbes de l'itération 2 n'oscillent pas. Une attaque peut tuer l'humain (`proba-mort-attaque`) et nourrir le zombie (`gain-attaque-zombie`), comme dans *Wolf Sheep Predation*. Depuis que la colonie protège ses habitants, les 20 zombies du départ meurent surtout de vieillesse (`duree-vie-zombie`, 480 ticks) et sont remplacés par les humains infectés en sortie qui se transforment. Le gain d'un repas compte peu, car les proies (humains en sortie) sont rares.
- `zombie-se-nourrir` nuance l'hypothèse du TP5 « le zombie n'a pas besoin de nourriture » : il n'en a pas besoin pour vivre, mais un repas prolonge sa vie. À formuler ainsi dans le rapport.
- Le TP5 dit que l'humain choisit « le point le plus proche dont le stock est strictement positif » ; le modèle choisit le plus proche **rentable** (correction 11 de `CORRECTIONS_IT1_IT2.md`), pour qu'aucune sortie ne coûte plus qu'elle ne rapporte. Écart à justifier dans le rapport.
- Un critère de l'itération 1 est évalué statistiquement (au moins 18 simulations sur 20). Depuis la réservation du stock, aucune des 20 graines ne connaît plus de famine : celle de la graine 8, attribuée à la malchance, venait d'un point vidé par une autre colonie.
- `proba-defense` (0,125) : le critère de calibrage (zombies présents à 720 ticks dans au moins 50 % des simulations, humains éteints dans au plus 10 %) est rempli pour toutes les valeurs de 0 à 0,5 et ne départage plus. 0,125 garde des zombies dans plus de 90 % des simulations, avec et sans obstacles, sans saturer la survie (`analyse/calibration_defense.py`).
