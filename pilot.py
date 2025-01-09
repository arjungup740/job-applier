from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import random
import os

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
# Modified dictionary creation
web_elem_dict_of_questions = {}
for question in application_questions:
    question_html = question.get_attribute('outerHTML')
    soup = BeautifulSoup(question_html, 'html.parser')
    application_label = soup.find('div', class_=lambda x: x and 'application-label' in x)
    if application_label:
        # Get the actual WebElement for the field instead of BeautifulSoup object
        field_container = question.find_element(By.CSS_SELECTOR, "[class*='application-field']")
        input_elements = field_container.find_elements(By.TAG_NAME, 'input')
        
        web_elem_dict_of_questions[application_label.text.strip()] = {
            "field_container": field_container,
            "input_elements": input_elements,
            "input_types": [elem.get_attribute('type') for elem in input_elements]
        }

# web_elem_dict_of_questions['Full name✱']['input_elements']#[0].get_attribute('outerHTML') # sample

for field_label, field_data in web_elem_dict_of_questions.items():
    print(field_label, field_data['input_types'])

fields = {
    'Resume/CV ✱': 'Resume_AGupta_2024.pdf',
    "Full name✱": "John Doe",
    "Email✱": "johndoe@example.com",
    "Phone ✱": "123-456-7890",
    # "Current location ✱": "New York, NY",
    # "Current company": "Example Company",
    # "LinkedIn URL": "https://linkedin.com/in/example",
    # "Twitter URL": "https://twitter.com/example",
    # "GitHub URL": "https://github.com/example",
    # "Portfolio URL": "https://example.com",
    # "Other website": "https://example-other.com",
    # "Do you live in the NYC Area?✱": "Yes",  # Radio button
    # "If not, are you willing to relocate?✱": "Yes",  # Radio button
    # "What are your pronouns?": "He/Him",
    # "What is your desired compensation for this role?": "$100,000",
}

for field_label, field_data in web_elem_dict_of_questions.items():
    if field_label in fields:  # fields is your dictionary of dummy data
        try:
            dummy_value = fields[field_label]
            input_elements = field_data['input_elements']
            field_container = field_data['field_container']
            
            # Scroll the field container into view
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", field_container)
            
            for input_elem in input_elements:
                input_type = input_elem.get_attribute('type')
                
                if input_type == "radio":
                    if dummy_value in ["Yes", "No"] and input_elem.get_attribute("value") == dummy_value:
                        input_elem.click()
                elif input_type == "file":
                    # Convert relative path to absolute path if needed
                    file_path = os.path.abspath(dummy_value)
                    input_elem.send_keys(file_path)
                elif input_type in ["text", "email", "tel", "url"]:
                    if isinstance(dummy_value, str):
                        input_elem.send_keys(dummy_value)
                        
            # Add a small delay after scrolling and interacting
            time.sleep(random.uniform(0.5, 1))
            
        except Exception as e:
            print(f"Error processing field '{field_label}': {e}")


# Define fields and dummy data

time.sleep(5)

# Quit the browser
# driver.quit()

############## the lab
