#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import re

def Stage3_Analyzing_firmware(firmware):
    fylesystems = ['Squashfs', 'Romfs', 'Jffs2', 'Ubifs', 'Cramfs', 'Cpio']
    arch = ['ARM', 'MIPS']

    # Get filesystem type
    output = subprocess.check_output('binwalk ' + firmware, shell=True)
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
    file.write("Firmware: " + str(firmware) + "\nFylesystem: " + 
    str(scanFilesystem[0] + "\n" + "Arch: " + str(scanArch[0] + "\n")))
    file.close()
    S=(str(scanFilesystem[0]))
    # print(S.lower())
    return S.lower()
