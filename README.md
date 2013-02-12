Warbase
=======

Introduction
------------

### Contexte

Ce package python (qui n'en n'est pas un mais seulement une collection de 3
packages pure python) sert de base à certaines applications WArtisans.

Son positionnement open source (licence MIT) ne sert pas à grand chose, si ce
n'est à éviter de payer pour son hebergement sur Github.

Si ce package peut être utile (pédagogie/adaptation à d'autres projets), c'est
tant mieux !

### Objectif

Cette collection de package permet de gérer les utilisateurs et les applications
d'un client.

### Dépendances

* SQLAlchemy (0.8)
* Voluptuous (0.6)

Architecture
------------

### warbmodel

Package contenant les modèles SQLAlchemy et les schéma Voluptuous nécessaires.

### warbdata

Package faisant office de couche d'intégrité pour la base de données. En charge
de vérifier la cohérence des données qui intégreront la base de données.

Est le seul package a avoir le droit (par convention) d'écrire (INSERT/UPDATE),
dans la base.

### warbbiz

Package faisant office de couche business. C'est la seule API censée être
utilisée.

Fait appel à warbdata pour insérer des données en base.

Documentation
-------------
