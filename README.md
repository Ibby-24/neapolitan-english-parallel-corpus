This readme file was generated on 2026-01-28 by Ibrahim Syed

# GENERAL INFORMATION

* Title of Dataset: 
A Low-Resource Neapolitan-English Parallel Corpus

## Author / Principle Investigator
Name: Ibrahim Syed 
ORCID: N/A
Institution: University of Illinois Chicago (Undergraduate)
Address: Hinsdale, IL, USA
Email: ibrahims4224@gmail.com 

* Date of data collection: 2026-01-14 to (ongoing)
* Geographic location of data collection: Campania, Italy
* Funding sources: None (independent student project)


# Project Goal 
To my knowledge, there are no publicly available Neapolitan-English parallel datasets of meaningful size. Searches in major corpora repositories (e.g. OPUS, Tatoeba, Wikipedia) yield at most small examples. Additionally, LLMs such as OpenAI's ChatGPT or Google's Gemini tend to mistranslate many low-resource languages. This dataset, containing X examples, represents a means to enrich the list of available resources for this heavily underrepresented language. The goal of this project is to collect and process lines of Neapolitan, a low-resource language, to create a translator from Neapolitan to English. Because of Neapolitan's orthography, regional variation, and low resources, it is more difficult create a standard dataset for it to translate. The goal of this project is to build a dataset that can lead to some solution in standardizing thousands of texts, deal with problems like accents, context, and irregularity in everyday language, to create an accurate Neapolitan to English translator. The goal isn't perfect accuracy, but rather create a beginning point and experiment with datasets.

# Current State 
Currently, the dataset is being filled in. Data is being found from various sources online and collected. 

# Coming Next 
Once data has been collected, the model will be built and trained on the data. More data will continue to be collected over time.


# SHARING/ACCESS INFORMATION

* Licenses/restrictions placed on the data:  
The dataset is intended for research and educational use. Licensing depends on the original sources of collected text; see data source notes for details.
* Links to publications that cite or use the data: 
None (dataset under development)
* Links to other publicly accessible locations of the data: https://github.com/Ibby-24
* Links/relationships to ancillary data sets: 
* Was data derived from another source?: Yes 
Sources:
 - Publicly available Neapolitan song lyrics
 - User-generated content (e.g. social media, forums)
 - Parallel examples manually collected and translated
* Recommended citation for this dataset: 
Syed, I. (2026). A Low-Resource Neapolitan-English Parallel Corpus. https://github.com/Ibby-24

Some content is derived from Wikipedia and is shared under CC BY-SA.

# DATA & FILE OVERVIEW

## File List:

data/
  raw/      Raw collected Neapolitan and English text
  processed/      Normalized and aligned parallel data

src/
  preprocessing.py      Text normalization and cleaning scripts
  baseline_nt.py      Baseline translation experiments

notes/
  linguistic_notes.md     Observations on dialectal variation and orthography

* Relationship between files, if important: 
Raw data is collected from multiple sources and stored in data/raw/.
Processing scripts normalize orthography and align sentence pairs, producing data/processed/ files used for modeling

* Are there multiple versions of the dataset?
No. Initial version under active development.

# METHODOLOGICAL INFORMATION

## Description of methods used for collection/generation of data: 
Data was collected from publicly available Neapolitan-language sources, including song lyrics, informal written text, and manually curated examples. Parallel English translations were obtained through manual translation and alignment.


## Methods for processing the data: 
Processing involved normalization of orthographic variation (e.g. accent usage, spelling variants), removal of non-linguistic artifacts, and sentence-level alignment between Neapolitan and English. Multiple normalization were explored to balance linguistic variation with model compatability.

## Instruments: 
- Python 3.10+
- pandas
- regex
- (tokenization)

* Quality Assurance:
Quality assurance involved manual insepction of aligned sentence pairs and review of common preprocessing errors, particularly those related to accent loss and Italian interface.

# DATA-SPECIFIC INFORMATION FOR: neapolitan_english_parallel.csv 

* Number of variables: 3

* Number of rows: numRows

Variable List:
- neapolitan_text: Original Neapolitan sentence
- english_text: Corresponding English translation
-  source: Origin of the sentence

* Missing data codes:
- NA: translation unavailable or unclear

