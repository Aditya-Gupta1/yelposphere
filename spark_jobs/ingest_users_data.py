from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, FloatType, IntegerType, TimestampType
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument("--input", required=True, help='GCS file path to the input business JSON file')
parser.add_argument("--dataset", required=True, help='BigQuery dataset name')
parser.add_argument("--table", required=True)
parser.add_argument("--tempGcsBucket", required=True)
parser.add_argument("--dateFormat", default='yyyy-MM-dd HH:mm:ss')

args = parser.parse_args()

spark = SparkSession \
        .builder \
        .appName('ingest_users_data') \
        .getOrCreate()

user_schema = StructType([
    StructField("user_id", StringType(), True),
    StructField("name", StringType(), True),
    StructField("review_count", IntegerType(), True),
    StructField("yelping_since", TimestampType(), True),
    StructField("useful", IntegerType(), True),
    StructField("funny", IntegerType(), True),
    StructField("cool", IntegerType(), True),
    StructField("fans", IntegerType(), True),
    StructField("average_stars", FloatType(), True)
])

df = spark \
    .read \
    .option('dateFormat', args.dateFormat) \
    .schema(user_schema) \
    .json(args.input)

df \
    .write \
    .format('bigquery') \
    .option("table", f"{args.dataset}.{args.table}") \
    .option("temporaryGcsBucket", f"{args.tempGcsBucket}") \
    .mode('overwrite') \
    .save()
