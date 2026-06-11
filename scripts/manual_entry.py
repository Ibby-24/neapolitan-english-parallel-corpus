#manual_entry.py - A Tkinter-based GUI for manual data entry into the Neapolitan corpus JSON file.

from datetime import datetime
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "..", "data", "raw", "corpus_raw.json")

#data schema options
SOURCE_TYPES = ["website", "book", "academic paper", "oral tradition", "other"]
DOMAINS = [
    "informal-digital",
    "encyclopedic-prose",
    "lyric-poetry",
    "theatrical-script",
    "paremiology",
    "historical-literature"
]
RELIABILITY_OPTIONS = ["High", "Medium", "Low"]
PROFILES = ["philological", "vernacular-intuitive"]


def load_existing_corpus():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def calculate_next_id(corpus):
    max_num = 0
    for entry in corpus:
        entry_id = entry.get("id", "")
        if entry_id.startswith("nap_"):
            try:
                num_part = int(entry_id.split("_")[1])
                if num_part > max_num:
                    max_num = num_part
            except (IndexError, ValueError):
                continue
    return f"nap_{(max_num + 1):04d}"


def save_entry(event=None):
    #required text validation guardrail
    nap_text = nap_var.get().strip()
    if not (nap_text):
        messagebox.showwarning("Validation Error", "'nap' (Neapolitan text) cannot be empty.")
        nap_entry.focus_set()
        return
    
    eng_text = eng_var.get().strip()
    if not (eng_text):
        messagebox.showwarning("Validation Error", "'eng' (English text) cannot be empty.")
        eng_entry.focus_set()
        return

    #convert empty fields to None (translates to JSON null)
    def clean_val(variable):
        val = variable.get().strip()
        return val if val != "" else None

    corpus = load_existing_corpus()
    generated_id = calculate_next_id(corpus)

    #compile the unified dictionary structure with automated null support
    new_record = {
        "id": generated_id,
        "nap": nap_text,
        "ita_intermediate": clean_val(ita_var),
        "eng": clean_val(eng_var),
        "manually_translated": manual_trans_var.get(),
        "source": {
            "type": source_type_var.get(),
            "reference": clean_val(source_ref_var),
            "accessed_date": clean_val(source_acc_date_var)
        },
        "domain": domain_var.get(),
        "reliability": reliability_var.get(),
        "orthographic_profile": profile_var.get(),
        "notes": clean_val(notes_var),
        "date_added": date_added_var.get().strip()
    }

    #append and commit to local storage
    corpus.append(new_record)
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(corpus, file, indent=4, ensure_ascii=False)
        
        status_label.config(text=f"Successfully recorded: {generated_id}", foreground="green")
        reset_input_fields()
        
    except Exception as e:
        messagebox.showerror("File Error", f"Failed to commit transaction to disk:\n{str(e)}")


