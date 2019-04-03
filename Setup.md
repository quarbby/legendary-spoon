# Setup 

- git
- neo4j
- elasticsearch

## Git Setup



```bash
git clone git@github.com:quarbby/legendary-spoon.git TECHSCAN_BACKEND
```



## Neo4J



## ElasticSearch 6.7

download from <https://www.elastic.co/downloads/elasticsearch>

installation https://www.elastic.co/guide/en/elasticsearch/reference/6.7/windows.html



_Download Java SE Development Kit_

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



## Anaconda

<https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/>

```
conda -V
conda update conda
```

Check your python version

```
conda search "^python$"
```

Create a conda environment for this project

```
conda create -n yourenvname python=x.x anaconda
```



# 



# Running TechScan 1.0

#### 1. Start Neo4J Server



#### 2. Start Elasticsearch server

<https://www.elastic.co/guide/en/elasticsearch/reference/6.7/windows.html>

```bash
cd c:\elastic-search-6.7.0
.\bin\elasticsearch.exe
```



#### 3. Run Python scripts

in the root folder,  ``` python manage.py runserver``` 

Django project is available at ```<http://localhost:3000/>```







## Running TechScan 2.0

#### 3. Run npm

- ensure node modules are updated
- run ```npm start```
- 





