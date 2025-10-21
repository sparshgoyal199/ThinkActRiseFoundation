from models.model import *
from config.db import *
from sqlmodel import Session, select
from fastapi import FastAPI,HTTPException
import uvicorn
import requests
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from bs4 import BeautifulSoup
import html
import json
import pdfkit


app = FastAPI()
session = None
resp = None
scid_value = None
BASE_PAGE = "https://newdelhi.dcourts.gov.in/cause-list-%E2%81%84-daily-board/"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["*"] for all origins (not recommended in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/fetchingstates')
def fetchingStates():
    try:
        with Session(engine) as session:
            states = session.exec(select(statecodes)).all()
        return states
    except Exception as e:
        print("An exception occurred")
        print(e)
        raise (HTTPException(status_code=422, detail=f'{e}'))
    
@app.get('/fetchingdistricts/{statecode}')
def fetchingDistricts(statecode:str):
    url = "https://services.ecourts.gov.in/ecourtindia_v6/?p=casestatus/fillDistrict"

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9,en-IN;q=0.8",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://services.ecourts.gov.in",
        "referer": "https://services.ecourts.gov.in/",
        "sec-ch-ua": '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
        "x-requested-with": "XMLHttpRequest"
    }

    # cookies = {
    #     "SERVICES_SESSID": "1grfpvvleqegkk1cbeabsnjldg",
    #     "JSESSION": "5523233"
    # }

    data = {
        "state_code": f"{statecode}",
        "ajax_req": "true",
        # "app_token": "889481c136bfaf5096254f6a4057a6290b87763e1cddc91f5ee2896f3d5c2579"
    }

    response = requests.post(url, headers=headers, data=data)
    districtHtml = response.text
    soup = BeautifulSoup(districtHtml, "lxml")  # 'lxml' parser is fast and lenient

# Print formatted (pretty) HTML
    options = soup.find_all("option")
    districts = []
    for i in range(len(options)):
        length = len(options[i].text.strip())
        if(i != len(options)-1):
            districts.append({"code":options[i]["value"],"district":options[i].text.strip()[:length-10]})
        else:
            districts.append({"code":options[i]["value"],"district":options[i].text.strip()[:length-102]})
    return districts

def findingCourtComplexCode(complexCode:str):
    code = ''
    for i in complexCode:
        if i == '@':
            break
        else:
            code += i
    return code

@app.get('/fetchingCourtComplex/{statecode}/{districtcode}')
def fetchingCourtComplex(statecode:str,districtcode:str):
    url = "https://services.ecourts.gov.in/ecourtindia_v6/?p=casestatus/fillcomplex"

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9,en-IN;q=0.8",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://services.ecourts.gov.in",
        "priority": "u=0, i",
        "referer": "https://services.ecourts.gov.in/",
        "sec-ch-ua": '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
        "x-requested-with": "XMLHttpRequest",
    }

    # cookies = {
    #     "SERVICES_SESSID": "721n3bkmj3quegp5komih7phg8",
    #     "JSESSION": "78254983"
    # }

    data = {
        "state_code": statecode,
        "dist_code": districtcode,
        "ajax_req": "true",
        # "app_token": "751f4e864525fdb209e0c04ec12765a8dd0179a28cd0f0b43f871d2a13b5b24b"
    }

    response = requests.post(url, headers=headers, data=data)
    courtComplexHtml = response.text
    soup = BeautifulSoup(courtComplexHtml, "lxml")  # 'lxml' parser is fast and lenient

# Print formatted (pretty) HTML
    options = soup.find_all("option")
    courtComplex = []
    for i in range(len(options)):
        length = len(options[i].text.strip())
        codeValue = findingCourtComplexCode(options[i]["value"])
        if(i != len(options)-1):
            courtComplex.append({"code":codeValue,"courtComplex":options[i].text.strip()[:length-10]})
        else:
            courtComplex.append({"code":codeValue,"courtComplex":options[i].text.strip()[:length-102]})
    return courtComplex
    # Print JSON response
    
