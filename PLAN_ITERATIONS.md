# Plan par itérations - Projet colonies / zombies

Point de départ : vendredi 13 novembre 2026. Oral du projet : mercredi 16 décembre 2026.
Les dates ci-dessous sont une proposition à ajuster selon vos disponibilités.

## Principe

- **Une paire d'agents à la fois.** On teste la paire jusqu'à ce que son comportement soit stable, puis on ajoute le dernier élément.
- **Trois parties (A, B, C) par itération**, travaillées en parallèle, une par personne, chacune dans son fichier `.nls`.
- **Séance d'assemblage** à la fin de chaque itération : on fusionne, on compile, on vérifie les critères de sortie, puis on répartit l'itération suivante.
- **On ne passe pas à l'itération suivante** tant que les critères de sortie ne sont pas tous vérifiés.
- **Rotation conseillée** : changez de lettre (A, B, C) d'une itération à l'autre. Chacun doit comprendre tout le modèle pour l'oral.

| It. | Paire testée | Agents actifs | Dates | Sorties attendues |
|---|---|---|---|---|
| 1 | environnement / humain | humains, colonies, patches (`nb-zombies = 0`) | 13 -> 20 nov | cycle de vie des colonies stable, sans zombie |
| 2 | humain / zombie | + zombies, sans obstacle (`nb-obstacles = 0`) | 20 -> 27 nov | attaque, défense, infection, transformation validées |
| 3 | environnement / zombie | zombies + obstacles et bords | 27 nov -> 4 déc | déplacement des zombies dans l'environnement réel |
| 4 | tous les agents | stratégies de groupe | 4 -> 9 déc | trois stratégies comparables |
| 5 | expériences | plan complet | 9 -> 14 déc | résultats, calibration, validation, rapport |

Du 14 au 16 décembre : répétition de l'oral. Si le calendrier glisse, la première chose à fusionner est l'itération 3 dans l'itération 2.

## Fichiers

Un fichier par partie et par itération, nommé `itN_X_sujet.nls`, inclus dans `Projet_zombies_base.nlogox`.
Les variables communes (globals, breeds, `*-own`) restent dans le fichier principal : toute modification doit être annoncée aux deux autres.
Les fichiers des itérations 3 à 5 sont créés au début de chaque itération.

## Itération 1 - environnement / humain

**Réglages de test** : `nb-zombies = 0`. Zombies absents, donc `evoluer-infection` et les attaques ne sont pas encore appelés.

| Partie | Fichier | Contenu |
|---|---|---|
| A | `it1_A_environnement_colonies.nls` | `setup-environnement`, `setup-colonies`, `regenerer-points`, `evenements-journaliers` (consommation, famine), `reproduire`, `mourir` |
| B | `it1_B_humains_sorties.nls` | `setup-humains`, `humain-agir`, `decider-sortie`, `choisir-point`, `aller-vers-point`, `collecter`, `rentrer-a-la-colonie` (stratégie individuelle) |
| C | `it1_C_indicateurs_verification.nls` | indicateurs de population et de stocks, `invariants-ok?`, courbes, réglage du taux de naissance, scénarios de test |

**À décider dès le début de l'itération (parties B et C ensemble)** : plafond de sorties simultanées par colonie. Sans plafond, tous les humains partent en même temps dès que le stock passe sous `S_min`.

**Critères de sortie** :
1. `setup` puis 720 ticks de `go` sans erreur, sur 20 graines.
2. `invariants-ok?` est vrai tout au long de la simulation.
3. Sans zombie, la population reste stable : `proportion-survivants` entre 0,9 et 1,1 à 720 ticks, en moyenne et pour au moins 18 simulations sur 20 (décision D7, `DECISIONS_IT1.md`).
4. Les points de ravitaillement se régénèrent et ne tombent pas durablement à zéro (moins de 10 % des ticks sans point) ; les morts de famine restent inférieures à 5 % des humains, en moyenne et pour au moins 18 simulations sur 20 (décision D10, `DECISIONS_IT1.md`).
5. Au moins une sortie complète est observée par colonie (aller, collecte, retour) sans traverser d'obstacle.
6. Les deux consommations sont distinguées et documentées : 1 unité par tick de déplacement, `consommation-jour` à la colonie.

## Itération 2 - humain / zombie

**Réglages de test** : `nb-zombies = 20`, `nb-obstacles = 0`, `proba-defense = 0,125` (décision D11), pour isoler l'interaction humain/zombie.

