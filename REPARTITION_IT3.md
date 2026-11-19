# Répartition de l'itération 3 (environnement / zombie)

**Branche** : `iteration3-corrigee`, recréée à partir des corrections des itérations 1 et 2 (branche `correction-iteration1-iteration2`, voir `CORRECTIONS_IT1_IT2.md`). Elle remplacera l'ancienne branche `iteration3` si les trois sont d'accord (pas de `push --force` sans accord). Si la relecture des corrections entraîne de nouveaux changements, ils seront reportés ici.

Décision de l'équipe : **chaque personne garde la même lettre à chaque itération**. Il n'y a donc pas de rotation. Reste à valider ensemble la définition de « zombie immobile » et le calendrier (voir « À trancher »).

## Qui fait quoi

| Personne | Partie | Fichier | Contenu à l'itération 3 |
|---|---|---|---|
| Soumia | **A** | `it3_A_zombies_obstacles.nls` | déplacement des zombies autour des obstacles et des bords |
| Amandine | **B** | `it3_B_zombies_parametres.nls` | paramètres des zombies : vitesse, portée, durée de vie, revalidation de `proba-defense` |
| Vanessa | **C** | `it3_C_indicateurs_tests.nls` | indicateurs spatiaux, invariants, `tester-it3`, courbes et carte de densité |

Continuité avec les itérations 1 et 2 :
- **Soumia** a écrit le code des zombies (création, errance, poursuite, attaque) et ses premiers tests : elle connaît `zombie-agir`, `avancer-zombie` et `case-franchissable?`, ce qu'il faut pour les faire contourner des obstacles.
- **Amandine** a écrit les sorties, les trajets et la défense : elle connaît l'équilibre entre les paramètres (règle de rentabilité des sorties, plafond, défense et infection), utile pour régler ceux des zombies.
- **Vanessa** a écrit les indicateurs, les invariants et les tests des deux itérations, dont la version pas à pas : même rôle ici.

Deux liens à exploiter : le contournement d'obstacle peut réutiliser le calcul de trajet d'Amandine (`chemin-vers-ravitaillement`, `it1_B_humains_sorties.nls`), donc Soumia et Amandine se parlent tôt ; Soumia et Vanessa se mettent d'accord le premier jour sur la définition d'un zombie immobile.

## Comprendre tout le modèle sans rotation : la relecture croisée

Le plan souhaitait que chacune comprenne tout le modèle pour l'oral du 16 décembre. Sans rotation, une relecture croisée y répond, sans retarder l'itération :

| La partie de | est relue par |
|---|---|
| Soumia (A) | Amandine |
| Amandine (B) | Vanessa |
| Vanessa (C) | Soumia |

La relecture se fait dans les deux jours qui précèdent la séance d'assemblage. Elle vérifie : le fichier compile ; `tester-it1` redonne les lignes de `results/reference_tester_it1.txt` ; les commentaires permettent de comprendre la logique sans l'auteure. La relectrice doit pouvoir expliquer la partie qu'elle a relue. À la répétition de l'oral, chacune présente l'itération en s'appuyant sur la partie qu'elle a relue plutôt que sur la sienne.

## Contenu de chaque partie

