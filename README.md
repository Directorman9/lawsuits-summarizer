# lawsuits-summarizer
A lawsuit is long (5-100 pages) document detailing a legal case. 
The goal of this project is to develope an endpoint where given a lawsuit document returns its short (less than 500 words) summary. 
The summary should be written a language such that any person not trained in the legal domain can understand the gist of the case

## Challenges.
- Document length: documents far exceeding the standard document length of 512 tokens (approximately 320 words). In our case, we have some documents
that are over 250 pages long. No out-of-the-box summarization models can
summarize such long documents without additional tricks.
