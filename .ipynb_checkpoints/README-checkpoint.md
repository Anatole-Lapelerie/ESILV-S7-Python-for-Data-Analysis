# Prédiction du temps de transcodage des vidéos

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Devoir 2021 de Python for Data Analysis à l'ESILV pour le Semestre 7 par **Anatole Lapelerie** incluant :
1. Un powerpoint expliquant les tenants et aboutissants du problème ;
2. Un code en python avec data-visualisation et modélisation ;
3. Une API Django.

Les datasets analysés proviennent du *Machine Learning Repository* de l'UCI : [Online Video Characteristics and Transcoding Time Dataset Data Set](https://archive.ics.uci.edu/ml/datasets/Online+Video+Characteristics+and+Transcoding+Time+Dataset) et sont présents dans un dossier `input` ignoré par un fichier `.gitignore`. Pour pouvoir exécuter le code, il faudra placer les datasets décompressés dans leur format original dans un dossier `input` créé en local à la racine du projet. On importe ainsi :
* Le premier dataset : `youtube_videos.tsv`, contenant 10 colonnes de caractéristiques fondamentales de vidéos YouTube ;
* Le second dataset : `transcoding_mesurment.tsv`, contenant 20 colonnes de données liées au transcodage de vidéos.