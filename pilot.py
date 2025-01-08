from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import random

# Initialize WebDriver with custom User-Agent
options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.205 Safari/537.36")
driver = webdriver.Chrome(options=options)

# Open the URL
driver.get('https://jobs.lever.co/matchgroup/354cd021-8ea8-45e9-9dea-d1f6a5a0728f/apply')

# Wait for the page to load
wait = WebDriverWait(driver, 10)

# Wait for the form to be present in the DOM
application_form = wait.until(EC.presence_of_element_located((By.ID, "application-form")))

# Extract all application questions
application_questions = application_form.find_elements(By.CSS_SELECTOR, "[class*='application-question']")

# Parse questions using BeautifulSoup
dict_of_questions = {}
for question in application_questions:
    question_html = question.get_attribute('outerHTML')
    soup = BeautifulSoup(question_html, 'html.parser')
    application_label = soup.find('div', class_='application-label')
    application_field = soup.find('div', class_='application-field')
    if application_label:
        dict_of_questions[application_label.text.strip()] = {
            "application_field": application_field,
            "input_types": [input_tag.get('type') for input_tag in application_field.find_all('input')] if application_field else []
        }

# Define fields and dummy data
fields = {
    "Full name✱": "John Doe",
    "Email✱": "johndoe@example.com",
    "Phone ✱": "123-456-7890",
    # "Current location ✱": "New York, NY",
    "Current company": "Example Company",
    "LinkedIn URL": "https://linkedin.com/in/example",
    "Twitter URL": "https://twitter.com/example",
    "GitHub URL": "https://github.com/example",
    "Portfolio URL": "https://example.com",
    "Other website": "https://example-other.com",
    "Do you live in the NYC Area?✱": "Yes",  # Radio button
    "If not, are you willing to relocate?✱": "No",  # Radio button
    "What are your pronouns?": "He/Him",
    "What is your desired compensation for this role?": "$100,000",
}

# Loop through fields and interact with them
for field_label, dummy_value in fields.items():
    try:
        # Locate the application label containing the field name
        label_element = wait.until(EC.presence_of_element_located((
            By.XPATH, f"//div[@class='application-label' and contains(text(), '{field_label.split('✱')[0].strip()}')]"
        )))

        # Scroll to the element to simulate human behavior
        # driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", label_element)

        # Simulate mouse movement
        # action = ActionChains(driver)
        # action.move_to_element(label_element).perform()
        # time.sleep(random.uniform(0.5, 1.5))  # Random delay to mimic human interaction

        # Locate the corresponding application field
        field_container = label_element.find_element(By.XPATH, "../div[@class='application-field']")

        # Handle different input types
        if isinstance(dummy_value, str):  # Text or file input
            input_field = field_container.find_element(By.XPATH, ".//input")
            input_type = input_field.get_attribute("type")
            if input_type == "file":  # File upload
                input_field.send_keys(dummy_value)
            else:  # Text, email, etc.
                input_field.send_keys(dummy_value)
        elif isinstance(dummy_value, list):  # Checkboxes
            checkboxes = field_container.find_elements(By.XPATH, ".//input[@type='checkbox']")
            for checkbox in checkboxes:
                if checkbox.get_attribute("value") in dummy_value:
                    checkbox.click()
        elif dummy_value in ["Yes", "No"]:  # Radio buttons
            radio_buttons = field_container.find_elements(By.XPATH, ".//input[@type='radio']")
            for radio in radio_buttons:
                if radio.get_attribute("value") == dummy_value:
                    radio.click()
        else:
            print(f"Skipping field '{field_label}' with no valid dummy value.")
        
        print(f"Processed field: {field_label}")
        time.sleep(random.uniform(1, 3))  # Random delay between processing fields
    except Exception as e:
        print(f"Error processing field '{field_label}': {e}")

# Optional: Add a short wait to observe the action before closing
time.sleep(5)

# Quit the browser
driver.quit()
