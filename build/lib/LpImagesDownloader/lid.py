import os
import re
import logging
import requests
import validators
from typing import Optional
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def setup_driver(headless: bool = True, timeout: int = 30) -> webdriver.Chrome:
    """
    Set up and return a Selenium webdriver instance.

    :param headless: Whether to run the browser in headless mode.
    :param timeout: Timeout for driver operations.
    :return: Selenium WebDriver instance.
    """
    options = Options()
    options.headless = headless
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options,
        )
        driver.set_page_load_timeout(timeout)
        return driver
    except WebDriverException as e:
        logging.error(f"Failed to initialize WebDriver: {e}")
        raise


def is_valid_image_url(url: str) -> bool:
    """
    Check if a URL is a valid image URL.

    :param url: URL to validate.
    :return: True if valid, False otherwise.
    """
    return validators.url(url) and not url.endswith(("Video_icon2017.png", ".svg"))


def download_image(url: str, save_path: str) -> bool:
    """
    Download an image from a URL to a specified path.

    :param url: Image URL.
    :param save_path: Path to save the image.
    :return: True if successful, False otherwise.
    """
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(save_path, "wb") as file:
                file.write(response.content)
            return True
        else:
            logging.warning(f"Failed to download {url}: HTTP {response.status_code}")
    except requests.RequestException as e:
        logging.warning(f"Error downloading {url}: {e}")
    return False


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
        print(f"Loading URL: {source}")
        driver.get(source)
        print("Running operations in the background. You will get the results shortly...")
        driver.minimize_window()

        for i in range(nooftimesyouwanttoscroll):
            print(f"Scrolling page {i + 1}...")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.implicitly_wait(2)

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
            try:
                response = requests.get(url)
                response.raise_for_status()
                with open(savingpath, "wb") as f:
                    f.write(response.content)
                count += 1
            except requests.exceptions.RequestException as e:
                print(f"Failed to download {url}: {e}")

        print(f"Total detected images on page: {valid_images}")
        print(f"Total images downloaded: {count}")
        print(f"You can view the saved images at {os.path.abspath(savloc)}.")

    except NoSuchElementException as e:
        print("Element not found:", e)

    except Exception as e:
        print("An error occurred:", e)

    finally:
        driver.close()
        driver.quit()

   



if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    download_images("https://example.com", scroll_count=3)
