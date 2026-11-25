"""Iteration 4 (partie C) : comparaison des trois strategies de ravitaillement.

Lit le CSV de l'experience BehaviorSpace `it4-comparaison` (results/it4_comparaison.csv :
strategie individuelle, groupe fixe et groupe adaptatif, taille-groupe = 5, 20 zombies, 30 obstacles,
100 graines par strategie, graine = numero de repetition : les trois strategies voient les memes
graines). Affiche, par strategie, les moyennes et un intervalle de confiance a 95 % de la proportion
de survivants, et sauvegarde figures/it4_comparaison.png.

Usage, depuis la racine du depot :
    python analyse/comparaison_strategies_it4.py [chemin du CSV]

Pour regenerer le CSV (NetLogo 7.0.4) :
    netlogo-headless --model Projet_zombies_base.nlogox --experiment it4-comparaison --threads 8 --table results/it4_comparaison.csv

Tant que les parties A et B de l'iteration 4 ne sont pas ecrites, les trois strategies donnent les
memes resultats (les groupes ne se forment pas) : la colonne plus_grand_groupe le montre.
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RACINE = Path(__file__).resolve().parent.parent
CSV = Path(sys.argv[1]) if len(sys.argv) > 1 else RACINE / "results" / "it4_comparaison.csv"
FIGURE = RACINE / "figures" / "it4_comparaison.png"
ORDRE = ["individuelle", "groupe fixe", "groupe adaptatif"]


def lire_table(chemin):
    lignes = chemin.read_text(encoding="utf-8").splitlines()
    debut = next(i for i, ligne in enumerate(lignes) if ligne.startswith('"[run number]"'))
    return pd.read_csv(chemin, skiprows=debut)


def main():
    d = lire_table(CSV)
    d["part_retours_infectes"] = np.where(d["nb-retours"] > 0, d["nb-retours-infectes"] / d["nb-retours"].clip(lower=1), 0)
    groupes = d.groupby("strategie")
    table = groupes.agg(
        simulations=("count humains", "size"),
        invariants=("invariants-ok?", lambda s: s.astype(str).str.lower().eq("true").all()),
        survivants=("proportion-survivants", "mean"),
        survivants_ecart_type=("proportion-survivants", "std"),
        morts_attaque=("nb-morts-attaque", "mean"),
        morts_famine=("nb-morts-famine", "mean"),
        morts_infection=("nb-morts-infection", "mean"),
        departs=("nb-departs", "mean"),
        sorties_de_groupe=("nb-departs-groupes", "mean"),
        part_retours_infectes=("part_retours_infectes", "mean"),
        nourriture_par_sortie=("nourriture-par-sortie", "mean"),
        plus_grand_groupe=("taille-max-groupe-observee", "max"),
    ).reindex([s for s in ORDRE if s in groupes.groups])
    table["ic95_survivants"] = 1.96 * table["survivants_ecart_type"] / np.sqrt(table["simulations"])

    # Ecart apparie a la strategie individuelle (memes graines) : plus precis qu'une difference de moyennes.
    if "individuelle" in groupes.groups:
        base = d[d["strategie"] == "individuelle"].set_index("[run number]")
        base = base.assign(graine=((base.index - 1) % 100) + 1).set_index("graine")["proportion-survivants"]
        for s in table.index:
            autre = d[d["strategie"] == s]
            autre = autre.assign(graine=((autre["[run number]"] - 1) % 100) + 1).set_index("graine")["proportion-survivants"]
            ecart = (autre - base).dropna()
            table.loc[s, "ecart_vs_individuelle"] = ecart.mean()
            table.loc[s, "ic95_ecart"] = 1.96 * ecart.std() / np.sqrt(len(ecart)) if len(ecart) > 1 else np.nan

    figure, axes = plt.subplots(1, 3, figsize=(12, 4))
    donnees = [d.loc[d["strategie"] == s, "proportion-survivants"] for s in table.index]
    axes[0].boxplot(donnees, tick_labels=table.index)
    axes[0].set_title("Proportion de survivants a 720 ticks")
    axes[1].bar(table.index, table["part_retours_infectes"], color="#ff7f0e")
    axes[1].set_title("Part des retours qui ramenent un infecte")
    axes[2].bar(table.index, table["nourriture_par_sortie"], color="#2ca02c")
    axes[2].set_title("Nourriture nette par humain parti")
    for ax in axes:
        ax.tick_params(axis="x", labelrotation=15)
        ax.grid(alpha=0.3, axis="y")
    figure.suptitle(f"Iteration 4 : comparaison des strategies ({int(table['simulations'].iloc[0])} graines, 20 zombies, 30 obstacles)")
    figure.tight_layout()
    FIGURE.parent.mkdir(exist_ok=True)
    figure.savefig(FIGURE, dpi=150)
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", 30)
    print(table.round(3).T.to_string())
    print(f"\nFigure enregistree : {FIGURE}")
    if table["plus_grand_groupe"].max() <= 1:
        print("ATTENTION : aucun groupe de plus d'un humain ; les parties A et B de l'iteration 4 ne sont pas encore ecrites.")


if __name__ == "__main__":
    main()
