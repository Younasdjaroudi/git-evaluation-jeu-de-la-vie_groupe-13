# Jeu de la vie – Groupe 13

Simulation en Python du [jeu de la vie de Conway](https://fr.wikipedia.org/wiki/Jeu_de_la_vie).
Le programme `main.py` génère une grille aléatoire ou lit une grille sur l'entrée standard, puis calcule son évolution avec des conditions aux limites fixes ou périodiques. Le résultat est écrit sous forme d'images PNG ou affiché en texte.

## Installation

Le programme utilise uniquement **Python 3** et sa bibliothèque standard : aucune dépendance externe n'est nécessaire. Les vidéos nécessitent en plus **ffmpeg** et **Gource**.

### Ubuntu ou Debian

```bash
sudo apt update
sudo apt install python3 git ffmpeg gource
```

### macOS

```bash
brew install python ffmpeg gource
```

### Windows

Installer Python depuis [python.org](https://www.python.org/downloads/) en cochant **« Add python.exe to PATH »**, puis, dans PowerShell :

```powershell
winget install Gyan.FFmpeg
winget install acaudwell.Gource
```

Sous Windows, la commande Python s'appelle souvent `py` ou `python` au lieu de `python3`. Les scripts de test utilisent `python3` : on peut les lancer depuis [WSL](https://learn.microsoft.com/fr-fr/windows/wsl/install) ou Git Bash.

### Récupérer le projet

```bash
git clone https://github.com/Younasdjaroudi/git-evaluation-jeu-de-la-vie_groupe-13.git
cd git-evaluation-jeu-de-la-vie_groupe-13
```

## Exécution

Toutes les commandes se lancent depuis la racine du dépôt.

### Sans option : grille aléatoire et images

Le programme utilise les valeurs par défaut (grille 10×10, graine 42, 20 itérations) et écrit 21 images dans `outputs`, de `grid_0000.png` à `grid_0020.png` :

```bash
$ python3 main.py
Generation of 21 images in directory outputs
```

### Grille aléatoire personnalisée

```bash
$ python3 main.py -n 50 -m 200 -s 4200
Generation of 201 images in directory outputs
```

### Lecture d'une grille sur l'entrée standard

La première ligne contient la taille de la grille, puis une ligne par rangée avec des cellules `0` (morte) ou `1` (vivante) séparées par des espaces :

```text
3
1 0 1
0 0 1
1 0 1
```

Avec la sortie texte, seule la dernière itération demandée est affichée :

```bash
$ cat tests/matrix3/input.txt | python3 main.py -m 1 -t text
iteration: 1
0 1 0
0 0 1
0 1 0
```

Avec les conditions aux limites périodiques (`-p`), les bords opposés sont reliés :

```bash
$ cat tests/matrix3/input.txt | python3 main.py -m 1 -p -t text
iteration: 1
0 0 0
0 0 0
0 0 0
```

### Gestion des erreurs

Une grille invalide, une taille non positive, une itération négative ou un type de sortie inconnu provoquent un message sur la sortie d'erreur et un code de sortie différent de `0` :

```bash
$ echo "" | python3 main.py
Erreur : grille invalide : la grille est vide
$ echo $?
1
```

### Tests

```bash
sh check_script_options.sh   # Nb test success: 6 / 6
sh check_tests.sh            # Nb test success: 82 / 82
```

## Arguments

| Option courte | Option longue | Description | Valeur par défaut |
|---|---|---|---|
| `-n N` | `--nb_cells N` | nombre de cellules par côté pour une grille aléatoire (entier > 0) | `10` |
| `-m N` | `--max_iterations N` | numéro de la dernière itération à calculer (entier ≥ 0) | `20` |
| `-s N` | `--seed N` | graine du générateur aléatoire (entier) | `42` |
| `-o DOSSIER` | `--output_directory DOSSIER` | dossier dans lequel écrire les images (créé s'il n'existe pas) | `outputs` |
| `-t TYPE` | `--output_type TYPE` | type de sortie : `image` ou `text` | `image` |
| `-p` | `--periodic` | active les conditions aux limites périodiques | désactivée |
| `-h` | `--help` | affiche l'aide du programme | — |

La génération initiale porte le numéro `0` : avec `-m 20`, le programme calcule 21 générations. Lorsqu'une grille est fournie sur l'entrée standard, les options `-n` et `-s` n'ont pas d'effet.
