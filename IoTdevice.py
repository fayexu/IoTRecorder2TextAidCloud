#######################################################################################################################
# Author: Maurice Snoeren                                                                                             #
# Version: 0.1 beta (use at your own risk)                                                                            #
#                                                                                                                     #
# MyOwnPeer2PeerNode is an example how to use the p2pnet.Node to implement your own peer-to-peer network node.        #
#######################################################################################################################
from p2pnetwork.node import Node

import argparse
import audio_transmit_helper

class IoTdeviceNode (Node):

    # Python class constructor
    def __init__(self, host, port):
        super(IoTdeviceNode, self).__init__(host, port, None)
        print("IoTdeviceNode: Started")

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
        print("node_message from " + node.id + ": " + str(data))
        
    def node_disconnect_with_outbound_node(self, node):
        print("node wants to disconnect with oher outbound node: " + node.id)
        
    def node_request_to_stop(self):
        print("node is requested to stop!")

    def publish_messages(self, project_id, topic_id, file_path):
        """Publishes multiple messages to a Pub/Sub topic."""
        # [START pubsub_quickstart_publisher]
        # [START pubsub_publish]
        from google.cloud import pubsub_v1

        # TODO(developer)
        # project_id = "your-project-id"
        # topic_id = "your-topic-id"

        publisher = pubsub_v1.PublisherClient()
        # The `topic_path` method creates a fully qualified identifier
        # in the form `projects/{project_id}/topics/{topic_id}`
        topic_path = publisher.topic_path(project_id, topic_id)
        data = audio_transmit_helper.encode(file_path)
        future = publisher.publish(topic_path, data.encode("utf-8"))
        print(future.result())

        # for n in range(1, 10):
        #     data = "Message number {}".format(n)
        #     # Data must be a bytestring
        #     data = data.encode("utf-8")
        #     # When you publish a message, the client returns a future.
        #     future = publisher.publish(topic_path, data)
        #     print(future.result())

        print(f"Published messages to {topic_path}.")
        # [END pubsub_quickstart_publisher]
        # [END pubsub_publish]
