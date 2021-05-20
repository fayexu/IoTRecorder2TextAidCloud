#######################################################################################################################
# Author: Maurice Snoeren                                                                                             #
# Version: 0.1 beta (use at your own risk)                                                                            #
#                                                                                                                     #
# MyOwnPeer2PeerNode is an example how to use the p2pnet.Node to implement your own peer-to-peer network node.        #
#######################################################################################################################
from p2pnetwork.node import Node

import argparse
import base64
import binascii
import io

import time
import boto3
import requests

class TranscribeNode (Node):

    # Python class constructor
    def __init__(self, host, port):
        super(TranscribeNode, self).__init__(host, port, None)
        print("TranscribeNode: Started")

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

    def receive_messages(self, project_id, subscription_id, timeout):
        """Receives messages from a pull subscription."""
        # [START pubsub_subscriber_async_pull]
        # [START pubsub_quickstart_subscriber]
        from concurrent.futures import TimeoutError
        from google.cloud import pubsub_v1
        global count
        count = 0
        file_pattern = "{}-{}.{}"

        # TODO(developer)
        # project_id = "your-project-id"
        # subscription_id = "your-subscription-id"
        # Number of seconds the subscriber should listen for messages
        # timeout = 5.0

        subscriber = pubsub_v1.SubscriberClient()
        # The `subscription_path` method creates a fully qualified identifier
        # in the form `projects/{project_id}/subscriptions/{subscription_id}`
        subscription_path = subscriber.subscription_path(project_id, subscription_id)

        # def callback(message):
        #     print(f"Received {message}.")
        #     message.ack()

        # def callback(message):
        #     tmp = message.data
        #     print(f"Received {tmp}.")
        #     #print("#############here to receive ##############")
        #     out.write(tmp.decode('utf-8'))
        #     out.flush()
        #     if message.attributes:
        #         print("Attributes:")
        #         for key in message.attributes:
        #             value = message.attributes.get(key)
        #             print(f"{key}: {value}")
        #     message.ack()

        def callback(message):
            global count
            try:
                count = count + 1
                print("Received audio {}:".format(count))
                image_data = base64.b64decode(message.data)

                with io.open(file_pattern.format("audio", count, "m4a"), "wb") as f:
                    f.write(image_data)
                    message.ack()
                    # Signal to the main thread that we can exit.
            except binascii.Error:
                message.ack()  # To move forward if a message can't be processed

        streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
        print(f"Listening for messages on {subscription_path}..\n")

        # Wrap subscriber in a 'with' block to automatically call close() when done.
        with subscriber:
            try:
                # When `timeout` is not set, result() will block indefinitely,
                # unless an exception is encountered first.
                streaming_pull_future.result(timeout=timeout)
            except TimeoutError:
                streaming_pull_future.cancel()
        # [END pubsub_subscriber_async_pull]
        # [END pubsub_quickstart_subscriber]

    def upload_to_aws(self, local_file, bucket, s3_file):
        s3 = boto3.client('s3',region_name='us-west-2')
        try:
            s3.upload_file(local_file, bucket, s3_file)
            print("Upload Successful")
            return True
        except FileNotFoundError:
            print("The file was not found")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False

    def transcribe_file(self, job_name, file_uri, transcribe_client):
        transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': file_uri},
            MediaFormat='mp4',
            LanguageCode='en-US'
        )

        max_tries = 60
        while max_tries > 0:
            max_tries -= 1
            job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
            job_status = job['TranscriptionJob']['TranscriptionJobStatus']
            if job_status in ['COMPLETED', 'FAILED']:
                print(f"Job {job_name} is {job_status}.")
                if job_status == 'COMPLETED':
                    print(
                        f"Download the transcript from\n"
                        f"\t{job['TranscriptionJob']['Transcript']['TranscriptFileUri']}.")
                    
                break
            else:
                print(f"Waiting for {job_name}. Current status is {job_status}.")
            time.sleep(10)

        data = job['TranscriptionJob']['Transcript']['TranscriptFileUri']
        data = requests.get(data).json()
        txt_data = data["results"]["transcripts"][0]["transcript"]
        print(txt_data)
        return txt_data
        
