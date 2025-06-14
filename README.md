# todoproject

# SETUP LOCAL

# LINUX
# Clone le projet
git clone https://github.com/Raneult0708/todoproject.git
cd PIL1_2425_1

# Créer un environnement virtuel
python3 -m venv env 
source env/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Preparation du fichier .env
Créer un fichier .env selon le format du fichier env.example en suivant les instructions qu'il contient

# Lancer le serveur
python manage.py runserver


# WINDOWS

# Clone le projet
git clone https://github.com/Raneult0708/todoproject.git
cd PIL1_2425_1

# Créer un environnement virtuel
python -m venv env 
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\env\Scripts\Activate.ps1


# Installer les dépendances
pip install -r requirements.txt

# Preparation du fichier .env
Créer un fichier .env selon le format du fichier env.example en suivant les instructions qu'il contient

# Lancer le serveur
python manage.py runserver

# Requète de création de votre base de données
CREATE DATABASE tododb;
CREATE USER 'todo_user'@'localhost' IDENTIFIED BY 'motdepassefort';
GRANT ALL PRIVILEGES ON tododb.* TO 'todo_user'@'localhost';
FLUSH PRIVILEGES;