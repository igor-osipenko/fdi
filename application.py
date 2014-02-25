from flask import Flask
import os
from itertools import izip

DEBUG = True
SECRET_KEY = '\xf0k\x80\xddJ\xf9me\xb1\x0c>\x1a\xfa\x8bRv\xebt7[\xb1\xdf\x03G'
FILE_UPLOAD_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'files')
IZIP = izip

app = Flask(__name__)
app.config.from_object(__name__)