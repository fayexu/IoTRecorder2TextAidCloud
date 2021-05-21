#######################################################################################################################
# Author: Maurice Snoeren                                                                                             #
# Version: 0.1 beta (use at your own risk)                                                                            #
#                                                                                                                     #
# This example show how to derive a own Node class (MyOwnPeer2PeerNode) from p2pnet.Node to implement your own Node   #
# implementation. See the MyOwnPeer2PeerNode.py for all the details. In that class all your own application specific  #
# details are coded.                                                                                                  #
#######################################################################################################################

import sys
import time
sys.path.insert(0, '.') # Import the files where the modules are located

import argparse
import base64
import binascii
import io

import time
import boto3
import requests

from IoTdevice import IoTdeviceNode
from transcribe import TranscribeNode
from blockchain import BlockChainNode


parser = argparse.ArgumentParser()
   
parser.add_argument('project_id')
parser.add_argument('file_path')
parser.add_argument('topic_id')
parser.add_argument('subscription_id')
parser.add_argument('bucket_id')
parser.add_argument('region')
parser.add_argument('job_name')

args = parser.parse_args()

# print(f'{args.name} is {args.age} years old')

node_1 = IoTdeviceNode("127.0.0.1", 8001)
node_2 = TranscribeNode("127.0.0.1", 8002)
node_3 = BlockChainNode("127.0.0.1", 8003)

time.sleep(1)

node_1.start()
node_2.start()
node_3.start()

time.sleep(1)

node_1.connect_with_node('127.0.0.1', 8002)
node_2.connect_with_node('127.0.0.1', 8003)
node_3.connect_with_node('127.0.0.1', 8002)

time.sleep(2)

node_1.publish_messages(args.project_id, args.topic_id, args.file_path)
audio = args.file_path.split("/")[-1]
node_1.send_to_nodes("Pub/" + audio)

time.sleep(3)

node_2.receive_messages(args.project_id, args.subscription_id, 5)
aud_name = 'audio-1'
node_2.send_to_nodes("Sub/" + aud_name)
bucket_name = args.bucket_id
region_name = args.region
audio_name = 'audio_1'
is_uploaded = node_2.upload_to_aws(aud_name+'.m4a', bucket_name, audio_name+'.m4a', region_name)
transcribe_client = boto3.client('transcribe')
file_uri = 's3://' + bucket_name + '/' + audio_name + '.m4a'
job_name = args.job_name
txt_data = node_2.transcribe_file(job_name, file_uri, transcribe_client)
node_2.send_to_nodes("Trans/" + aud_name + '/' + node_2.audio + '/' + txt_data)

time.sleep(10)

node_3.save_to_QLDB()
node_3.send_to_nodes("DB/finish saving a transcript to QLDB")

time.sleep(3)

print('end application')

node_1.stop()
node_2.stop()
node_3.stop()


