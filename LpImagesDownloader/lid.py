import os
import re
import requests
import validators
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver(headless=True):
    """
    Set up and return a Selenium webdriver instance.
    """
    options = Options()
    options.headless = True
    # options.add_argument("--window-size=1920,1200")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )
    return driver

def download_images(pageurl, nooftimesyouwanttoscroll):
    """
    Downloads all the images from the URL provided.
    """
    if not isinstance(pageurl, str):
        raise TypeError("URL should be a string.")

    if not isinstance(nooftimesyouwanttoscroll, int):
        raise TypeError("No of times should be an integer.")

    if not validators.url(pageurl):
        raise ValueError("Invalid URL.")

    savloc = ''
    print("Setting up environment...")
    driver = setup_driver()

    try:
        source = pageurl
        print("Running operations in the background. You will get the results shortly...")
        driver.get(source)
        driver.maximize_window()

        for i in range(nooftimesyouwanttoscroll):
            print(f"Scrolling page {i + 1}...")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.implicitly_wait(1)

        all_images = driver.find_elements(By.XPATH, "//img")
        print(f"Total detected images on page: {len(all_images)}")

        title = re.sub(r"[^\w\s-]", "", driver.title).strip()
        title = " ".join(title.split())
        savloc = f"Saved Images/{title}"
        os.makedirs(savloc, exist_ok=True)

        valid_images = 0
        count = 0

        for valid_images, img_element in enumerate(all_images, 1):
            url = img_element.get_attribute("src")
            
            if not validators.url(url):
                print("Invalid URL:", url)
                continue

            if url.endswith("Video_icon2017.png") or url.endswith(".svg"):
                print("Skipping broken image detected:", url)
                continue

            filename = f"{valid_images}.jpg"
            savingpath = os.path.join(savloc, filename)

            print(f"Downloading {filename} from {url}...")
            response = requests.get(url)

            if response.status_code == 200:
                with open(savingpath, "wb") as f:
                    f.write(response.content)
                count += 1

        print(f"Total detected images on page: {valid_images}")
        print(f"Total images downloaded: {count}")
        print(f"You can view the saved images at {os.path.abspath(savloc)}.")

    except NoSuchElementException as e:
        print("Element not found:", e)

    except Exception as e:
        print("An error occurred:", e)

    finally:
        driver.quit()

# Example usage:
# download_images("https://example.com", 3)
