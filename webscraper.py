import requests

header = {
    "accept": "application/json",
    "accept-language": "en-US,en;q=0.9",
    "sec-ch-ua":
    "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "cookie":
    "BIGipServer~OIT-SISS~spprd.siss_http_pool=4092692490.16671.0000; siss-csweb-102-5600-PORTAL-PSJSESSIONID=HPMnVGVoszJfUiV1QUlFspQ4k8M-ppJp!-1828746355; PS_TokenSite=https://dukehub.duke.edu/psc/CSPRD01/?siss-csweb-102-5600-PORTAL-PSJSESSIONID; hpt_institution=DUKEU; PS_LOGINLIST=https://dukehub.duke.edu/CSPRD01; SignOnDefault=; PS_TOKEN=sgAAAAQDAgEBAAAAvAIAAAAAAAAsAAAABABTaGRyAk4Aewg4AC4AMQAwABSUeC6dZMFCPMixQkz4ojSmXVP6C3IAAAAFAFNkYXRhZnicJYjNCkVgFEWXnwzvA3gH4iM/QyGZSG43Q6WUB2Dk1TycnXtWZ69z9gW4jm1Z8m3zjt/wY2FmY6Xi5GDX39PgtQx0fGq+jExqImJSIxkRyLnyf8ci1CbKhEJpKF9yMngAiLkODw==; PS_DEVICEFEATURES=width:1920 height:1080 pixelratio:1 touch:0 geolocation:1 websockets:1 webworkers:1 datepicker:1 dtpicker:1 timepicker:1 dnd:1 sessionstorage:1 localstorage:1 history:1 canvas:1 svg:1 postmessage:1 hc:0 maf:0; springboard=%7B%22DUKEU%22%3A%7B%22persona%22%3A%22HPT_MAIN%22%2C%22tileExclusions%22%3A%7B%7D%7D%7D; ExpirePage=https://dukehub.duke.edu/psp/CSPRD01/; PS_LASTSITE=https://dukehub.duke.edu/psp/CSPRD01/; CSRFCookie=4894f59e-5216-4aeb-9734-1fb17c45e19f; PS_TOKENEXPIRE=20_Jul_2022_10:15:41_GMT",
    "Referer":
    "https://dukehub.duke.edu/psc/CSPRD01/EMPLOYEE/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_Main?x_acad_career=UGRD&class_nbr=5758&enrl_stat=O",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}


async def GetCourse(cid):
    global header
    url = f"https://dukehub.duke.edu/psc/CSPRD01/EMPLOYEE/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassDetails?institution=DUKEU&term=1820&class_nbr={cid}"
    res = requests.get(url, headers=header)

    # print(res.json())
    return res.json()


async def SearchCourse(keyword):
    global header
    url = f"https://dukehub.duke.edu/psc/CSPRD01/EMPLOYEE/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=DUKEU&term=1820&date_from=&date_thru=&subject=&subject_like=&catalog_nbr=&time_range=&days=&campus=&location=&x_acad_career=UGRD&acad_group=&rqmnt_designtn=&instruction_mode=&keyword={keyword}&class_nbr=&acad_org=&enrl_stat=&crse_attr=&crse_attr_value=&instructor_name=&session_code=&units=&page=1"
    res = requests.get(url, headers=header)

    print(res.json())
    return res.json()
