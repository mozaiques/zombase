Warbase
=======

Introduction
------------

### Contexte

Ce package python sert de base à certaines applications wartisans.

### Objectif

Ce package permet de gérer des utilisateurs, des actions et des valeurs

### Dépendances

* [SQLAlchemy](http://hg.sqlalchemy.org/sqlalchemy) (0.8)
* [Voluptuous](https://github.com/alecthomas/voluptuous) (0.6)

Architecture
------------

### warbase.model

Package contenant les modèles SQLAlchemy et les schéma Voluptuous nécessaires.

### warbase.data

Package faisant office de couche d'intégrité pour la base de données. En charge
de vérifier la cohérence des données qui intégreront la base de données.

Est le seul package à avoir le droit (par convention) d'écrire (INSERT/UPDATE)
dans la base.

### warbase.business

Package faisant office de couche business. C'est la seule API censée être
utilisée.

Fait appel à warbdata pour insérer des données en base.

Documentation
-------------

TODO
