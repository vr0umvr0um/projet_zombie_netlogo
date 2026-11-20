"""Validation des reglages : chaque curseur est balaye seul autour de sa valeur par defaut.

Deux series, 100 graines par valeur (graine = numero de repetition, donc reproductible) :
  - modele complet (20 zombies, 30 obstacles) : tous les curseurs du modele ;
  - sans zombie (30 obstacles) : les curseurs de l'iteration 1 (environnement, colonies, sorties).
Les autres curseurs restent a leur valeur par defaut. Chaque simulation s'arrete si invariants-ok?
devient faux (exitCondition) : ticks < 720 signale donc une violation.

Pour chaque valeur : invariants vrais a chaque tick, humains a 720 ticks (sur 100), part des
simulations avec des zombies a 720 ticks, part des simulations ou les humains sont eteints, morts
par cause, naissances, sorties terminees et deficitaires.

Usage, depuis la racine du depot :
    python analyse/validation_reglages.py --lancer     # lance les simulations (environ 30 minutes)
    python analyse/validation_reglages.py              # synthese seulement, a partir des tables

Les tables brutes vont dans results/validation_reglages/ (non versionnees, regenerables) et la
synthese dans results/validation_reglages.csv.
"""
import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

import pandas as pd

RACINE = Path(__file__).resolve().parent.parent
MODELE = RACINE / "Projet_zombies_base.nlogox"
TABLES = RACINE / "results" / "validation_reglages"
SYNTHESE = RACINE / "results" / "validation_reglages.csv"
NETLOGO = Path("C:/Program Files/NetLogo 7.0.4")
GRAINES = 100

DEFAUTS = {
    "nb-points-ravitaillement": 16, "nb-obstacles": 30, "stock-initial-colonie": 100,
    "stock-initial-point": 150, "regeneration-point": 0.5, "s-min": 80, "capacite-transport": 50,
    "portee-detection": 3, "proba-infection": 0.5, "proba-defense": 0.125, "delai-transformation": 48,
    "proba-mort-infection": 0.3, "duree-vie-zombie": 480, "consommation-jour": 0.25,
    "taux-naissance": 0.01, "seuil-naissance": 80, "proba-mort-attaque": 0.1,
    "gain-attaque-zombie": 48, "nb-zombies": 20,
}
VALEURS = {
    "nb-points-ravitaillement": [8, 12, 16, 24], "nb-obstacles": [0, 15, 30, 60],
    "stock-initial-colonie": [50, 100, 150], "stock-initial-point": [100, 150, 200],
    "regeneration-point": [0.25, 0.5, 1], "s-min": [40, 80, 120], "capacite-transport": [25, 50, 75],
    "portee-detection": [2, 3, 5], "proba-infection": [0.25, 0.5, 0.75], "proba-defense": [0, 0.125, 0.3],
    "delai-transformation": [24, 48, 96], "proba-mort-infection": [0.1, 0.3, 0.5],
    "duree-vie-zombie": [240, 480, 720], "consommation-jour": [0.125, 0.25, 0.5],
    "taux-naissance": [0.005, 0.01, 0.02], "seuil-naissance": [40, 80, 120],
    "proba-mort-attaque": [0, 0.1, 0.3], "gain-attaque-zombie": [0, 48, 96], "nb-zombies": [0, 10, 20, 40],
}
CURSEURS_IT1 = ["nb-points-ravitaillement", "nb-obstacles", "stock-initial-colonie", "stock-initial-point",
                "regeneration-point", "s-min", "capacite-transport", "consommation-jour",
                "taux-naissance", "seuil-naissance"]
METRIQUES = ["ticks", "invariants-ok?", "count humains", "count zombies", "nb-morts-attaque",
             "nb-morts-famine", "nb-morts-infection", "nb-transformations", "nb-zombies-detruits",
             "nb-zombies-vieux", "nb-naissances", "nb-sorties-deficitaires", "nb-sorties-terminees"]


def series():
    """(nom de l'experience, curseur balaye, curseurs fixes)."""
    for curseur in VALEURS:
        yield f"z_{curseur}", curseur, {"nb-zombies": 20, "nb-obstacles": 30}
    for curseur in CURSEURS_IT1:
        yield f"s_{curseur}", curseur, {"nb-zombies": 0, "nb-obstacles": 30}


