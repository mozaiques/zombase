mozbase
=======

Dépendances
------------

* [SQLAlchemy](http://hg.sqlalchemy.org/sqlalchemy) (0.8.1)
* [Voluptuous](https://github.com/alecthomas/voluptuous) (0.7.2)

Architecture
------------

### mozbase.model

Package contenant les modèles SQLAlchemy et les schéma Voluptuous nécessaires.

### mozbase.data

Package faisant office de couche d'intégrité pour la base de données. En charge
de vérifier la cohérence des données qui intégreront la base de données.

### mobase.biz

Bla
