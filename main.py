"""Simulation du jeu de la vie de Conway."""

import argparse
import random
import sys
from pathlib import Path

from lib import write_grid


def positive_int(value):
    """Convertir value en entier strictement positif pour argparse."""
    number = int_value(value)
    if number <= 0:
        raise argparse.ArgumentTypeError(f"{value} n'est pas un entier strictement positif")
    return number


def non_negative_int(value):
    """Convertir value en entier positif ou nul pour argparse."""
    number = int_value(value)
    if number < 0:
        raise argparse.ArgumentTypeError(f"{value} n'est pas un entier positif ou nul")
    return number


def int_value(value):
    """Convertir value en entier ou lever une erreur argparse."""
    try:
        return int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} n'est pas un entier") from None


def parse_arguments(argv=None):
    """Lire et valider les arguments de la ligne de commande."""
    parser = argparse.ArgumentParser(description="Simulation du jeu de la vie de Conway.")
    parser.add_argument("-n", "--nb_cells", type=positive_int, default=10,
                        help="nombre de cellules par côté pour une grille aléatoire (défaut : 10)")
    parser.add_argument("-m", "--max_iterations", type=non_negative_int, default=20,
                        help="numéro de la dernière itération à calculer (défaut : 20)")
    parser.add_argument("-s", "--seed", type=int_value, default=42,
                        help="graine du générateur aléatoire (défaut : 42)")
    parser.add_argument("-o", "--output_directory", default="outputs",
                        help="dossier dans lequel écrire les images (défaut : outputs)")
    parser.add_argument("-t", "--output_type", choices=["image", "text"], default="image",
                        help="type de sortie : image ou text (défaut : image)")
    parser.add_argument("-p", "--periodic", action="store_true",
                        help="active les conditions aux limites périodiques")
    return parser.parse_args(argv)


def generate_random_grid(nb_cells, seed):
    """Créer une grille carrée aléatoire reproductible à partir de seed."""
    rng = random.Random(seed)
    return [[rng.choice([0, 1]) for _ in range(nb_cells)] for _ in range(nb_cells)]


def write_image(grid, directory, iteration):
    """Écrire l'image PNG d'une génération dans directory."""
    write_grid(matrix=grid, filename=Path(directory) / f"grid_{iteration:04d}.png")


def main():
    args = parse_arguments()
    grid = generate_random_grid(args.nb_cells, args.seed)
    Path(args.output_directory).mkdir(parents=True, exist_ok=True)
    write_image(grid, args.output_directory, 0)


if __name__ == "__main__":
    main()
