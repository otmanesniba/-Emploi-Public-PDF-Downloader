import time
import os
import random
import sys
import shutil
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from fake_useragent import UserAgent
import pyfiglet
from colorama import Fore, Style, Back, init
from datetime import datetime
import re
import requests
import threading
import time

# Initialize colorama with autoreset
init(autoreset=True)

# ================== CUSTOM BANNER ==================
def print_ascii_banner():
    # Clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # ASCII art banner for "EMPLOI PUBLIC PDF DOWNLOADER"
    banner = """
    ███████╗███╗   ███╗██████╗ ██╗      ██████╗ ██╗    ██████╗ ██╗   ██╗██████╗ ██╗     ██╗ ██████╗
    ██╔════╝████╗ ████║██╔══██╗██║     ██╔═══██╗██║    ██╔══██╗██║   ██║██╔══██╗██║     ██║██╔════╝
    █████╗  ██╔████╔██║██████╔╝██║     ██║   ██║██║    ██████╔╝██║   ██║██████╔╝██║     ██║██║     
    ██╔══╝  ██║╚██╔╝██║██╔═══╝ ██║     ██║   ██║██║    ██╔═══╝ ██║   ██║██╔══██╗██║     ██║██║     
    ███████╗██║ ╚═╝ ██║██║     ███████╗╚██████╔╝██║    ██║     ╚██████╔╝██████╔╝███████╗██║╚██████╗
    ╚══════╝╚═╝     ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝    ╚═╝      ╚═════╝ ╚═════╝ ╚══════╝╚═╝ ╚═════╝
                                                                                                      
    ██████╗ ██████╗ ███████╗    ██████╗  ██████╗ ██╗    ██╗███╗   ██╗██╗      ██████╗  █████╗ ██████╗ ███████╗██████╗ 
    ██╔══██╗██╔══██╗██╔════╝    ██╔══██╗██╔═══██╗██║    ██║████╗  ██║██║     ██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
    ██████╔╝██║  ██║█████╗      ██║  ██║██║   ██║██║ █╗ ██║██╔██╗ ██║██║     ██║   ██║███████║██║  ██║█████╗  ██████╔╝
    ██╔═══╝ ██║  ██║██╔══╝      ██║  ██║██║   ██║██║███╗██║██║╚██╗██║██║     ██║   ██║██╔══██║██║  ██║██╔══╝  ██╔══██╗
    ██║     ██████╔╝██║         ██████╔╝╚██████╔╝╚███╔███╔╝██║ ╚████║███████╗╚██████╔╝██║  ██║██████╔╝███████╗██║  ██║
    ╚═╝     ╚═════╝ ╚═╝         ╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
    """
    
    # Print the banner with a cool color effect
    lines = banner.split('\n')
    colors = [Fore.CYAN, Fore.BLUE, Fore.MAGENTA, Fore.RED, Fore.YELLOW, Fore.GREEN]
    
    for i, line in enumerate(lines):
        color = colors[i % len(colors)]
        print(color + line)
    
    # Print author credit with a different style
    print("\n" + Back.BLACK + Fore.WHITE + Style.BRIGHT + "                                  Made by OTMANE SNIBA                                  " + Style.RESET_ALL + "\n")

# ================== PROGRESS BAR ==================
def progress_bar(iteration, total, prefix='', suffix='', length=50, fill='█', print_end="\r"):
    """Display a progress bar in the console."""
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{Fore.GREEN}{bar}{Style.RESET_ALL}| {percent}% {suffix}', end=print_end)
    if iteration == total: 
        print()

# ================== SPINNER ANIMATION ==================
class Spinner:
    """A spinner animation for console output."""
    def __init__(self, message="Loading", delay=0.1):
        self.spinner_chars = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
        self.delay = delay
        self.message = message
        self.running = False
        self.spinner_thread = None

    def spin(self):
        while self.running:
            for char in self.spinner_chars:
                sys.stdout.write(f'\r{Fore.YELLOW}{char} {self.message}...{Style.RESET_ALL}')
                sys.stdout.flush()
                time.sleep(self.delay)

    def start(self):
        self.running = True
        self.spinner_thread = threading.Thread(target=self.spin)
        self.spinner_thread.daemon = True
        self.spinner_thread.start()

    def stop(self):
        self.running = False
        if self.spinner_thread:
            self.spinner_thread.join()
        sys.stdout.write('\r' + ' ' * (len(self.message) + 10) + '\r')
        sys.stdout.flush()

# ================== DRIVER SETUP ==================
def setup_edge_driver():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    # Set a larger window size to avoid viewport issues
    options.add_argument("--window-size=1920,1080")
    
    # Realistic browser configuration
    ua = UserAgent(browsers=['edge'])
    user_agent = ua.random
    options.add_argument(f"user-agent={user_agent}")
    
    # Configure download settings
    download_dir = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'Concours_PDFs')
    screenshots_dir = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'Concours_Screenshots')
    
    # Create directories if they don't exist
    os.makedirs(download_dir, exist_ok=True)
    os.makedirs(screenshots_dir, exist_ok=True)
    
    options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True  # Don't open PDFs in browser
    })

    # Configure driver path (update this to your actual path)
    edge_path = r'C:\Users\otmane sniba\Desktop\out of topic\msedgedriver.exe'
    service = Service(executable_path=edge_path)
    
    driver = webdriver.Edge(service=service, options=options)
    
    # Remove automation flags
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"}
    )
    
    return driver, download_dir, screenshots_dir

# ================== HUMAN-LIKE BEHAVIOR ==================
def human_like_delay(min_seconds=1, max_seconds=3):
    """Add random delays to mimic human behavior."""
    time.sleep(random.uniform(min_seconds, max_seconds))

def human_like_typing(element, text):
    """Simulate human-like typing with random delays."""
    for char in text:
        element.send_keys(char)
        human_like_delay(0.05, 0.15)  # Random delay between keystrokes

def human_like_scroll(driver, scroll_amount=None):
    """Scroll the page like a human."""
    if scroll_amount is None:
        scroll_amount = random.randint(300, 700)
    
    driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
    human_like_delay()

# ================== EMPLOI PUBLIC SPECIFIC FUNCTIONS ==================
def navigate_to_emploi_public(driver):
    """Navigate to the emploi-public.ma website."""
    try:
        spinner = Spinner("Navigating to emploi-public.ma")
        spinner.start()
        
        driver.get("https://www.emploi-public.ma/fr/")
        
        # Wait for the page to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        spinner.stop()
        
        # Check if we're on the right page
        if "emploi-public.ma" not in driver.current_url:
            print(Fore.RED + "✗ Failed to navigate to emploi-public.ma" + Style.RESET_ALL)
            return False
            
        print(Fore.GREEN + "✓ Successfully navigated to emploi-public.ma" + Style.RESET_ALL)
        return True
    except Exception as e:
        if 'spinner' in locals():
            spinner.stop()
        print(Fore.RED + f"✗ Error navigating to emploi-public.ma: {e}" + Style.RESET_ALL)
        return False

def navigate_to_concours_list(driver):
    """Navigate to the concours list page using multiple approaches."""
    try:
        spinner = Spinner("Navigating to concours list page")
        spinner.start()
        
        # Try direct navigation first (most reliable)
        driver.get("https://www.emploi-public.ma/fr/concours-liste")
        human_like_delay(3, 5)
        
        # Check if we're on a concours page
        if "concours" in driver.current_url:
            spinner.stop()
            print(Fore.GREEN + "✓ Successfully navigated to concours list page" + Style.RESET_ALL)
            return True
        
        # If direct navigation failed, try alternative URLs
        alternative_urls = [
            "https://www.emploi-public.ma/fr/concours",
            "https://www.emploi-public.ma/fr/concours-recrutement",
            "https://www.emploi-public.ma/fr/offres-emploi"
        ]
        
        for url in alternative_urls:
            spinner.message = f"Trying alternative URL: {url}"
            driver.get(url)
            human_like_delay(3, 5)
            
            if "concours" in driver.current_url or "offres" in driver.current_url:
                spinner.stop()
                print(Fore.GREEN + "✓ Successfully navigated to concours page" + Style.RESET_ALL)
                return True
        
        # If all direct navigation attempts failed, try from homepage
        spinner.message = "Trying navigation from homepage"
        driver.get("https://www.emploi-public.ma/fr/")
        human_like_delay(3, 5)
        
        # Look for concours links on homepage
        concours_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'concours') or contains(text(), 'Concours')]")
        if concours_links:
            for link in concours_links:
                try:
                    # Scroll to make the link visible
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
                    human_like_delay(1, 2)
                    
                    # Click the link
                    link.click()
                    human_like_delay(3, 5)
                    
                    if "concours" in driver.current_url:
                        spinner.stop()
                        print(Fore.GREEN + "✓ Successfully navigated to concours page" + Style.RESET_ALL)
                        return True
                except Exception as e:
                    continue
        
        spinner.stop()
        print(Fore.RED + "✗ Failed to navigate to concours list page" + Style.RESET_ALL)
        return False
    except Exception as e:
        if 'spinner' in locals():
            spinner.stop()
        print(Fore.RED + f"✗ Error navigating to concours list page: {e}" + Style.RESET_ALL)
        return False

