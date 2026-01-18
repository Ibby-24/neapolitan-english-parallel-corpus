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


# SHARING/ACCESS INFORMATION

* Licenses/restrictions placed on the data:  
The dataset is intended for research and educational use. Licensing depends on the original sources of collected text; see data source notes for details.
* Links to publications that cite or use the data: 
None (dataset under development)
* Links to other publicly accessible locations of the data: [Github repo]*
* Links/relationships to ancillary data sets: 
* Was data derived from another source?: Yes 
Sources:
 - Publicly avalaible Neapolitan song lyrics
 - User-generated content (e.g. social media, forums)
 - Parallel examples manually collected and translated
* Recommended citation for this dataset: 
Syed, I. (2026). A Low-Resource Neapolitan-English Parallel Corpus. [Github repo]*

# DATA & FILE OVERVIEW

## File List: *list all files (or folders, as appropriate for dataset organization) contained in the dataset, with a brief description*

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

## Instrument- or software-specific information needed to interpret the data: 
- Python 3.10+
- pandas
- regex
- (tokenization)

* Quality Assurance:
Quality assurance involved manual insepction of aligned sentence pairs and review of common preprocessing errors, particularly those related to accent loss and Italian interface.

# DATA-SPECIFIC INFORMATION FOR: neapolitan_english_parallel.csv 

* Number of variables: | Column1 | Column2 | Column3 |
| --------------- | --------------- | --------------- |
| Item1.1 | Item2.1 | Item3.1 |
| Item1.2 | Item2.2 | Item3.2 |


* Number of variables: 
* Number of cases/rows: 
* Variable List: *list variable name(s), description(s), unit(s) and value labels as appropriate for each*
* Missing data codes: *list code/symbol and definition*
* Specialized formats or other abbreviations used: 
