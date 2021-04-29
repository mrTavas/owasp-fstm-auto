#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import argparse
import re
import stage3_Analyzing_firmware
import stage4_Extracting_filesystem

def Stage4_Extracting_filesystem(firmware, filesystemType):
    
    # Try extract filesystem
    try:
        subprocess.check_call('binwsalk -ess ' + firmware, shell=True)

    except:
        
        # Wrile Filesystem address if config file
        subprocess.check_call('binwalk ' + firmware + ' | grep -i fylesystem | awk \'{print $2}\' >> config.conf', shell=True)

        # Get Filesystem address from config file
        with open("config.conf", "r") as f:
            addressFilesystem = str(f.readlines()[3]).rstrip()
        
        # Put filesystem in manual mode
        subprocess.check_call('dd if=' + firmware + ' bs=1 skip=$((' + addressFilesystem + ')) of=dir.' + filesystemType, shell=True)
        print(filesystemType)
    
        # Unpaking filesystem in manual mode
        if filesystemType == "squashfs":
            subprocess.check_call('unsquashfs dir.squshfs', shell=True)
        
        if filesystemType == "romfs":
            subprocess.check_call('extract-romfs dir.romfs', shell=True)

        if filesystemType == "jfss2":
            subprocess.check_call('jefferson dir.jfss2', shell=True)

        if filesystemType == "ubifs":
            subprocess.check_call('python3 ubidump.py dir.ubi', shell=True)

        if filesystemType == "cramfs":
            subprocess.check_call('uncramfs dir.cramfs', shell=True)

        if filesystemType == "cpio":
            subprocess.check_call('cpio -iv dir.cpio', shell=True)
            return False

    return True


# Main
parser = argparse.ArgumentParser()
parser.add_argument('-f', help = 'Firmware image')

args = parser.parse_args()
firmware_file = args.f

filesystemType = stage3_Analyzing_firmware.Stage3_Analyzing_firmware(firmware_file)
er = stage4_Extracting_filesystem.Stage4_Extracting_filesystem(firmware_file, filesystemType)