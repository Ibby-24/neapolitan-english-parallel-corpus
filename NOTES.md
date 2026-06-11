#############################################
#Schema definitions and types
"id" Documentation:
Will be formatted as a structured ID

"nap" Documentation:
Contains raw neapolitan text

"eng" Documentation:
Contains the English translation of the Neapolitan text

"ita_intermediary" Documentation:
Contains Italian translation of Neapolitan text if available. This field will be entered either if the source contained the Standard Italian translation along with the English translation, or if the source only contained the Neapolitan to Standard Italian parallel and the text was then manually translated to English.

"manually_translated" Documentation:
Set to true if the source only contains the Neapolitan to Standard Italian translation. Indicates if English translation was manually translated.

"source" Documentation:
- "type": type of source (website, book, academic_paper, etc.)
- "reference": a URL or citation string
- "accessed_date": Date of accessing website

"domain" Documentation:
Contains domain type from the following defined list:
- informal-digital: Modern, user-generated text from the internet. This includes social media posts, blog comments, messages, and forum posts. High frequency of shortcuts, missing accents, heavy Italian code-switching, heavy inclusion of slang and vernacular
- encyclopedic-prose: Formally structured, objective text written to inform or educate. Primary sourced from portals like Neapolitan Wikipedia, digital encyclopedias, or contemporary news articles written in Neapolitan. Features high vocabulary diversity, structured syntax, and usually a highly disciplined attempt at a unified philological or curated web standard
- lyric-poetry: Text written for artistic, rhythmic, or musical performances. This covers Neapolitan songs, contemporary music lyrics of all genres, and formal poetry. Features heavy use of truncation to fit musical meters, rich emotional metaphors, and a mix of historical philological structures preserved via artistic tradition. Contemporary music will feature heavy amounts of slang, cultural notions, and a general informal speech.
- theatrical-script: Written dialogue meant for stage, cinema, or television. This includes plays and modern script transcriptions. As these are intended to be read aloud, it mimics natural spoken cadences. It relies heavily on apostrophes to show where actors should drop vowels or merge words, almost strictly following the "venacular-intuitive" path.
- paremiology: Traditional, short, fixed expressions passed down through oral culture. This includes proverbs, idioms, and fiddles. These tend to be more static over time periods, and may even contain archaisms (words no longer used in daily speech) or rigid rhythmic patterns from centuries ago.
- historical-literature: Formal narrative prose, historical accounts, or translated classics. These tend to be more complex, have archaic grammar, dense morphology, and strict adherence to historical orthographies, potentially devoid of the influence of a Standardized Italian.

"reliability" Documentation:
Reliability will be defined and categorized as the following three:
- High: direct NAP->ENG from a verified bilingual source, or from a professional academic translation
- Medium: NAP->ITA (manually verified) -> ENG (manually translated), single personal translation, or indirect alignment from parallel source articles
- Low: machine-assisted, uncertain alignment, orthographically ambiguous score, or reconstructed from context


"orthographic_profile" Documentation:
To account for the highly unstandardized nature of the Neapolitan language, I will be categorizing all entries are one of two orthographic profiles: philological or vernacular-intuitive. The distinction will be determined by the following definitions:
- philological: Text that strictly adheres to historical etymology, utilizes complex accent systems to denote vowel openness and explicitly preserves syntactic gemination. Avoids excessive, non-etymological apostrophes
- vernacular-intuitive: Text driven by oral immediacy, theatrical scripts, song lyrics, or casual communication. Relies heavily on Standard Italian spelling conventions as a baseline. Contains high frequency of apostrophes to mark casual elision and relies on pheonetic guesswork rather than strict etymological rules for consonant doubling.

"notes" Documentation:
This field will contain any extra notes or flags that may be a problem to solve at a later time, or a note to consider about the specific entry. Any orthographic anomalies will also be written down in this field. Otherwise, this field will be left as NULL.

"date_added" Documentation:
Tracks growth of corpus and the session an entry was added in the case of a systematic error found later on. Will be in ISO format as a string.
