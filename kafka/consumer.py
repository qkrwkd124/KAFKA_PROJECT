from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, to_timestamp, round, date_format
from pyspark.sql.types import StructType,StructField,StringType,DoubleType


# SparkConf를 이용하여 Maven 의존성 설정 자동으로 캐싱됨. $HOME/.ivy2/에 저장됨
spark = SparkSession.builder\
    .appName("KafkaSparkStreamingConsumer")\
    .config(
            "spark.jars.packages", 
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.postgresql:postgresql:42.7.4"
        )\
    .getOrCreate()

schema = StructType([
    StructField("timestamp",StringType(),True),
    StructField("sensor_id",StringType(),True),
    StructField("value",DoubleType(),True)
])

def write_to_db(df,epoch_id):
    df.write\
        .mode("append")\
        .format("jdbc")\
        .option("url","jdbc:postgresql://localhost:5432/kafka")\
        .option("driver","org.postgresql.Driver")\
        .option("dbtable","sensor_test")\
        .option("user","airflow")\
        .option("password","airflow")\
        .save()


df = spark.readStream\
    .format("kafka")\
    .option("kafka.bootstrap.servers","localhost:29092")\
    .option("subscribe","sensor-data")\
    .option("startingOffsets","latest")\
    .load()


# 데이터 파싱 
parsed_df = df.select(from_json(col("value").cast("string"),schema).alias("data")).select("data.*")

# - timestamp: 문자열을 to_timestamp()로 타임스탬프 타입으로 변환한 후, date_format()으로 "YYYYMMDDHHMMSS" 포맷으로 변경
# - value: spark_round()를 사용하여 소수점 아래 2자리로 반올림 처리
transformed_df = parsed_df.withColumn("timestamp",date_format(to_timestamp(col("timestamp")),"yyyyMMddHHmmss"))\
                            .withColumn("value",round(col("value"),1))\
                            .withColumnRenamed("timestamp","sensor_date")


query = transformed_df.writeStream\
    .foreachBatch(write_to_db)\
    .outputMode("append")\
    .start()

query.awaitTermination()