def navigate_to_tous_les_concours(driver):
    """Navigate to the 'Tous les concours' page."""
    try:
        spinner = Spinner("Navigating to 'Tous les concours' page")
        spinner.start()
        
        # Try direct navigation first
        driver.get("https://www.emploi-public.ma/fr/concours-liste")
        human_like_delay(3, 5)
        
        # Look for "Tous les concours" link or button
        try:
            # Method 1: Look for link with text
            tous_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Tous les concours')]")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tous_link)
            human_like_delay(1, 2)
            tous_link.click()
            human_like_delay(3, 5)
            spinner.stop()
            print(Fore.GREEN + "✓ Successfully navigated to 'Tous les concours' page" + Style.RESET_ALL)
            return True
        except:
            try:
                # Method 2: Look for button with text
                tous_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Tous les concours')]")
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tous_button)
                human_like_delay(1, 2)
                tous_button.click()
                human_like_delay(3, 5)
                spinner.stop()
                print(Fore.GREEN + "✓ Successfully navigated to 'Tous les concours' page" + Style.RESET_ALL)
                return True
            except:
                try:
                    # Method 3: Look for any element with text
                    tous_element = driver.find_element(By.XPATH, "//*[contains(text(), 'Tous les concours')]")
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tous_element)
                    human_like_delay(1, 2)
                    tous_element.click()
                    human_like_delay(3, 5)
                    spinner.stop()
                    print(Fore.GREEN + "✓ Successfully navigated to 'Tous les concours' page" + Style.RESET_ALL)
                    return True
                except:
                    # Method 4: Try to find the tab or navigation element
                    try:
                        nav_elements = driver.find_elements(By.CSS_SELECTOR, ".nav-item, .tab, .nav-link")
                        for element in nav_elements:
                            if "tous" in element.text.lower() or "concours" in element.text.lower():
                                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                                human_like_delay(1, 2)
                                element.click()
                                human_like_delay(3, 5)
                                spinner.stop()
                                print(Fore.GREEN + "✓ Successfully navigated to 'Tous les concours' page" + Style.RESET_ALL)
                                return True
                    except:
                        pass
        
        # If all attempts failed, we're probably already on the concours list page
        spinner.stop()
        print(Fore.YELLOW + "⚠ Could not find 'Tous les concours' link, assuming we're already on the correct page" + Style.RESET_ALL)
        return True
    except Exception as e:
        if 'spinner' in locals():
            spinner.stop()
        print(Fore.RED + f"✗ Error navigating to 'Tous les concours' page: {e}" + Style.RESET_ALL)
        return False

def get_concours_urls_with_pagination(driver, num_concours):
    """Extract URLs for concours listings across multiple pages if needed."""
    try:
        spinner = Spinner("Extracting concours URLs")
        spinner.start()
        
        # Initialize list to store concours URLs
        all_concours_urls = []
        current_page = 1
        
        # Continue extracting until we have enough concours or no more pages
        while len(all_concours_urls) < num_concours:
            # Wait for the page to fully load
            human_like_delay(2, 3)
            
            # Find all concours cards on current page
            cards = driver.find_elements(By.CSS_SELECTOR, ".card")
            
            # If no cards found, try alternative selectors
            if not cards:
                cards = driver.find_elements(By.CSS_SELECTOR, "article, .concours-item, .listing-item")
            
            # If still no cards, try XPath
            if not cards:
                cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'card') or contains(@class, 'concours') or contains(@class, 'offre')]")
            
            # If still no cards, try to find any clickable elements
            if not cards:
                cards = driver.find_elements(By.XPATH, "//a[contains(@href, 'concours/details/')]")
                if not cards:
                    cards = driver.find_elements(By.XPATH, "//a[contains(@href, 'concours')]")
            
            # Extract URLs from each card
            for card in cards:
                try:
                    # Extract URL
                    url = ""
                    try:
                        # Try to find a link in the card
                        link = card.find_element(By.TAG_NAME, "a")
                        url = link.get_attribute("href")
                    except:
                        # If no link found, try to find a button
                        try:
                            button = card.find_element(By.TAG_NAME, "button")
                            # Get the onclick attribute
                            onclick = button.get_attribute("onclick")
                            if onclick and "window.location" in onclick:
                                url = onclick.split("'")[1]
                        except:
                            # If card itself is a link
                            try:
                                url = card.get_attribute("href")
                            except:
                                pass
                    
                    # Only add if we have a URL and haven't reached the limit
                    if url and "concours" in url and len(all_concours_urls) < num_concours:
                        all_concours_urls.append(url)
                        
                        # If we have enough concours, break
                        if len(all_concours_urls) >= num_concours:
                            break
                except Exception as e:
                    print(Fore.YELLOW + f"⚠ Error extracting URL from card: {e}" + Style.RESET_ALL)
            
            # If we have enough concours, break
            if len(all_concours_urls) >= num_concours:
                break
            
            # Try to navigate to the next page
            try:
                # Check if there's a next page button
                next_button = None
                try:
                    next_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Next') or contains(text(), 'Suivant') or contains(@aria-label, 'Next') or contains(@class, 'next')]")
                except:
                    try:
                        next_button = driver.find_element(By.CSS_SELECTOR, ".pagination .next, .pagination .page-next")
                    except:
                        pass
                
                if next_button:
                    # Check if the next button is disabled
                    disabled = next_button.get_attribute("disabled") or next_button.get_attribute("aria-disabled") == "true" or "disabled" in next_button.get_attribute("class") or not next_button.is_enabled()
                    
                    if not disabled:
                        spinner.message = f"Navigating to page {current_page + 1}"
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
                        human_like_delay(1, 2)
                        next_button.click()
                        human_like_delay(3, 5)
                        current_page += 1
                        continue
                
                # If no next button or it's disabled, we've reached the last page
                break
            except:
                # If navigation fails, try direct URL manipulation
                try:
                    current_url = driver.current_url
                    if "page=" in current_url:
                        new_url = re.sub(r'page=\d+', f'page={current_page + 1}', current_url)
                    else:
                        if "?" in current_url:
                            new_url = current_url + f"&page={current_page + 1}"
                        else:
                            new_url = current_url + f"?page={current_page + 1}"
                    
                    spinner.message = f"Navigating to page {current_page + 1}"
                    driver.get(new_url)
                    human_like_delay(3, 5)
                    current_page += 1
                    
                    # Check if we're still on the same page (URL manipulation didn't work)
                    if driver.current_url == current_url:
                        break
                    
                    continue
                except:
                    # If all navigation attempts fail, we've reached the last page
                    break
        
        spinner.stop()
        
        # Limit to the requested number of concours
        if len(all_concours_urls) > num_concours:
            all_concours_urls = all_concours_urls[:num_concours]
        
        print(Fore.GREEN + f"✓ Extracted {len(all_concours_urls)} concours URLs" + Style.RESET_ALL)
        return all_concours_urls
    except Exception as e:
        if 'spinner' in locals():
            spinner.stop()
        print(Fore.RED + f"✗ Error extracting concours URLs: {e}" + Style.RESET_ALL)
        return []

