# Itération 2 — Partie A : premiers tests

Responsable : Soumia
Date : 18 novembre 2026

Le code des zombies était fourni dans le squelette. Les essais ci-dessous ont été exécutés manuellement dans le Command Center de NetLogo 7.0.4, sans obstacles. Résultats observés sur les captures des essais ; pas de campagne automatique.

| Test | Résultat observé |
|---|---|
| Création | 20 zombies ; âge initial égal à 0 pour tous. |
| Errance et âge | Déplacements observés sans humains ; âge égal à 1 après une action. |
| Vieillesse | Après placement à la durée de vie maximale puis une action : 0 zombie et 20 morts de vieillesse. |
| Poursuite | Un humain immobile à 3 patches ; après deux actions, distance égale à 2 (vitesse : 0,5 patch par action). |
| Défense certaine | Défense à 1 : zombie détruit et compteur augmenté de 1. |
| Infection certaine | Défense à 0 et infection à 1 : humain infecté et une nouvelle infection comptée. |
| Infection impossible | Défense à 0 et infection à 0 : humain sain et aucune nouvelle infection. |
| Deux zombies au contact | Défense à 1, deux passages : 0 zombie et 2 destructions, sans erreur. |

Les agents et compteurs ont été manipulés pour isoler chaque test. Ces états ne constituent pas une simulation complète et ne permettent pas de valider les invariants démographiques.

## Limites et travail restant

- Les tests ne valident pas encore tous les cas, les obstacles ni une simulation complète de 720 ticks sur plusieurs graines.
- Le test avec deux zombies ne vérifie pas que la défense cible toujours le zombie qui attaque : ce point reste à examiner avec B.
- Les appels à setup-zombies et zombie-agir restent commentés dans le fichier principal ; leur activation et le branchement de evoluer-infection dans humain-agir restent à intégrer avec B.
- Les probabilités extrêmes servent aux tests. Valeurs de départ à rétablir avant les essais normaux : proba-defense 0.3, proba-infection 0.5, portee-detection 3 ; nb-obstacles 0 pour cette itération.
