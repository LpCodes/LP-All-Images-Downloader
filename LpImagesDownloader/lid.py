import os
import re
import logging
import requests
import validators
from typing import Optional, List
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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


def download_images(pageurl: str, nooftimesyouwanttoscroll: int) -> List[str]:
    """
    Downloads all the images from the URL provided.
    
    Args:
        pageurl (str): The URL of the page to download images from
        nooftimesyouwanttoscroll (int): Number of times to scroll the page
        
    Returns:
        List[str]: List of paths to downloaded images
        
    Raises:
        TypeError: If pageurl is not a string or nooftimesyouwanttoscroll is not an integer
        ValueError: If the URL is invalid
    """
    if not isinstance(pageurl, str):
        raise TypeError("URL should be a string.")

    if not isinstance(nooftimesyouwanttoscroll, int):
        raise TypeError("No of times should be an integer.")

    if not validators.url(pageurl):
        raise ValueError("Invalid URL.")

    downloaded_files = []
    logger.info("Setting up environment...")
    driver = setup_driver()

    try:
        source = pageurl
        logger.info(f"Loading URL: {source}")
        driver.get(source)
        logger.info("Running operations in the background. You will get the results shortly...")
        driver.minimize_window()

        for i in range(nooftimesyouwanttoscroll):
            logger.info(f"Scrolling page {i + 1}...")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.implicitly_wait(2)

        all_images = driver.find_elements(By.XPATH, "//img")
        logger.info(f"Total detected images on page: {len(all_images)}")

        title = re.sub(r"[^\w\s-]", "", driver.title).strip()
        title = " ".join(title.split())
        savloc = f"Saved Images/{title}"
        os.makedirs(savloc, exist_ok=True)

        valid_images = 0
        count = 0

        for valid_images, img_element in enumerate(all_images, 1):
            url = img_element.get_attribute("src")
            
            if not validators.url(url):
                logger.warning(f"Invalid URL: {url}")
                continue

            if url.endswith("Video_icon2017.png") or url.endswith(".svg"):
                logger.info(f"Skipping non-image file: {url}")
                continue

            filename = f"{valid_images}.jpg"
            savingpath = os.path.join(savloc, filename)

            logger.info(f"Downloading {filename} from {url}...")
            if download_image(url, savingpath):
                downloaded_files.append(savingpath)
                count += 1

        logger.info(f"Total detected images on page: {valid_images}")
        logger.info(f"Total images downloaded: {count}")
        logger.info(f"You can view the saved images at {os.path.abspath(savloc)}.")
        return downloaded_files

    except TimeoutException:
        logger.error("Page load timed out. Please check your internet connection and try again.")
        raise
    except NoSuchElementException as e:
        logger.error(f"Element not found: {e}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise
    finally:
        try:
            driver.close()
            driver.quit()
        except Exception as e:
            logger.error(f"Error while closing driver: {e}")

if __name__ == "__main__":
    try:
        # Example usage
        downloaded_files = download_images("https://example.com", 3)
        logger.info(f"Successfully downloaded {len(downloaded_files)} images")
    except Exception as e:
        logger.error(f"Failed to download images: {e}")
