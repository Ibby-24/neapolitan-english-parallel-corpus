#validate_corpus.py - serves as a strict validator for dataset. 
#reviews data fields and catches formatting errors, illegal vocab injections, and structural corruption


#validate_corpus.py - serves as a validator for the dataset,
#reviews data fields and catches formatting errors, illegal vocab injections,
#structural corruption, and text deduplication issues.

import json
import os
import re
import sys
from datetime import datetime

#controlled domains
VALID_DOMAINS = {
    "informal-digital",
    "encyclopedic-prose",
    "lyric-poetry",
    "theatrical-script",
    "paremiology",
    "historical-literature"
}

VALID_RELIABILITIES = {"High", "Medium", "Low"}

VALID_ORTHOGRAPHIC_PROFILES = {"philological", "vernacular-intuitive"}

VALID_SOURCE_TYPES = {"website", "book", "academic_paper", "audio_recording", "manuscript"}

def is_valid_iso_date(date_str):
    if not isinstance(date_str, str):
        return False
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def normalize_for_dedup(text):
    #lowercases, strips punctuation, and normalizes spaces for fuzzy deduplications
    if not text:
        return ""
    #remove punctuation/symbols and collapses whitespaces
    cleaned = re.sub(r"[^\w\s]", "", text.lower(), flags=re.UNICODE)
    return re.sub(r"\s+", " ", cleaned).strip()

