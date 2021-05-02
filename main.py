#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import argparse
import stage3_Analyzing_firmware
import stage4_Extracting_filesystem


# Main
parser = argparse.ArgumentParser()
parser.add_argument('-f', help = 'Firmware image')

args = parser.parse_args()
firmware_file = args.f

filesystemType = stage3_Analyzing_firmware.Stage3_Analyzing_firmware(firmware_file)
er = stage4_Extracting_filesystem.Stage4_Extracting_filesystem(firmware_file, filesystemType)