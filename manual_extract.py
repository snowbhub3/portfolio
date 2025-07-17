#!/usr/bin/env python3
import zipfile
import os
import sys

def extract_zip(zip_path, extract_to='.'):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # List files first
            file_list = zip_ref.namelist()
            print(f"Found {len(file_list)} files in archive:")
            for i, name in enumerate(file_list[:10]):
                print(f"  {name}")
            if len(file_list) > 10:
                print(f"  ... and {len(file_list) - 10} more files")
            
            # Extract all files
            zip_ref.extractall(extract_to)
            print(f"\nSuccessfully extracted {len(file_list)} files to {extract_to}")
            return True
    except Exception as e:
        print(f"Error extracting zip: {e}")
        return False

if __name__ == "__main__":
    extract_zip('nova-landing.zip')
