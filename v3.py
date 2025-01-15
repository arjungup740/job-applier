from selenium import webdriver
import undetected_chromedriver as uc
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import random
import os
import json
# from dotenv import load_dotenv
# load_dotenv()
from openai import OpenAI
from openai.types.beta.threads.message_create_params import (
    Attachment,
    AttachmentToolFileSearch,
)
import re



# Initialize WebDriver with enhanced anti-detection options
def initialize_driver():
    options = uc.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')
    options.add_argument("--disable-gpu")

    # Set a realistic user agent
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    # Add additional arguments to make automation less detectable
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")

    # If you still want the browser to stay open after the script finishes, 
    # you can add this instead:
    options.headless = False

    # Add CDP commands to modify navigator.webdriver flag
    driver = uc.Chrome(options=options)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'})
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })

    # Add stealth settings
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    
    return driver

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


def get_application_questions(driver):

    # Wait for the page to load
    wait = WebDriverWait(driver, 10)

    # Wait for the form to be present in the DOM
    application_form = wait.until(EC.presence_of_element_located((By.ID, "application-form")))

    # Extract all application questions
    application_questions = application_form.find_elements(By.CSS_SELECTOR, "[class*='application-question']")

    web_elem_dict_of_questions = {}
    for question in application_questions:
        question_html = question.get_attribute('outerHTML')
        soup = BeautifulSoup(question_html, 'html.parser')
        application_label = soup.find('div', class_=lambda x: x and 'application-label' in x)
        if application_label:
            web_elem_dict_of_questions[application_label.text.strip()] = FormField(question)

    return web_elem_dict_of_questions

def upload_resume(driver, web_elem_dict_of_questions):
    for key, field_data in web_elem_dict_of_questions.items():
        if 'resume' in key.lower():
            print('resume found, checking input type and beginning upload')
            input_elements = field_data.get_input_elements()
            field_container = field_data.get_field_container()
            if len(input_elements) == 1 and field_data.get_input_types()[0] == 'file':
                file_path = os.path.abspath('Resume_AGupta_2024.pdf')
                input_elements[0].send_keys(file_path)
                print('resume uploaded, waiting for success button')
                max_wait = 15
                print(f"waiting for resume to upload, max time is {max_wait} seconds")
                time.sleep(max_wait)
                # Wait for "Success!" text in the resume-upload-label
                # WebDriverWait(driver, max_wait).until(
                #     lambda x: x.find_element(By.CSS_SELECTOR, '.resume-upload-label').text.strip() == "Success!"
                # )
                # success_element = driver.find_element(By.CSS_SELECTOR, '.resume-upload-label')
                # print(f"Actual text: '{success_element.text}'")
        else:
            print('resume input element not found')

def create_and_run_assistant(filename, prompt):
    client = OpenAI(api_key=os.environ.get("MY_OPENAI_KEY"))

    pdf_assistant = client.beta.assistants.create(
        model="gpt-4o",
        description="An assistant to use info from a resume to fill in the fields of a job application.",
        tools=[{"type": "file_search"}],
        name="PDF assistant",
    )

    # Create thread
    thread = client.beta.threads.create()

    file = client.files.create(file=open(filename, "rb"), purpose="assistants")

    # Create assistant
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        attachments=[
            Attachment(
                file_id=file.id, tools=[AttachmentToolFileSearch(type="file_search")]
            )
        ],
        content=prompt,
    )

    # Run thread
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, assistant_id=pdf_assistant.id, timeout=1000
    )

    if run.status != "completed":
        raise Exception("Run failed:", run.status)
    
    return thread, run

def extract_json(text):
    """
    Extracts the JSON object from a text containing commentary and JSON content.

    Parameters:
        text (str): The input text containing commentary and a JSON object.

    Returns:
        dict: The extracted JSON object as a Python dictionary.
    """
    # Use regex to match a JSON-like structure
    json_match = re.search(r"\{.*?\}", text, re.DOTALL)
    
    if json_match:
        json_string = json_match.group()
        try:
            # Parse the JSON string into a dictionary
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            return None
    else:
        print("No JSON object found in the text.")
        return None


def get_thread_messages(client, thread):

    messages_cursor = client.beta.threads.messages.list(thread_id=thread.id)
    messages = [message for message in messages_cursor]
    res_txt = messages[0].content[0].text.value

    if res_txt:
       parsed_json = extract_json(res_txt)
    else:
        print("No JSON object found in the text.")
        parsed_json = None

    return messages, parsed_json

def get_completion_and_fields(client, messages):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        response_format={"type": "json_object"}
    )
    final_fields = None
    if completion.choices[0].message.content:
        final_fields = json.loads(completion.choices[0].message.content)
    else:
        print("No JSON object found in the text.")

    return completion, final_fields