def extract_concours_details(driver, url):
    """Extract all details from a concours page using improved selectors."""
    try:
        print(Fore.CYAN + f"Extracting details from {url}..." + Style.RESET_ALL)
        
        # Navigate to the concours page
        driver.get(url)
        
        # Wait for the page to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Initialize concours info dictionary with default values
        info = {
            "url": url,
            "title": "Concours",
            "ministry": "Non spécifié",
            "specialite": "Non spécifié",
            "grade": "Non spécifié",
            "postes": "Non spécifié",
            "type_recrutement": "Non spécifié",
            "type_depot": "Non spécifié",
            "date_depot": "Non spécifié",
            "date_concours": "Non spécifié",
            "date_publication": "Non spécifié",
            "site_depot": "Non spécifié"
        }
        
        # Extract title - try multiple methods
        try:
            # Method 1: Look for h1 or h2 with title class
            title_element = driver.find_element(By.CSS_SELECTOR, "h1, h2.title, .concours-title")
            if title_element and title_element.text.strip():
                info["title"] = title_element.text.strip()
                print(Fore.GREEN + f"✓ Extracted title: {info['title']}" + Style.RESET_ALL)
        except:
            try:
                # Method 2: Look for any h1
                title_element = driver.find_element(By.TAG_NAME, "h1")
                if title_element and title_element.text.strip():
                    info["title"] = title_element.text.strip()
                    print(Fore.GREEN + f"✓ Extracted title: {info['title']}" + Style.RESET_ALL)
            except:
                try:
                    # Method 3: Use JavaScript to get the page title
                    page_title = driver.execute_script("return document.title")
                    if page_title and "EMPLOI-PUBLIC" in page_title:
                        info["title"] = page_title.replace("EMPLOI-PUBLIC - ", "").strip()
                        print(Fore.GREEN + f"✓ Extracted title from page title: {info['title']}" + Style.RESET_ALL)
                except:
                    print(Fore.YELLOW + "⚠ Could not extract title" + Style.RESET_ALL)
        
        # IMPROVED EXTRACTION METHOD 1: Direct text extraction
        # This method looks for specific text labels and extracts their adjacent values
        
        # Extract ministry/administration
        try:
            ministry_element = driver.find_element(By.XPATH, "//*[contains(text(), 'Administration qui recrute')]/following-sibling::*")
            if ministry_element and ministry_element.text.strip():
                info["ministry"] = ministry_element.text.strip()
                print(Fore.GREEN + f"✓ Extracted ministry: {info['ministry']}" + Style.RESET_ALL)
        except:
            try:
                ministry_element = driver.find_element(By.XPATH, "//div[contains(text(), 'Administration qui recrute')]/following::div[1]")
                if ministry_element and ministry_element.text.strip():
                    info["ministry"] = ministry_element.text.strip()
                    print(Fore.GREEN + f"✓ Extracted ministry (alt method): {info['ministry']}" + Style.RESET_ALL)
            except:
                try:
                    # Try to find the text directly
                    page_text = driver.find_element(By.TAG_NAME, "body").text
                    ministry_match = re.search(r"Administration qui recrute\s*\n*\s*(.*?)(?:\n|$)", page_text)
                    if ministry_match:
                        info["ministry"] = ministry_match.group(1).strip()
                        print(Fore.GREEN + f"✓ Extracted ministry (regex): {info['ministry']}" + Style.RESET_ALL)
                except:
                    print(Fore.YELLOW + "⚠ Could not extract ministry" + Style.RESET_ALL)
        
        # Extract deposit deadline
        try:
            date_depot_element = driver.find_element(By.XPATH, "//*[contains(text(), 'Délai de dépôt')]/following-sibling::*")
            if date_depot_element and date_depot_element.text.strip():
                info["date_depot"] = date_depot_element.text.strip()
                print(Fore.GREEN + f"✓ Extracted deposit deadline: {info['date_depot']}" + Style.RESET_ALL)
        except:
            try:
                date_depot_element = driver.find_element(By.XPATH, "//div[contains(text(), 'Délai de dépôt')]/following::div[1]")
                if date_depot_element and date_depot_element.text.strip():
                    info["date_depot"] = date_depot_element.text.strip()
                    print(Fore.GREEN + f"✓ Extracted deposit deadline (alt method): {info['date_depot']}" + Style.RESET_ALL)
            except:
                try:
                    # Try to find the text directly
                    page_text = driver.find_element(By.TAG_NAME, "body").text
                    date_depot_match = re.search(r"Délai de dépôt des candidatures\s*\n*\s*(.*?)(?:\n|$)", page_text)
                    if date_depot_match:
                        info["date_depot"] = date_depot_match.group(1).strip()
                        print(Fore.GREEN + f"✓ Extracted deposit deadline (regex): {info['date_depot']}" + Style.RESET_ALL)
                except:
                    print(Fore.YELLOW + "⚠ Could not extract deposit deadline" + Style.RESET_ALL)
        
        # Extract concours date
        try:
            date_concours_element = driver.find_element(By.XPATH, "//*[contains(text(), 'Date du concours')]/following-sibling::*")
            if date_concours_element and date_concours_element.text.strip():
                info["date_concours"] = date_concours_element.text.strip()
                print(Fore.GREEN + f"✓ Extracted concours date: {info['date_concours']}" + Style.RESET_ALL)
        except:
            try:
                date_concours_element = driver.find_element(By.XPATH, "//div[contains(text(), 'Date du concours')]/following::div[1]")
                if date_concours_element and date_concours_element.text.strip():
                    info["date_concours"] = date_concours_element.text.strip()
                    print(Fore.GREEN + f"✓ Extracted concours date (alt method): {info['date_concours']}" + Style.RESET_ALL)
            except:
                try:
                    # Try to find the text directly
                    page_text = driver.find_element(By.TAG_NAME, "body").text
                    date_concours_match = re.search(r"Date du concours\s*\n*\s*(.*?)(?:\n|$)", page_text)
                    if date_concours_match:
                        info["date_concours"] = date_concours_match.group(1).strip()
                        print(Fore.GREEN + f"✓ Extracted concours date (regex): {info['date_concours']}" + Style.RESET_ALL)
                except:
                    print(Fore.YELLOW + "⚠ Could not extract concours date" + Style.RESET_ALL)
        
        # Extract publication date
        try:
            date_publication_element = driver.find_element(By.XPATH, "//*[contains(text(), 'Date de publication')]/following-sibling::*")
            if date_publication_element and date_publication_element.text.strip():
                info["date_publication"] = date_publication_element.text.strip()
                print(Fore.GREEN + f"✓ Extracted publication date: {info['date_publication']}" + Style.RESET_ALL)
        except:
            try:
                date_publication_element = driver.find_element(By.XPATH, "//div[contains(text(), 'Date de publication')]/following::div[1]")
                if date_publication_element and date_publication_element.text.strip():
                    info["date_publication"] = date_publication_element.text.strip()
                    print(Fore.GREEN + f"✓ Extracted publication date (alt method): {info['date_publication']}" + Style.RESET_ALL)
            except:
                try:
                    # Try to find the text directly
                    page_text = driver.find_element(By.TAG_NAME, "body").text
                    date_publication_match = re.search(r"Date de publication\s*\n*\s*(.*?)(?:\n|$)", page_text)
                    if date_publication_match:
                        info["date_publication"] = date_publication_match.group(1).strip()
                        print(Fore.GREEN + f"✓ Extracted publication date (regex): {info['date_publication']}" + Style.RESET_ALL)
                except:
                    print(Fore.YELLOW + "⚠ Could not extract publication date" + Style.RESET_ALL)
        
        # Extract specialty
        try:
            specialite_element = driver.find_element(By.XPATH, "//*[contains(text(), 'Spécialité')]/following-sibling::*")
            if specialite_element and specialite_element.text.strip():
                info["specialite"] = specialite_element.text.strip()
                print(Fore.GREEN + f"✓ Extracted specialty: {info['specialite']}" + Style.RESET_ALL)
        except:
            try:
                specialite_element = driver.find_element(By.XPATH, "//div[contains(text(), 'Spécialité')]/following::div[1]")
                if specialite_element and specialite_element.text.strip():
                    info["specialite"] = specialite_element.text.strip()
                    print(Fore.GREEN + f"✓ Extracted specialty (alt method): {info['specialite']}" + Style.RESET_ALL)
            except:
                try:
                    # Try to find the text directly
                    page_text = driver.find_element(By.TAG_NAME, "body").text
                    specialite_match = re.search(r"Spécialité\s*:?\s*\n*\s*(.*?)(?:\n|$)", page_text)
                    if specialite_match:
                        info["specialite"] = specialite_match.group(1).strip()
                        print(Fore.GREEN + f"✓ Extracted specialty (regex): {info['specialite']}" + Style.RESET_ALL)
                except:
                    print(Fore.YELLOW + "⚠ Could not extract specialty" + Style.RESET_ALL)
        
        # Extract grade
        try:
            grade_element = driver.find_element(By.XPATH, "//*[contains(text(), 'Grade')]/following-sibling::*")
            if grade_element and grade_element.text.strip():
                info["grade"] = grade_element.text.strip()
                print(Fore.GREEN + f"✓ Extracted grade: {info['grade']}" + Style.RESET_ALL)
        except:
            try:
                grade_element = driver.find_element(By.XPATH, "//div[contains(text(), 'Grade')]/following::div[1]")
                if grade_element and grade_element.text.strip():
                    info["grade"] = grade_element.text.strip()
                    print(Fore.GREEN + f"✓ Extracted grade (alt method): {info['grade']}" + Style.RESET_ALL)
            except:
                try:
                    # Try to find the text directly
                    page_text = driver.find_element(By.TAG_NAME, "body").text
                    grade_match = re.search(r"Grade\s*:?\s*\n*\s*(.*?)(?:\n|$)", page_text)
                    if grade_match:
                        info["grade"] = grade_match.group(1).strip()
                        print(Fore.GREEN + f"✓ Extracted grade (regex): {info['grade']}" + Style.RESET_ALL)
                except:
                    print(Fore.YELLOW + "⚠ Could not extract grade" + Style.RESET_ALL)
        
        # Extract number of positions
        try:
            postes_element = driver.find_element(By.XPATH, "//*[contains(text(), 'Nombre de postes')]/following-sibling::*")
            if postes_element and postes_element.text.strip():
                info["postes"] = postes_element.text.strip()
                print(Fore.GREEN + f"✓ Extracted number of positions: {info['postes']}" + Style.RESET_ALL)
        except:
            try:
                postes_element = driver.find_element(By.XPATH, "//div[contains(text(), 'Nombre de postes')]/following::div[1]")
                if postes_element and postes_element.text.strip():
                    info["postes"] = postes_element.text.strip()
                    print(Fore.GREEN + f"✓ Extracted number of positions (alt method): {info['postes']}" + Style.RESET_ALL)
            except:
                try:
                    # Try to find the text directly
                    page_text = driver.find_element(By.TAG_NAME, "body").text
                    postes_match = re.search(r"Nombre de postes\s*:?\s*\n*\s*(.*?)(?:\n|$)", page_text)
                    if postes_match:
                        info["postes"] = postes_match.group(1).strip()
                        print(Fore.GREEN + f"✓ Extracted number of positions (regex): {info['postes']}" + Style.RESET_ALL)
                except:
                    print(Fore.YELLOW + "⚠ Could not extract number of positions" + Style.RESET_ALL)
        
        # Extract recruitment type
        try:
            type_recrutement_element = driver.find_element(By.XPATH, "//*[contains(text(), 'Type de recrutement')]/following-sibling::*")
            if type_recrutement_element and type_recrutement_element.text.strip():
                info["type_recrutement"] = type_recrutement_element.text.strip()
                print(Fore.GREEN + f"✓ Extracted recruitment type: {info['type_recrutement']}" + Style.RESET_ALL)
        except:
            try:
                type_recrutement_element = driver.find_element(By.XPATH, "//div[contains(text(), 'Type de recrutement')]/following::div[1]")
                if type_recrutement_element and type_recrutement_element.text.strip():
                    info["type_recrutement"] = type_recrutement_element.text.strip()
                    print(Fore.GREEN + f"✓ Extracted recruitment type (alt method): {info['type_recrutement']}" + Style.RESET_ALL)
            except:
                try:
                    # Try to find the text directly
                    page_text = driver.find_element(By.TAG_NAME, "body").text
                    type_recrutement_match = re.search(r"Type de recrutement\s*:?\s*\n*\s*(.*?)(?:\n|$)", page_text)
                    if type_recrutement_match:
                        info["type_recrutement"] = type_recrutement_match.group(1).strip()
                        print(Fore.GREEN + f"✓ Extracted recruitment type (regex): {info['type_recrutement']}" + Style.RESET_ALL)
                except:
                    print(Fore.YELLOW + "⚠ Could not extract recruitment type" + Style.RESET_ALL)
        
        # Extract deposit type
        try:
            type_depot_element = driver.find_element(By.XPATH, "//*[contains(text(), 'Type de dépôt')]/following-sibling::*")
            if type_depot_element and type_depot_element.text.strip():
                info["type_depot"] = type_depot_element.text.strip()
                print(Fore.GREEN + f"✓ Extracted deposit type: {info['type_depot']}" + Style.RESET_ALL)
        except:
            try:
                type_depot_element = driver.find_element(By.XPATH, "//div[contains(text(), 'Type de dépôt')]/following::div[1]")
                if type_depot_element and type_depot_element.text.strip():
                    info["type_depot"] = type_depot_element.text.strip()
                    print(Fore.GREEN + f"✓ Extracted deposit type (alt method): {info['type_depot']}" + Style.RESET_ALL)
            except:
                try:
                    # Try to find the text directly
                    page_text = driver.find_element(By.TAG_NAME, "body").text
                    type_depot_match = re.search(r"Type de dépôt\s*:?\s*\n*\s*(.*?)(?:\n|$)", page_text)
                    if type_depot_match:
                        info["type_depot"] = type_depot_match.group(1).strip()
                        print(Fore.GREEN + f"✓ Extracted deposit type (regex): {info['type_depot']}" + Style.RESET_ALL)
                except:
                    print(Fore.YELLOW + "⚠ Could not extract deposit type" + Style.RESET_ALL)
        
        # Extract deposit site
        try:
            site_depot_element = driver.find_element(By.XPATH, "//*[contains(text(), 'Site de dépôt')]/following-sibling::*")
            if site_depot_element and site_depot_element.text.strip():
                info["site_depot"] = site_depot_element.text.strip()
                print(Fore.GREEN + f"✓ Extracted deposit site: {info['site_depot']}" + Style.RESET_ALL)
        except:
            try:
                site_depot_element = driver.find_element(By.XPATH, "//div[contains(text(), 'Site de dépôt')]/following::div[1]")
                if site_depot_element and site_depot_element.text.strip():
                    info["site_depot"] = site_depot_element.text.strip()
                    print(Fore.GREEN + f"✓ Extracted deposit site (alt method): {info['site_depot']}" + Style.RESET_ALL)
            except:
                try:
                    # Try to find the text directly
                    page_text = driver.find_element(By.TAG_NAME, "body").text
                    site_depot_match = re.search(r"Site de dépôt\s*:?\s*\n*\s*(.*?)(?:\n|$)", page_text)
                    if site_depot_match:
                        info["site_depot"] = site_depot_match.group(1).strip()
                        print(Fore.GREEN + f"✓ Extracted deposit site (regex): {info['site_depot']}" + Style.RESET_ALL)
                except:
                    print(Fore.YELLOW + "⚠ Could not extract deposit site" + Style.RESET_ALL)
        
        # IMPROVED EXTRACTION METHOD 2: Direct DOM inspection
        # This method directly inspects the DOM structure to find information
        
        # Try to find detail sections by class or structure
        try:
            # Look for cards or sections that might contain the details
            detail_cards = driver.find_elements(By.CSS_SELECTOR, ".card, .section, .details, .info-block")
            
            for card in detail_cards:
                card_text = card.text.strip()
                
                # Check if this card contains detail information
                if "Administration qui recrute" in card_text and info["ministry"] == "Non spécifié":
                    # Extract ministry
                    try:
                        ministry_lines = card_text.split("\n")
                        for i, line in enumerate(ministry_lines):
                            if "Administration qui recrute" in line and i+1 < len(ministry_lines):
                                info["ministry"] = ministry_lines[i+1].strip()
                                print(Fore.GREEN + f"✓ Extracted ministry (card method): {info['ministry']}" + Style.RESET_ALL)
                                break
                    except:
                        pass
                
                # Check if this card contains date information
                if "Délai de dépôt" in card_text and info["date_depot"] == "Non spécifié":
                    # Extract deposit deadline
                    try:
                        date_lines = card_text.split("\n")
                        for i, line in enumerate(date_lines):
                            if "Délai de dépôt" in line and i+1 < len(date_lines):
                                info["date_depot"] = date_lines[i+1].strip()
                                print(Fore.GREEN + f"✓ Extracted deposit deadline (card method): {info['date_depot']}" + Style.RESET_ALL)
                                break
                    except:
                        pass
                
                # Check if this card contains concours date information
                if "Date du concours" in card_text and info["date_concours"] == "Non spécifié":
                    # Extract concours date
                    try:
                        date_lines = card_text.split("\n")
                        for i, line in enumerate(date_lines):
                            if "Date du concours" in line and i+1 < len(date_lines):
                                info["date_concours"] = date_lines[i+1].strip()
                                print(Fore.GREEN + f"✓ Extracted concours date (card method): {info['date_concours']}" + Style.RESET_ALL)
                                break
                    except:
                        pass
                
                # Check if this card contains publication date information
                if "Date de publication" in card_text and info["date_publication"] == "Non spécifié":
                    # Extract publication date
                    try:
                        date_lines = card_text.split("\n")
                        for i, line in enumerate(date_lines):
                            if "Date de publication" in line and i+1 < len(date_lines):
                                info["date_publication"] = date_lines[i+1].strip()
                                print(Fore.GREEN + f"✓ Extracted publication date (card method): {info['date_publication']}" + Style.RESET_ALL)
                                break
                    except:
                        pass
        except:
            pass
        
        # IMPROVED EXTRACTION METHOD 3: JavaScript extraction
        # This method uses JavaScript to extract information directly from the page
        
        try:
            # Use JavaScript to extract text content from the page
            page_content = driver.execute_script("""
                return document.body.innerText;
            """)
            
            # Extract ministry if not already found
            if info["ministry"] == "Non spécifié":
                ministry_match = re.search(r"Administration qui recrute\s*\n*\s*(.*?)(?:\n|$)", page_content)
                if ministry_match:
                    info["ministry"] = ministry_match.group(1).strip()
                    print(Fore.GREEN + f"✓ Extracted ministry (JS method): {info['ministry']}" + Style.RESET_ALL)
            
            # Extract deposit deadline if not already found
            if info["date_depot"] == "Non spécifié":
                date_depot_match = re.search(r"Délai de dépôt des candidatures\s*\n*\s*(.*?)(?:\n|$)", page_content)
                if date_depot_match:
                    info["date_depot"] = date_depot_match.group(1).strip()
                    print(Fore.GREEN + f"✓ Extracted deposit deadline (JS method): {info['date_depot']}" + Style.RESET_ALL)
            
            # Extract concours date if not already found
            if info["date_concours"] == "Non spécifié":
                date_concours_match = re.search(r"Date du concours\s*\n*\s*(.*?)(?:\n|$)", page_content)
                if date_concours_match:
                    info["date_concours"] = date_concours_match.group(1).strip()
                    print(Fore.GREEN + f"✓ Extracted concours date (JS method): {info['date_concours']}" + Style.RESET_ALL)
            
            # Extract publication date if not already found
            if info["date_publication"] == "Non spécifié":
                date_publication_match = re.search(r"Date de publication\s*\n*\s*(.*?)(?:\n|$)", page_content)
                if date_publication_match:
                    info["date_publication"] = date_publication_match.group(1).strip()
                    print(Fore.GREEN + f"✓ Extracted publication date (JS method): {info['date_publication']}" + Style.RESET_ALL)
            
            # Extract specialty if not already found
            if info["specialite"] == "Non spécifié":
                specialite_match = re.search(r"Spécialité\s*:?\s*\n*\s*(.*?)(?:\n|$)", page_content)
                if specialite_match:
                    info["specialite"] = specialite_match.group(1).strip()
                    print(Fore.GREEN + f"✓ Extracted specialty (JS method): {info['specialite']}" + Style.RESET_ALL)
            
            # Extract grade if not already found
            if info["grade"] == "Non spécifié":
                grade_match = re.search(r"Grade\s*:?\s*\n*\s*(.*?)(?:\n|$)", page_content)
                if grade_match:
                    info["grade"] = grade_match.group(1).strip()
                    print(Fore.GREEN + f"✓ Extracted grade (JS method): {info['grade']}" + Style.RESET_ALL)
            
            # Extract number of positions if not already found
            if info["postes"] == "Non spécifié":
                postes_match = re.search(r"Nombre de postes\s*:?\s*\n*\s*(.*?)(?:\n|$)", page_content)
                if postes_match:
                    info["postes"] = postes_match.group(1).strip()
                    print(Fore.GREEN + f"✓ Extracted number of positions (JS method): {info['postes']}" + Style.RESET_ALL)
            
            # Extract recruitment type if not already found
            if info["type_recrutement"] == "Non spécifié":
                type_recrutement_match = re.search(r"Type de recrutement\s*:?\s*\n*\s*(.*?)(?:\n|$)", page_content)
                if type_recrutement_match:
                    info["type_recrutement"] = type_recrutement_match.group(1).strip()
                    print(Fore.GREEN + f"✓ Extracted recruitment type (JS method): {info['type_recrutement']}" + Style.RESET_ALL)
            
            # Extract deposit type if not already found
            if info["type_depot"] == "Non spécifié":
                type_depot_match = re.search(r"Type de dépôt\s*:?\s*\n*\s*(.*?)(?:\n|$)", page_content)
                if type_depot_match:
                    info["type_depot"] = type_depot_match.group(1).strip()
                    print(Fore.GREEN + f"✓ Extracted deposit type (JS method): {info['type_depot']}" + Style.RESET_ALL)
            
            # Extract deposit site if not already found
            if info["site_depot"] == "Non spécifié":
                site_depot_match = re.search(r"Site de dépôt\s*:?\s*\n*\s*(.*?)(?:\n|$)", page_content)
                if site_depot_match:
                    info["site_depot"] = site_depot_match.group(1).strip()
                    print(Fore.GREEN + f"✓ Extracted deposit site (JS method): {info['site_depot']}" + Style.RESET_ALL)
        except:
            pass
        
        return info
    except Exception as e:
        print(Fore.RED + f"✗ Error extracting concours details: {e}" + Style.RESET_ALL)
        return None

