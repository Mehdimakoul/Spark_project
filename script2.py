from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count
import matplotlib.pyplot as plt
import seaborn as sns
spark = SparkSession.builder.appName("MiniProjet").getOrCreate()
df = spark.read.csv("/tmp/data.csv", header=True, inferSchema=True)
df.printSchema()
df.show(5)
df = df.dropna(subset=["remise", "nom_site","profit","mode_paiement","mois"])
# --------- GRAPHE 1 : Histogramme du nombre d'entrées par site ---------
if "nom_site" in df.columns:
    print("Nombre d'entrées par site :")
    site_count_df = df.groupBy("nom_site").count()
    site_count_df.show()
    pdf1 = site_count_df.toPandas()
    plt.figure(figsize=(10, 6))
    sns.barplot(x="nom_site", y="count", data=pdf1, palette="viridis")
    plt.title("Nombre d'entrées par site")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("/tmp/histogramme_par_site.png")  
# --------- GRAPHE 2 : Camembert de la moyenne des remises par site ---------
if "nom_site" in df.columns and "remise" in df.columns:
    print("Moyenne des remises par site :")
    remise_df = df.groupBy("nom_site").agg(avg("remise").alias("moyenne_remise"))
    remise_df.show()
    pdf2 = remise_df.toPandas()
    plt.figure(figsize=(8, 8))
    plt.pie(pdf2["moyenne_remise"], labels=pdf2["nom_site"], autopct='%1.1f%%', startangle=140)
    plt.title("Répartition des remises moyennes par site")
    plt.savefig("/tmp/camembert_remise.png")

# --------- GRAPHE 3 : Boxplot des profits par mode de paiement ---------
if "mode_paiement" in df.columns and "profit" in df.columns:
    print("Moyenne du profit par mode de paiement :")
    profit_df = df.select("mode_paiement", "profit")
    profit_df = profit_df.dropna()
    pdf3 = profit_df.toPandas()
    plt.figure(figsize=(10, 6))
    sns.boxplot(x="mode_paiement", y="profit", data=pdf3, palette="Set2")
    plt.title("Distribution des profits par mode de paiement")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("/tmp/boxplot_profit.png")
# --------- GRAPHE 4 : Courbe du profit moyen par mois ---------
if "mois" in df.columns and "profit" in df.columns:
    print("Moyenne du profit par mois :")
    mois_df = df.groupBy("mois").agg(avg("profit").alias("moyenne_profit"))
    mois_df.show()
    pdf4 = mois_df.toPandas().sort_values("mois")
    plt.figure(figsize=(10, 6))
    sns.lineplot(x="mois", y="moyenne_profit", data=pdf4, marker='o', color='orange')
    plt.title("Profit moyen par mois")
    plt.xlabel("Mois")
    plt.ylabel("Profit moyen")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("/tmp/line_profit_mois.png")
spark.stop()
