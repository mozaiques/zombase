Warbase
=======

Cette doc est clairement obsolète.

Dépendances
------------

* [SQLAlchemy](http://hg.sqlalchemy.org/sqlalchemy) (0.8)
* [Voluptuous](https://github.com/alecthomas/voluptuous) (0.7)

Architecture
------------

### mozbase.model

Package contenant les modèles SQLAlchemy et les schéma Voluptuous nécessaires.

### mozbase.data

Package faisant office de couche d'intégrité pour la base de données. En charge
de vérifier la cohérence des données qui intégreront la base de données.

Est le seul package à avoir le droit (par convention) d'écrire (INSERT/UPDATE)
dans la base.

### mozbase.business

Package faisant office de couche business. C'est la seule API censée être
directement utilisée.

Fait appel à warbase.data pour insérer des données en base.
