"""Calibrage de proba-defense (iteration 2) : critere de la decision initiale.

Lit le CSV de l'experience BehaviorSpace `it2-calibration-defense`
(results/it2_calibration_defense.csv : proba-defense de 0 a 0,5 par pas de 0,025, sans obstacle
et avec 30 obstacles, 100 graines par valeur, 20 zombies, autres curseurs par defaut) et, pour
chaque valeur, calcule :
  - la part des simulations ou il reste des zombies a 720 ticks (seuil : au moins 50 %) ;
  - la part des simulations ou tous les humains sont morts (seuil : au plus 10 %) ;
  - le nombre moyen d'humains a 720 ticks (sur 100 au depart).
Affiche le tableau et sauvegarde figures/it2_calibration_defense.png.

Depuis que la colonie protege ses habitants (seuls les humains en sortie sont attaques), le critere
est rempli pour toutes les valeurs : il ne departage plus. 0,125 est gardee car elle laisse des
zombies dans plus de 90 % des simulations (avec et sans obstacles) sans saturer la survie, ce qui
laisse de la marge pour comparer les strategies de ravitaillement.

Usage, depuis la racine du depot :
    python analyse/calibration_defense.py

Pour regenerer le CSV (NetLogo 7.0.4, graine = numero de la repetition, donc reproductible) :
    netlogo-headless --model Projet_zombies_base.nlogox --experiment it2-calibration-defense ^
        --threads 8 --table results/it2_calibration_defense.csv
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

RACINE = Path(__file__).resolve().parent.parent
CSV = RACINE / "results" / "it2_calibration_defense.csv"
FIGURE = RACINE / "figures" / "it2_calibration_defense.png"
SEUIL_ZOMBIES = 0.5   # part minimale de simulations avec des zombies a 720 ticks
SEUIL_EXTINCTION = 0.1  # part maximale de simulations sans humain a 720 ticks


def lire_table_behaviorspace(chemin):
    """Lit un CSV BehaviorSpace : quelques lignes de metadonnees, puis l'en-tete."""
    lignes = chemin.read_text(encoding="utf-8").splitlines()
    debut = next(i for i, ligne in enumerate(lignes) if ligne.startswith('"[run number]"'))
    return pd.read_csv(chemin, skiprows=debut)


def synthese(donnees):
    donnees = donnees.assign(
        avec_zombies=donnees["count zombies"] > 0,
        humains_eteints=donnees["count humains"] == 0,
    )
    table = donnees.groupby([donnees["nb-obstacles"], donnees["proba-defense"].round(3)]).agg(
        simulations=("count humains", "size"),
        humains_moyenne=("count humains", "mean"),
        part_avec_zombies=("avec_zombies", "mean"),
        part_humains_eteints=("humains_eteints", "mean"),
        invariants=("invariants-ok?", "all"),
    )
    table["critere"] = ((table["part_avec_zombies"] >= SEUIL_ZOMBIES)
                        & (table["part_humains_eteints"] <= SEUIL_EXTINCTION))
    return table


def main():
    table = synthese(lire_table_behaviorspace(CSV))

    figure, ax = plt.subplots(figsize=(8, 4.6))
    styles = {0: "-", 30: ":"}
    for obstacles, sous_table in table.groupby(level="nb-obstacles"):
        x = sous_table.index.get_level_values("proba-defense")
        trait = styles.get(obstacles, "-.")
        ax.plot(x, sous_table["part_avec_zombies"], trait, marker="o", markersize=3, color="#8c2d8c",
                label=f"avec des zombies a 720 ticks ({obstacles} obstacles)")
        ax.plot(x, sous_table["part_humains_eteints"], trait, marker="o", markersize=3, color="#1f77b4",
                label=f"humains eteints ({obstacles} obstacles)")
        ax.plot(x, sous_table["humains_moyenne"] / 100, trait, color="#2ca02c",
                label=f"humains a 720 ticks / 100 ({obstacles} obstacles)")
    ax.axhline(SEUIL_ZOMBIES, color="#8c2d8c", linestyle="--", linewidth=1,
               label="seuil : au moins 50 % avec zombies")
    ax.axhline(SEUIL_EXTINCTION, color="#1f77b4", linestyle="--", linewidth=1,
               label="seuil : au plus 10 % d'extinction")
    ax.axvline(0.125, color="grey", linewidth=1)
    ax.set_xlabel("proba-defense (trait vertical : 0,125 retenue)")
    ax.set_ylabel(f"Part des {int(table['simulations'].iloc[0])} simulations")
    ax.set_ylim(-0.02, 1.02)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=7, loc="lower right", bbox_to_anchor=(1, 0.12), ncol=2)
    ax.set_title("Calibrage de proba-defense (20 zombies, colonie protegee)")
    figure.tight_layout()

    FIGURE.parent.mkdir(exist_ok=True)
    figure.savefig(FIGURE, dpi=150)
    print(f"Figure enregistree : {FIGURE}")
    print(table.round(3).to_string())


if __name__ == "__main__":
    main()
