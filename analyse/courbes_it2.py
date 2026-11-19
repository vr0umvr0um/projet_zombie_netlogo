"""Courbes de l'iteration 2 : humains(t) et zombies(t).

Lit le CSV de l'experience BehaviorSpace `it2-courbes` (results/it2_courbes.csv) et trace,
pour chaque effectif, les simulations individuelles, la moyenne et l'intervalle entre le
premier et le troisieme quartile. Sauvegarde figures/it2_courbes.png.

Usage, depuis la racine du depot :
    python analyse/courbes_it2.py

Pour regenerer le CSV (NetLogo 7.0.4, 20 simulations de 720 ticks, nb-zombies = 20,
nb-obstacles = 0, reglages par defaut des curseurs,
graine = numero de simulation, donc CSV reproductible) :
    netlogo-headless --model Projet_zombies_base.nlogox --experiment it2-courbes ^
        --threads 8 --table results/it2_courbes.csv
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

RACINE = Path(__file__).resolve().parent.parent
CSV = RACINE / "results" / "it2_courbes.csv"
FIGURE = RACINE / "figures" / "it2_courbes.png"
TICKS_PAR_JOUR = 24


def lire_table_behaviorspace(chemin):
    """Lit un CSV BehaviorSpace : quelques lignes de metadonnees, puis l'en-tete."""
    lignes = chemin.read_text(encoding="utf-8").splitlines()
    debut = next(i for i, ligne in enumerate(lignes) if ligne.startswith('"[run number]"'))
    return pd.read_csv(chemin, skiprows=debut)


def preparer(donnees):
    donnees = donnees.rename(
        columns={"[run number]": "simulation", "[step]": "tick",
                 "count humains": "humains", "count zombies": "zombies"})
    donnees["jour"] = donnees["tick"] / TICKS_PAR_JOUR
    return donnees


def tracer_effectif(ax, donnees, colonne, couleur, titre):
    pivot = donnees.pivot(index="jour", columns="simulation", values=colonne)
    q1 = pivot.quantile(0.25, axis=1)
    q3 = pivot.quantile(0.75, axis=1)
    moyenne = pivot.mean(axis=1)

    ax.plot(pivot.index, pivot.values, color=couleur, alpha=0.12, linewidth=0.8)
    ax.fill_between(pivot.index, q1, q3, color=couleur, alpha=0.25,
                    label="entre le 1er et le 3e quartile")
    ax.plot(pivot.index, moyenne, color=couleur, linewidth=2.2, label="moyenne")
    ax.set_title(titre)
    ax.set_xlabel("Jour")
    ax.set_xlim(0, 30)
    ax.set_ylim(bottom=0)
    ax.grid(alpha=0.3)
    ax.legend(loc="upper right")


def resume(donnees):
    """Tableau de synthese affiche dans le terminal (jours 0, 2, 5, 10, ... 30)."""
    jours = [0, 2, 5, 10, 15, 20, 25, 30]
    lignes = []
    for jour in jours:
        instant = donnees[donnees["tick"] == jour * TICKS_PAR_JOUR]
        lignes.append({
            "jour": jour,
            "humains (moyenne)": round(instant["humains"].mean(), 1),
            "zombies (moyenne)": round(instant["zombies"].mean(), 1),
            "simulations avec humains": f"{int((instant['humains'] > 0).sum())} / {len(instant)}",
            "simulations avec zombies": f"{int((instant['zombies'] > 0).sum())} / {len(instant)}",
        })
    return pd.DataFrame(lignes)


def main():
    donnees = preparer(lire_table_behaviorspace(CSV))
    nb_simulations = donnees["simulation"].nunique()

    figure, (ax_h, ax_z) = plt.subplots(1, 2, figsize=(11, 4.2))
    tracer_effectif(ax_h, donnees, "humains", "#1f77b4", "Humains vivants")
    tracer_effectif(ax_z, donnees, "zombies", "#8c2d8c", "Zombies")
    ax_h.set_ylabel("Effectif")
    figure.suptitle(
        f"Iteration 2 : humains et zombies ({nb_simulations} simulations, "
        "20 zombies au depart, sans obstacle)")
    figure.tight_layout()

    FIGURE.parent.mkdir(exist_ok=True)
    figure.savefig(FIGURE, dpi=150)
    print(f"Figure enregistree : {FIGURE}")
    print(resume(donnees).to_string(index=False))


if __name__ == "__main__":
    main()
