import re
from datetime import time

name_pattern = '^[a-zA-Z]{2,30}$'
email_pattern = "^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
password_pattern = '^.{1,30}$'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def is_valid_name(inpt):
    if inpt is not None and re.match(name_pattern,inpt):
       return True
    return False

def is_valid_email(inpt):
    if inpt is not None and re.match(email_pattern,inpt):
       return True
    return False

def is_valid_pass(inpt):
    if inpt is not None and re.match(password_pattern,inpt):
       return True
    return False

def is_valid_number(inpt):
    return True
    '''
    if inpt is not None and re.match(number_pattern,inpt):
       return True
    return False
    '''
    
def defaultconverter(o):
  if isinstance(o, time):
     return o.__str__()
     

def is_valid_filename(filename):
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
       return True
    return False
