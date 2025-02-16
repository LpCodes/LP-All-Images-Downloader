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


def download_images(page_url: str, scroll_count: int = 3, output_dir: Optional[str] = None):
    """
    Download all images from a given URL.

    :param page_url: The web page URL.
    :param scroll_count: Number of times to scroll down the page.
    :param output_dir: Directory to save the downloaded images. Defaults to "Saved Images/<page_title>".
    """
    if not isinstance(page_url, str) or not validators.url(page_url):
        raise ValueError("Invalid URL provided.")
    if not isinstance(scroll_count, int) or scroll_count < 0:
        raise ValueError("scroll_count must be a non-negative integer.")

    logging.info("Setting up WebDriver...")
    driver = setup_driver()

    try:
        logging.info(f"Accessing URL: {page_url}")
        driver.get(page_url)
        driver.minimize_window()

        for i in range(scroll_count):
            logging.info(f"Scrolling page {i + 1}...")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.implicitly_wait(2)

        all_images = driver.find_elements(By.XPATH, "//img")
        logging.info(f"Total detected images on page: {len(all_images)}")

        page_title = re.sub(r"[^\w\s-]", "", driver.title).strip()
        page_title = " ".join(page_title.split())
        output_dir = output_dir or os.path.join("Saved Images", page_title)
        os.makedirs(output_dir, exist_ok=True)

        downloaded_count = 0
        for idx, img_element in enumerate(all_images, start=1):
            img_url = img_element.get_attribute("src")
            if not is_valid_image_url(img_url):
                continue

            save_path = os.path.join(output_dir, f"{idx}.jpg")
            if download_image(img_url, save_path):
                downloaded_count += 1

        logging.info(f"Downloaded {downloaded_count} images to {os.path.abspath(output_dir)}.")
    except NoSuchElementException as e:
        logging.error(f"Error finding elements: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    download_images("https://example.com", scroll_count=3)
