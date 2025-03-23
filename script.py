from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count
# Initialiser la session Spark
spark = SparkSession.builder.appName("MiniProjet").getOrCreate()
# Charger le fichier CSV
df = spark.read.csv("/tmp/data.csv", header=True, inferSchema=True)
# Afficher le schéma pour voir les colonnes
df.printSchema()
# Voir les premières lignes du dataset
df.show(5)

## Traitements des données 
# Exemple 1 : Nombre de lignes par site 
if "nom_site" in df.columns:
    print("Nombre d'entrées par site :")
    df.groupBy("nom_site").count().show()

# Exemple 2 : Moyenne des remises par site
if "nom_site" in df.columns and "remise" in df.columns:
    print("Moyenne des remises par site :")
    df.groupBy("nom_site").agg(avg("remise").alias("moyenne_remise")).show()
# Exemple 3 : Moyenne du profit  par mode de paiement
if "mode_paiement" in df.columns and "profit" in df.columns:
    print("Moyenne du profit  par mode de paiement :")
    df.groupBy("mode_paiement").agg(avg("profit").alias("moyenne_profit")).show()
# Exemple 4 : Moyenne du profit par mois
if "mois" in df.columns and "profit" in df.columns:
    print("Moyenne du profit par mois :")
    df.groupBy("mois").agg(avg("profit").alias("moyenne_profit")).show()
# Sauvegarder un résultat dans un fichier CSV pour visualiser ensuite
if "nom_site" in df.columns and "remise" in df.columns:
    df.groupBy("nom_site").agg(avg("remise").alias("moyenne_remise")) \
      .coalesce(1) \
      .write \
      .option("header", True) \
      .csv("/tmp/resultats_moyenne_remise")
spark.stop()