def reset_input_fields():
    nap_var.set("")
    ita_var.set("")
    eng_var.set("")
    manual_trans_var.set(False)
    #source_ref_var.set("")
    #source_acc_date_var.set("")
    #notes_var.set("")
    
    #auto-populate today's current ISO date format
    date_added_var.set(datetime.now().strftime("%Y-%m-%d"))
    
    #direct keyboard cursor straight back to initial text window
    nap_entry.focus_set()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Neapolitan Corpus Manual Entry Interface")
    root.geometry("620x560")
    root.resizable(False, False)

    main_frame = ttk.Frame(root, padding="15")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    nap_var = tk.StringVar()
    ita_var = tk.StringVar()
    eng_var = tk.StringVar()
    manual_trans_var = tk.BooleanVar(value=False)

    source_type_var = tk.StringVar()
    source_ref_var = tk.StringVar()
    source_acc_date_var = tk.StringVar()

    domain_var = tk.StringVar()
    reliability_var = tk.StringVar()
    profile_var = tk.StringVar()
    notes_var = tk.StringVar()
    date_added_var = tk.StringVar()


    #Row 0: Neapolitan (Textbox)
    ttk.Label(main_frame, text="Neapolitan (nap):").grid(row=0, column=0, sticky=tk.W, pady=4)
    nap_entry = ttk.Entry(main_frame, textvariable=nap_var, width=50)
    nap_entry.grid(row=0, column=1, sticky=tk.W, pady=4)

    #Row 1: Italian Intermediate (Textbox)
    ttk.Label(main_frame, text="Italian Translation (ita_intermediate):").grid(row=1, column=0, sticky=tk.W, pady=4)
    ita_entry = ttk.Entry(main_frame, textvariable=ita_var, width=50)
    ita_entry.grid(row=1, column=1, sticky=tk.W, pady=4)

    #Row 2: English (Textbox)
    ttk.Label(main_frame, text="English Translation (eng):").grid(row=2, column=0, sticky=tk.W, pady=4)
    eng_entry = ttk.Entry(main_frame, textvariable=eng_var, width=50)
    eng_entry.grid(row=2, column=1, sticky=tk.W, pady=4)

    #Row 3: Manually Translated (Checkbox)
    ttk.Label(main_frame, text="Manually Translated:").grid(row=3, column=0, sticky=tk.W, pady=4)
    manual_checkbox = ttk.Checkbutton(main_frame, text="True (Leave empty for False)", variable=manual_trans_var)
    manual_checkbox.grid(row=3, column=1, sticky=tk.W, pady=4)

    #Row 4: Source -> Type, Reference, Accessed Date
    source_subframe = ttk.LabelFrame(main_frame, text="Source Attribution", padding="10")
    source_subframe.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=10, pady=8)

    ttk.Label(source_subframe, text="Type:").grid(row=0, column=0, sticky=tk.W, padx=2)
    source_dropdown = ttk.Combobox(source_subframe, textvariable=source_type_var, values=SOURCE_TYPES, width=15, state="readonly")
    source_dropdown.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
    source_dropdown.set(SOURCE_TYPES[0])

    ttk.Label(source_subframe, text="Reference:").grid(row=0, column=2, sticky=tk.W, padx=2)
    source_ref_entry = ttk.Entry(source_subframe, textvariable=source_ref_var, width=18)
    source_ref_entry.grid(row=0, column=3, sticky=tk.W, padx=5, pady=2)

    ttk.Label(source_subframe, text="Accessed Date:").grid(row=1, column=0, sticky=tk.W, padx=2)
    source_date_entry = ttk.Entry(source_subframe, textvariable=source_acc_date_var, width=15)
    source_date_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=4)

    #Row 5: Domain (Dropdown)
    ttk.Label(main_frame, text="Domain Category:").grid(row=5, column=0, sticky=tk.W, pady=4)
    domain_dropdown = ttk.Combobox(main_frame, textvariable=domain_var, values=DOMAINS, width=30, state="readonly")
    domain_dropdown.grid(row=5, column=1, sticky=tk.W, pady=4)
    domain_dropdown.set(DOMAINS[0])

    #Row 6: Reliability (Dropdown)
    ttk.Label(main_frame, text="Data Reliability:").grid(row=6, column=0, sticky=tk.W, pady=4)
    reliability_dropdown = ttk.Combobox(main_frame, textvariable=reliability_var, values=RELIABILITY_OPTIONS, width=15, state="readonly")
    reliability_dropdown.grid(row=6, column=1, sticky=tk.W, pady=4)
    reliability_dropdown.set(RELIABILITY_OPTIONS[0])

    #Row 7: Orthographic Profile (Dropdown)
    ttk.Label(main_frame, text="Orthographic Profile:").grid(row=7, column=0, sticky=tk.W, pady=4)
    profile_dropdown = ttk.Combobox(main_frame, textvariable=profile_var, values=PROFILES, width=25, state="readonly")
    profile_dropdown.grid(row=7, column=1, sticky=tk.W, pady=4)
    profile_dropdown.set(PROFILES[0])

    #Row 8: Notes (Textbox)
    ttk.Label(main_frame, text="Notes:").grid(row=8, column=0, sticky=tk.W, pady=4)
    notes_entry = ttk.Entry(main_frame, textvariable=notes_var, width=50)
    notes_entry.grid(row=8, column=1, sticky=tk.W, pady=4)

    #Row 9: Date Added (Textbox)
    ttk.Label(main_frame, text="Date Added (ISO Format):").grid(row=9, column=0, sticky=tk.W, pady=4)
    date_entry = ttk.Entry(main_frame, textvariable=date_added_var, width=20)
    date_entry.grid(row=9, column=1, sticky=tk.W, pady=4)


    submit_btn = ttk.Button(main_frame, text="Submit Entry (Enter)", command=save_entry)
    submit_btn.grid(row=10, column=1, sticky=tk.W, pady=15)

    close_btn = ttk.Button(main_frame, text="Finish & Close", command=root.destroy)
    close_btn.grid(row=10, column=1, sticky=tk.E, pady=15)

    status_label = ttk.Label(main_frame, text="Console Status: Ready for collection loop.", font=("Arial", 10, "italic"))
    status_label.grid(row=11, column=0, columnspan=2, sticky=tk.W, pady=5)

    root.bind('<Return>', save_entry)
    reset_input_fields()

    root.mainloop()