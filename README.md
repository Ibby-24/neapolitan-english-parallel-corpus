# Neapolitan–English Neural Machine Translator 🇮🇹

A low-resource neural machine translation (NMT) system for Neapolitan → English, built from the ground up,  corpus and all.

## Overview

Neapolitan is a Romance language spoken across Campania and parts of southern Italy. Despite having millions of speakers, it has virtually no existing parallel corpora, no standardized orthography, and minimal NLP tooling.

My goal is to build the full stack: a cleaned parallel corpus of Neapolitan–English sentence pairs, a fine-tuned multilingual translation model, a REST API, and a minimal web interface, all documented and reproducible throughout.

> **Status:** 🚧 Active development: currently working on writing scripts and data entry.

## What's Being Built

| Component | Description |
|---|---|
| 📚 Parallel Corpus | Cleaned, versioned Neapolitan/English sentence pairs with source metadata and confidence flags |
| 🤖 Translation Model | Fine-tuned multilingual model (Helsinki-NLP OPUS-MT or mBART-50) via transfer learning |
| ⚡ REST API | FastAPI service serving translation inference |
| 🌐 Web UI | Minimal single-page React app: type Neapolitan, get English |

## Why This Is Hard

The biggest challenge with this low-resource NMT project is the linguistics of Neapolitan:

- **No standardized orthography** — the same word can appear 5 different ways across sources, requiring deliberate normalization decisions
- **Source scarcity** — corpus data is compiled manually from Neapolitan Wikipedia, Wikisource, bilingual folk song archives, religious texts, and academic sources
- **No synthetic ground truth** — machine translation cannot be used to build training data; entries are human-verified and confidence-flagged
- **Register variation** — folk songs, prose, and formal writing require domain labels to avoid polluting the training signal

## Stack

**Language:** Python 3.10+

**Data**
- Storage: JSON (collection) → Parquet (training pipeline)
- Processing: `pandas`, HuggingFace `datasets`

**Modeling**
- Base model: Helsinki-NLP OPUS-MT or mBART-50
- Framework: HuggingFace `transformers` + PyTorch
- Evaluation: `sacrebleu`
- Experiment tracking: Weights & Biases (`wandb`)

**Serving**
- API: FastAPI
- Frontend: React (minimal)

**Environment:** `venv` + `requirements.txt` · Git throughout

## Project Structure

```
neapolitan-translator/
├── data/
│   ├── raw/               # source data before cleaning
│   ├── cleaned/           # normalized, confidence-flagged pairs
│   └── final/             # finalized, ready to use dataset
├── scripts/
│   └── manual_entry.py    # tkinter gui to input new entries
├── src/
│   ├── api/
│       └── main.py        # FastAPI app
│   ├── model/
│       ├── train.py
│       └── evaluate.py
│   └── data/
|       ├── sources.md
│       └── monolingual.md          
├── schema.md              # corpus design decisions
├── ui/                    # React frontend
├── requirements.txt
├── NOTES.md
└── README.md
```

## Roadmap

- [x] Phase 0 — Environment & Git structure
- [x] Phase 1 — Corpus strategy & source mapping
- [x] Phase 2 — Data collection
- [ ] Phase 3 — Corpus schema design & storage
- [ ] Phase 4 — Data cleaning pipeline
- [ ] Phase 5 — Tokenization & preprocessing
- [ ] Phase 6 — Model fine-tuning
- [ ] Phase 7 — Evaluation (BLEU + human review)
- [ ] Phase 8 — API development
- [ ] Phase 9 — Frontend & deployment
- [ ] Phase 10 — Documentation & writeup

## Getting Started

> Full setup instructions will be added as the project matures. For now:

### Prerequisites

```bash
pip install -r requirements.txt
```

### Running the API (once available)

```bash
uvicorn api.main:app --reload
```

## Data Sources

Corpus data is compiled from:
- [Neapolitan Wikipedia](https://nap.wikipedia.org)
- Wikisource Neapolitan texts
- Bilingual folk song archives
- Religious texts (Neapolitan Bible translations)
- Academic papers with quoted Neapolitan passages

All entries are human-verified.
All entries' translations are either compiled from their respective source or manually translated via Italian.

## Limitations

- BLEU scores on low-resource languages are noisy, human evaluation remains essential
- The corpus is small by MT standards; model performance will reflect this honestly
- Orthographic normalization decisions are documented but opinionated

## Author

Ibrahim Syed — in progress, 2025
