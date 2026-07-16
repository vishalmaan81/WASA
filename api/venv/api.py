import time
from flask import Flask, request, jsonify
from Wappalyzer import Wappalyzer, WebPage
import warnings
import json
from vulners import Vulners
from xssTest import getVulnerabilities
from newNetAttack import scanNetworkMainFunction
#import jsonpickle
import subprocess
from sqliTest import scanSqlInjection

warnings.simplefilter("ignore")

app = Flask(__name__)
app.debug = True

#CORS(app)

if __name__ == "__main__":
    app.run(debug=TRUE)

global vulnCount

@app.route('/time')
def getCurrentTime():
    return {'time':time.time()}


@app.route('/detectTechnologies', methods=['POST'])
def detect_technologies():
    data = request.json
    print("Request - ", data)
    url = data['url']
    softwareVulnerabilities = getVulnerableSoftware(url)

   
    print(softwareVulnerabilities)
    return softwareVulnerabilities


@app.route('/scanXss', methods=['POST'])
def scanXss():
    data = request.json
    print("Request - ", data)
    url = data['url']
    vulnerabilities = getVulnerabilities(url)

    print(vulnerabilities)
    return jsonify(response=vulnerabilities)

@app.route('/scanNetwork', methods=['POST'])
def scanNetwork():
    data = request.json
    print("Request - ", data)
    url = data['url']
    passwordList=radingPasswordList()
    output = scanNetworkMainFunction(url,passwordList)
    # output, error = run_python_file(file_path, inputs)
    print("Output:")
    print(output)
    json_data = json.dumps(output)
    print(json_data)
    return output


@app.route('/scanSQLI', methods=['POST'])
def scanSQLI():
    data = request.json
    print("Request - ", data)
    url = data['url']
    output = scanSqlInjection(url)
    result = {"response": output}
    return jsonify(result) 

    
def radingPasswordList():
    # global listOfPasswords
    password_list = []
    with open('passwordsFile.txt', 'r') as file:
        for line in file:
            password = line.strip()
            password_list.append(password)
    return password_list
    # with app.open_resource('passwordsFile.txt') as f:
    # # with open("passwordsFile.txt", 'r') as f:
    #     data = f.read().decode('utf-8')
    #     filedata=data.split("\n")
    #     listOfPasswords=list(filter(lambda x:x !='',filedata))
    #     print("Password file read Done",listOfPasswords)
    #     return listOfPasswords

# def run_python_file(file_path, inputs):
#     command = ['python', file_path, inputs]
#     proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
#     stdout, stderr = proc.communicate(inputs)
#     return stdout, stderr


def getVulnerableSoftware(url):
    wappalyzer = Wappalyzer.latest()
    vulners_api = Vulners(api_key='H0BJ1SS8M6LAVJLGE8Q8FUQNRNK4B8OWLWEWQ19YUHT45GZ0N8SUNKWKPAC9KUF7')  # Replace 'YOUR_API_KEY' with your Vulners API key

    webpage = WebPage.new_from_url(url)
    technologies = wappalyzer.analyze_with_versions(webpage)
    print("Teh ",technologies)
    
    validTech = []

    for key, value in technologies.items():
        if value['versions']:
            validTech.append([key, value['versions'][0]])

    vulnerabilities = {}
    for technology in validTech:
        results = vulners_api.softwareVulnerabilities(technology[0], technology[1])
        #results = vulners_api.softwareVulnerabilities("jQuery", "2.2.4")


        print("Valid Technologies - ",technology[0],technology[1])
        print("Resule - ",results)

        software_list = results.get('software')
        print("Software -  ",software_list)

        vulnCount=1
        if software_list:
            for vulnList in software_list:
                if vulnList.get("cvss").get("score"):
                    vulnerabilities[vulnCount]={}
                    vulnerabilities[vulnCount]['softwareversion']=technology[0]+":"+technology[1]
                    vulnerabilities[vulnCount]['title']=vulnList.get('title')
                    vulnerabilities[vulnCount]['cvescore']=vulnList.get("cvss").get("score")
                    vulnerabilities[vulnCount]['href']=vulnList.get("href")
                    print("Title - ", vulnList.get('title'))
                    print("CVE Sore - ",vulnList.get("cvss").get("score"))
                    print("URL - ",vulnList.get("href"))
                    vulnCount += 1
            vulnCount=0
        

    return vulnerabilities


@app.after_request
def set_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    return response


# 
# Calling another file
# 
def run_python_file(file_path, inputs):
    command = ['python', file_path, inputs]
    proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = proc.communicate(inputs)
    return stdout, stderr

def callNetAttack(url):
    file_path = 'netAttackNew.py'
    inputs = url
    # inputs = 'http://192.168.202.128:3000/'
    output, error = run_python_file(file_path, inputs)
    print("Output:")
    print(output)
    print("Error:")
    print(error)