def create_formatted_screenshot(driver, info, screenshot_path):
    """Create a formatted screenshot with the extracted information."""
    try:
        print(Fore.CYAN + "Creating formatted screenshot..." + Style.RESET_ALL)
        
        # Inject CSS to improve the appearance
        driver.execute_script("""
            // Create a style element
            var style = document.createElement('style');
            style.type = 'text/css';
            style.innerHTML = `
                .manus-enhanced-card {
                    background-color: white;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    margin: 10px;
                    padding: 20px;
                    font-family: Arial, sans-serif;
                }
                .manus-card-title {
                    color: #003366;
                    font-size: 20px;
                    font-weight: bold;
                    margin-bottom: 15px;
                    padding-bottom: 10px;
                    border-bottom: 1px solid #eee;
                }
                .manus-card-content {
                    margin-top: 10px;
                }
                .manus-label {
                    font-weight: bold;
                    margin-bottom: 5px;
                }
                .manus-value {
                    color: #003366;
                    font-weight: bold;
                    margin-bottom: 15px;
                }
                .manus-container {
                    display: flex;
                    justify-content: space-between;
                    max-width: 1200px;
                    margin: 0 auto;
                    background-color: #f5f5f5;
                    padding: 20px;
                    border-radius: 12px;
                }
                .manus-card {
                    width: 48%;
                }
            `;
            document.head.appendChild(style);
            
            // Create container for the cards
            var container = document.createElement('div');
            container.className = 'manus-container';
            container.id = 'manus-screenshot-container';
            document.body.appendChild(container);
        """)
        
        # Create the detail card
        detail_html = """
        <div class="manus-enhanced-card manus-card">
            <div class="manus-card-title">Détail de l'annonce</div>
            <div class="manus-card-content">
                <div class="manus-label">Administration qui recrute</div>
                <div class="manus-value">{ministry}</div>
                
                <div class="manus-label">Délai de dépôt des candidatures</div>
                <div class="manus-value">{date_depot}</div>
                
                <div class="manus-label">Date du concours</div>
                <div class="manus-value">{date_concours}</div>
                
                <div class="manus-label">Date de publication</div>
                <div class="manus-value">{date_publication}</div>
            </div>
        </div>
        """.format(
            ministry=info["ministry"],
            date_depot=info["date_depot"],
            date_concours=info["date_concours"],
            date_publication=info["date_publication"]
        )
        
        # Create the description card
        description_html = """
        <div class="manus-enhanced-card manus-card">
            <div class="manus-card-title">Description</div>
            <div class="manus-card-content">
                <div class="manus-label">Spécialité :</div>
                <div class="manus-value">{specialite}</div>
                
                <div class="manus-label">Grade :</div>
                <div class="manus-value">{grade}</div>
                
                <div class="manus-label">Nombre de postes :</div>
                <div class="manus-value">{postes}</div>
                
                <div class="manus-label">Type de recrutement :</div>
                <div class="manus-value">{type_recrutement}</div>
                
                <div class="manus-label">Type de dépôt :</div>
                <div class="manus-value">{type_depot}</div>
                
                <div class="manus-label">Site de dépôt :</div>
                <div class="manus-value">{site_depot}</div>
            </div>
        </div>
        """.format(
            specialite=info["specialite"],
            grade=info["grade"],
            postes=info["postes"],
            type_recrutement=info["type_recrutement"],
            type_depot=info["type_depot"],
            site_depot=info["site_depot"]
        )
        
        # Add the cards to the container
        driver.execute_script("""
            var container = document.getElementById('manus-screenshot-container');
            container.innerHTML = arguments[0] + arguments[1];
            
            // Scroll to the container
            container.scrollIntoView({behavior: 'smooth', block: 'center'});
        """, detail_html, description_html)
        
        # Wait for the container to be visible
        human_like_delay(1, 2)
        
        # Take screenshot of the container
        container = driver.find_element(By.ID, "manus-screenshot-container")
        container.screenshot(screenshot_path)
        
        print(Fore.GREEN + f"✓ Saved formatted screenshot to {screenshot_path}" + Style.RESET_ALL)
        return True
    except Exception as e:
        print(Fore.RED + f"✗ Error creating formatted screenshot: {e}" + Style.RESET_ALL)
        return False

