#######################################################################################################################
# Author: Maurice Snoeren                                                                                             #
# Version: 0.1 beta (use at your own risk)                                                                            #
#                                                                                                                     #
# MyOwnPeer2PeerNode is an example how to use the p2pnet.Node to implement your own peer-to-peer network node.        #
#######################################################################################################################
from p2pnetwork.node import Node

from pyqldb.config.retry_config import RetryConfig
from pyqldb.driver.qldb_driver import QldbDriver

class BlockChainNode (Node):
    # messages = [None, None, None]
    # count = 0
    transcript = [None, None, None]

    # Python class constructor
    def __init__(self, host, port):
        super(BlockChainNode, self).__init__(host, port, None)
        print("BlockChainNode: Started")

    # all the methods below are called when things happen in the network.
    # implement your network node behavior to create the required functionality.

    def outbound_node_connected(self, node):
        print("outbound_node_connected: " + node.id)
        
    def inbound_node_connected(self, node):
        print("inbound_node_connected: " + node.id)

    def inbound_node_disconnected(self, node):
        print("inbound_node_disconnected: " + node.id)

    def outbound_node_disconnected(self, node):
        print("outbound_node_disconnected: " + node.id)

    def node_message(self, node, data):
        # self.messages[self.count] = data
        # self.count = self.count + 1
        cmd = data.split("/")[0]
        if cmd == "Trans":
            self.transcript[0] = data.split("/")[1]
            self.transcript[1] = data.split("/")[2]
            self.transcript[2] = data.split("/")[3]
            print()
        print("node_message from " + node.id + ": " + str(data))
        
    def node_disconnect_with_outbound_node(self, node):
        print("node wants to disconnect with oher outbound node: " + node.id)
        
    def node_request_to_stop(self):
        print("node is requested to stop!")

    def create_table(self, transaction_executor):
        print("Creating a table")
        transaction_executor.execute_statement("CREATE TABLE CC_Project")


    def create_index(self, transaction_executor):
        print("Creating an index")
        transaction_executor.execute_statement("CREATE INDEX ON CC_Project(node_id)")


    def insert_documents(self, transaction_executor, arg_1):
        print("Inserting a document")
        transaction_executor.execute_statement("INSERT INTO CC_Project ?", arg_1)


    def read_documents(self, transaction_executor, node_id):
        print("Querying the table")
        cursor = transaction_executor.execute_statement("SELECT * FROM CC_Project WHERE node_id = ?", node_id)

        for doc in cursor:
            if doc["node_id"] == node_id:
                print(doc["node_id"])
                print(doc["audio_name"])
                print(doc["transcript"])

    def update_documents(self, transaction_executor, audio_name, transcript, node_id):
        print("Updating the document")
        transaction_executor.execute_statement("UPDATE CC_Project SET audio_name = ? transcript = ? WHERE node_id = ?", audio_name, transcript, node_id)

    def save_to_QLDB(self):
        # Configure retry limit to 3
        retry_config = RetryConfig(retry_limit=3)

        # Initialize the driver
        print("Initializing the driver")
        qldb_driver = QldbDriver("cc-pj-blockchain-registration", retry_config=retry_config)

        # print(self.id)
        # print(self.messages[0])
        # print(self.messages[1])
        # Insert a document
        doc_1 = {'node_id': self.id,
                 'audio_name': self.transcript[1],
                 'transcript': self.transcript[2],
                 }

        qldb_driver.execute_lambda(lambda x: self.insert_documents(x, doc_1))

        # Query the table
        qldb_driver.execute_lambda(lambda executor: self.read_documents(executor, self.id))


        
