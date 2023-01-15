import torch, os, subprocess, codecs, random, requests
import pytesseract, time, glob, pdf2image, re, validations as v
from transformers import LEDTokenizer, LEDForConditionalGeneration
from summarizer.sbert import SBertSummarizer
from itertools import chain
from werkzeug.utils import secure_filename


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
content_model_name = "allenai/led-base-16384-multi_lexsum-source-long"
title_model_name = "allenai/led-base-16384-multi_lexsum-source-tiny"
tokenizer = LEDTokenizer.from_pretrained(content_model_name)
content_model = LEDForConditionalGeneration.from_pretrained(content_model_name).to(device)
title_model = LEDForConditionalGeneration.from_pretrained(title_model_name).to(device)
stransformer_model = SBertSummarizer('paraphrase-MiniLM-L6-v2')
upload_folder = "static/uploads"

def current_time():
    ts = str(time.time())
    ts = "".join(ts.split('.'))
    return ts
    

def download_file(url:str):
    '''
    Downloads a file from the web
    '''
    command = f"wget {url}"
    subprocess.call(command, shell=True)


def upload_file(file:str):
    '''
    Uploads a file to server
    '''
    filename = secure_filename(file.filename)
    filename = current_time() + "." + filename.rsplit('.', 1)[1].lower()
    
    file.save(os.path.join(upload_folder, filename))
    file.close()
    
    return filename



def pdf_to_text(file_name):
    '''
    Extracts text from pdf
    '''
    pages = pdf2image.convert_from_path(file_name)

    text = ""
    for page in pages:
        #page = orient_page(page) 
        page_text = pytesseract.image_to_string(page, lang = 'eng',config='--psm 6')
        text = text + " " + page_text
        
    return text
    
    
def remove_file(file_name):
    '''
    Deletes a pdf file from the working folder
    '''
    os.popen(f"rm {file_name}")
    
    
def clean_line(line:str)->str:
    line = "".join([char for char in line if char not in "|"])
    line = line.split()
    line = [word for word in line if len(word) <= 20]
    try:
       if line[0].isdigit() or line[0][:-1].isdigit() or len(line[0][:-1])==1: #Line number of letter.
          return " ".join(line[1:])
       else:
          return " ".join(line)
    except:
       return ""
         
def paragraph_to_sentences(paragraph):
    lines = paragraph.split('\n')
    text = ""
    for line in lines:
        line = line.strip()
        if not line or line.isupper(): continue
        text = text + " " + clean_line(line)
        
    sentences =  [e+'.' for e in text.split('. ')]
    sentences = [sentence for sentence in sentences if len(sentence.split()) > 10 and len(sentence.split()) < 50]    
    sentences = [s.strip() for s in sentences]
    return sentences
                
def summarize_extractively(doc:str)->str:
    '''
    Extracts informative sentences from a long text.
    '''
    paragraphs = re.split('\n{2,}', doc)
    sentences = [paragraph_to_sentences(paragraph) for paragraph in paragraphs]
    sentences = list(chain.from_iterable(sentences))
    
    if len(sentences) > 50:
       s_limit = 100
       chunk_size = 10
       sentences_per_chunk = 5
       
       sentences = sentences[0:s_limit]
       chunks = [sentences[i:i + chunk_size] for i in range(0, len(sentences), chunk_size)]
       chunks = [" ".join(chunk) for chunk in chunks]
       chunks = [stransformer_model(chunk, num_sentences=sentences_per_chunk) for chunk in chunks]
       summary = "\n".join(chunks)
    else:   
       summary = " ".join(sentences)
    
    return summary
    
        
      

def summarize_abstractively(prompt:str):
    max_summary_length = 500
    
    input_ids = tokenizer([prompt], return_tensors="pt")["input_ids"]

    prediction = content_model.generate(input_ids, max_new_tokens=max_summary_length)[0]

    summary = tokenizer.decode(prediction, skip_special_tokens=True)
    
    return summary
    

def generate_heading(prompt:str):
    max_summary_length = 30
    
    input_ids = tokenizer([prompt], return_tensors="pt")["input_ids"]

    prediction = title_model.generate(input_ids, max_new_tokens=max_summary_length)[0]

    summary = tokenizer.decode(prediction, skip_special_tokens=True)
    
    return summary