def capture_improved_screenshots(driver, urls, screenshots_dir):
    """Capture improved screenshots of the detail sections for each concours page."""
    concours_info = []
    
    print(Fore.CYAN + Style.BRIGHT + "\n📸 CAPTURING DETAILED SCREENSHOTS OF CONCOURS" + Style.RESET_ALL)
    print(Fore.CYAN + "─" * shutil.get_terminal_size().columns + Style.RESET_ALL)
    
    for i, url in enumerate(urls):
        try:
            print(Fore.MAGENTA + f"\nProcessing concours #{i+1}/{len(urls)}..." + Style.RESET_ALL)
            
            spinner = Spinner(f"Navigating to concours #{i+1}")
            spinner.start()
            
            # Extract concours details
            info = extract_concours_details(driver, url)
            
            if not info:
                spinner.stop()
                print(Fore.RED + f"✗ Failed to extract details for concours #{i+1}" + Style.RESET_ALL)
                continue
            
            spinner.stop()
            
            # Add index to info
            info["index"] = i + 1
            
            # Create screenshot paths
            info["screenshot_path"] = os.path.join(screenshots_dir, f"concours_{i+1}_details.png")
            
            # Create formatted screenshot
            if not create_formatted_screenshot(driver, info, info["screenshot_path"]):
                print(Fore.RED + f"✗ Failed to create formatted screenshot for concours #{i+1}" + Style.RESET_ALL)
                
                # Try to take a full page screenshot as fallback
                try:
                    driver.save_screenshot(info["screenshot_path"])
                    print(Fore.GREEN + f"✓ Saved full page screenshot to {info['screenshot_path']}" + Style.RESET_ALL)
                except Exception as e:
                    print(Fore.RED + f"✗ Error taking fallback screenshot: {e}" + Style.RESET_ALL)
            
            # Add to concours info list
            concours_info.append(info)
            
        except Exception as e:
            print(Fore.RED + f"✗ Error processing concours #{i+1}: {e}" + Style.RESET_ALL)
    
    return concours_info