| Partie | Fichier | Contenu |
|---|---|---|
| A | `it2_A_zombies.nls` | côté zombie : `setup-zombies`, `zombie-agir`, errance, poursuite, `zombie-attaquer`, vitesse et distance de contact |
| B | `it2_B_infection_defense.nls` | côté humain : `detecter-et-defendre`, `infecter`, `evoluer-infection`, `transformer` ; branchement de `evoluer-infection` dans `humain-agir` |
| C | `it2_C_indicateurs_tests.nls` | infectés, part d'infectés, scénarios unitaires, courbes humains/zombies |

Le code des parties A et B est écrit, assemblé et testé (`tester-it2`, version marquée par le tag `it1-it2`).

**Critères de sortie** :
1. `proba-infection = 0` : aucune infection. `proba-defense = 1` : aucun humain infecté et zombies détruits. `proba-defense = 0` et `proba-infection = 1` : infection à chaque contact.
2. Un infecté meurt ou se transforme après `delai-transformation` ; la part qui meurt est proche de `proba-mort-infection` (20 graines).
3. `invariants-ok?` est vrai ; avec `nb-zombies = 0`, aucune infection (retour à l'état de l'itération 1).
4. Un agent tué n'agit plus ensuite, sans erreur d'exécution.
5. Les courbes humains(t) et zombies(t) sont décrites (20 graines) et comparées qualitativement à *Wolf Sheep Predation*.

## Itération 3 - environnement / zombie

**Réglages de test** : `nb-obstacles` normal, tous les agents présents.

| Partie | Contenu prévu |
|---|---|
| A | Déplacement des zombies autour des obstacles et des bords (aucun zombie ne reste bloqué) |
| B | Durée de vie, vitesse et portée de détection des zombies ; réglage de leur effectif |
| C | Indicateurs spatiaux (carte de densité des zombies), invariant « aucun zombie sur un obstacle », courbes |

**Critères de sortie** : aucun zombie sur un obstacle ni hors carte ; moins de 5 % de zombies immobiles ; 20 graines du modèle complet sans erreur ; vitesse, portée et durée de vie des zombies fixées et justifiées.

## Itération 4 - stratégies de groupe

| Partie | Contenu prévu |
|---|---|
| A | Groupe fixe : constitution aléatoire, trajet commun, retour commun |
| B | Groupe adaptatif : taille selon les zombies repérés autour de la colonie |
| C | Défense collective, plafond de sorties, indicateurs de comparaison (infections introduites au retour, nourriture par sortie, nombre de sorties) |

**Critères de sortie** : avec `taille-groupe = 1`, le groupe fixe donne les mêmes résultats que la stratégie individuelle (comparer sur 20 graines) ; le groupe se déplace et se défend ensemble ; invariants vrais pour les trois stratégies.

## Itération 5 - expériences, calibration, validation

| Partie | Contenu prévu |
|---|---|
| A | BehaviorSpace : sensibilité (un paramètre à la fois) puis plan principal, 3 x 2 x 2 x 20 = 240 simulations |
| B | Données Covid : préparation (`01_preparation.py`), grille de calibration sur 2 paramètres |
| C | Analyse Python (moyenne et dispersion), validation sur la seconde période, README et ODD |

**Critères de sortie** : résultats reproductibles (graines notées, README) ; figures lisibles ; seuil RMSE fixé avant la calibration ; validation sans réajustement ; limites rédigées.

## Piste transversale : données et rapport

Indépendante du code, à avancer dès l'itération 1 par la personne la plus libre :
- choix du pays et des deux périodes, fiche descriptive de chaque jeu de données ;
- rédaction progressive du rapport (question, modèle, hypothèses) au fil des itérations ;
- rappel : le rapport et le code livrés doivent être votre travail, pas du texte généré.

## Séance d'assemblage (30 à 45 minutes)

1. Chacun partage son fichier `.nls` ; on les met dans un même dossier.
2. Le modèle compile.
3. `setup` et `go` tournent sur 3 graines sans erreur.
4. `invariants-ok?` est vrai.
5. Les critères de sortie de l'itération sont cochés un par un.
6. On note 5 lignes de bilan : ce qui marche, ce qui est reporté, les décisions prises.
7. On commite la version assemblée, puis on répartit les parties de l'itération suivante.

## Contrats entre parties

- `mourir [ cause ]` : "infection", "attaque" ou "famine" ; incrémente le compteur et retire l'agent (fichier A de l'itération 1).
- `detecter-et-defendre` : procédure d'humain, appelée par le zombie qui attaque, jamais par `humain-agir`.
- `infecter`, `transformer` : procédures d'humain (itération 2).
- `choisir-point` : renvoie un patch de ravitaillement avec un stock > 0, ou `nobody`.
- `invariants-ok?` : booléen ; il doit rester valide à chaque itération.
