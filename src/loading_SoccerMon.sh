#!/bin/bash

# Make directories
mkdir ../data/SoccerMon
mkdir ../data/SoccerMon/OBJECTIVE

#Define the URL of the folder you want to download
URL_OBJECTIVE="https://files.osf.io/v1/resources/uryz9/providers/dropbox/Objective/?zip=1"

# Define the output zip file name
ZIP_FILE_OBJECTIVE="../data/SoccerMon/OBJECTIVE.zip"

# Download the folder using wget and save it as a zip file
wget -r -nH --cut-dirs=1 --no-parent --no-check-certificate "$URL_OBJECTIVE" -O "$ZIP_FILE_OBJECTIVE"

# Unzip the main folder
unzip "$ZIP_FILE_OBJECTIVE" -d ../data/SoccerMon/OBJECTIVE

# Function to unzip .zip files in a given folder recursively
unzip_recursive() {
    local dir="$1"
    for item in "$dir"/*; do
        if [ -d "$item" ]; then
            unzip_recursive "$item"
        elif [ -f "$item" ] && [[ "$item" == *.zip ]]; then
            unzip "$item" -d "${item%.zip}"
        fi
    done
}

# Call the function to unzip .zip files recursively in the main folder and its subfolders
unzip_recursive "../data/SoccerMon/OBJECTIVE"

find "../data" -name "*.zip" -type f -delete

# SUBJECTIVE DATA IMPORT
mkdir ../data/SoccerMon/SUBJECTIVE

URL_SUBJECTIVE="https://files.osf.io/v1/resources/uryz9/providers/dropbox/Subjective/?zip=1"

ZIP_FILE_SUBJECTIVE="../data/SoccerMon/SUBJECTIVE.zip"

# Download the folder using wget and save it as a zip file
wget -r -nH --cut-dirs=1 --no-parent --no-check-certificate "$URL_SUBJECTIVE" -O "$ZIP_FILE_SUBJECTIVE"

# Unzip the main folder
unzip "$ZIP_FILE_SUBJECTIVE" -d ../data/SoccerMon/SUBJECTIVE

find "../data" -name "*.zip" -type f -delete
