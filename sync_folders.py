# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 10:21:17 2023

@author: I538929
"""

import os
import shutil
import sys
import logging
import time



# Function to copy or update files from source to destination
def copy_or_update_file(source_file, destination_file):
    os.makedirs(os.path.dirname(destination_file), exist_ok=True)
    if not os.path.exists(destination_file):
        shutil.copy2(source_file, destination_file)
        logging.info(f"Copied: {source_file} to {destination_file}")
        print(f"Copied {source_file} to {destination_file}")
    if  os.path.exists(destination_file):
        if os.path.getmtime(source_file) > os.path.getmtime(destination_file):
            shutil.copy2(source_file, destination_file)
            logging.info(f"Updated: {destination_file} according to {source_file}")
            print(f"Updated {destination_file} according to {source_file}")
        
# Remove files in the destination folder that don't exist in the source folder
def remove_files(source_folder,destination_folder):
    for root, _, files in os.walk(destination_folder):
        for file in files:
            dest_file = os.path.join(root, file)
            relative_file = os.path.relpath(dest_file, destination_folder)
            source_file = os.path.join(source_folder, relative_file)
    
            if not os.path.exists(source_file):
                os.remove(dest_file)
                logging.info(f"Deleted {dest_file}")
                print(f"Deleted {dest_file}")
                
# Ensure both source and destination folders exist
def check_folders(source_folder,destination_folder):
    if not os.path.exists(source_folder):
        logging.error(f"Source folder '{source_folder}' does not exist.")
        print(f"Source folder '{source_folder}' does not exist.")
        return
    if not os.path.exists(destination_folder):
        logging.error(f"Destination {destination_folder} folder doesn't exist. Created destinaton folder")
        print(f"Destination {destination_folder} folder doesn't exist. Created destinaton folder")
        os.makedirs(destination_folder)
    
    
def synchronize_folders(source_folder, destination_folder,log_file):
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')    
    check_folders(source_folder,destination_folder)
    # Copy or update files from source to destination
    for root, _, files in os.walk(source_folder):
        for file in files:
            source_file = os.path.join(root, file)
            relative_path = os.path.relpath(source_file, source_folder)
            destination_file = os.path.join(destination_folder, relative_path)
            copy_or_update_file(source_file, destination_file)

    remove_files(source_folder,destination_folder)


if __name__ == "__main__":
    while(True):        
        source_folder = sys.argv[1]
        destination_folder = sys.argv[2]
        log_file = sys.argv[3]
        sync_interval = sys.argv[4]
        synchronize_folders(source_folder, destination_folder,log_file)
        time.sleep(int(sync_interval))
        

