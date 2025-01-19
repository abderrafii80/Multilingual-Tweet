from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim

# Initialiser Spark
spark = SparkSession.builder \
    .appName("DataCleaning") \
    .enableHiveSupport() \
    .getOrCreate()


# Le traitement du pipeline ETL ete fait sur ces 3 articles (googlenews_fr_en_ar)


df_fr = spark.sql("SELECT * FROM data_mining.news_fr")
df_ar = spark.sql("SELECT * FROM data_mining.news_ar")
df_en = spark.sql("SELECT * FROM data_mining.news_en")


df_fr_cleaned = df_fr.withColumn("title_cleaned", trim(col("title")))
df_ar_cleaned = df_ar.withColumn("title_cleaned", trim(col("title")))
df_en_cleaned = df_en.withColumn("title_cleaned", trim(col("title")))

