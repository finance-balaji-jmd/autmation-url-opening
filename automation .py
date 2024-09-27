import os
import random
import shutil
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from faker import Faker

fake = Faker()

# Function to delete old profile data
def delete_old_profiles():
    profile_dirs = ['chrome_profiles', 'edge_profiles']
    for dir in profile_dirs:
        if os.path.exists(dir):
            shutil.rmtree(dir)
        os.makedirs(dir)

# Create random user profile
def create_random_profile():
    profile = {
        "name": fake.name(),
        "age": random.randint(18, 70),
        "gender": random.choice(["Male", "Female"])
    }
    return profile

# Function to open URLs in random browser instances
def open_browser(urls, browser_type, driver_path):
    options = None
    if browser_type == "chrome":
        options = webdriver.ChromeOptions()
        profile_dir = f"chrome_profiles/{create_random_profile()['name']}"
        options.add_argument(f"user-data-dir={profile_dir}")
        driver = webdriver.Chrome(service=Service(driver_path), options=options)
    elif browser_type == "edge":
        options = webdriver.EdgeOptions()
        profile_dir = f"edge_profiles/{create_random_profile()['name']}"
        options.add_argument(f"user-data-dir={profile_dir}")
        driver = webdriver.Edge(service=EdgeService(driver_path), options=options)

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

# Start the main automation process
def start_automation():
    driver_path_chrome = chrome_driver_path.get()
    driver_path_edge = edge_driver_path.get()
    urls_file_path = url_path.get()
    num_chrome = int(num_chrome_drivers.get())
    num_edge = int(num_edge_drivers.get())

    delete_old_profiles()

    # Load URLs from text file
    if not os.path.exists(urls_file_path):
        messagebox.showerror("Error", f"'{urls_file_path}' not found. Please provide a valid path.")
        return

    with open(urls_file_path, 'r') as f:
        urls = [url.strip() for url in f.readlines()]

    # Start Chrome and Edge instances
    chrome_drivers = [open_browser(urls, "chrome", driver_path_chrome) for _ in range(num_chrome)]
    edge_drivers = [open_browser(urls, "edge", driver_path_edge) for _ in range(num_edge)]

    # Perform actions in a loop
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

# GUI Setup
root = tk.Tk()
root.title("URL Automation Tool")

# Chrome Driver Path
tk.Label(root, text="Chrome Driver Path:").grid(row=0, column=0, padx=10, pady=10)
chrome_driver_path = tk.Entry(root, width=50)
chrome_driver_path.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=lambda: chrome_driver_path.insert(0, filedialog.askopenfilename())).grid(row=0, column=2)

# Edge Driver Path
tk.Label(root, text="Edge Driver Path:").grid(row=1, column=0, padx=10, pady=10)
edge_driver_path = tk.Entry(root, width=50)
edge_driver_path.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=lambda: edge_driver_path.insert(0, filedialog.askopenfilename())).grid(row=1, column=2)

# URL Path
tk.Label(root, text="URLs File Path:").grid(row=2, column=0, padx=10, pady=10)
url_path = tk.Entry(root, width=50)
url_path.grid(row=2, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=lambda: url_path.insert(0, filedialog.askopenfilename())).grid(row=2, column=2)

# Number of Chrome Drivers
tk.Label(root, text="Number of Chrome Drivers:").grid(row=3, column=0, padx=10, pady=10)
num_chrome_drivers = tk.Entry(root, width=10)
num_chrome_drivers.grid(row=3, column=1, padx=10, pady=10)

# Number of Edge Drivers
tk.Label(root, text="Number of Edge Drivers:").grid(row=4, column=0, padx=10, pady=10)
num_edge_drivers = tk.Entry(root, width=10)
num_edge_drivers.grid(row=4, column=1, padx=10, pady=10)

# Start Button
tk.Button(root, text="Start Automation", command=start_automation).grid(row=5, columnspan=3, pady=20)

root.mainloop()