def display_concours_with_screenshots(concours_info):
    """Display a list of concours with screenshots and ask user which ones to download PDFs from."""
    terminal_width = shutil.get_terminal_size().columns
    
    # Create a fancy box for the list
    box_width = min(80, terminal_width - 4)
    horizontal_line = "═" * box_width
    
    print(Fore.YELLOW + "╔" + horizontal_line + "╗")
    
    # Center the text in the box
    text = "LISTE DES CONCOURS CAPTURÉS"
    padding = (box_width - len(text)) // 2
    print(Fore.YELLOW + "║" + " " * padding + Fore.CYAN + Style.BRIGHT + text + Style.NORMAL + " " * (box_width - len(text) - padding) + Fore.YELLOW + "║")
    
    print(Fore.YELLOW + "╠" + horizontal_line + "╣")
    
    # Display each concours
    for info in concours_info:
        # Get the title or use a placeholder
        name = info.get('title', f"Concours #{info['index']}")
        
        # Truncate name if too long
        display_name = name[:box_width-10] + "..." if len(name) > box_width-10 else name
        print(Fore.YELLOW + "║ " + Fore.GREEN + f"{info['index']:2d}. " + Fore.WHITE + display_name + " " * (box_width - len(display_name) - 6) + Fore.YELLOW + "║")
        
        # Display ministry if available
        if info.get('ministry') and info['ministry'] != "Non spécifié":
            ministry = f"   Ministère: {info['ministry']}"
            if len(ministry) > box_width - 4:
                ministry = ministry[:box_width-7] + "..."
            print(Fore.YELLOW + "║ " + Fore.CYAN + ministry + " " * (box_width - len(ministry) - 2) + Fore.YELLOW + "║")
        
        # Display grade if available
        if info.get('grade') and info['grade'] != "Non spécifié":
            grade = f"   Grade: {info['grade']}"
            if len(grade) > box_width - 4:
                grade = grade[:box_width-7] + "..."
            print(Fore.YELLOW + "║ " + Fore.CYAN + grade + " " * (box_width - len(grade) - 2) + Fore.YELLOW + "║")
        
        # Display number of positions if available
        if info.get('postes') and info['postes'] != "Non spécifié":
            postes = f"   Nombre de postes: {info['postes']}"
            if len(postes) > box_width - 4:
                postes = postes[:box_width-7] + "..."
            print(Fore.YELLOW + "║ " + Fore.CYAN + postes + " " * (box_width - len(postes) - 2) + Fore.YELLOW + "║")
        
        # Display specialty if available
        if info.get('specialite') and info['specialite'] != "Non spécifié":
            specialite = f"   Spécialité: {info['specialite']}"
            if len(specialite) > box_width - 4:
                specialite = specialite[:box_width-7] + "..."
            print(Fore.YELLOW + "║ " + Fore.CYAN + specialite + " " * (box_width - len(specialite) - 2) + Fore.YELLOW + "║")
        
        # Display concours date if available
        if info.get('date_concours') and info['date_concours'] != "Non spécifié":
            date_concours = f"   Date du concours: {info['date_concours']}"
            if len(date_concours) > box_width - 4:
                date_concours = date_concours[:box_width-7] + "..."
            print(Fore.YELLOW + "║ " + Fore.CYAN + date_concours + " " * (box_width - len(date_concours) - 2) + Fore.YELLOW + "║")
        
        # Display deposit deadline if available
        if info.get('date_depot') and info['date_depot'] != "Non spécifié":
            date_depot = f"   Délai de dépôt: {info['date_depot']}"
            if len(date_depot) > box_width - 4:
                date_depot = date_depot[:box_width-7] + "..."
            print(Fore.YELLOW + "║ " + Fore.CYAN + date_depot + " " * (box_width - len(date_depot) - 2) + Fore.YELLOW + "║")
        
        # Display screenshot paths
        if info.get('screenshot_path'):
            screenshot = f"   Screenshot: {os.path.basename(info['screenshot_path'])}"
            if len(screenshot) > box_width - 4:
                screenshot = screenshot[:box_width-7] + "..."
            print(Fore.YELLOW + "║ " + Fore.CYAN + screenshot + " " * (box_width - len(screenshot) - 2) + Fore.YELLOW + "║")
        
        print(Fore.YELLOW + "║" + " " * (box_width - 2) + "║")
    
    print(Fore.YELLOW + "╚" + horizontal_line + "╝" + Style.RESET_ALL)
    
    # Open screenshots folder
    try:
        screenshots_dir = os.path.dirname(concours_info[0]['screenshot_path'])
        print(Fore.GREEN + f"\n✓ Screenshots saved to: {screenshots_dir}" + Style.RESET_ALL)
        print(Fore.CYAN + "\nOpening screenshots folder..." + Style.RESET_ALL)
        os.startfile(screenshots_dir)
    except:
        print(Fore.YELLOW + "\n⚠ Could not open screenshots folder automatically" + Style.RESET_ALL)
    
    # Ask user which concours to download PDFs from
    print(Fore.CYAN + Style.BRIGHT + "\nQuels concours voulez-vous télécharger?" + Style.RESET_ALL)
    print(Fore.WHITE + "Entrez les numéros séparés par des virgules (ex: 1,3,5)" + Style.RESET_ALL)
    print(Fore.WHITE + "Ou entrez 'all' pour télécharger tous les concours" + Style.RESET_ALL)
    print(Fore.WHITE + "Ou entrez '0' pour quitter sans télécharger" + Style.RESET_ALL)
    
    while True:
        choice = input(f"\n{Fore.YELLOW}❯ {Style.BRIGHT}Votre choix: {Style.RESET_ALL}").strip().lower()
        
        if choice == '0':
            return []
        
        if choice == 'all':
            return concours_info
        
        try:
            # Parse comma-separated list of numbers
            indices = [int(x.strip()) for x in choice.split(',')]
            
            # Validate indices
            valid_indices = [i for i in indices if 1 <= i <= len(concours_info)]
            
            if not valid_indices:
                print(Fore.RED + "⚠ Aucun numéro valide! Veuillez réessayer." + Style.RESET_ALL)
                continue
            
            # Get selected concours
            selected_concours = [info for info in concours_info if info['index'] in valid_indices]
            
            return selected_concours
        except ValueError:
            print(Fore.RED + "⚠ Format invalide! Veuillez entrer des numéros séparés par des virgules." + Style.RESET_ALL)

