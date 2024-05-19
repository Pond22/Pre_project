from django.test import TestCase
from selenium import webdriver
import multiprocessing
import os


 
  
def find_file_path():
    font_path = os.path.join(os.path.dirname(__file__), 'static', 'font', 'THSarabunNew.ttf')
    print(f"Checking font path: {font_path}")
    if os.path.exists(font_path):
        print("Found the font file.")
    else:
        print("Font file not found.")


find_file_path()