@app.get('/fetchingCourtEstablishment/{statecode}/{districtcode}/{complexcode}')
def fetchingCourtEstablishment(statecode:str,districtcode:str,complexcode:str):
    url = "https://services.ecourts.gov.in/ecourtindia_v6/?p=casestatus/fillCourtEstablishment"

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9,en-IN;q=0.8",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://services.ecourts.gov.in",
        "priority": "u=0, i",
        "referer": "https://services.ecourts.gov.in/",
        "sec-ch-ua": '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
        "x-requested-with": "XMLHttpRequest",
    }

    # cookies = {
    #     "SERVICES_SESSID": "38t4olt3roggqshhb4knf4d8gk",
    #     "JSESSION": "29923727"
    # }

    data = {
        "state_code": f'{statecode}',
        "dist_code": f'{districtcode}',
        "court_complex_code": f'{complexcode}',
        "ajax_req": "true"
        # "app_token": "4a30b917e6425061fb09fc3de5389a7263714c9448924dc4012985e711ad9120"
    }

    response = requests.post(url, headers=headers, data=data)
    courtEstablishmentHtml = response.text
    soup = BeautifulSoup(courtEstablishmentHtml , "lxml")  # 'lxml' parser is fast and lenient

# Print formatted (pretty) HTML
    options = soup.find_all("option")
    courtEstablishment = []
    for i in range(len(options)):
        length = len(options[i].text.strip())
        if(i != len(options)-1):
            courtEstablishment.append({"code":options[i]["value"],"courtEstablishment":options[i].text.strip()[:length-10]})
        else:
            courtEstablishment.append({"code":options[i]["value"],"courtEstablishment":options[i].text.strip()[:length-102]})
    return courtEstablishment

@app.get('/fetchingCourtNames/{statecode}/{districtcode}/{complexcode}')
def fetchingCourtNames(statecode:str,districtcode:str,complexcode:str):
    url =  "https://services.ecourts.gov.in/ecourtindia_v6/?p=cause_list/fillCauseList"
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9,en-IN;q=0.8",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://services.ecourts.gov.in",
        "priority": "u=0, i",
        "referer": "https://services.ecourts.gov.in/",
        "sec-ch-ua": '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
        "x-requested-with": "XMLHttpRequest",
    }
    
    # cookies = {
    #     "SERVICES_SESSID": "38t4olt3roggqshhb4knf4d8gk",
    #     "JSESSION": "29923727"
    # }
    
    data = {
    "state_code": f'{statecode}',
    "dist_code": f'{districtcode}',
    "court_complex_code": f'{complexcode}',
    # "est_code": "",
    # "search_act": "undefined",
    "ajax_req": "true"
    # "app_token": "1930805fd2374dbbf256101bcde6ad34b9b73dfb05bb0cbfd44e308be0f942f4"
}
    
    response = requests.post(url, headers=headers, data=data)
    courtNamesHtml = response.text
    soup = BeautifulSoup(courtNamesHtml , "lxml")  # 'lxml' parser is fast and lenient

# Print formatted (pretty) HTML
    options = soup.find_all("option")
    courtNames = []
    for i in range(len(options)):
        length = len(options[i].text.strip())
        if(i != len(options)-1):
            courtNames.append({"code":options[i]["value"],"courtName":options[i].text.strip()[:length-10]})
        else:
            courtNames.append({"code":options[i]["value"],"courtName":options[i].text.strip()[:length-102]})
    return courtNames
    # soup = BeautifulSoup(courtNamesHtml , "lxml")
    # options = soup.find_all("option")
    # # Print JSON response
    # print(options)
    # return options
    
#/{statecode}/{districtcode}/{complexcode}/{clcourtno}/{causelistdate}/{courtname}/{estcode}/{cicri}/{selprevdays}
#statecode:str,districtcode:str,complexcode:str,clcourtno:str,causelistdate:str,courtname:str,estcode:str,cicri:str,selprevdays:str
@app.get('/fetchingCauseList')
def fetchingCauseList():
    url = "https://services.ecourts.gov.in/ecourtindia_v6/?p=cause_list/submitCauseList"

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9,en-IN;q=0.8",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://services.ecourts.gov.in",
        "priority": "u=0, i",
        "referer": "https://services.ecourts.gov.in/",
        "sec-ch-ua": '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
        "x-requested-with": "XMLHttpRequest",
    }

    # cookies = {
    #     "SERVICES_SESSID": "94qigkknm51qc747ojqtvdqnvl",
    #     "JSESSION": "78757334"
    # }

    data = {
        "CL_court_no": "1^5E442",
        "causelist_date": "19-10-2025",
        # "cause_list_captcha_code": "mga42a",
        "court_name_txt": "442-Sh. Praveen Singh-Additional Sessions Judge",
        "state_code": "26",
        "dist_code": "1",
        "court_complex_code": "1260001",
        "est_code": "1",
        "cicri": "civ",
        "selprevdays": "0",
        "ajax_req": "true",
        # "app_token": "05582d7885af815f78af12c1e3130c9df8c11e45c339b2bae2d32f256ec9b8ed"
    }

    response = requests.post(url, headers=headers, data=data)

    # Try to print JSON response, else fallback to text
    try:
        print(response.text)
    except ValueError:
        print(response.text)
    return response.text

