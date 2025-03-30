from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import os
import requests
import time

def setup_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def download_image(url, actor_name):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Create images directory if it doesn't exist
            if not os.path.exists("static/images"):
                os.makedirs("static/images")
            
            # Clean filename
            filename = actor_name.lower().replace(" ", "-") + ".jpg"
            filepath = os.path.join("static/images", filename)
            
            with open(filepath, "wb") as f:
                f.write(response.content)
            return f"/static/images/{filename}"
        return None
    except Exception as e:
        print(f"Error downloading image for {actor_name}: {str(e)}")
        return None

def scrape_actors():
    driver = setup_driver()
    url = "https://www.ranker.com/list/famous-korean-actors/ranker-entertainment"
    driver.get(url)
    
    # Wait for the content to load
    #WebDriverWait(driver, 10).until(
    #    EC.presence_of_element_located((By.XPATH, '//figure[contains(@class, "Media_main__Mh6I0")]/img'))
    #)
    time.sleep(6)
    # Scroll to load more content
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    actors = []
    elements = driver.find_elements(By.XPATH, '//figure[contains(@class, "Media_main__Mh6I0")]/img')
    
    for idx, item in enumerate(elements[:50], 1):  # Get top 20 actors
        try:
            name = item.get_attribute("alt")
            try:
                img_url = item.get_attribute("src")
                if img_url:
                    image_path = download_image(img_url, name)
                    if image_path:
                        actors.append({
                            "id": idx,
                            "name": name,
                            "image": image_path
                        })
                        print(f"Added {name}")
            except Exception as e:
                print(f"Error processing image for {name}: {str(e)}")
        except Exception as e:
            print(f"Error processing actor {idx}: {str(e)}")
    
    driver.quit()
    
    # Save to JSON file
    with open("celebrities.json", "w", encoding="utf-8") as f:
        json.dump(actors, f, ensure_ascii=False, indent=2)
    
    return actors

if __name__ == "__main__":
    print("Starting to scrape Korean actors...")
    actors = scrape_actors()
    print(f"Successfully scraped {len(actors)} actors")
