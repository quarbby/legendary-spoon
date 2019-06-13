## Sourcetree Setup

1. Download and Install [Sourcetree](<https://www.sourcetreeapp.com/>). This will require to create a dummy Bitbucket account. It will be link to github eventually

2. Open Sourcetree and link github account. Clone the project

   ```
   git@github.com:quarbby/legendary-spoon.git
   ```

3. Follow this [guide](<https://confluence.atlassian.com/bitbucket/set-up-an-ssh-key-728138079.html#SetupanSSHkey-ssh3>) for setting up SSH keys.

#### Basic Stuff

- **FETCH** : Gets latest commits from the project, *SAFE to do*, please do so often
- **PULL** : After fetching, if someone has added to your branch, *pull* to update your working copy to latest commit in the branch 
- **COMMIT** :  Add your files from `unstaged` to `staged` first
- **PUSH** : Push your commit **! NOTE** Untick all branches, and push ONLY to your branch
- **MERGE** : right click any other branch, to *merge* into your current branch
- **CHECKOUT** : Right click another branch to *checkout*. Make sure that there are no local unsaved changes first.
- **STASH** : Stash *uncommitted changes*

## ElasticSearch 6.70 Setup

- Download [Elasticsearch](<https://www.elastic.co/downloads/past-releases/elasticsearch-6-7-0>) 
- Download [Java JDK 11.0.3](<https://www.oracle.com/technetwork/java/javase/downloads/jdk11-downloads-5066655.html>)

in `elasticsearch-6.7.0/bin/elasticsearch.bat`, under `SET params='%*'`add `SET "JAVA_HOME=C:\Program Files\Java\jdk-11.0.2"`

```bash
@echo off

setlocal enabledelayedexpansion
setlocal enableextensions

SET params='%*'
SET "JAVA_HOME=C:\Program Files\Java\jdk-11.0.2"

:loop
```

set `JAVA_HOME=C:\Program Files\Java\jdk-11.0.2` 


## Neo4j Setup

- Download [Neo4j](https://neo4j.com/download/ )

- Download data 

  http://www.sharecsv.com/dl/83328676c09c77d0b9265e679aedcb3e/Field.csv

  <http://www.sharecsv.com/dl/ece29217aca59ad56eb31a49e79edcda/fieldPartOf.csv>

-  Store them in imports folder. Create graph using cypher queries.

```cypher
CREATE CONSTRAINT ON (field:Field) ASSERT field.fieldID IS UNIQUE

LOAD CSV WITH HEADERS FROM "file:///Field.csv" AS line
CREATE (:Field {fieldID: line.fieldID, fieldName: line.fieldName, fieldLevel: line.fieldLevel, fieldPaperNum: line.fieldPaperNum, fieldReferenceCount:line.fieldReferenceCount})

LOAD CSV WITH HEADERS FROM "file:///fieldPartOf.csv" AS line
MATCH (f:Field{fieldID:line.fieldID}), (f1:Field{fieldID:line.fieldID2})
CREATE (f)-[:PART_OF_FIELD]->(f1)
```



## Installing Dependencies

First create a virtual environment with pipenv.

```bash
pip install pipenv
cd [project_location]
pipenv shell
```

Next, download and place these 2 files in the root directory

- [python i-graph cp37](<https://www.lfd.uci.edu/~gohlke/pythonlibs/#python-igraph>) (for python 3.7)
- [spacy-models](https://github.com/explosion/spacy-models/releases/download/en_core_web_md-2.1.0/en_core_web_md-2.1.0.tar.gz)

Run `pipenv install` This will install all requirements from Pipfile. 

Finally, download [chromedriver](https://chromedriver.storage.googleapis.com/index.html?path=74.0.3729.6/) and place it at the the same directory as `manage.py` 


## Starting Server

Start Elasticsearch and Neo4j, then run `python manage.py runserver` 

Open chrome and load `localhost:8000` 