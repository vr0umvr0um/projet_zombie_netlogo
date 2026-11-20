"""Iteration 3 (partie C) : zombies dans l'environnement, courbes et carte de densite.

Lit les CSV des experiences BehaviorSpace :
  - results/it3_courbes.csv (it3-courbes : 20 graines, 20 zombies, 30 obstacles, mesures a chaque
    tick : humains, zombies, zombies immobiles, zombies sur un obstacle, invariants) ;
  - results/it3_densite.csv (it3-densite : memes reglages, a 720 ticks, carte-densite-zombies et
    carte-types, listes des patches dans l'ordre de sort patches : ligne par ligne, de haut en bas,
    de gauche a droite).
Ecrit figures/it3_courbes.png et figures/it3_carte_densite.png, et affiche un resume.

Usage, depuis la racine du depot :
    python analyse/carte_densite_it3.py

Pour regenerer les CSV (NetLogo 7.0.4, graine = numero de la simulation) :
    netlogo-headless --model Projet_zombies_base.nlogox --experiment it3-courbes --threads 8 --table results/it3_courbes.csv
    netlogo-headless --model Projet_zombies_base.nlogox --experiment it3-densite --threads 8 --table results/it3_densite.csv
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap

RACINE = Path(__file__).resolve().parent.parent
COURBES = RACINE / "results" / "it3_courbes.csv"
DENSITE = RACINE / "results" / "it3_densite.csv"
FIG_COURBES = RACINE / "figures" / "it3_courbes.png"
FIG_CARTE = RACINE / "figures" / "it3_carte_densite.png"
COTE = 33  # monde de -16 a 16
TICKS_PAR_JOUR = 24


def lire_table(chemin):
    lignes = chemin.read_text(encoding="utf-8").splitlines()
    debut = next(i for i, ligne in enumerate(lignes) if ligne.startswith('"[run number]"'))
    return pd.read_csv(chemin, skiprows=debut)


def liste_netlogo(texte):
    return np.array([float(v) for v in texte.strip("[]").split()])


def courbes():
    d = lire_table(COURBES)
    d["jour"] = d["[step]"] / TICKS_PAR_JOUR
    d["part immobiles"] = np.where(d["count zombies"] > 0, d["nb-zombies-immobiles"] / d["count zombies"].clip(lower=1), 0)
    moyenne = d.groupby("jour")[["count humains", "count zombies", "nb-zombies-immobiles", "part immobiles"]].mean()

    figure, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
    for _, run in d.groupby("[run number]"):
        ax1.plot(run["jour"], run["count zombies"], color="#8c2d8c", alpha=0.15, linewidth=0.8)
    ax1.plot(moyenne.index, moyenne["count zombies"], color="#8c2d8c", linewidth=2, label="zombies (moyenne)")
    ax1.plot(moyenne.index, moyenne["nb-zombies-immobiles"], color="#d62728", linewidth=2, label="zombies immobiles (moyenne)")
    ax1.set_xlabel("Jour")
    ax1.set_ylabel("Effectif")
    ax1.set_title("Zombies et zombies immobiles")
    ax1.legend(fontsize=8)
    ax1.grid(alpha=0.3)

    ax2.plot(moyenne.index, 100 * moyenne["part immobiles"], color="#d62728", linewidth=1.5)
    ax2.axhline(5, color="black", linestyle="--", linewidth=1, label="seuil : 5 %")
    ax2.set_xlabel("Jour")
    ax2.set_ylabel("% de zombies immobiles")
    ax2.set_ylim(0, 10)
    ax2.set_title("Part de zombies immobiles (moyenne des 20 graines)")
    ax2.legend(fontsize=8)
    ax2.grid(alpha=0.3)
    figure.suptitle("Iteration 3 : 20 simulations, 20 zombies, 30 obstacles")
    figure.tight_layout()
    figure.savefig(FIG_COURBES, dpi=150)

    fin = d[d["[step]"] == d["[step]"].max()]
    invariants = d["invariants-ok?"].astype(str).str.lower().eq("true").all()
    print(f"Figure enregistree : {FIG_COURBES}")
    print(f"invariants vrais a chaque tick : {invariants} ; zombies sur un obstacle (max) : {d['nb-zombies-sur-obstacle'].max()}")
    print(f"part de zombies immobiles : moyenne {100 * d.loc[d['count zombies'] > 0, 'part immobiles'].mean():.3f} %, "
          f"maximum {100 * d['part immobiles'].max():.1f} %")
    print(f"a 720 ticks : {fin['count humains'].mean():.1f} humains et {fin['count zombies'].mean():.1f} zombies en moyenne, "
          f"zombies presents dans {(fin['count zombies'] > 0).sum()} simulations sur {len(fin)}")


def carte():
    d = lire_table(DENSITE).sort_values("[run number]")
    densites = np.stack([liste_netlogo(t).reshape(COTE, COTE) for t in d["carte-densite-zombies"]])
    types = np.stack([liste_netlogo(t).reshape(COTE, COTE) for t in d["carte-types"]])
    etendue = [-16.5, 16.5, -16.5, 16.5]  # premiere ligne = max-pycor : imshow origin "upper"

    figure, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))
    image = ax1.imshow(densites[0], cmap="magma_r", extent=etendue)
    obstacles = np.ma.masked_where(types[0] != 1, types[0])
    ax1.imshow(obstacles, cmap=ListedColormap(["#4d4d4d"]), extent=etendue)
    for code, couleur, nom in ((2, "#2ca02c", "ravitaillement"), (3, "#1f77b4", "colonie")):
        lignes, colonnes = np.nonzero(types[0] == code)
        ax1.scatter(colonnes - 16, 16 - lignes, s=40 if code == 3 else 18, marker="s" if code == 3 else "o",
                    facecolors="none", edgecolors=couleur, linewidths=1.5, label=nom)
    ax1.set_title(f"Graine {int(d['[run number]'].iloc[0])} : passages de zombies par patch\n(gris : obstacles)")
    ax1.legend(fontsize=7, loc="lower left")
    figure.colorbar(image, ax=ax1, fraction=0.046, label="zombies x ticks")

    moyenne = densites.mean(axis=0)
    image2 = ax2.imshow(moyenne, cmap="magma_r", extent=etendue)
    ax2.set_title(f"Moyenne des {len(densites)} graines\n(obstacles et colonies differents d'une graine a l'autre)")
    figure.colorbar(image2, ax=ax2, fraction=0.046, label="zombies x ticks")
    for ax in (ax1, ax2):
        ax.set_xlabel("pxcor")
        ax.set_ylabel("pycor")
    figure.tight_layout()
    figure.savefig(FIG_CARTE, dpi=150)

    # Bords : part des passages sur la couronne exterieure (1 patch) par rapport a sa part de la surface
    bord = np.zeros((COTE, COTE), dtype=bool)
    bord[0, :] = bord[-1, :] = bord[:, 0] = bord[:, -1] = True
    part_bord = densites[:, bord].sum() / densites.sum()
    sur_obstacle = (densites * (types == 1)).sum()
    print(f"Figure enregistree : {FIG_CARTE}")
    print(f"passages sur un obstacle : {int(sur_obstacle)} (doit valoir 0)")
    print(f"part des passages sur le bord de la carte : {100 * part_bord:.1f} % (part de la surface : {100 * bord.mean():.1f} %)")


if __name__ == "__main__":
    FIG_COURBES.parent.mkdir(exist_ok=True)
    courbes()
    carte()
