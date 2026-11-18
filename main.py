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


def error(message):
    """Écrire message sur STDERR et quitter avec le code 1."""
    print(f"Erreur : {message}", file=sys.stderr)
    sys.exit(1)


def generate_random_grid(nb_cells, seed):
    """Créer une grille carrée aléatoire reproductible à partir de seed."""
    rng = random.Random(seed)
    return [[rng.choice([0, 1]) for _ in range(nb_cells)] for _ in range(nb_cells)]


def parse_grid(text):
    """Convertir le texte lu sur STDIN en grille, ou lever ValueError."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        raise ValueError("la grille est vide")

    try:
        size = int(lines[0])
    except ValueError:
        raise ValueError(f"la taille « {lines[0]} » n'est pas un entier") from None
    if size <= 0:
        raise ValueError(f"la taille doit être strictement positive (reçu : {size})")

    rows = lines[1:]
    if len(rows) != size:
        raise ValueError(f"{size} lignes attendues, {len(rows)} reçues")

    grid = []
    for row_number, row in enumerate(rows, start=1):
        cells = row.split()
        if len(cells) != size:
            raise ValueError(
                f"ligne {row_number} : {size} cellules attendues, {len(cells)} reçues")
        for cell in cells:
            if cell not in ("0", "1"):
                raise ValueError(f"ligne {row_number} : cellule invalide « {cell} » (0 ou 1)")
        grid.append([int(cell) for cell in cells])
    return grid


def read_grid_from_stdin():
    """Lire la grille initiale sur STDIN si une entrée est redirigée, sinon None."""
    if sys.stdin is None or sys.stdin.isatty():
        return None
    return parse_grid(sys.stdin.read())


def count_neighbors(grid, row, col, periodic):
    """Compter les voisines vivantes de la cellule (row, col)."""
    size = len(grid)
    count = 0
    for d_row in (-1, 0, 1):
        for d_col in (-1, 0, 1):
            if d_row == 0 and d_col == 0:
                continue
            r, c = row + d_row, col + d_col
            if periodic:
                r, c = r % size, c % size
            elif not (0 <= r < size and 0 <= c < size):
                continue
            count += grid[r][c]
    return count


def next_generation(grid, periodic):
    """Calculer la génération suivante sans modifier la grille courante."""
    size = len(grid)
    new_grid = []
    for row in range(size):
        new_row = []
        for col in range(size):
            neighbors = count_neighbors(grid, row, col, periodic)
            alive = grid[row][col] == 1
            new_row.append(1 if neighbors == 3 or (alive and neighbors == 2) else 0)
        new_grid.append(new_row)
    return new_grid


def format_grid(grid, iteration):
    """Mettre en forme une grille pour la sortie texte."""
    lines = [f"iteration: {iteration}"]
    lines += [" ".join(str(cell) for cell in row) for row in grid]
    return "\n".join(lines)


def write_image(grid, directory, iteration):
    """Écrire l'image PNG d'une génération dans directory."""
    write_grid(matrix=grid, filename=Path(directory) / f"grid_{iteration:04d}.png")


def run_image(grid, max_iterations, periodic, directory):
    """Écrire une image par génération, de 0 à max_iterations."""
    try:
        Path(directory).mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        error(f"impossible de créer le dossier « {directory} » : {exc.strerror}")
    write_image(grid, directory, 0)
    for iteration in range(1, max_iterations + 1):
        grid = next_generation(grid, periodic)
        write_image(grid, directory, iteration)
    print(f"Generation of {max_iterations + 1} images in directory {directory}")


def run_text(grid, max_iterations, periodic):
    """Afficher sur STDOUT uniquement la dernière génération demandée."""
    for _ in range(max_iterations):
        grid = next_generation(grid, periodic)
    print(format_grid(grid, max_iterations))


def main():
    args = parse_arguments()

    try:
        grid = read_grid_from_stdin()
    except ValueError as exc:
        error(f"grille invalide : {exc}")
    if grid is None:
        grid = generate_random_grid(args.nb_cells, args.seed)

    if args.output_type == "text":
        run_text(grid, args.max_iterations, args.periodic)
    else:
        run_image(grid, args.max_iterations, args.periodic, args.output_directory)


if __name__ == "__main__":
    main()
