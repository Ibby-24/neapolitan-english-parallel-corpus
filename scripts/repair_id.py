import os
import json

def reindex_corpus_ids():
    print("--- Beginning ID Repair ---")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    raw_path = os.path.normpath(os.path.join(project_root, "data", "raw", "corpus_raw.json"))
    
    if not os.path.exists(raw_path):
        print(f"[ERROR] Could not find raw file at: {raw_path}")
        return

    try:
        with open(raw_path, 'r', encoding='utf-8') as f:
            corpus = json.load(f)
            
        if not isinstance(corpus, list):
            print("[FATAL] File is not a JSON list layout.")
            return

        print(f"Loaded {len(corpus)} total entries. Starting sequential re-indexing...")
        
        #Loop through every entry and calculate its correct ID based on its list position
        for index, entry in enumerate(corpus):
            correct_number = index + 1
            new_id = f"nap_{correct_number:04d}"
            entry["id"] = new_id

        with open(raw_path, 'w', encoding='utf-8') as f:
            json.dump(corpus, f, ensure_ascii=False, indent=4)
            
        print("Success! Every entry in your raw file has been sequentially re-indexed.")
        print(f"IDs now run flawlessly from nap_0001 to nap_{len(corpus):04d}.")

    except Exception as e:
        print(f"[FATAL] ID repair aborted due to error: {e}")

if __name__ == "__main__":
    reindex_corpus_ids()