#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import re

def Stage4_Extracting_filesystem(firmware):
    
    fylesystems = ['Squashfs', 'Romfs', 'Jffs2', 'Ubifs', 'Cramfs']
    arch = ['ARM', 'MIPS', 'ARMEB', 'MIPSEL']

    # Get filesystem type
    output = subprocess.check_output('binwalk -e ' + firmware, shell=True)
    for string in fylesystems:
        scanFilesystem = re.findall(string, str(output))

        if scanFilesystem: break

    # Get Arch
    output = subprocess.check_output('binwalk -A ' + firmware, shell=True)
    for string in arch:    
        scanArch = re.findall(string, str(output))

        if scanArch: break

    # Not found fylesysmet and arch (need check enthropy)
    if ( not scanFilesystem and not scanArch ):
        output = subprocess.run('binwalk -E ' +  firmware, shell=True)
        return False
    
    # Write in config file
    file = open("config.conf", "w")
    file.write("Firmware: " + str(firmware) + "\nFylesystem: " + str(scanFilesystem[0] + "\n" + "Arch: " + str(scanArch[0] + "\n")))
    file.close()

    return True
