#!/usr/bin/env python
# coding: utf-8

'''
@File   : qldb-quick-start.py
@Copyright: Fei
@Date   :5/20/21
@Desc   :
'''

from pyqldb.config.retry_config import RetryConfig
from pyqldb.driver.qldb_driver import QldbDriver


def create_table(transaction_executor):
    print("Creating a table")
    transaction_executor.execute_statement("CREATE TABLE CC_Project")


def create_index(transaction_executor):
    print("Creating an index")
    transaction_executor.execute_statement("CREATE INDEX ON CC_Project(node_id)")


def insert_documents(transaction_executor, arg_1):
    print("Inserting a document")
    transaction_executor.execute_statement("INSERT INTO CC_Project ?", arg_1)


def read_documents(transaction_executor, node_id):
    print("Querying the table")
    cursor = transaction_executor.execute_statement("SELECT * FROM CC_Project WHERE node_id = ?", node_id)

    for doc in cursor:
        print(doc["node_id"])
        print(doc["audio_name"])
        print(doc["transcript"])


def update_documents(transaction_executor, audio_name, node_id):
    print("Updating the document")
    transaction_executor.execute_statement("UPDATE CC_Project SET audio_name = ? WHERE node_id = ?", audio_name, node_id)


# Configure retry limit to 3
retry_config = RetryConfig(retry_limit=3)

# Initialize the driver
print("Initializing the driver")
qldb_driver = QldbDriver("cc-pj-blockchain-registration", retry_config=retry_config)

# Create a table
qldb_driver.execute_lambda(lambda executor: create_table(executor))

# Create an index on the table
qldb_driver.execute_lambda(lambda executor: create_index(executor))

# Insert a document
doc_1 = {'node_id': "3",
         'audio_name': "test_3",
         'transcript': "hello hi how are you",
         }

qldb_driver.execute_lambda(lambda x: insert_documents(x, doc_1))

# Query the table
qldb_driver.execute_lambda(lambda executor: read_documents(executor, '3'))

# Update the document
audio_name = "test_2"
node_id = "1"

qldb_driver.execute_lambda(lambda x: update_documents(x, audio_name, node_id))

# Query the table for the updated document
qldb_driver.execute_lambda(lambda executor: read_documents(executor, node_id))


