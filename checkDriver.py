from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Setup options (you can add any other options you need here)
options = Options()
options.add_argument("--start-maximized")  # Open browser maximized
# You can add other options as needed

# Initialize the WebDriver
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),  # Use the correct path from ChromeDriverManager
    options=options  # Add the options
)

driver.get("https://www.google.com")
print(driver.title)
driver.quit()
