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
