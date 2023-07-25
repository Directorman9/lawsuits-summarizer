# lawsuits-summarizer
A lawsuit is long (5-100 pages) document detailing a legal case. 
The goal of this project is to develope an endpoint where given a lawsuit document returns its short (less than 500 words) summary. 
The summary should contain all important details and be written a language such that any person not trained in the legal domain can understand.

## Challenges.
- Document length: lawsuit far exceeding the standard document length (512-16384 tokens) that can be processed by a pretained language model.
- Domain specificity: The summarization model needs not only to be able to handle long documents but also to comprehend the legal language.