def experience_xml(nom, curseur, fixes):
    valeurs = "".join(f'<value value="{v}"></value>' for v in VALEURS[curseur])
    constantes = "".join(
        f'        <enumeratedValueSet variable="{k}"><value value="{v}"></value></enumeratedValueSet>\n'
        for k, v in fixes.items() if k != curseur)
    metriques = "".join(f"        <metric>{m}</metric>\n" for m in METRIQUES)
    return f"""    <experiment name="{nom}" repetitions="{GRAINES}" sequentialRunOrder="true" runMetricsEveryStep="false" timeLimit="720">
      <setup>random-seed (((behaviorspace-run-number - 1) mod {GRAINES}) + 1)
setup</setup>
      <go>go</go>
      <exitCondition>not invariants-ok?</exitCondition>
      <metrics>
{metriques}      </metrics>
      <constants>
{constantes}        <enumeratedValueSet variable="{curseur}">{valeurs}</enumeratedValueSet>
      </constants>
    </experiment>
"""


def lancer(threads):
    """Copie le modele dans un dossier temporaire, y ajoute les experiences et les lance."""
    TABLES.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as dossier:
        dossier = Path(dossier)
        for fichier in RACINE.glob("*.nls"):
            shutil.copy(fichier, dossier)
        texte = MODELE.read_text(encoding="utf-8")
        ajout = "".join(experience_xml(*s) for s in series())
        (dossier / "modele.nlogox").write_text(texte.replace("</experiments>", ajout + "  </experiments>"),
                                               encoding="utf-8")
        java = NETLOGO / "runtime" / "bin" / "java"
        for nom, _, _ in series():
            table = TABLES / f"{nom}.csv"
            print(f"{nom} ...", flush=True)
            subprocess.run([str(java), "-Xmx6g", "-cp", str(NETLOGO / "app" / "*"), "org.nlogo.headless.Main",
                            "--model", "modele.nlogox", "--experiment", nom, "--threads", str(threads),
                            "--table", str(table)], cwd=dossier, check=True)


def lire_table(chemin):
    lignes = chemin.read_text(encoding="utf-8").splitlines()
    debut = next(i for i, ligne in enumerate(lignes) if ligne.startswith('"[run number]"'))
    return pd.read_csv(chemin, skiprows=debut)


def synthese():
    lignes = []
    for nom, curseur, _ in series():
        donnees = lire_table(TABLES / f"{nom}.csv")
        for valeur, g in donnees.groupby(curseur):
            lignes.append({
                "serie": "sans zombie" if nom.startswith("s_") else "complet",
                "curseur": curseur,
                "valeur": valeur,
                "defaut": abs(valeur - DEFAUTS[curseur]) < 1e-9,
                "simulations": len(g),
                "invariants_ok": bool((g["invariants-ok?"].astype(str).str.lower() == "true").all()
                                      and (g["ticks"] >= 720).all()),
                "humains_720": g["count humains"].mean(),
                "humains_min": g["count humains"].min(),
                "part_avec_zombies": (g["count zombies"] > 0).mean(),
                "part_humains_eteints": (g["count humains"] == 0).mean(),
                "morts_famine": g["nb-morts-famine"].mean(),
                "morts_attaque": g["nb-morts-attaque"].mean(),
                "morts_infection": g["nb-morts-infection"].mean(),
                "naissances": g["nb-naissances"].mean(),
                "sorties": g["nb-sorties-terminees"].mean(),
                "sorties_deficitaires": int(g["nb-sorties-deficitaires"].sum()),
                "zombies_vieux": g["nb-zombies-vieux"].mean(),
                "zombies_detruits": g["nb-zombies-detruits"].mean(),
            })
    table = pd.DataFrame(lignes)
    table.round(3).to_csv(SYNTHESE, index=False)
    pd.set_option("display.width", 250)
    pd.set_option("display.max_rows", 200)
    colonnes = ["serie", "curseur", "valeur", "defaut", "invariants_ok", "humains_720", "humains_min",
                "part_avec_zombies", "part_humains_eteints", "morts_famine", "morts_attaque", "naissances",
                "sorties_deficitaires"]
    print(table[colonnes].round(2).to_string(index=False))
    print(f"\nSynthese enregistree : {SYNTHESE}")


if __name__ == "__main__":
    arguments = argparse.ArgumentParser()
    arguments.add_argument("--lancer", action="store_true", help="lancer les simulations avant la synthese")
    arguments.add_argument("--threads", type=int, default=8)
    options = arguments.parse_args()
    if options.lancer:
        lancer(options.threads)
    synthese()
