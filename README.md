# Prédiction du temps de transcodage des vidéos

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Devoir 2021 de Python for Data Analysis à l'ESILV pour le Semestre 7 par Marwan Laroussi et Anatole Lapelerie incluant :
1. Un powerpoint expliquant les tenants et aboutissants du problème ;
2. Un code en Python avec data-visualisation et modélisation ;
3. Une API Flask.

On utilise deux datasets provenant du *Machine Learning Repository* de l'UCI, regroupés sour la référence [Online Video Characteristics and Transcoding Time Dataset Data Set](https://archive.ics.uci.edu/ml/datasets/Online+Video+Characteristics+and+Transcoding+Time+Dataset). Ces datasets sont les suivants :
* Le premier dataset : `youtube_videos.tsv`, contenant 10 colonnes de caractéristiques diverses de vidéos YouTube ;
* Le second dataset : `transcoding_mesurment.tsv`, contenant 20 colonnes de données relatives au transcodage de vidéos issues du premier dataset, mené sur une machine Intel i7-3720QM CPU grâce au logiciel FFmpeg 4.

----

## Installation

1. Télécharger ce projet sur votre PC ;
2. Créer un dossier `input` à la racine du projet ;
3. Télécharger les deux [datasets](https://archive.ics.uci.edu/ml/datasets/Online+Video+Characteristics+and+Transcoding+Time+Dataset) dans le dossier `input`.

Une fois ces trois opérations réalisées, il vous sera possible d'exécuter le code Python du Jupyter Notebook `main.ipynb` et l'API `app.py`.

Une fois `app.py` exécuté, veuillez vous rendre à l'adresse `http://127.0.0.1:5000/` sur votre navigateur.

----

## Introduction au transcodage

Cette partie introductive est également disponible dans le fichier main.

### Intérêt du transcodage et de l'étude

En vidéo, le transcodage est le fait de changer le format de codage d'un média pour le comprimer ou l'encapsuler dans un fichier, ou pour transporter un signal analogique ou numérique. Bien souvent, la transformation comporte des pertes d'information.

Pour illustrer la nécessité du transcodage des vidéos au quotidien, prenons l'exemple des DVD du commerce du début des années 2010. Au format PAL (25 images par seconde), un film de DVD a une résolution de 720 par 576 pixels. Pour un codage RGB sur 3 octets, cela équivaut à 720 x 557 = 414 720 pixels par image, soit 414 720 x 3 octets pour coder la couleur et la luminance de chaque point. Une image de film fait donc 1 244 160 octets, soit 1 215 ko. À raison de 25 images par seconde, on atteint 30 375 ko, soit 29 Mo par seconde, 1 780 Mo par minute et 104 Go par heure !

Les DVD commerciaux ne pouvant contenir que 4,7 ou 9 Go d'informations, il est nécessaire de compresser l'information et de donc de réaliser un transcodage, d'une source lourde à un fichier de sortie réduit.

A une époque où les résolutions d'images sur des sites web d'hébergement de vidéos augmentent considérablement (on trouve des vidéos de 3 840 x 2 160 pixels sur YouTube aujourd'hui) et où la demande et l'exigeance des consommateurs augmente sur ces plateformes de streaming, il parait pertinent de savoir exploiter les données liées à l'encodage de vidéos pour estimer la durée totale de transcodage de ces dernières ou l'espace mémoire total utile au traitement de ces vidéos.

### Fonctionnement du transcodage

Pour "lire" et "écrire" un fichier de vidéo, on utilise un dispositif appelé codec, de l'anglais *coder-decoder*. Différent du *container*, que l'on appelle plus simplement le format de la vidéo (mp4, mov, avi...) et qui regroupe l'ensemble des données image, audio, textuelles et méta, le codec est une implémentation logicielle d'une norme de compression, pour les vidéos dans notre cas. Les codecs les plus répandus aujourd'hui pour la vidéo sont :
* le H.264, datant de 2003, que l'on retrouve dans les fichiers mp4, est le plus utilisé et supporté des codecs ;
* le H.265, sorti en 2013, successeur du H.264. Il a une réduction de bitrate améliorée, mais nécessite plus de ressources et reste peu utilisé ;
* le VP9, développé en 2012 par Google pour YouTube, moins supporté et gourmand en ressources, mais intéressant pour des vidéos en straming et à haute résolution.

Pour compresser un fichier, on peut utiliser des algorithmes de compression sans perte, dits *lossless*, qui nous donnent la garantie qu'aucune information ne disparait lors d'une compression. La compression au format zip en est un. Pour réduire encore plus la taille d'un fichier, il faut accepter de perdre définitivement quelques informations jugées moins utiles. C'est le cas pour les vidéos. Ainsi, la plupart des opérations de transcodage réduisent la quantité d'informations que l'on aura à l'écran lorsque la vidéo sera lue. De plus, pour traiter la décompression et "décoder" les informations relatives à la compression, la machine a besoin de mémoire vive. Plus les opérations de compression seront complexes, plus l'ordinateur devra calculer. Il faut donc trouver le juste équilibre entre la taille du fichier, la qualité de la vidéo et la mémoire vive allouée à la lecture de la vidéo.

On détaille maintenant quelques techniques utilisées par les codecs pour compresser une vidéo.

#### Sous échantillonnage de la chrominance

La première des techniques est évidemment la réduction, certes relative, de la résolution d'une image. Si les dimensions en hauteur et en largeur de la vidéo ne changent pas, le transcodeur peut procéder à une réduction du nombre de pixels "utiles". Un pixel étant défini à la fois par sa luminance Y, sa chrominance bleue Cb et sa chrominance rouge Cr, on peut échantillonner l'image pour définir localement les propriétés des pixels selon l'échantillon auxquels ils appartiennent. Pour conserver une bonne qualité d'image, on pourra par exemple décider que dans un échantillon, si tous les pixels prennent les mêmes chrominances Cb et Cr, ils conservent chacun leur luminance Y individuelle.

![CC BY-SA 4.0 - Ellande - Wikipédia](https://upload.wikimedia.org/wikipedia/commons/1/13/Sous-%C3%A9chantillonnage_de_la_chrominance.png)

Les structures d'échantillonnage sont définies par leurs chiffres J:a:b :
* J est le nombre d'échantillons de luminance (Y) par ligne (toujours identique sur les deux lignes de J pixels). Habituellement, 4 ;
* a est le nombre d'échantillons de chrominance (Cb, Cr) sur la première ligne de pixels ;
* b est le nombre d'échantillons de chrominance (Cb, Cr) sur la deuxième ligne de pixels.

#### Compression spatiale

Une seconde technique consiste à identifier dans une image de vidéo les régions où la couleur est similaire à un seuil déterminée au préalable. Plus une image de vidéo contient de pixels adjacents similaires, plus cette dernière pourra être compressée et son information simplifiée.

Selon le seuil choisi, on pourra remarquer sur la vidéo la présence de rectangles dans lesquels la couleur est identique. Plus la compression est forte, plus les détails d'une image disparaissent.

#### Compression temporelle

La dernière technique de compression de vidéo est la compression temporelle. Il s'agit de la plus importante des techniques dans le cadre de notre étude, car, comme nous allons le voir, de nombreuses données de nos datasets portent sur cette méthode et son fonctionnement. Ici, on ne compresse plus la vidéo image par image mais également sur des périodes temporelles. Des images qui se suivent sur une vidéo comprennent souvent les mêmes objets ou les mêmes paysages. Pour gagner de la place mémoire, on peut considérer que seule l'information de la première image à laquelle apparaît un objet ou un paysage est conservée. Dans le fichier compressé, aucune des images suivantes ne contiendra l'information de l'objet identifié. Elles ne conserveront que la référence expliquant que l'information est à récupérer à l'image précédente. Il est possible de faire de même dans "l'autre sens", en allant chercher une information à l'image suivante. 

Cette technique est d'autant plus intéressante qu'elle est également applicable à des objets en mouvement sur un fond immobile. L'information conservée sur ces images n'est alors que le mouvement de translation de la voiture, les autres informations relatives au fond et à la forme de la voiture étant contenues dans les images précédentes.

Là aussi, la question de similarité des objets ou des paysages entre plusieurs *frames* est sujette à un "seuil de ressemblance". Plus le seuil sera élevé, plus on perdra de petites informations qui pourraient différencier les parties similaires des différentes images et donc moins bonne sera la qualité de la vidéo. De même, aller chercher une information visuelle à une *frame* suivante ou précédente nécessite plus de ressources.

![[Public domain]](https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/I_P_and_B_frames.svg/1920px-I_P_and_B_frames.svg.png)

On identifie alors plusieurs types d'images (*frames*) :
* les *i frames* (*intra-coded picture*), des images complètes contenant toutes l'information dont elles ont besoin ;
* les *p frames* (*predicted picture*), des images ne conservant que les changements par rapport à la précédente image ;
* les *b frames* (*bidirectionnal predicted picture*), des images ne conservant que les changements par rapport à l'image précédente et à l'image suivante. Le traitement de ces images est plus gourmand en ressources.

Les images p et b sont également appelées *inter frames*. Selon le codec, les références aux images précédentes et suivantes peuvent ne concerner qu'une image adjacente ou une image plus éloignée (dans le cas ou l'objet reste immobile plusieurs images d'affilées). Dans le premier cas, le transcodeur doit donc aller, image après image, jusqu'à l'information, ce qui est potentiellement plus gourmand en ressources.

Le codec MPEG-1 utilise également des *d frames*, mais leur intérêt limité a poussé les développeurs à ne pas les intégrer à des codecs plus récents.

----

## Conclusion

Après avoir testé différents modèle, il s'est avéré que le modèle le plus performant était le réseau de neurones DNN réalisé avec Keras.

Ce dernier est composé d'une couche de normalisation des paramètres d'entrée, de deux couches Dense à 64 neurones et d'un neurone de sortie qui retourne l'estimation de la durée de transcodage de la vidéo en fonction des paramètres d'entrée.

L'entraînement du modèle se fait sur 20 époques, en suivant l'optimiseur Adam sur la fonction de perte *Mean Squared Error*.

![[Entraînement du modèle DNN]](media/history_dnn.png)

Le modèle n'est alors pas surentraîné : `val_loss` et `loss` sont équivalents. 

En comparant les données de test avec les prédictions faites par le modèle, on trouve les caractéristiques suivantes : R² = 0.997 et MSE = 0.843.

![[Données de test]](media/dnn_performances.png)

Le modèle est globalement satisfaisant et prédit avec une bonne fiabilité les durées de transcodages de vidéo à mémoire allouée fixée et connue.