#this is an example of pyscript code

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import gs_flatten
from awsgluedq.transforms import EvaluateDataQuality

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node Amazon DynamoDB
AmazonDynamoDB_node1745735865419 = glueContext.create_dynamic_frame.from_catalog(database="resume-parser", table_name="resumestable", transformation_ctx="AmazonDynamoDB_node1745735865419")

# Script generated for node Flatten
Flatten_node1745739538919 = AmazonDynamoDB_node1745735865419.gs_flatten()

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=Flatten_node1745739538919, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1745733889980", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1745736073451 = glueContext.write_dynamic_frame.from_options(frame=Flatten_node1745739538919, connection_type="s3", format="json", connection_options={"path": "s3://resume-data-transformed-rishi", "partitionKeys": []}, transformation_ctx="AmazonS3_node1745736073451")

job.commit()