# Setup 


- git
- neo4j
- elasticsearch

## Git Setup

- First, try 

  ```
  git clone git@github.com:quarbby/legendary-spoon.git TECHSCAN_BACKEND
  ```

- It will fail because permission have not been set. First we need to generate a key, and add your terminal to Github as a trusted source.

- Generate a key

  ```
  generate ssh key ` ssh-keygen -t rsa -b 4096 -C "yourGithubEmail@email.com"
  ```

- ```eval $(ssh-agent -s)``` should print ```Agent pid ___```

- copy SSH key `clip < ~/.ssh/id_rsa.pub`

- go to *Github > account > settings > SSH and GPG keys > New SSH keys > New SSH key >* any title, paste into Key

- this will work now: `git clone git@github.com:quarbby/legendary-spoon.git TECHSCAN_BACKEND`

## Sourcetree Setup

- Clone the project, `fetch`/`pull`/`push` won't work, same reason as before
- `Tools`  > `Create or Import SSH Key` to open **PuTTy Key Generator**
  - Generate key (move mouse over area to generate randomness)
  - Under `Key`>`Public key for pasting into OpenSSH authorized_keys file:` copy entire public key (starts with `ssh-rsa...`)
    - Like above, add to _**Github** > account > settings > SSH and GPG keys > New SSH keys > New SSH key >_ any title, paste into Key
  - `Save public key` and `Save private key` in **PuTTy Key Generator**
  - In the windows toolbar / system tray, open **Pagaent** (icon of computer wearing a hat), add in the *private key* file
- Sourcetree should work now

#### Basic Stuff

- **FETCH** : Gets latest commits from the project, *SAFE to do*, please do so often
- **PULL** : After fetching, if someone has added to your branch, *pull* to update your working copy to latest commit in the branch 
- **COMMIT** :  Add your files from `unstaged` to `staged` first
- **PUSH** : Push your commit **! NOTE** Untick all branches, and push ONLY to your branch
- **MERGE** : right click any other branch, to *merge* into your current branch
- **CHECKOUT** : Right click another branch to *checkout*. Make sure that there are no local unsaved changes first.
- **STASH** : Stash *uncommited changes*

## Neo4J

Download from https://neo4j.com/download/ 

## ElasticSearch 6.7

Download from <https://www.elastic.co/downloads/elasticsearch>

Installation https://www.elastic.co/guide/en/elasticsearch/reference/6.7/windows.html




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


Pip install all dependencies from requirements.txt in the virtual environment






# Running TechScan 1.0

#### 1. Start Neo4J Server

Open Neo4j, start a new project and create new graph. Set the graph password to 123.

2. Start Elasticsearch server

<https://www.elastic.co/guide/en/elasticsearch/reference/6.7/windows.html>

```bash
cd c:\elastic-search-6.7.0

.\bin\elasticsearch.bat

```



#### 3. Run Python scripts


In the root folder,  ``` python manage.py runserver``` 

Django project is available at ```<http://localhost:8000/>```








## Running TechScan 2.0

#### 3. Run npm

- ensure node modules are updated
- run ```npm start```
- 





