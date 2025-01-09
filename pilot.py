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
    # "Current company": "Example Company",
    # "LinkedIn URL": "https://linkedin.com/in/example",
    # "Twitter URL": "https://twitter.com/example",
    # "GitHub URL": "https://github.com/example",
    # "Portfolio URL": "https://example.com",
    "Other website": "https://example-other.com",
    "Do you live in the NYC Area?✱": "Yes",  # Radio button
    # "If not, are you willing to relocate?✱": "No",  # Radio button
    # "What are your pronouns?": "He/Him",
    # "What is your desired compensation for this role?": "$100,000",
}

# Loop through fields and interact with them
for field_label, dummy_value in fields.items():
    print(f'current field_label: {field_label}')
    try:
        try: # see if better way to do this
            # logic for simple structure
            label_element = wait.until(EC.presence_of_element_located((
                By.XPATH, f"//div[contains(@class, 'application-label') and contains(text(), '{field_label.split('✱')[0].strip()}')]"
            )))
        except:
            # next try looking for nested div.text structure
            label_element = wait.until(EC.presence_of_element_located((
                By.XPATH, f"//div[contains(@class, 'application-label')]//div[@class='text'][contains(text(), '{field_label.split('✱')[0].strip()}')]/.."
            )))
        
        if label_element:
            print('got here')
        # Rest of the code inside try block should be at this indentation level
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", label_element)
        field_container = label_element.find_element(By.XPATH, "../div[@class='application-field']")
        input_elements = field_container.find_elements(By.XPATH, ".//input")
        print(f'len(input_elements): {len(input_elements)}')
        for input_element in input_elements:
            input_type = input_element.get_attribute("type")
            print(input_type)
            if input_type == "radio":
                print('got here 1')
                if dummy_value in ["Yes", "No"] and input_element.get_attribute("value") == dummy_value:
                    print('got here 2')
                    input_element.click()
            elif input_type == "checkbox":
                if isinstance(dummy_value, list) and input_element.get_attribute("value") in dummy_value:
                    input_element.click()
            elif input_type == "file":
                input_element.send_keys(dummy_value)
            elif input_type in ["text", "email", "tel", "url"]:
                if isinstance(dummy_value, str):
                    input_element.send_keys(dummy_value)
            else:
                print(f"Unhandled input type '{input_type}' for field '{field_label}'")
        
        print(f"Processed field: {field_label}")
        time.sleep(random.uniform(1, 2))  # Random delay between processing fields
    except Exception as e:
        print(f"Error processing field '{field_label}': {e}")

# Optional: Add a short wait to observe the action before closing
time.sleep(5)

# Quit the browser
# driver.quit()

############## the lab
field_label
label_element = wait.until(EC.presence_of_element_located((
    By.XPATH, f"//div[contains(@class, 'application-label')]//div[@class='text'][contains(text(), '{field_label.split('✱')[0].strip()}')]/.."
)))
label_element.get_attribute('outerHTML')

<div class="application-label full-width multiple-choice"><div class="text">Do you live in the NYC Area?<span class="required">✱</span></div></div>

dict_of_questions.keys()
dict_of_questions[field_label]