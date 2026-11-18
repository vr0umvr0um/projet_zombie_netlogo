# Bilan d'assemblage : itérations 1 et 2

Document préparé pour la séance d'assemblage à trois. Les points marqués **à confirmer ensemble** demandent l'accord des trois personnes. Version marquée par le tag `it1-it2`.

## Bilan en cinq lignes

1. **Ce qui marche.** Les parties A, B et C des deux itérations sont fusionnées et compilent ; les invariants sont vrais à chaque tick sur 20 graines ; `tester-it1` (critères 1 à 4) et `tester-it2` (critères 1 à 4) passent, les critères 5 et 6 de l'itération 1 sont vérifiés à la main.
2. **Ce qui avait cassé et a été réglé.** Avec les curseurs d'origine, toute la population mourait de famine (survie 0) : nouveaux réglages (D1), sorties rentables (D2), stock des points (D9), seuil de naissance (D6).
3. **Ce qui est reporté.** Les stratégies de groupe (itération 4) ; la réservation du stock et la limite d'avance prélevée sur une colonie, nécessaires dès que plusieurs humains partent ensemble ; les données Covid, la calibration et la validation (itération 5).
4. **Décisions prises** (détail et preuves dans `DECISIONS_IT1.md`) : plafond de 1 sortie par colonie, règle de famine inchangée, critères 3 et 4 évalués statistiquement (au moins 18 simulations sur 20), `proba-defense` à 0,125 pour que les zombies ne disparaissent pas.
5. **Points d'attention pour la suite.** Les courbes de l'itération 2 décroissent sans oscillation (extinction progressive, pas de cycle proie-prédateur) ; `proba-defense` est un paramètre structurant à rouvrir dans la sensibilité ; une simulation sur 50 environ connaît encore une famine de plus de 5 %.

## Checklist de la séance (`PLAN_ITERATIONS.md`)

| Étape | État |
|---|---|
| 1. Chacun partage son fichier `.nls`, même dossier | fait : tout est sur la branche `iteration1-iteration2` |
| 2. Le modèle compile | fait |
| 3. `setup` et `go` tournent sur 3 graines sans erreur | fait (20 graines dans chaque test) |
| 4. `invariants-ok?` est vrai | fait |
| 5. Critères de sortie cochés un par un | fait pour les itérations 1 et 2 |
| 6. Bilan de 5 lignes | ci-dessus, **à confirmer ensemble** |
| 7. Commit de la version assemblée, répartition de l'itération suivante | commit et tag faits ; **répartition de l'itération 3 à décider ensemble** |

## À décider ensemble

- **Répartition de l'itération 3** (parties A, B, C), avec rotation des lettres conseillée.
- **Valider les décisions D9, D10 et D11**, prises sur mesures et appliquées après le dernier accord de l'équipe sur D1 à D8 : stock initial des points à 150, critère 4 évalué statistiquement, `proba-defense` à 0,125.
- **Garder ou non le délai de grâce de 3 jours** comme option si les ressources se tendent (non appliqué : aucun gain mesuré au réglage par défaut).
- **Qui rédige quoi dans le rapport** : le rapport et l'onglet Info du modèle doivent rester le travail de l'équipe.

## Vérification rapide pour chacune

```bash
git fetch origin
git checkout iteration1-iteration2
git reset --hard origin/iteration1-iteration2
```

(Sauvegarder d'abord tout travail local non poussé.) Puis ouvrir `Projet_zombies_base.nlogox`, cliquer sur « Test it1 » et « Test it2 » et comparer avec les résultats attendus dans `DECISIONS_IT1.md`.
