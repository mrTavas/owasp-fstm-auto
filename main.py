#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import argparse

import stage3_Analyzing_firmware
import stage4_Extracting_filesystem

# def Stage3_Analyzing_firmware(firmware):
#     fylesystems = ['Squashfs', 'Romfs', 'Jffs2', 'Ubifs', 'Cramfs']
#     arch = ['ARM', 'MIPS', 'ARMEB', 'MIPSEL']

#     # Get filesystem type
#     output = subprocess.check_output('binwalk ' + firmware, shell=True)
#     for string in fylesystems:
#         scanFilesystem = re.findall(string, str(output))

#         if scanFilesystem: break

#     # Get Arch
#     output = subprocess.check_output('binwalk -A ' + firmware, shell=True)
#     for string in arch:    
#         scanArch = re.findall(string, str(output))

#         if scanArch: break

#     # Not found fylesysmet and arch (need check enthropy)
#     if ( not scanFilesystem and not scanArch ):
#         output = subprocess.run('binwalk -E ' +  firmware, shell=True)
#         return False
    
#     # Write in config file
#     file = open("config.conf", "w")
#     file.write("Firmware: " + str(firmware) + "\nFylesystem: " + str(scanFilesystem[0] + "\n" + "Arch: " + str(scanArch[0] + "\n")))
#     file.close()

#     return True

# def Stage4_Extracting_filesystem(firmware):
    
#     fylesystems = ['Squashfs', 'Romfs', 'Jffs2', 'Ubifs', 'Cramfs']
#     arch = ['ARM', 'MIPS', 'ARMEB', 'MIPSEL']

#     # Get filesystem type
#     output = subprocess.check_output('binwalk -e ' + firmware, shell=True)
#     for string in fylesystems:
#         scanFilesystem = re.findall(string, str(output))

#         if scanFilesystem: break

#     # Get Arch
#     output = subprocess.check_output('binwalk -A ' + firmware, shell=True)
#     for string in arch:    
#         scanArch = re.findall(string, str(output))

#         if scanArch: break

#     # Not found fylesysmet and arch (need check enthropy)
#     if ( not scanFilesystem and not scanArch ):
#         output = subprocess.run('binwalk -E ' +  firmware, shell=True)
#         return False
    
#     # Write in config file
#     file = open("config.conf", "w")
#     file.write("Firmware: " + str(firmware) + "\nFylesystem: " + str(scanFilesystem[0] + "\n" + "Arch: " + str(scanArch[0] + "\n")))
#     file.close()

#     return True


# Main
parser = argparse.ArgumentParser()
parser.add_argument('-f', help = 'Firmware image')


args = parser.parse_args()
firmware_file = args.f

er = stage3_Analyzing_firmware.Stage3_Analyzing_firmware(firmware_file)