def fill_remaining_fields(remaining_fields_dict, final_fields, driver):
    for field_label, field_data in remaining_fields_dict.items():
        if field_label in final_fields:  # fields is your dictionary of dummy data
            try:
                dummy_value = final_fields[field_label]
                input_elements = field_data.get_input_elements()
                field_container = field_data.get_field_container()
                if field_data.is_filled():
                    print(f"Skipping {field_label} because it is already filled")
                    continue
                # Scroll the field container into view
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", field_container)
                
                for input_elem in input_elements:
                    # Add human-like mouse movement
                    # human_like_mouse_move(driver, input_elem)
                    
                    input_type = input_elem.get_attribute('type')
                    
                    if input_type == "radio":
                        if dummy_value in ["Yes", "No"] and input_elem.get_attribute("value") == dummy_value:
                            input_elem.click()
                    elif input_type == "file":
                        # Convert relative path to absolute path if needed
                        file_path = os.path.abspath(dummy_value)
                        input_elem.send_keys(file_path)
                        if field_label == 'Resume/CV ✱':
                            max_wait = 15
                            print(f"waiting for resume to upload, max time is {max_wait} seconds")
                            # Wait for "Success!" text in the resume-upload-label
                            WebDriverWait(driver, max_wait).until(
                                lambda x: x.find_element(By.CSS_SELECTOR, '.resume-upload-label').text.strip() == "Success!"
                            )
                            success_element = driver.find_element(By.CSS_SELECTOR, '.resume-upload-label')
                            print(f"Actual text: '{success_element.text}'")
                    elif input_type in ["text", "email", "tel", "url"]:
                        if isinstance(dummy_value, str):
                            # Type like a human with random delays
                            for char in dummy_value:
                                input_elem.send_keys(char)
                                time.sleep(random.uniform(0.05, 0.1))
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
                    
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                print(f"Error processing field '{field_label}': {e}")

input("Press Enter to close the browser...")
# driver.quit()

########################### runner

#### create driver, nav to page
driver = initialize_driver()
driver.get('https://jobs.lever.co/spotify/df8c49b0-4509-453a-8919-9314b61bede2/apply')
#### get questions
web_elem_dict_of_questions = get_application_questions(driver)
#### upload resume
upload_resume(driver, web_elem_dict_of_questions)
######## fill in remaining fields resume didn't cover with AI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
remaining_fields_dict = {key:field_data for key,field_data in web_elem_dict_of_questions.items() if not field_data.is_filled()}
questions_and_types_dict = {key:remaining_fields_dict[key].get_input_types() for key in remaining_fields_dict.keys()}

filename = "Resume_AGupta_2024.pdf"

sample_fields = {
    'Resume/CV ✱': 'Resume_AGupta_2024.pdf',
    "Full name✱": "Arjun Gupta",
    "Email✱": "arjungup740@gmail.com",
    "Phone ✱": "704-307-7983",
    "Current location ✱": "New York, NY",
    "LinkedIn URL": "https://www.linkedin.com/in/arjun-s-gupta-193a178a/",
    "GitHub URL": "https://github.com/arjungup740",
    "Portfolio URL": "https://quantitativecuriosity.substack.com/s/projects",
    "Do you live in the NYC Area?✱": "Yes", 
    "If not, are you willing to relocate?✱": "Yes",  
    'Do you now or will you in the future require sponsorship for employment authorization to work in the US? (If so, Please let us know more information if you can.)✱': "No",
}


prompt = f"""You are a personal assistant helping to fill a web form job application. Given the dictionary of fields and the corresponding html, use the information in the resume to generate a json object of answers that a program can use to fill in the fields
                Here is an example of the dictionary you should produce: {sample_fields}.
                Do not answer any demographic questions -- don't even include them in the json
                Here is the dictionary of fields and their input types: {questions_and_types_dict}. Only produce json for the fields that are in this dictionary, though you may use the example dictionary to help you with information if needed -- it has real data
                """

thread, run = create_and_run_assistant(filename, prompt)

messages, parsed_json = get_thread_messages(client, thread)

##### have a second AI check the json produced

user_info = """
Arjun Gupta is located in New York, NY. He does not require sponsorship for employment authorization to work in the US. His portfolio is https://quantitativecuriosity.substack.com/s/projects
"""

messages = [
				{"role": "system", "content": """You are a detail-oriented assistant reviewing the answers to a web form job application that was generated by another AI. Given the generated responses and the dictionary of fields to fill, compare the two and see if the generated answer missed anything and fill it in"""},
                {"role": "system", "content": f"IGNORE ANY DEMOGRAPHIC QUESTIONS (race, ethnicity, gender, veteran status, pronouns etc.) -- don't even include them in the json"},
                {"role": "system", "content": f"Here is some additional information about the user: {sample_fields}"},
                {"role": "user", "content": f"Here is the generated json of answers: {final_fields} and the dictionary of fields and their input types that needs to be filled: {questions_and_types_dict}"}
			]

completion, final_fields = get_completion_and_fields(client, messages)

fill_remaining_fields(remaining_fields_dict, final_fields, driver)

input("Press Enter to close the browser...")
driver.quit()
