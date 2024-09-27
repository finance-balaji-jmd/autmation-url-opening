import os
import random
import shutil
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from faker import Faker

fake = Faker()

# Ensure paths are handled correctly
current_dir = os.path.dirname(os.path.abspath(__file__))

# Function to delete old profile data
def delete_old_profiles():
    profile_dirs = ['chrome_profiles', 'edge_profiles']
    for dir in profile_dirs:
        full_path = os.path.join(current_dir, dir)
        if os.path.exists(full_path):
            shutil.rmtree(full_path)
        os.makedirs(full_path)

# Create random user profile
def create_random_profile():
    profile = {
        "name": fake.name(),
        "age": random.randint(18, 70),
        "gender": random.choice(["Male", "Female"])
    }
    return profile

# Function to open URLs in random browser instances
def open_browser(urls, browser_type="chrome"):
    options = None
    if browser_type == "chrome":
        options = webdriver.ChromeOptions()
        profile_dir = os.path.join(current_dir, f"chrome_profiles/{create_random_profile()['name']}")
        options.add_argument(f"user-data-dir={profile_dir}")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    elif browser_type == "edge":
        options = webdriver.EdgeOptions()
        profile_dir = os.path.join(current_dir, f"edge_profiles/{create_random_profile()['name']}")
        options.add_argument(f"user-data-dir={profile_dir}")
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)

    url = random.choice(urls)
    driver.get(url)

    # Perform random zoom and scroll
    random_zoom(driver)
    random_scroll(driver)

    return driver

# Perform random zooming
def random_zoom(driver):
    zoom_level = random.randint(50, 150)
    driver.execute_script(f"document.body.style.zoom='{zoom_level}%'")

# Perform random scrolling
def random_scroll(driver):
    scroll_amount = random.randint(200, 1000)
    driver.execute_script(f"window.scrollTo(0, {scroll_amount})")

# Main loop
def main():
    delete_old_profiles()
    
    # Load URLs from text file
    urls_file_path = os.path.join(current_dir, 'urls.txt')
    if not os.path.exists(urls_file_path):
        print(f"Error: '{urls_file_path}' not found. Please place 'urls.txt' in the script's directory.")
        return

    with open(urls_file_path, 'r') as f:
        urls = [url.strip() for url in f.readlines()]

    # Start Chrome and Edge instances
    chrome_drivers = [open_browser(urls, "chrome") for _ in range(4)]
    edge_drivers = [open_browser(urls, "edge") for _ in range(5)]
    
    try:
        while True:
            for driver in chrome_drivers + edge_drivers:
                url = random.choice(urls)
                driver.get(url)
                random_zoom(driver)
                random_scroll(driver)
                time.sleep(random.randint(2, 5))  # Random delay between actions
    except KeyboardInterrupt:
        for driver in chrome_drivers + edge_drivers:
            driver.quit()

if __name__ == "__main__":
    main()
