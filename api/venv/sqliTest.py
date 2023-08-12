import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from pprint import pprint



def scanSqlInjection(url):
    returnSqlResult=[]
    # Test on the URL
    for c in "\"'":
        # Add quote/double quote character to the URL
        new_url = f"{url}{c}"
        print("[!] Trying", new_url)
        # Make the HTTP request
        res = s.get(new_url)
        if is_vulnerable(res):
            # SQL Injection detected on the URL itself,
            # no need to proceed for extracting forms and submitting them
            print("[+] SQL Injection vulnerability detected, link:", new_url)
            returnSqlResult.append(new_url)
            break

    # Test on HTML forms
    forms = get_all_forms(url)
    print(f"[+] Detected {len(forms)} forms on {url}.")
    for form in forms:
        form_details = get_form_details(form)
        for c in "\"'":
            # The data body we want to submit
            data = {}
            for input_tag in form_details["inputs"]:
                if input_tag["type"] == "hidden" or input_tag["value"]:
                    # Any input form that is hidden or has some value,
                    # just use it in the form body
                    try:
                        data[input_tag["name"]] = input_tag["value"] + c
                    except:
                        pass
                elif input_tag["type"] != "submit":
                    # All others except submit, use some junk data with a special character
                    data[input_tag["name"]] = f"test{c}"

            # Join the URL with the action (form request URL)
            url = urljoin(url, form_details["action"])
            if form_details["method"] == "post":
                res = s.post(url, data=data)
            elif form_details["method"] == "get":
                res = s.get(url, params=data)

            # Test whether the resulting page is vulnerable
            if is_vulnerable(res):
                print("[+] SQL Injection vulnerability detected, link:", url)
                print("[+] Form:")
                pprint(form_details)
                returnSqlResult.append(new_url)
                break
                #return "SQL Injection Detected On - ",url
                # break
    if returnSqlResult:
        return returnSqlResult
    else:
        return "NO SQL Vulnerability Found"

def is_vulnerable(response):
    """A simple boolean function that determines whether a page
    is SQL Injection vulnerable from its `response`"""
    errors = {
        # MySQL
        "you have an error in your sql syntax;",
        "warning: mysql",
        # SQL Server
        "unclosed quotation mark after the character string",
        # Oracle
        "quoted string not properly terminated",
    }
    for error in errors:
        # If you find one of these errors, return True
        if error in response.content.decode().lower():
            return True
    # No error detected
    return False

def get_all_forms(url):
    """Given a `url`, it returns all forms from the HTML content"""
    soup = bs(s.get(url).content, "html.parser")
    return soup.find_all("form")

def get_form_details(form):
    """
    This function extracts all possible useful information about an HTML `form`
    """
    details = {}
    # Get the form action (target URL)
    try:
        action = form.attrs.get("action").lower()
    except:
        action = None
    # Get the form method (POST, GET, etc.)
    method = form.attrs.get("method", "get").lower()
    # Get all the input details such as type, name, and value
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
    # Put everything into the resulting dictionary
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

# Initialize an HTTP session and set the browser
s = requests.Session()
# s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
