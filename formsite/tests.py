from django.test import TestCase
from selenium import webdriver
import multiprocessing

def test1(num):
    driver=webdriver.Chrome()
    url = "http://127.0.0.1:8000/test"
    driver.get(url)

    file_input = driver.find_element("name", "csv_file")
    file_path = r"C:\Users\pondb\Downloads\TEST_DATA\(3)DataSet_UTF-8.csv"  
    file_input.send_keys(file_path)

    submit_button = driver.find_element("name", "import")
    submit_button.click()
    
if __name__ == "__main__":
    processes = []
    for i in range(20):
        p = multiprocessing.Process(target=test1, args=(i,))
        p.start()
 



