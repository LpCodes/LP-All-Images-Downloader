import os
import re

import requests
import validators
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


foldername = savingpath = savloc = None


def down_all(pageurl, nooftimesyouwanttoscroll):
    # sourcery skip: raise-specific-error
    """downloads all the images from the url provided"""
    global foldername, savingpath, savloc
    if (type(pageurl)) != str:
        raise Exception(
            f"URL {pageurl} provided is not a valid string Did you forget to enclose it with quotes ?"
        )

    if (type(nooftimesyouwanttoscroll)) != int:
        raise Exception(
            f"No of times {nooftimesyouwanttoscroll} provided is not a valid integer Did you forget to enclose it with quotes ?"
        )

    if not validators.url(pageurl):
        raise Exception(f"URL {pageurl} is not a valid URL")

    print("Setting Up Environment ... ")
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    # DRIVER_PATH = "/driver/chromedriver.exe"
    desired_capabilities = DesiredCapabilities.CHROME.copy()
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
        desired_capabilities=desired_capabilities,
    )
    # driver = webdriver.Chrome(
    #     options=options,
    #     executable_path=DRIVER_PATH,
    #     desired_capabilities=desired_capabilities,
    # )
    all_images = None
    source = f"{pageurl}"
    print("Running Operations in background you will get the results shortly ... ")
    driver.get(source)

    # driver.maximize_window()
    driver.implicitly_wait(1)  # seconds
    print("Scrolling page")
    for i in range(nooftimesyouwanttoscroll):
        print(f"Scrolling Page {i}")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        all_images = driver.find_elements(By.XPATH, "//img")
        driver.implicitly_wait(1)

    valid_images = 0
    count = 0

    try:
        all_images = driver.find_elements(By.XPATH, "//img")
        print(f"Total detected images on page {len(all_images)}")
        title = str(driver.title)
        replaced_name = re.sub(r"[/|',;.:\?()\"-]+", "", title)
        replaced_name = " ".join(replaced_name.split())
        for x in all_images:
            valid_images += 1
            savloc = f"Saved Images/{replaced_name}"
            os.makedirs(savloc, exist_ok=True)

            url = str(x.get_attribute("src"))
            filename = f"{valid_images}.jpg"
            savingpath = os.path.join(f"{savloc}", filename)
            if validators.url(url):
                if url.endswith("Video_icon2017.png") or url.endswith("svg"):
                    print("Skipping broken image detected")
                else:
                    count += 1
                    print(f"Downloading {filename}")
                    # urlretrieve(url, filename=savingpath)
                    response = requests.get(url)
                    if response.status_code == 200:
                        with open(savingpath, "wb+") as f:
                            f.write(response.content)
            else:
                print("Invalid url ")

    except NoSuchElementException:
        pass
    except Exception as e:
        print(e)
    finally:
        driver.close()

    print(
        f"Total detected images on page {len(all_images)}\nTotal Images Downloaded {count}"
    )
    print(f"You can view the saved Images at {savloc}")


# I_down(
#     "https://github.com/LpCodes",
#     3,
# )


# down_all( "https://github.com/LpCodes",1)