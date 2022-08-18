from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import requests
from dotenv import load_dotenv

load_dotenv()


def fetch_image_urls(query, max_links_to_fetch, wd, sleep_between_interactions=1):
    """
    Fetch image urls from Google image search.

    Parameters:
        query (str): The search term
        max_links_to_fetch (str): Number of urls to be fetched
        wd (webdriver):
        sleep_between_interactions (int): time in seconds to sleep before the next action, default 1

    Returns:
        Image urls (set)
    """

    def scroll_to_end(wd):
        """Scroll to the page bottom."""
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)

    # search images with specified search term
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0

    while image_count < max_links_to_fetch:
        # load more images by scrolling to the page bottom
        scroll_to_end(wd)

        # get all image thumbnail results
        thumbnail_results = wd.find_elements(By.CSS_SELECTOR, 'img.Q4LuWd')
        number_results = len(thumbnail_results)

        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

        # finish fetching if there are no more available image results
        if results_start == number_results:
            break

        # find button to load more images if available
        else:
            print("Found:", len(image_urls), "image links, looking for more ...")
            time.sleep(5)
            load_more_button = wd.find_element(By.XPATH, '//*[@id="islmp"]/div/div/div/div[1]/div[2]/div[2]/input')
            if load_more_button:
                print('load button found')
                wd.execute_script("document.querySelector('.mye4qd').click();")

        for img in thumbnail_results[results_start:number_results]:
            # try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except:
                continue

            # extract image urls
            actual_images = wd.find_elements(By.CSS_SELECTOR, 'img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            # finish fetching if enough images urls are scraped
            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break

        # move the result startpoint further down
        results_start = len(thumbnail_results)

    return image_urls


def persist_image(folder_path, url, counter):
    """
    Save images from fetched urls to local drive.

    Parameters:
        folder_path (str): Location where the images will be stored
        url (str): Fetched url
        counter (int):

    Returns:
        None
    """
    try:
        image_content = requests.get(url, timeout=10).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        f = open(os.path.join(folder_path, f'{search_term}_{str(counter)}.jpg'), 'wb')
        f.write(image_content)
        f.close()
        print(f"SUCCESS - saved {url} - as {folder_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")


def search_and_download(search_term, driver_path, target_path, number_images=100):
    """
    Perform image scraping.

    Parameters:
        search_term (str): Search term
        driver_path (str): Path of chromedriver
        target_path (str): Path where the image folder will be created
        number_images(int): Number of images to be scraped, default 10

    Returns:
        None
    """

    # the search term will be the folder name of all scraped images, connected with underscores
    target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' ')))

    # create folder if it does not exist
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # fetch urls
    with webdriver.Chrome(executable_path=driver_path) as wd:
        res = fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=0.5)

    # save images from the fetched urls
    counter = 0
    for elem in res:
        persist_image(target_folder, elem, counter)
        counter += 1


DRIVER_PATH = os.getenv('DRIVER_PATH')
TARGET_PATH = os.getenv('TARGET_PATH')
search_term = 'donkey'
search_and_download(search_term=search_term, driver_path=DRIVER_PATH, target_path=TARGET_PATH)

