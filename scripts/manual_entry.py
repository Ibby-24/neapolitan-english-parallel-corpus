####manual_entry.py
####input new entry into json dataset


import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

DATA_FILE = "data/raw/corpus_raw.json"

#options for specific labels
PROFILES = ["philological", "vernacular-intuitive"]
DOMAINS = [
    "informal-digital",
    "encyclopedic-prose",
    "lyric-poetry",
    "theatrical-script",
    "paremiology",
    "historical-literature"
]

#Open/load json file
def load_existing_corpus():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        #fallback if file exists but is empty or corrupt
        return []

#insert new entry
def save_entry(event=None):
    #gather UI inputs, append to JSON file, and reset field
    raw_text = text_entry.get().strip()
    profile = profile_combobox.get()
    domain = domain_combobox.get()

    #Data Validation
    if not raw_text:
        messagebox.showwarning("Input Error", "The raw text field cannot be empty.")
        text_entry.focus_set()
        return

    #read existing data to determine next sequential id
    corpus = load_existing_corpus()
    next_index = len(corpus) + 1
    generated_id = f"nap_{next_index:04d}"
    
    #build unified schema object
    new_record = {
        "id": generated_id,
        "raw_text": raw_text,
        "normalized_text": "", #left empty for later script operation
        "orthographic_profile": profile,
        "domain_type": domain,
        "metadata": {
            "annotated_via": "manual_entry_gui"
        }
    }

    #commit to disk
    corpus.append(new_record)
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(corpus, file, indent=4, ensure_ascii=False)

            status_label.config(text=f"Success: Saved {generated_id}", foreground="green")
            text_entry.delete(0, tk.END)
            text_entry.focus_set()

    except Exception as e:
        messagebox.showerror("Write Error", f"Could not write data to file:\n{str(e)}")

#gui window initialization
root = tk.Tk()
root.title("Neapolitan Corpus Builder - Data Entry")
root.geometry("550x300")
root.resizable(False, False)

#main container frame
frame = ttk.Frame(root, padding="20")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

#UI layout
#Row 0: Raw text inputs
ttk.Label(frame, text="Raw Text Line:").grid(row=0, column=0, sticky=tk.W, pady=5)
text_entry = ttk.Entry(frame, width=45)
text_entry.grid(row=0, column=1, columnspan=2, sticky=tk.W, pady=5)
text_entry.focus_set()

#Row 1: Orthographic Profile Selector
ttk.Label(frame, text="Orthographic Profile:").grid(row=1, column=0, sticky=tk.W, pady=5)
profile_combobox = ttk.Combobox(frame, values=PROFILES, width=25, state="readonly")
profile_combobox.grid(row=1, column=1, sticky=tk.W, pady=5)
profile_combobox.set(PROFILES[0])

#Row 2: Domain Type Selector
ttk.Label(frame, text="Domain Type:").grid(row=2, column=0, sticky=tk.W, pady=5)
domain_combobox = ttk.Combobox(frame, values=DOMAINS, width=25, state="readonly")
domain_combobox.grid(row=2, column=1, sticky=tk.W, pady=5)
domain_combobox.set(DOMAINS[0])

#Row 3: Action Buttons
submit_btn = ttk.Button(frame, text="Submit (Enter)", command=save_entry)
submit_btn.grid(row=3, column=1, sticky=tk.W, pady=20)
quit_btn = ttk.Button(frame, text="Finish & Close", command=root.destroy)
quit_btn.grid(row=3, column=2, sticky=tk.E, pady=20)

#Row 4: Dynamic Status Notification Strip
status_label = ttk.Label(frame, text="System Ready. Awaiting first input...", font=("Arial", 10, "italic"))
status_label.grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=10)

#Keyboard Shortcut: binds 'Enter" key to save_entry function
root.bind('<Return>', save_entry)

#start UI event loop
root.mainloop()
