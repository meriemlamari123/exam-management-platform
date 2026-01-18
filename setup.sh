#!/bin/bash

# Créer le répertoire de configuration Streamlit
mkdir -p ~/.streamlit/

# Créer le fichier de configuration
echo "\
[general]\n\
email = \"votre.email@example.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml

# Initialiser la base de données
python database/init_db.py
