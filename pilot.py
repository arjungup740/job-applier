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
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)


# Open the URL
driver.get('https://jobs.lever.co/matchgroup/354cd021-8ea8-45e9-9dea-d1f6a5a0728f/apply')

# Wait for the page to load
wait = WebDriverWait(driver, 10)

# Wait for the form to be present in the DOM
application_form = wait.until(EC.presence_of_element_located((By.ID, "application-form")))

# Extract all application questions
application_questions = application_form.find_elements(By.CSS_SELECTOR, "[class*='application-question']")

class FormField:
    def __init__(self, question_element):
        self.question_element = question_element
        
    def get_field_container(self):
        return self.question_element.find_element(By.CSS_SELECTOR, "[class*='application-field']")
        
    def get_input_elements(self):
        # First try to find regular input elements
        inputs = self.get_field_container().find_elements(By.TAG_NAME, 'input')
        # If no inputs found, look for textarea
        if not inputs:
            textareas = self.get_field_container().find_elements(By.TAG_NAME, 'textarea')
            return textareas
        return inputs
        
    def get_input_types(self):
        elements = self.get_input_elements()
        return ['textarea' if elem.tag_name == 'textarea' else elem.get_attribute('type') for elem in elements]
        
    def is_filled(self):
        input_elements = self.get_input_elements()
        for input_elem in input_elements:
            if input_elem.tag_name == 'textarea':
                if input_elem.get_attribute('value').strip():
                    return True
            else:  # handle regular inputs as before
                input_type = input_elem.get_attribute('type')
                if input_type == 'radio':
                    if input_elem.is_selected():
                        return True
                elif input_type == 'file':
                    if input_elem.get_attribute('value'):
                        return True
                else:  # text, email, tel, url
                    if input_elem.get_attribute('value').strip():
                        return True
        return False

# Modified dictionary creation
web_elem_dict_of_questions = {}
for question in application_questions:
    question_html = question.get_attribute('outerHTML')
    soup = BeautifulSoup(question_html, 'html.parser')
    application_label = soup.find('div', class_=lambda x: x and 'application-label' in x)
    if application_label:
        web_elem_dict_of_questions[application_label.text.strip()] = FormField(question)

web_elem_dict_of_questions['Do you now or will you in the future require sponsorship for employment authorization to work in the US? (If so, Please let us know more information if you can.)✱'].get_input_types()#['input_elements']#[0].get_attribute('outerHTML') # sample

# for field_label, field_data in web_elem_dict_of_questions.items():
#     print(field_label, field_data.get_input_types())

required_fields = []
for field_label, field_data in web_elem_dict_of_questions.items():
    if '✱' in field_label:
        required_fields.append(field_label)


fields = {
    # 'Resume/CV ✱': 'Resume_AGupta_2024.pdf',
    # "Full name✱": "Arjun Gupta",
    # "Email✱": "arjungup740@gmail.com",
    # "Phone ✱": "704-307-7983",
    # # "Current location ✱": "New York, NY",
    # "LinkedIn URL": "https://www.linkedin.com/in/arjun-s-gupta-193a178a/",
    # "GitHub URL": "https://github.com/arjungup740",
    # "Portfolio URL": "https://quantitativecuriosity.substack.com/s/projects",
    # "Do you live in the NYC Area?✱": "Yes",  # Radio button
    # "If not, are you willing to relocate?✱": "Yes",  # Radio button
    # # "What are your pronouns?": "He/Him",
    # 'Do you now or will you in the future require sponsorship for employment authorization to work in the US? (If so, Please let us know more information if you can.)✱': "No",
    # # "What is your desired compensation for this role?": "$100,000",
}


for field_label, field_data in web_elem_dict_of_questions.items():
    if field_label in fields:  # fields is your dictionary of dummy data
        try:
            dummy_value = fields[field_label]
            input_elements = field_data.get_input_elements()
            field_container = field_data.get_field_container()
            if field_data.is_filled():
                print(f"Skipping {field_label} because it is already filled")
                continue
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
                    if field_label == 'Resume/CV ✱':
                        max_wait = 30
                        print(f"waiting for resume to upload, max time is {max_wait} seconds")
                        # Wait for "Success!" text in the resume-upload-label
                        WebDriverWait(driver, max_wait).until(
                            lambda x: x.find_element(By.CSS_SELECTOR, '.resume-upload-label').text.strip() == "Success!"
                        )
                        success_element = driver.find_element(By.CSS_SELECTOR, '.resume-upload-label')
                        print(f"Actual text: '{success_element.text}'")
                elif input_type in ["text", "email", "tel", "url"]:
                    if isinstance(dummy_value, str):
                        input_elem.send_keys(dummy_value)
                elif input_elem.tag_name == 'textarea':
                    input_elem.send_keys(dummy_value)
                elif input_type == "text" and "location-input" in input_elem.get_attribute("class"):
                    # Enter the location text
                    input_elem.send_keys(dummy_value)
                    time.sleep(1)  # Wait for dropdown to appear
                    
                    # Wait for and click the first dropdown result
                    try:
                        dropdown_results = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, ".dropdown-results div"))
                        )
                        dropdown_results.click()
                    except Exception as e:
                        print(f"Could not select location from dropdown: {e}")
                        # Clear and try again with just text if dropdown fails
                        input_elem.clear()
                        input_elem.send_keys(dummy_value)
                        
            # Add a small delay after scrolling and interacting
            time.sleep(random.uniform(0.5, 1))
            
            # Check if field was successfully filled
            if field_data.is_filled():
                print(f"Successfully filled {field_label}")
            else:
                print(f"Failed to fill {field_label}")
                
            time.sleep(random.uniform(0.5, 1))
            
        except Exception as e:
            print(f"Error processing field '{field_label}': {e}")


# Define fields and dummy data

# time.sleep(5)

# Quit the browser
# driver.quit()

############## the lab
