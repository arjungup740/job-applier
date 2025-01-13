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
from openai import OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Initialize WebDriver with enhanced anti-detection options
options = uc.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920,1080')
options.add_argument("--disable-gpu")

# Set a realistic user agent
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")


# Add additional arguments to make automation less detectable
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-dev-shm-usage")

# Add experimental options
# options.add_experimental_option("detach", True)
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)

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

# Add this function for human-like mouse movements
def human_like_mouse_move(driver, element):
    action = ActionChains(driver)
    
    # Get element location and viewport size
    viewport_width = driver.execute_script("return window.innerWidth;")
    viewport_height = driver.execute_script("return window.innerHeight;")
    
    # Get element location after scrolling it into view
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(0.5)  # Give time for scrolling to complete
    
    location = element.location
    size = element.size
    
    # Calculate a random point within the element
    target_x = location['x'] + size['width'] // 2
    target_y = location['y'] + size['height'] // 2
    
    # Create multiple points for natural curve movement
    # But ensure they stay within viewport bounds
    points = []
    for _ in range(random.randint(2, 4)):
        # Limit the random offsets to stay within viewport
        x_offset = random.randint(-50, 50)
        y_offset = random.randint(-50, 50)
        
        new_x = min(max(target_x + x_offset, 0), viewport_width)
        new_y = min(max(target_y + y_offset, 0), viewport_height)
        
        points.append((new_x, new_y))
    
    # Move through points with random delays
    for point in points:
        action.move_by_offset(point[0], point[1])
        action.pause(random.uniform(0.1, 0.2))
    
    # Finally move to the element
    action.move_to_element(element)
    action.pause(random.uniform(0.1, 0.2))
    
    try:
        action.perform()
    except Exception as e:
        print(f"Couldn't perform mouse movement, falling back to direct interaction")

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

web_elem_dict_of_questions = {}
for question in application_questions:
    question_html = question.get_attribute('outerHTML')
    soup = BeautifulSoup(question_html, 'html.parser')
    application_label = soup.find('div', class_=lambda x: x and 'application-label' in x)
    if application_label:
        web_elem_dict_of_questions[application_label.text.strip()] = FormField(question)


for key in web_elem_dict_of_questions.keys():
    if not web_elem_dict_of_questions[key].is_filled():
        print(f'-- question: {key}, type: {web_elem_dict_of_questions[key].get_input_types()}')
        # print(web_elem_dict_of_questions[key].get_input_types())
        # print(web_elem_dict_of_questions[key].get_field_container().get_attribute('outerHTML'))
        # print('---' + '\n\n')



############################## Feed web elem dict of questions to gpt and ask it to generate an answer dict

sample_dict = fields = {
    'Resume/CV ✱': 'Resume.pdf',
    "Full name✱": "Jimmy Holland",
    "Email✱": "some_email@gmail.com",
    "Phone ✱": "888-888-8888",
    "LinkedIn URL": "https://www.linkedin.com/in/some-identifier/",
    "GitHub URL": "https://github.com/some_username",
    "Portfolio URL": "some link",
}

user_info = """
ARJUN GUPTA
704-307-7983 | arjungup740@gmail.com| https://github.com/arjungup740 | https://www.linkedin.com/in/arjun-s-gupta-193a178a/ | https://quantitativecuriosity.substack.com/s/projects
"""

questions_and_types_dict = {key: web_elem_dict_of_questions[key].get_input_types() for key in web_elem_dict_of_questions.keys()}

messages = [
				{"role": "system", "content": """You are a personal assistant helping to fill a web form job application. Given the dictionary of fields and the corresponding html, generate a dictionary of answers that a program can use to fill in the fields"""},
				{"role": "system", "content": f"Here is an example of the dictionary you should produce: {sample_dict}"},
                {"role": "system", "content": f"Do not answer any demographic questions"},
                {"role": "system", "content": f"some info parsed from the user's resume: {user_info}"},
                {"role": "user", "content": f"Here is the dictionary of fields and their input types: {questions_and_types_dict}"}
			]
	
answer = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    response_format='json_object'
)

print(completion.choices[0].message)
############################# sub-optim -- uploade resume for autofill first, check what's not filled in and fill in the rest
resume_field_exists = False
for key in web_elem_dict_of_questions.keys():
    if 'resume' in key.lower():
        print('resume found')
        resume_field_exists = True
        break

if resume_field_exists:
    ## uploade resume for autofill


input("Press Enter to close the browser...")
driver.quit()