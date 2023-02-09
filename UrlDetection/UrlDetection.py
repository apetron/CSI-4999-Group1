import requests
import urllib
import json
import spacy
from spacy.lang.en import English
from publicsuffixlist import PublicSuffixList
from spacy.cli import download

#download('en_core_web_lg')
#download('en_core_web_sm')

def loadConfigSettings(configFile):
    f = open(configFile)
    data = json.load(f)
    return data["mode"], data["domains"]

def urlType(token):
    if "http://" in token:
        return "h"
    elif "https://" in token:
        return "hs"
    else:
        return "n"

def getUrlDomain(url, type):
    noProtocol = url.replace("https://", "") if type == "hs" else url.replace("http://", "") if type == "h" else ""
    print(noProtocol)

    domains = noProtocol
    if ":" in noProtocol:
        domains = noProtocol[:noProtocol.index(":")]
    elif "/" in noProtocol:
        domains = noProtocol[:noProtocol.index("/")]
    print(domains)

    psl = PublicSuffixList()
    tld = psl.publicsuffix(domains)
    print(tld)
    noTld = domains.replace("." + tld, "")
    print(noTld)

    domain = noTld
    if domain.count(".") > 0:
        domain = noTld[noTld.rfind(".") + 1:]
    
    finalDomain = domain + "." + tld
    print("The domain is: " + finalDomain)
    return finalDomain 
    
def validateUrl(type, url, mode, domains):
    domain = getUrlDomain(url, type)
    print(domain)

    if mode == "whitelist":
        #print("url" if domain not in domains else "not")
        if domain not in domains:
            print("Url is not allowed")
            return False
        else:
            print("Url is allowed")
            return True
    elif mode == "blacklist":
        if domain in domains:
            print("Url is not allowed")
            return False
        else:
            print("Url is allowed")
            return True
    else:
        print("Config is invalid, must be either set to 'whitelist' or 'blacklist'")

    

def checkUrls(text):
    #This may not be optimal, it might be better to load the config settings somewhere within the bot's code
    #Then just pass them into this function. Might not want to load from a file everytime a message is sent in discord
    mode, domains = loadConfigSettings("UrlDetection/domainConfig.json")
    if mode == "whitelist" or mode == "blacklist":
        nlp = spacy.load("en_core_web_sm")
        msg = nlp(text)
        for token in msg:
            type = urlType(token.text)
            if not type == "n":
                validateUrl(type, token.text, mode, domains)
    else:
        raise ValueError("Error: the url detection mode is not in a valid configuraion. It must be either whitelist or blacklist")
    

url = "https://mail.google.com" #example, test with a bunch
url1 = "http://apps.js.medium.co.uk:80/artificialis/phishing-url_detection_with-python-a2c3dd3a87e8?test=7"
url2 = "https://drive.google.com/drive/u/0/folders/1XWUjjkndB6pD7Bt79pJKM3cVyNgX0JMf"
text = "Some text with a url: " + url + "."
print(text)
checkUrls(text)
    
#encoded_url = urllib.parse.quote(url, safe='')
#api_url = "https://ipqualityscore.com/api/json/url/YOUR_KEY/"
#data = requests.get(api_url + encoded_url)
#print(json.dumps(json.data(), indent=4))