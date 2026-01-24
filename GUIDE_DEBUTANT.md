# Guide du Débutant : Maîtriser le Modern Lakehouse

Bienvenue dans ce projet ! Si vous débutez en ingénierie de données, ce guide va vous aider à comprendre l'architecture que nous construisons ensemble et pourquoi elle est "Moderne".

## 1. C'est quoi un "Lakehouse" ?

Traditionnellement, on avait deux mondes :
- **Le Data Lake** (Lac de Données) : Un immense dossier (comme MinIO/S3) où on jette des fichiers (CSV, Parquet). C'est pas cher, mais c'est le chaos : pas de transactions, difficile à modifier.
- **Le Data Warehouse** (Entrepôt de Données) : Une base de données structurée (Postgres, Snowflake). C'est propre et rapide, mais ça coûte cher à grande échelle.

**Le Lakehouse** combine les deux : On garde les fichiers sur un stockage pas cher (MinIO), mais on ajoute une couche d'intelligence (**Apache Iceberg**) qui permet de gérer ces fichiers comme s'ils étaient dans une base de données (avec des transactions `INSERT`, `UPDATE`, `DELETE`).

---

## 2. L'Ingestion de Données : Le Point de Départ

L'ingestion est le processus de collecte des données depuis une source externe vers notre stockage brut (**Raw Data**).

### Pourquoi NiFi ?
Dans une organisation réelle, les données arrivent de partout : APIs, bases de données de vente, capteurs. **Apache NiFi** est un outil visuel qui permet de créer des flux de données. 
- Il "aspire" la donnée.
- Il la dépose dans notre "Zone de Débarquement" (Landing Zone) dans **MinIO**.

### Notre flux d'ingestion (votre projet) :
1.  **Source** : Données NYC Taxi (simulées ou réelles).
2.  **Traitement NiFi** : Récupération périodique.
3.  **Destination** : Bucket `raw-data` dans **MinIO**.

> [!TIP]
> **Le format Parquet** : Au lieu de stocker des CSV (texte lourd), on transforme souvent les données en Parquet. C'est un format "colonnaire" compressé qui permet de lire les données 10x plus vite.

---

## 3. Le Parcours de la Donnée (Pipeline)

### Étape 1 : Bronze (Raw)
Les données arrivent dans `raw-data` telles quelles. C'est historique et immuable. Si on fait une erreur plus tard, on peut toujours repartir d'ici.

### Étape 2 : Silver (Iceberg)
**Spark** lit les fichiers bruts, les nettoie (ex: formats de date, suppression des doublons) et les écrit dans le format **Iceberg**. 
- C'est ici que la magie opère : Spark calcule de manière distribuée sur plusieurs cœurs/machines.

### Étape 3 : Gold (Datamart)
On fait des agrégations (ex: CA par jour). On pousse ces résultats finaux dans **PostgreSQL**. Pourquoi ? Parce que les outils de visualisation (Tableau, PowerBI) ou les applications web préfèrent interroger une base de données rapide plutôt que de scanner des millions de fichiers.

---

## 4. Comment naviguer dans ce projet ?

-   `docker-compose.yml` : C'est la télécommande qui allume tous les serveurs.
-   `spark/jobs/` : C'est là que se trouve le "cerveau" (le code Python qui transforme la donnée).
-   `minio` : Allez sur `http://localhost:9001` pour voir vos fichiers (comme un Google Drive local).

---

## 5. Prochaines étapes pour vous
1.  Lancez l'infrastructure : `docker-compose up -d`.
2.  Regardez les fichiers arriver dans MinIO.
3.  Lancez le job Spark et allez voir les chiffres apparaître dans Postgres.

**Bienvenue dans le monde de la Data Engineering !**