def validate_corpus():
    print("=== Validating Data ===")
    
   
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    processed_path = os.path.normpath(os.path.join(project_root, "data", "processed", "corpus_processed.json"))
    
    if not os.path.exists(processed_path):
        print(f"[ERROR] Processed corpus target missing at location:\n           {processed_path}")
        print("Please execute 'clean_data.py' first to build the processed artifact.")
        sys.exit(1)
        
    try:
        with open(processed_path, 'r', encoding='utf-8') as f:
            corpus = json.load(f)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Malformed JSON structure prevented evaluation: {e}")
        sys.exit(1)
        
    if not isinstance(corpus, list):
        print(f"[ERROR] Root structure validation failed. Expected a JSON List, got {type(corpus).__name__}")
        sys.exit(1)
        
    total_entries = len(corpus)
    print(f"Targeting {total_entries} entries for testing...")


    #tracking variables
    seen_ids = set()
    seen_nap_exact = {}
    seen_nap_normalized = {}

    errors_count = 0
    warnings_count = 0
    
    #clean up report printing
    def log_issue(entry_id, idx, severity, field, message):
        nonlocal errors_count, warnings_count
        label = f"[{severity.upper()}]"
        identifier = f"ID: {entry_id}" if entry_id else f"Index: {idx}"
        print(f"{label:<10} {identifier:<12} | Field: {field:<20} | {message}")
        if severity.lower() == "error":
            errors_count += 1
        else:
            warnings_count += 1

    #evaluate field by field
    for idx, entry in enumerate(corpus):
        if not isinstance(entry, dict):
            log_issue(None, idx, "error", "root", "Entry is completely malformed (not a JSON Object/Dict).")
            continue
            
        entry_id = entry.get("id")

        #ID validation
        if not entry_id:
            log_issue(None, idx, "error", "id", "ID field is missing or empty.")
        elif not isinstance(entry_id, str):
            log_issue(None, idx, "error", "id", f"ID must be a string. Got type: {type(entry_id).__name__}")
        else:
            if entry_id in seen_ids:
                log_issue(entry_id, idx, "error", "id", "Duplicate ID collision detected! Already assigned elsewhere.")
            seen_ids.add(entry_id)
            if not re.match(r"^nap_\d{4}$", entry_id):
                log_issue(entry_id, idx, "warning", "id", f"ID style format mismatch. Expected shape 'nap_XXXX', got '{entry_id}'")

        #Neapolitan Text Validation
        nap_text = entry.get("nap")
        if nap_text is None:
            log_issue(entry_id, idx, "error", "nap", "Field is completely missing.")
        elif not isinstance(nap_text, str):
            log_issue(entry_id, idx, "error", "nap", f"Field is not a string. Got type: {type(nap_text).__name__}")
        elif not nap_text.strip():
            log_issue(entry_id, idx, "error", "nap", "Field contains an empty or whitespace-only string.")
        else:
            #Exact Deduplication Check
            if nap_text in seen_nap_exact:
                log_issue(
                    entry_id, idx, "warning", "nap", 
                    f"Exact duplicate Neapolitan text detected! Matches text in entry '{seen_nap_exact[nap_text]}'."
                )
            else:
                seen_nap_exact[nap_text] = entry_id

            #Normalized Deduplication Check
            norm_nap = normalize_for_dedup(nap_text)
            if norm_nap in seen_nap_normalized and nap_text not in seen_nap_exact:
                log_issue(
                    entry_id, idx, "warning", "nap", 
                    f"Near-duplicate text overlap detected! Content strongly matches entry '{seen_nap_normalized[norm_nap]}'."
                )
            else:
                seen_nap_normalized[norm_nap] = entry_id

        #English Text Validation
        eng_text = entry.get("eng")
        if eng_text is None:
            log_issue(entry_id, idx, "error", "eng", "Field is completely missing.")
        elif not isinstance(eng_text, str):
            log_issue(entry_id, idx, "error", "eng", f"Field is not a string. Got type: {type(eng_text).__name__}")
        elif not eng_text.strip():
            log_issue(entry_id, idx, "error", "eng", "Field contains an empty or whitespace-only string.")

        #Italian Intermediate Schema Check            
        if "ita_intermediary" in entry:
            log_issue(entry_id, idx, "error", "ita_intermediary", "Typo alert! Field key spelled as 'intermediary' instead of schema standard 'ita_intermediate'.")
            
        ita_text = entry.get("ita_intermediate")
        if ita_text is not None and not isinstance(ita_text, str):
            log_issue(entry_id, idx, "error", "ita_intermediate", f"Must be a string or explicit null. Got type: {type(ita_text).__name__}")

        #Metadata & Source Validation
        man_trans = entry.get("manually_translated")
        if man_trans is None:
            log_issue(entry_id, idx, "error", "manually_translated", "Field is missing.")
        elif not isinstance(man_trans, bool):
            log_issue(entry_id, idx, "error", "manually_translated", f"Must be a Boolean (true/false). Got type: {type(man_trans).__name__}")

        source = entry.get("source")
        if not source:
            log_issue(entry_id, idx, "error", "source", "Source block object is missing or null.")
        elif not isinstance(source, dict):
            log_issue(entry_id, idx, "error", "source", f"Source block must be an object. Got type: {type(source).__name__}")
        else:
            s_type = source.get("type")
            if not s_type:
                log_issue(entry_id, idx, "error", "source.type", "Source type classification missing.")
            elif s_type not in VALID_SOURCE_TYPES:
                log_issue(entry_id, idx, "error", "source.type", f"Invalid value '{s_type}'. Allowed: {list(VALID_SOURCE_TYPES)}")
            
            s_ref = source.get("reference")
            if not s_ref or not isinstance(s_ref, str) or not s_ref.strip():
                log_issue(entry_id, idx, "error", "source.reference", "Reference string or URL is missing or empty.")
                
            s_acc_date = source.get("accessed_date")
            if s_acc_date is not None and not is_valid_iso_date(s_acc_date):
                log_issue(entry_id, idx, "error", "source.accessed_date", f"Value '{s_acc_date}' is not a valid YYYY-MM-DD ISO date string.")

        #Controlled variables        
        domain = entry.get("domain")
        if not domain:
            log_issue(entry_id, idx, "error", "domain", "Domain setting missing.")
        elif domain not in VALID_DOMAINS:
            log_issue(entry_id, idx, "error", "domain", f"Illegal vocabulary usage: '{domain}'. Allowed: {list(VALID_DOMAINS)}")

        reliability = entry.get("reliability")
        if not reliability:
            log_issue(entry_id, idx, "error", "reliability", "Reliability ranking missing.")
        elif reliability not in VALID_RELIABILITIES:
            log_issue(entry_id, idx, "error", "reliability", f"Illegal vocabulary usage: '{reliability}'. Allowed: {list(VALID_RELIABILITIES)}")

        ortho = entry.get("orthographic_profile")
        if not ortho:
            log_issue(entry_id, idx, "error", "orthographic_profile", "Orthographic profile missing.")
        elif ortho not in VALID_ORTHOGRAPHIC_PROFILES:
            log_issue(entry_id, idx, "error", "orthographic_profile", f"Illegal vocabulary usage: '{ortho}'. Allowed: {list(VALID_ORTHOGRAPHIC_PROFILES)}")

        notes = entry.get("notes")
        if notes is not None and not isinstance(notes, str):
            log_issue(entry_id, idx, "error", "notes", f"Must be a string or explicit null. Got type: {type(notes).__name__}")

        added_date = entry.get("date_added")
        if not added_date:
            log_issue(entry_id, idx, "error", "date_added", "Missing timeline insertion timestamp.")
        elif not is_valid_iso_date(added_date):
            log_issue(entry_id, idx, "error", "date_added", f"Value '{added_date}' is not a valid YYYY-MM-DD ISO format string.")


    #AUDIT RESULTS
    print("\n" + "="*60)
    print("AUDIT RESULTS SUMMARY")
    print("="*60)
    print(f"Total Reviewed Entries  : {total_entries}")
    print(f"Critical Schema Errors  : {errors_count}")
    print(f"Systematic Warnings     : {warnings_count}")
    print("="*60)
    
    if errors_count > 0:
        print("[STATUS] FAILED: Structural violations found. Do not pass this file downstream.")
        sys.exit(1)
    else:
        print("[STATUS] PASSED: Dataset matches your schema specifications perfectly.")
        sys.exit(0)

if __name__ == "__main__":
    validate_corpus()