import os
import re

import requests
import validators
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

savloc = ''


def download_images(pageurl: str, nooftimesyouwanttoscroll: int):
    """
    Downloads all the images from the URL provided.
    """
    global savloc
    if not isinstance(pageurl, str):
        raise TypeError(f"URL {pageurl} provided is not a valid string. Did you forget to enclose it with quotes?")

    if not isinstance(nooftimesyouwanttoscroll, int):
        raise TypeError(
            f"No of times {nooftimesyouwanttoscroll} provided is not a valid integer. Did you forget to enclose it "
            f"with quotes?")

    if not validators.url(pageurl):
        raise ValueError(f"URL {pageurl} is not a valid URL.")

    print("Setting up environment...")
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    desired_capabilities = DesiredCapabilities.CHROME.copy()
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
        desired_capabilities=desired_capabilities,
    )
    all_images = None
    source = f"{pageurl}"
    print("Running operations in background. You will get the results shortly...")
    driver.get(source)

    for i in range(nooftimesyouwanttoscroll):
        print(f"Scrolling page {i + 1}...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        all_images = driver.find_elements(By.XPATH, "//img")
        driver.implicitly_wait(1)

    valid_images = 0
    count = 0

    try:
        all_images = driver.find_elements(By.XPATH, "//img")
        print(f"Total detected images on page: {len(all_images)}")
        title = str(driver.title)
        replaced_name = re.sub(r"[^\w\s-]", "", title).strip()
        replaced_name = " ".join(replaced_name.split())
        savloc = f"Saved Images/{replaced_name}"
        os.makedirs(savloc, exist_ok=True)

        for x in all_images:
            valid_images += 1

            url = str(x.get_attribute("src"))
            if not validators.url(url):
                print("Invalid URL: ", url)
                continue

            if url.endswith("Video_icon2017.png") or url.endswith(".svg"):
                print("Skipping broken image detected: ", url)
                continue

            filename = f"{valid_images}.jpg"
            savingpath = os.path.join(savloc, filename)

            print(f"Downloading {filename} from {url}...")
            response = requests.get(url)
            if response.status_code == 200:
                with open(savingpath, "wb+") as f:
                    f.write(response.content)
                count += 1

    except NoSuchElementException:
        pass

    except Exception as e:
        print(e)

    finally:
        driver.close()

    print(f"Total detected images on page: {len(all_images)}")
    print(f"Total images downloaded: {count}")
    print(f"You can view the saved images at {os.path.abspath(savloc)}.")
