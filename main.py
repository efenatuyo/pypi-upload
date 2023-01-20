from flask import Flask, render_template, request
import requests
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import threading
from setuptools import setup, find_packages
import configparser
import os
import re
import shutil
import asyncio
from concurrent.futures import ThreadPoolExecutor
config = configparser.ConfigParser(allow_no_value=True)
result = None
class package_procces:
 def check_package_name(name):
    if not name.islower():
        return False
    
    if not re.match(r'^[a-z0-9_]+$', name):
        return False
    
    if not re.match(r'^[a-z][a-z0-9_]*$', name):
        return False
    
    return True

 def createfile(name, code):
    config.read('database.ini')
    config["current"]["name"] = name
    with open('database.ini', 'w') as configfile:
            config.write(configfile)
    os.mkdir(name)
    with open(f'{name}/__init__.py', 'w+') as codex:
            codex.writelines(code)
    os.system('python setup.py sdist bdist_wheel')
    os.system('python -m twine upload dist/* -u __token__ -p pypi-AgEIcHlwaS5vcmcCJDg3MzBkZmIxLWJlNTYtNGNjNy04ZWMwLWNiMTVlMDI5NTVlYgACKlszLCIyY2UxNzc0ZS0wMzc1LTQ4YTYtOTFkZS0zNThlM2UxMzdkMjMiXQAABiDiF-PRB0_6iDaeh-TqCSMJe2yUDvYTSNblN0Zv69ZV3A')
    package_procces.delete_files(name)
    return f"succesfully created package named {name}"

 def delete_files(name):
    shutil.rmtree(name)
    shutil.rmtree(f"{name}.egg-info")
    shutil.rmtree(f"dist")
    shutil.rmtree(f"build")




def run_in_thread(data_content, package_name):
    global result
    result = package_procces.createfile(data_content, package_name)
  

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

@app.route('/')
def main():
    return render_template('main.html')
  
@app.route('/code')
def index():
    return render_template('file.html')


  
@app.route('/process_form', methods=['POST'])
@limiter.limit("1 per minute")
def process_form():
    # Get the content of the file field
    print(request.files)
    data_content = request.form['data']
    package_name = request.form['package_name']
    if package_name:
     if data_content:
         thread = threading.Thread(target=run_in_thread, args=(package_name, data_content))
         thread.start()
         thread.join()
         return result
     else:
         return 'Error: no data received'
    else:
      return 'Error: no package name received'
      
asyncio.run(app.run(host='0.0.0.0', port=81))