def find_and_download_pdfs(driver, download_dir, concours_info):
    """Find and download PDF files from the selected concours pages."""
    all_downloaded_files = []
    
    print(Fore.CYAN + Style.BRIGHT + "\n📥 DOWNLOADING PDFS" + Style.RESET_ALL)
    print(Fore.CYAN + "─" * shutil.get_terminal_size().columns + Style.RESET_ALL)
    
    for info in concours_info:
        try:
            print(Fore.MAGENTA + Style.BRIGHT + f"\n🔍 CONCOURS {info['index']}: {info['title']}" + Style.RESET_ALL)
            print(Fore.MAGENTA + "─" * 30 + Style.RESET_ALL)
            
            spinner = Spinner(f"Navigating to concours #{info['index']}")
            spinner.start()
            
            # Navigate to the concours page
            driver.get(info['url'])
            
            # Wait for the page to load
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            spinner.stop()
            
            # Find and download PDFs
            spinner = Spinner("Looking for PDF files to download")
            spinner.start()
            
            # Wait for the page to fully load
            human_like_delay(3, 5)
            
            # Scroll down to make sure all content is visible
            for _ in range(3):
                human_like_scroll(driver)
                human_like_delay(1, 2)
            
            # Find all PDF links
            pdf_links = driver.find_elements(By.XPATH, "//a[contains(@href, '.pdf')]")
            
            if not pdf_links:
                # Try alternative selectors
                pdf_links = driver.find_elements(By.CSS_SELECTOR, "a[href$='.pdf'], a[href*='download'], a[href*='telecharger']")
            
            if not pdf_links:
                # Try to find any download links
                pdf_links = driver.find_elements(By.XPATH, "//a[contains(text(), 'télécharger') or contains(text(), 'Télécharger') or contains(text(), 'download') or contains(text(), 'Download')]")
            
            if not pdf_links:
                spinner.stop()
                print(Fore.YELLOW + "⚠ No PDF links found on this page" + Style.RESET_ALL)
                continue
            
            spinner.stop()
            print(Fore.GREEN + f"✓ Found {len(pdf_links)} PDF links" + Style.RESET_ALL)
            
            # Clean title for filename
            clean_title = re.sub(r'[\\/*?:"<>|]', '_', info['title'])
            clean_title = clean_title[:50]  # Limit length
            
            downloaded_files = []
            for i, pdf_link in enumerate(pdf_links):
                try:
                    # Get the PDF URL
                    pdf_url = pdf_link.get_attribute('href')
                    if not pdf_url:
                        continue
                    
                    # Get a name for the PDF file
                    pdf_name = f"{clean_title}_Document_{i+1}.pdf"
                    try:
                        # Try to get a better name from the link text or title
                        link_text = pdf_link.text.strip()
                        if link_text and len(link_text) > 3:
                            pdf_name = f"{clean_title}_{link_text}.pdf"
                        else:
                            # Try to get name from title attribute
                            link_title = pdf_link.get_attribute('title')
                            if link_title and len(link_title) > 3:
                                pdf_name = f"{clean_title}_{link_title}.pdf"
                    except:
                        pass
                    
                    # Clean the filename
                    pdf_name = re.sub(r'[\\/*?:"<>|]', '_', pdf_name)  # Replace invalid filename characters
                    
                    # Full path for the PDF file
                    pdf_path = os.path.join(download_dir, pdf_name)
                    
                    download_spinner = Spinner(f"Downloading PDF: {pdf_name}")
                    download_spinner.start()
                    
                    # Method 1: Try clicking the link to download via browser
                    try:
                        # Scroll to make the link visible
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pdf_link)
                        human_like_delay(1, 2)
                        
                        # Click the link
                        pdf_link.click()
                        
                        # Wait for download to start with progress animation
                        for j in range(10):
                            progress_bar(j+1, 10, prefix=f'Downloading {pdf_name}:', suffix='Complete', length=30)
                            time.sleep(0.5)
                        
                        # Check if file was downloaded
                        if any(f.endswith('.pdf') for f in os.listdir(download_dir)):
                            download_spinner.stop()
                            print(Fore.GREEN + f"✓ PDF downloaded successfully: {pdf_name}" + Style.RESET_ALL)
                            downloaded_files.append(pdf_path)
                            continue
                    except Exception as e:
                        pass
                    
                    # Method 2: Download using requests
                    try:
                        download_spinner.message = f"Downloading PDF using alternative method: {pdf_name}"
                        
                        # Get cookies from the browser
                        cookies = driver.get_cookies()
                        cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
                        
                        # Set headers to mimic browser
                        headers = {
                            'User-Agent': driver.execute_script("return navigator.userAgent"),
                            'Referer': driver.current_url
                        }
                        
                        # Download the PDF with progress bar
                        response = requests.get(pdf_url, cookies=cookies_dict, headers=headers, stream=True)
                        
                        if response.status_code == 200:
                            total_size = int(response.headers.get('content-length', 0))
                            block_size = 1024
                            
                            with open(pdf_path, 'wb') as f:
                                if total_size > 0:
                                    for i, data in enumerate(response.iter_content(block_size)):
                                        f.write(data)
                                        progress = min(i * block_size / total_size, 1.0)
                                        progress_bar(int(progress * 100), 100, prefix=f'Downloading {pdf_name}:', suffix='Complete', length=30)
                                else:
                                    f.write(response.content)
                            
                            download_spinner.stop()
                            print(Fore.GREEN + f"✓ PDF downloaded successfully: {pdf_name}" + Style.RESET_ALL)
                            downloaded_files.append(pdf_path)
                        else:
                            download_spinner.stop()
                            print(Fore.RED + f"✗ Failed to download PDF. Status code: {response.status_code}" + Style.RESET_ALL)
                    except Exception as e:
                        if 'download_spinner' in locals():
                            download_spinner.stop()
                        print(Fore.RED + f"✗ Error downloading PDF: {e}" + Style.RESET_ALL)
                except Exception as e:
                    if 'download_spinner' in locals():
                        download_spinner.stop()
                    print(Fore.RED + f"✗ Error processing PDF link: {e}" + Style.RESET_ALL)
            
            if downloaded_files:
                all_downloaded_files.extend(downloaded_files)
                print(Fore.GREEN + Style.BRIGHT + f"✓ Downloaded {len(downloaded_files)} PDF files for concours #{info['index']}" + Style.RESET_ALL)
                
                # Show list of downloaded files
                for j, file in enumerate(downloaded_files):
                    print(Fore.CYAN + f"  {j+1}. {os.path.basename(file)}" + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + "⚠ No PDF files downloaded for this concours" + Style.RESET_ALL)
        
        except Exception as e:
            print(Fore.RED + f"✗ Error downloading PDFs for concours #{info['index']}: {e}" + Style.RESET_ALL)
    
    return all_downloaded_files

