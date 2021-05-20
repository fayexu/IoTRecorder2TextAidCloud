#!/usr/bin/env python
# coding: utf-8

'''
@File   : audio_transmit_helper.py
@Copyright: Fei
@Date   :5/20/21
@Desc   :
'''
import argparse
import base64
import binascii
import io
import os
import sys


def encode(audio_path):
    with io.open(audio_path, "rb") as audio_file:
        audio_data = base64.b64encode(audio_file.read()).decode("utf-8")
        print("encode done")
        return audio_data


file_pattern = "{}-{}.{}"


def decode(audio_data_path):
    with io.open(audio_data_path, "rb") as audio_file:
        audio = base64.b64decode(audio_file.read())
        return audio


encode('./data/audio.m4a')