@app.get('/gettingCourtNames/{civcri}')
def gettingCourtNames(civcri:str):
    global scid_value
    # csrfSoup = BeautifulSoup(resp.text, "html.parser")
    # scid_input = csrfSoup.find("input", {"name": "scid"})
    # scid_value = scid_input["value"] if scid_input else None

    courtComplexUrl = "https://newdelhi.dcourts.gov.in/wp-admin/admin-ajax.php"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9,en-IN;q=0.8",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://newdelhi.dcourts.gov.in",
        "Referer": "https://newdelhi.dcourts.gov.in/cause-list-%E2%81%84-daily-board/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    data = {
        "action": "get_court_lists",
        "service_type": "courtComplex",
        "est_code": "DLND01,DLND02,DLND03,DLND04",
        "cause_type": civcri,
        "scid": scid_value,
        # "tok_9e9d046508deba684f8702b7901458ca120b105e": "a22d49b2bb2cd4b80d0295cd7664151ddbc1a688",
        "es_ajax_request": "1"
    }

    response = session.post(courtComplexUrl, data=data, headers=headers, timeout=20)

    courtNamesHtml = response.text
    courtSoup = BeautifulSoup(courtNamesHtml , "lxml")  # 'lxml' parser is fast and lenient

    # Print formatted (pretty) HTML
    options = courtSoup.find_all("option")
    courtNames = []
    for i in range(len(options)):
        nameLength = len(options[i].text.strip())
        length = len(options[i]["value"])
        courtNames.append({'code':options[i]["value"][2:length-2],'courtName':options[i].text.strip()[:nameLength-12]})
    return courtNames

@app.get('/fetchingEachCauseList/{courtName}/{date}/{civcri}/{captcha}/{count}')
def fetchingEachCauseList(courtName:str,date:str,civcri:str,captcha:str,count:str):
    global BASE_PAGE
    AJAX_URL = "https://newdelhi.dcourts.gov.in/wp-admin/admin-ajax.php"    
    data = {
        "service_type": "courtComplex",
        "est_code": "DLND01,DLND02,DLND03,DLND04",
        "date": date,
        "cause_type": civcri,
        "court": courtName,
        "scid": scid_value,
        "siwp_captcha_value": captcha,
        "action": "get_causes",
        "es_ajax_request": "1",
    }

    # headers if needed (mimic browser)
    headers = {
        "Referer": BASE_PAGE,
        "User-Agent": "Mozilla/5.0 (compatible)",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "application/json, text/javascript, */*; q=0.01",
    }

    post_resp = session.post(AJAX_URL, data=data, headers=headers, timeout=20)
    resp_json = json.loads(post_resp.text)
    if resp_json['success'] == False:
        raise HTTPException(status_code=400, detail="Item ID must be positive")
    
    html_content = resp_json['data']
    with open(f"C:/Users/spars/OneDrive/Desktop/imagesandhtml/page{count}.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    html_file = f"C:/Users/spars/OneDrive/Desktop/imagesandhtml/page{count}.html"

    # Output PDF file
    pdf_file = f"C:/Users/spars/OneDrive/Desktop/imagesandhtml/page{count}.pdf"

    # Convert
    pdfkit.from_file(html_file, pdf_file)

@app.get('/creatingSession')
def sessionCreate():
    global BASE_PAGE
    global session
    session = requests.Session()
    global resp
    resp = session.get(BASE_PAGE, timeout=15)
    csrfandImageSoup = BeautifulSoup(resp.text, "html.parser")
    scid_input = csrfandImageSoup.find("input", {"name": "scid"})
    global scid_value 
    scid_value = scid_input["value"] if scid_input else None
    captcha_img = csrfandImageSoup.find("img", {"id": "siwp_captcha_image_0"})  # or inspect HTML to find exact class
    if captcha_img:
        captcha_url = captcha_img["src"]
        return captcha_url
        # print(captcha_url)
        # print("CAPTCHA image URL:", captcha_url)
        # download captcha
        # img_resp = session.get(captcha_url)
        # print(img_resp)
        # with open("eCourtScraperUi/captcha.png", "wb") as f:
        #     f.write(img_resp.content)
            

if __name__ == "__main__":
    sessionCreate()
    create_table()
    uvicorn.run('main:app', host='127.0.0.1', port=60, reload=True)


