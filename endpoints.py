from flask import Blueprint, request, make_response, render_template
from utils import *
import requests, random, threading, time


endpoints_blueprint = Blueprint('endpoints_blueprint', __name__)


SUCCESS_CODE = 200
BAD_REQUEST = 400
INTERNAL_SERVER_ERROR = 500


progress_tracker = None

class ProgressTracker(threading.Thread):
    def __init__(self, inpt_text=None, inpt_file=None):
        self.progress = "Starting"
        self.abstractive_summary = ""
        self.heading = ""
        self.inpt_text = inpt_text
        self.inpt_file = inpt_file
        super().__init__()

    def run(self):     
        if self.inpt_text is not None:   
           file_name = self.inpt_text.split('/')[-1]   
             
           if file_name.split('.')[-1].lower() == 'pdf':
              self.progress = "Downloading file..."
              download_file(self.inpt_text)
        
              self.progress = "converting pdf to text...."
              text = pdf_to_text(file_name)        
              remove_file(file_name)
           else:
              text = self.inpt_text
              
        elif self.inpt_file is not None:
         
           self.progress = "converting pdf to text...."
           text = pdf_to_text(self.inpt_file)        
           remove_file(self.inpt_file)
        
              
        self.progress = "summarizing extractively...."
        extractive_summary = summarize_extractively(text)

        
        self.progress = "summarizing abstractively...."
        self.abstractive_summary = summarize_abstractively(extractive_summary)
        self.abstractive_summary = remove_incomplete_sentence(self.abstractive_summary)  


        self.progress = "Generating heading...."
        self.heading = generate_heading(extractive_summary)
        self.heading = remove_incomplete_sentence(self.heading)
        
        self.progress = "finished"

        
            
@endpoints_blueprint.route('/', methods=['GET'])
def index():
    return render_template('summarizer.html')



@endpoints_blueprint.route('/summarize',  methods=['POST'])
def summarize():

    global progress_tracker
     
    if 'file' in request.files: 
       file = request.files['file']
       filename = file.filename
       
       file.save(filename)
       file.close()
       
       progress_tracker = ProgressTracker(inpt_file = filename)
     
    else:
       data = request.get_json()
       inpt = data.get('inpt')

       inpt = inpt.strip()
       progress_tracker = ProgressTracker(inpt_text = inpt)
       
    summary = progress_tracker.start()   
    resp = {"summary": summary}
    response = make_response(resp, SUCCESS_CODE)      

    return response


@endpoints_blueprint.route('/progress', methods=['GET'])
def progress():
    
    global progress_tracker

    resp = {"heading": progress_tracker.heading ,
            "summary": progress_tracker.abstractive_summary,
            "progress":progress_tracker.progress}
               
    response =  make_response(resp, SUCCESS_CODE) 

    return response
    