# ================== USER INTERFACE ==================
def get_num_concours():
    """Ask user how many concours to process with an interactive interface."""
    terminal_width = shutil.get_terminal_size().columns
    
    # Create a fancy box for the input
    box_width = min(60, terminal_width - 4)
    horizontal_line = "═" * box_width
    
    print(Fore.YELLOW + "╔" + horizontal_line + "╗")
    
    # Center the text in the box
    text = "COMBIEN DE CONCOURS VOULEZ-VOUS EXPLORER?"
    padding = (box_width - len(text)) // 2
    print(Fore.YELLOW + "║" + " " * padding + Fore.CYAN + Style.BRIGHT + text + Style.NORMAL + " " * (box_width - len(text) - padding) + Fore.YELLOW + "║")
    
    print(Fore.YELLOW + "╚" + horizontal_line + "╝" + Style.RESET_ALL)
    
    while True:
        try:
            # Create a fancy input prompt
            num = int(input(f"\n{Fore.GREEN}❯ {Style.BRIGHT}Entrez le nombre de concours à explorer: {Style.RESET_ALL}").strip())
            if num > 0:
                # Show a confirmation message with animation
                print(f"\n{Fore.CYAN}✓ {Style.BRIGHT}Vous avez choisi d'explorer {Fore.GREEN}{num}{Fore.CYAN} concours.{Style.RESET_ALL}")
                
                # Animated confirmation
                for i in range(5):
                    sys.stdout.write(f"\r{Fore.YELLOW}{'■' * i}{' ' * (5-i)} Préparation en cours...{Style.RESET_ALL}")
                    sys.stdout.flush()
                    time.sleep(0.2)
                print("\n")
                
                return num
            print(Fore.RED + "⚠ Le nombre doit être supérieur à 0!" + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "⚠ Entrée invalide! Veuillez entrer un nombre." + Style.RESET_ALL)

# ================== MAIN PROGRAM ==================
def main():
    print_ascii_banner()
    
    # Fancy separator
    terminal_width = shutil.get_terminal_size().columns
    print(Fore.MAGENTA + Style.BRIGHT + "╔" + "═" * (terminal_width - 2) + "╗")
    centered_text = " Starting Emploi Public PDF Downloader "
    padding = (terminal_width - 2 - len(centered_text)) // 2
    print(Fore.MAGENTA + Style.BRIGHT + "║" + " " * padding + Fore.YELLOW + centered_text + Fore.MAGENTA + " " * (terminal_width - 2 - len(centered_text) - padding) + "║")
    print(Fore.MAGENTA + Style.BRIGHT + "╚" + "═" * (terminal_width - 2) + "╝" + Style.RESET_ALL)
    
    # Ask user how many concours to process
    num_concours = get_num_concours()
    
    driver, download_dir, screenshots_dir = setup_edge_driver()
    
    try:
        # Navigate to emploi-public.ma
        if not navigate_to_emploi_public(driver):
            print(Fore.RED + Style.BRIGHT + "⚠ Failed to access the website. Exiting..." + Style.RESET_ALL)
            return
        
        # Navigate to concours list page
        if not navigate_to_concours_list(driver):
            print(Fore.RED + Style.BRIGHT + "⚠ Failed to navigate to concours list page. Exiting..." + Style.RESET_ALL)
            return
        
        # Navigate to "Tous les concours" page
        if not navigate_to_tous_les_concours(driver):
            print(Fore.YELLOW + Style.BRIGHT + "⚠ Could not navigate to 'Tous les concours' page, continuing with current page..." + Style.RESET_ALL)
        
        # Get concours URLs with pagination support
        concours_urls = get_concours_urls_with_pagination(driver, num_concours)
        
        if not concours_urls:
            print(Fore.RED + Style.BRIGHT + "⚠ No concours URLs found. Exiting..." + Style.RESET_ALL)
            return
        
        # Capture detailed screenshots and extract information
        concours_info = capture_improved_screenshots(driver, concours_urls, screenshots_dir)
        
        if not concours_info:
            print(Fore.RED + Style.BRIGHT + "⚠ Failed to capture concours screenshots. Exiting..." + Style.RESET_ALL)
            return
        
        # Display concours with screenshots and ask user which ones to download PDFs from
        selected_concours = display_concours_with_screenshots(concours_info)
        
        if not selected_concours:
            print(Fore.YELLOW + Style.BRIGHT + "\nAucun concours sélectionné pour téléchargement. Exiting..." + Style.RESET_ALL)
            return
        
        # Download PDFs for selected concours
        downloaded_files = find_and_download_pdfs(driver, download_dir, selected_concours)
        
        # Fancy completion message
        print(Fore.MAGENTA + Style.BRIGHT + "\n" + "═" * terminal_width)
        centered_text = " DOWNLOAD COMPLETE! "
        padding = (terminal_width - len(centered_text)) // 2
        print(" " * padding + Back.GREEN + Fore.WHITE + Style.BRIGHT + centered_text + Style.RESET_ALL)
        print(Fore.MAGENTA + Style.BRIGHT + "═" * terminal_width + Style.RESET_ALL)
        
        # Summary with fancy formatting
        print(Fore.CYAN + Style.BRIGHT + f"\n📊 SUMMARY" + Style.RESET_ALL)
        print(Fore.CYAN + "─" * 30 + Style.RESET_ALL)
        print(Fore.GREEN + f"✓ Downloaded {len(downloaded_files)} PDF files in total" + Style.RESET_ALL)
        print(Fore.GREEN + f"✓ Files saved to: {download_dir}" + Style.RESET_ALL)
        print(Fore.GREEN + f"✓ Screenshots saved to: {screenshots_dir}" + Style.RESET_ALL)
        
        if downloaded_files:
            # Create a fancy prompt for opening the folder
            print(Fore.YELLOW + Style.BRIGHT + "\n" + "─" * terminal_width)
            print(f"📂 Press {Back.CYAN + Fore.WHITE + Style.BRIGHT} ENTER {Style.RESET_ALL + Fore.YELLOW + Style.BRIGHT} to open the download folder..." + Style.RESET_ALL)
            input()
            os.startfile(download_dir)

    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"\n⚠ An error occurred: {e}" + Style.RESET_ALL)
    finally:
        print(Fore.CYAN + "\n🔄 Closing browser..." + Style.RESET_ALL)
        driver.quit()
        
        # Final goodbye message
        print(Fore.GREEN + Style.BRIGHT + "\n✨ Thank you for using Emploi Public PDF Downloader! ✨" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
