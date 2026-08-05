#corpus_clean.py - will clean data entries of common edge cases and irregularities noticed during data collection

import os
import json
import re
import unicodedata
import sys

def clean_text_field(text):
    if not isinstance(text, str) or not text:
        return text
    
    #standardize all variants of curly/smart/backtick apostrophes to straight ones
    text = text.replace("’", "'")
    text = text.replace("`", "'")
    text = text.replace("‘", "'")
    text = text.replace("ʼ", "'")
    
    #fix leftover manual quote escape backslashes (Double-check fallback)
    text = text.replace('\\"', '"')
    
    #standardize Ellipses variations (converts single-character '…' to standard '...')
    text = text.replace("…", "...")
    
    #standardize Unicode Accent Encoding (NFC Normalization)
    text = unicodedata.normalize('NFC', text)
    
    #clean up erratic spacing around apostrophe clusters
    #ex input: "avit'    'a fá"
    #ex output: "avit' 'a fá"
    #regex logic: Finds an apostrophe, 2 or more whitespace characters, and a trailing apostrophe
    text = re.sub(r"'\s{2,}'", "' '", text)
    
    #clean up accidental general double-spaces left behind by manual typing
    text = re.sub(r" {2,}", " ", text)
    
    return text.strip()

def process_dataset():
    print("--- Beginning Data Cleaning ---")
    
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    input_path = os.path.normpath(os.path.join(project_root, "data", "raw", "corpus_raw.json"))
    output_path = os.path.normpath(os.path.join(project_root, "data", "processed", "corpus_processed.json"))
    

    if not os.path.exists(input_path):
        print(f"[ERROR] Critical failure: Could not find raw corpus file at absolute location:\n        {input_path}")
        sys.exit(1)

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            corpus = json.load(f)
            
        #safeguards the engine against empty files, invalid JSON roots, or dictionary conversions.
        if not isinstance(corpus, list):
            expected_type = type(corpus).__name__
            print("[ERROR] Structural Mismatch: Expected JSON root to be a LIST of entries.")
            print(f"              Instead, the file parsed as a dictionary root or primitive: '{expected_type}'")
            sys.exit(1)
            
        print(f"Loaded {len(corpus)} entries successfully from raw data.")
        
        #process entries
        processed_count = 0
        text_fields_to_clean = ['nap', 'eng', 'ita_intermediate']
        
        for entry in corpus:
            if not isinstance(entry, dict):
                print(f"[WARNING] Skipping malformed entry layout at index {processed_count}: entry is not an object.")
                continue
                
            for field in text_fields_to_clean:
                #only clean the field if it explicitly exists and holds string content (skips NULL/None values safely)
                if field in entry and entry[field] is not None:
                    entry[field] = clean_text_field(entry[field])
                    
            processed_count += 1

        #build execution folder tree if it doesn't exist
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Generated target environment folder: {output_dir}")

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(corpus, f, ensure_ascii=False, indent=4)
            
        print(f"Success! All {processed_count} entries processed and standardized.")
        print(f"Pristine destination file updated at:\n{output_path}")
        
    except json.JSONDecodeError as je:
        print(f"[FATAL ERROR] Malformed JSON syntax in raw file: {je}")
        sys.exit(1)
    except Exception as e:
        print(f"[FATAL ERROR] Pipeline failed unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    process_dataset()