### A : `it3_A_zombies_obstacles.nls` (le plus de code)
1. **Mesurer d'abord** : avec `nb-obstacles = 30`, y a-t-il vraiment des zombies coincés ? (Compter les zombies dont la position n'a pas changé depuis 24 ticks, sur 20 graines.) Ne corriger que ce qui est mesuré.
2. Définir `zombie-bloque?` (à convenir avec C, voir « À trancher »).
3. Écrire `contourner-obstacle` (essayer gauche puis droite, glisser le long de l'obstacle, ou réutiliser le calcul de trajet de la partie B) et l'appeler depuis `avancer-zombie` (`it2_A_zombies.nls`).
4. Gérer les bords de la carte (le monde n'est pas torique).
5. Attention au temps de calcul : un calcul de trajet par zombie et par tick ralentirait beaucoup : ne l'appeler que si le zombie est bloqué.

### B : `it3_B_zombies_parametres.nls` (le plus d'expériences)
1. **Revalider `proba-defense = 0,125` avec 30 obstacles** (elle a été choisie sans obstacle). Attention : depuis la prédation, **aucune valeur ne remplit les deux seuils, même sans obstacle** (zombies présents dans au moins la moitié des simulations, humains éteints dans au plus 10 % ; voir `analyse/calibration_defense.py`). Le critère est donc à trancher en équipe avant de lancer les balayages. Méthode à reprendre : l'expérience `it2-calibration-defense` (100 graines par valeur, graine = numéro de répétition), avec `nb-obstacles = 30`.
2. **Balayage un paramètre à la fois**, 100 simulations par valeur (avec 10 ou 20, le résultat bascule d'une valeur à l'autre) : vitesse des zombies (0,25 ; 0,5 ; 0,75), `portee-detection` (2 ; 3 ; 5), `duree-vie-zombie` (240 ; 480 ; 720).
3. Décider si `vitesse-zombie` devient un curseur (le reporter est dans `it2_A_zombies.nls` : à coordonner avec A).
4. Consigner les résultats (tableaux, niveau de certitude, limites) pour le rapport.

Pour démarrer les balayages : les expériences existantes (`it1-stabilite`, `it2-courbes`, `it1-reglage-taux-naissance`) servent de modèle (menu Tools > BehaviorSpace de NetLogo). En ligne de commande, la commande est dans le README. Méthode à reprendre : critères choisis avant les mesures, même nombre de simulations par case, tableaux complets.

### C : `it3_C_indicateurs_tests.nls` (le plus de tests)
1. `nb-zombies-sur-obstacle` (doit valoir 0), `nb-zombies-immobiles`, `part-zombies-immobiles`.
2. `liste-invariants-zombies-violes` (aucun zombie sur un obstacle ni hors carte) et branchement dans `liste-invariants-violes` (`it1_C_indicateurs_verification.nls`).
3. `tester-it3` **et** sa version pas à pas `tester-it3-pas`, sur le modèle de `it2_C` (bouton « forever » arrêtable), avec un bouton et un moniteur dans le fichier principal.
4. Expérience BehaviorSpace `it3-courbes`, carte de densité des zombies (variable de patch à déclarer dans le fichier principal) et script `analyse/carte_densite_it3.py` pour la figure.

## Dépendances et points de contact

| Ce qu'une partie fournit | À qui | Quand |
|---|---|---|
| `zombie-bloque?` et la variable `ticks-immobile` (dans `zombies-own`, fichier principal) : **Soumia** | Vanessa (compter les immobiles), Amandine (indicateur de balayage) | **dans les deux premiers jours** : tout le reste en dépend |
| Première version du contournement : **Soumia** | Amandine (balayages avec obstacles) | milieu d'itération ; Amandine peut commencer avec le mouvement actuel et relancer ensuite |
| Définition de « immobile » et seuils | Soumia et Vanessa ensemble | première réunion |
| Curseur éventuel pour la vitesse | Amandine (demande) et Soumia (propriétaire de `it2_A`) | avant qu'Amandine ne relance ses balayages |

Fichiers partagés : le fichier principal (variables, curseurs, boutons) et `it1_C_indicateurs_verification.nls` (invariants, modifié par Vanessa). Toute modification est annoncée aux deux autres avant le commit.

## Critères de fin (rappel de `PLAN_ITERATIONS.md`)
- Aucun zombie sur un obstacle ni hors de la carte.
- Moins de 5 % de zombies immobiles.
- 20 graines du modèle complet sans erreur.
- Vitesse, portée et durée de vie des zombies fixées et justifiées.

**Non-régression** :
- `tester-it1` (aucun zombie) doit redonner exactement les 20 lignes de `results/reference_tester_it1.txt` (régénéré sur la base corrigée : réservation du stock, sorties rentables) : le code de l'itération 3 ne doit rien changer quand il n'y a pas de zombie.
- `tester-it2` (sans obstacle) doit rester vrai sur ses critères. Ses lignes peuvent changer légèrement si la gestion des bords évolue.

## Calendrier proposé
Le plan prévoyait l'itération 3 du 27 novembre au 4 décembre. Les itérations 1 et 2 sont terminées en avance : proposition pour gagner une marge avant l'itération 4 (groupes) :

| Date | Étape |
|---|---|
| à fixer | réunion de lancement (validation, définition de « immobile », conventions) |
| +2 jours | Soumia livre `zombie-bloque?` et `ticks-immobile` |
| +5 jours | point d'étape rapide (15 minutes) : mouvement, premiers balayages, invariants |
| +6 à +7 jours | relecture croisée |
| +8 jours | séance d'assemblage (checklist de `PLAN_ITERATIONS.md`), bilan, tag `it3` |

Si vous préférez rester sur le calendrier du plan, l'assemblage est le 4 décembre.

## Méthode de travail
- Chacune travaille dans **son fichier** : les conflits sont alors rares. Branche commune : `iteration3-corrigee`.
- Avant de pousser : `git pull --rebase origin iteration3-corrigee`. Un commit par fonctionnalité terminée, message en français qui dit ce qui est mesuré.
- Jamais de `push --force` sans accord des trois.
- Chaque fonctionnalité est testée (au minimum compilation et `tester-it1` inchangé) avant le push.

## Pièges connus (appris aux itérations 1 et 2)
1. Une déclaration `globals` dans un fichier `.nls` doit précéder toute procédure.
2. `clear-all` (donc `setup`) remet toutes les variables globales à 0 : un test qui appelle `setup` doit sauvegarder et restaurer son état (voir `it1_C`).
3. Les reporters qui utilisent `of` consomment du hasard : les numéros de graines ne sont pas comparables d'une expérience à l'autre.
4. En ligne de commande, une erreur d'exécution dans `go` peut arrêter une expérience BehaviorSpace sans message : tester avec `carefully [ ... ] [ print error-message ]`.
5. Un bouton « forever » s'arrête avec `stop` au niveau de la procédure du bouton ; `die` interrompt la procédure de l'agent concerné.
6. Un agent mort ne peut plus servir d'argument (`member?`, `ask`) : le retrouver par son numéro `who`.
7. `list` avec plus de deux arguments demande des parenthèses : `(list a b c)`.
8. Les curseurs que seul `setup` lit (`nb-zombies`, `nb-obstacles`) doivent être remis à leur valeur après un test.
9. Un humain qui disparaît passe toujours par `mourir [ cause ]` ou `transformer`, jamais par un `die` direct : ces procédures rendent le stock qu'il avait réservé (`liberer-reservation`) et tiennent les compteurs. Sinon, l'invariant des réservations échoue.
10. Chaque test et chaque expérience fixe sa graine (`random-seed`) : sans cela, deux lancements ne donnent pas les mêmes chiffres.
11. 20 graines ne suffisent pas pour départager deux valeurs proches d'un paramètre : compter au moins 100 simulations par valeur.

## À trancher en début d'itération
- Définition de « zombie immobile » (proposition : position inchangée depuis 24 ticks, soit un jour simulé, alors qu'aucun humain n'est à portée de contact).
- Vitesse des zombies : curseur ou valeur fixe.
- Garder ou non le calendrier avancé.
- Adopter ou non la relecture croisée.
- Critère de `proba-defense` : aucune valeur ne garde des zombies dans au moins la moitié des simulations sans éteindre les humains dans plus de 10 % des cas. Assouplir un seuil, ou agir sur un autre paramètre (`proba-mort-attaque`, `duree-vie-zombie`) ?
- Remplacer l'ancienne branche `iteration3` par `iteration3-corrigee`.

## Message à envoyer
```
Itération 3 (zombies et obstacles). Chacune garde sa lettre :
- Soumia : partie A (déplacement des zombies autour des obstacles)
- Amandine : partie B (paramètres des zombies, balayages)
- Vanessa : partie C (indicateurs spatiaux, invariants, test)
Soumia, peux-tu livrer zombie-bloque? et ticks-immobile dans les deux premiers jours ? Le reste en dépend.
Proposition : une relecture croisée avant l'assemblage (Amandine relit A, Vanessa relit B, Soumia relit C) pour que chacune comprenne tout le modèle.
Détails, dépendances et calendrier dans REPARTITION_IT3.md (branche iteration3-corrigee).
Pour récupérer la branche : git fetch origin puis git checkout iteration3-corrigee.
```
