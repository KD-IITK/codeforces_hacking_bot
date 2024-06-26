import requests
import re
import subprocess
import os
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import sys
import time

cookies = {
    # Put Codeforces Cookie here
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=0, i',
    'referer': 'https://codeforces.com/service-worker-23218.js',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'same-origin',
    'sec-fetch-site': 'same-origin',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
}

params = {
    'order': 'BY_ARRIVED_ASC',
}


driver = uc.Chrome(use_subprocess=False)

driver.get("https://codeforces.com/contest/1985/status/page/1/")
wait = WebDriverWait(driver, 20)
problem_dropdown = Select(driver.find_element(By.ID, "frameProblemIndex"))
problem_dropdown.select_by_value("F")
verdict_dropdown = Select(driver.find_element(By.ID, "verdictName"))
verdict_dropdown.select_by_value("OK")
apply_button = driver.find_element(By.XPATH,"//input[contains(@value, 'Apply')]")
apply_button.click()


for page in range(33, 50):
    driver.get(f'https://codeforces.com/contest/1985/status/page/{page}?order=BY_ARRIVED_ASC')
    res = driver.page_source
    selenium_cookies = driver.get_cookies()
    cookies = {cookie['name']: cookie['value'] for cookie in selenium_cookies}
    # response = requests.get(f'https://codeforces.com/contest/1985/status/page/{page}', params=params, cookies=cookies, headers=headers)
    print(res)

    matches = re.findall(r'viewableSubmissionIds\ \= \[\s+([^\]]+)', res)
    all_text = matches[0]
    all_text = all_text.replace('"', '').replace("\r\n", "").replace(" ","")

    ids = all_text.split(",")


    matches = re.findall(r"""name=['"]csrf_token['"] value=['"]([^'"]+)""", res)
    csrf_token = matches[0]

    for iid in ids:

        # driver.get(f"https://codeforces.com/contest/1985/submission/{iid}")
        # res = 
        data = {
            'submissionId': iid,
            'csrf_token': csrf_token,
        }
        # print('----------------------------')
        # print(iid)
        while True:
            try:
                response = requests.post('https://codeforces.com/data/submitSource', cookies=cookies, headers=headers, data=data)
                res = response.json()
                break
            except KeyboardInterrupt:
                sys.exit()
            except:
                print("Failed!!")
                time.sleep(10)
                pass
        # print("================================================")
        # print(response.text)

        # print(res['source'])

        with open('/tmp/code.cpp', 'w') as f:
            f.write(res['source'])

        input_data = "1\n200000 2\n199998 1\n1 1\n"
        try:
            command = ["g++", "/tmp/code.cpp", "-o", "/tmp/output"]
            output = subprocess.check_output(command, stderr=subprocess.STDOUT)

            # Execute the command, passing the input data and capturing the output
            command = ["/tmp/output"]
            output = subprocess.check_output(command, input=input_data, text=True, stderr=subprocess.STDOUT, timeout=5)
            output = output.strip().replace(" ", "")
            # Print the output
            if output != "2":
                print(iid)
            print("Output:", output)
            time.sleep(2)
        except Exception as e:
            # If there's an error, print it
            print("Error:", e)
        
        # break

    # print(ids)

    # print(response.text)