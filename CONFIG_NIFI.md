# Configuration de l'ingestion NYC Taxi avec Apache NiFi

Ce guide vous explique comment configurer vote premier flux dans NiFi pour récupérer les données réelles du site de la ville de New York et les envoyer dans votre Lakehouse (MinIO).

## 1. Accéder à NiFi
- URL : `https://localhost:8443/nifi`
- Login : `admin` / `password12345678`

---

## 2. Création du flux (Pipeline)

Vous allez avoir besoin de deux composants (Processors) principaux.

### Étape A : Récupérer le fichier (InvokeHTTP)
1. Faites glisser l'icône **Processor** (le carré en haut à gauche) sur le canevas.
2. Recherchez et sélectionnez `InvokeHTTP`.
3. Faites un clic droit sur le processeur -> **Configure** -> onglet **Properties** :
   - **HTTP Method** : `GET`
   - **Remote URL** : `https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet`
     *(C'est l'URL officielle pour Janvier 2024)*.
4. Dans l'onglet **Scheduling**, réglez **Run Schedule** sur `1 day` (pour ne pas saturer le site distant).

### Étape B : Envoyer vers MinIO (PutS3Object)
1. Ajoutez un nouveau processeur : `PutS3Object`.
2. Configurez-le (**Properties**) :
   - **Bucket** : `raw-data`
   - **Access Key** : `admin`
   - **Secret Key** : `password`
   - **Endpoint Override URL** : `http://minio:9000`
   - **Region** : `us-east-1`
   - **Object Key** : `nyc-taxi/yellow_tripdata_2024-01.parquet`
   - **Communications Timeout** : `30 sec`
3. Allez dans l'onglet **Relationships** et cochez `success` et `failure` dans la colonne "Terminate" (pour ce test simple).

### Étape C : Connecter les deux
1. Survolez `InvokeHTTP`, maintenez l'icône de flèche et tirez-la vers `PutS3Object`.
2. Dans la boîte de dialogue qui s'ouvre, cochez `Response`. Cliquez sur **Add**.

---

## 3. Lancer le flux
1. Clic droit sur `InvokeHTTP` -> **Start**.
2. Clic droit sur `PutS3Object` -> **Start**.

### Vérification
1. Allez sur votre console MinIO : `http://localhost:9001` (admin/password).
2. Ouvrez le bucket `raw-data`.
3. Vous devriez voir un dossier `nyc-taxi` avec votre fichier Parquet à l'intérieur !

---

## 4. Note sur les formats (Parquet vs CSV)
Le site de NYC fournit maintenant des fichiers `.parquet`. 
C'est **mieux** que le CSV car c'est compressé et plus rapide à lire avec Spark.

> [!IMPORTANT]
> Si vous utilisez le format Parquet, assurez-vous de modifier votre job Spark `ingest_raw_to_iceberg.py` pour utiliser `.parquet()` au lieu de `.csv()`.

```python
# Dans ingest_raw_to_iceberg.py
df = spark.read.parquet("s3a://raw-data/nyc-taxi/")
```

---

## 5. Approche Avancée : Gérer plusieurs URLs (Dynamique)

Plutôt que de créer un processeur par mois, vous pouvez rendre le flux dynamique :

1.  **GenerateFlowFile** : Pour déclencher le flux.
2.  **ReplaceText** : Mettez vos URLs (une par ligne) dans le champ "Replacement Value".
3.  **SplitText** : Réglez `Line Split Count` sur `1`. (Cela crée un message par URL).
4.  **ExtractText** : Utilisez une Regex `(.*)` pour mettre l'URL dans un attribut (ex: `ma.url`).
5.  **InvokeHTTP** : Utilisez `${ma.url}` dans le champ **Remote URL**.

Cela vous permet de télécharger 12 mois de données avec un seul processeur `InvokeHTTP` !
