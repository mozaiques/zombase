Warbase
=======

Dépendances
------------

* [SQLAlchemy](http://hg.sqlalchemy.org/sqlalchemy) (0.8)
* [Voluptuous](https://github.com/alecthomas/voluptuous) (0.7)

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
directement utilisée.

Fait appel à warbase.data pour insérer des données en base.
