#### this got the main fields more correctly

sample_fields = {
    'Resume/CV ✱': 'Resume_AGupta_2024.pdf',
    "Full name✱": "Arjun Gupta",
    "Email✱": "arjungup740@gmail.com",
    "Phone ✱": "704-307-7983",
    # # "Current location ✱": "New York, NY",
    "LinkedIn URL": "https://www.linkedin.com/in/arjun-s-gupta-193a178a/",
    "GitHub URL": "https://github.com/arjungup740",
    "Portfolio URL": "https://quantitativecuriosity.substack.com/s/projects",
    "Do you live in the NYC Area?✱": "Yes",  # Radio button
    "If not, are you willing to relocate?✱": "Yes",  # Radio button
    # # "What are your pronouns?": "He/Him",
    'Do you now or will you in the future require sponsorship for employment authorization to work in the US? (If so, Please let us know more information if you can.)✱': "No",
    # # "What is your desired compensation for this role?": "$100,000",
}

user_info = """
located in New York, NY
"""

questions_and_types_dict = {key:remaining_fields_dict[key].get_input_types() for key in remaining_fields_dict.keys()}

messages = [
				{"role": "system", "content": """You are a personal assistant helping to fill a web form job application. Given the dictionary of fields and the corresponding html, generate a json object of answers that a program can use to fill in the fields"""},
				{"role": "system", "content": f"Here is an example of the dictionary you should produce: {sample_fields}"},
                {"role": "system", "content": f"Do not answer any demographic questions -- don't even include them in the json"},
                {"role": "system", "content": f"some info parsed from the user's resume: {user_info}"},
                {"role": "user", "content": f"Here is the dictionary of fields and their input types: {questions_and_types_dict}"}
			]
	
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    response_format={"type": "json_object"}
)

print(completion.choices[0].message.content)

fields = json.loads(completion.choices[0].message.content)

print(fields)

##### imitate human mouse movement
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




#### this got the main fields more correctly


htmldict_of_questions = {}
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

for application_label, application_field_html in dict_of_questions.items():
    application_field = application_field_html
    soup = BeautifulSoup(question_html, 'html.parser')
    application_label = soup.find('div', class_='application-label')
    if application_label.text.strip() in fields.keys():
        application_field = soup.find('div', class_='application-field')
        input_elements = application_field.find_elements(By.XPATH, ".//input")


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

# O

fields = {
    "resume": "Resume_AGupta_2024.pdf",  # /Users/arjungupta/Documents/projects/job_applier/ # Update with your file path
    "name": "John Doe",
    "email": "johndoe@example.com",
    "phone": "123-456-7890",
    "location": "New York, NY",
    "company": "Current Company"
}

# Interact with Resume field (file upload)
resume_field = driver.find_elements(By.CLASS_NAME, "application-field")

for element in resume_field:
    # Example: Get the text of each element
    print(element.text)

if resume_field:
    resume_field[0].find_element(By.TAG_NAME, "input").send_keys(fields["resume"])
else:
    print("Could not find resume field")

# Interact with Full Name field
name_field = driver.find_element(By.XPATH, "//input[@name='name']")
name_field.click()
name_field.send_keys(fields["name"])

# Interact with Email field
email_field = driver.find_element(By.XPATH, "//input[@name='email']")
email_field.click()
email_field.send_keys(fields["email"])

# Interact with Phone field
phone_field = driver.find_element(By.XPATH, "//input[@name='phone']")
phone_field.click()
phone_field.send_keys(fields["phone"])

# Interact with Current Location field
location_field = driver.find_element(By.XPATH, "//input[@id='location-input']")
location_field.click()
location_field.send_keys(fields["location"])
location_field.send_keys(Keys.ENTER)

# Interact with Current Company field
company_field = driver.find_element(By.XPATH, "//input[@name='company']")
company_field.click()
company_field.send_keys(fields["company"])

# Optional: Add a delay to visually inspect the filled form
import time
time.sleep(5)

# Close the browser
# driver.quit()

 # if application_label:
    #     application_label = application_label.get_text(strip=True)
    #     application_field = soup.find('div', class_='application-field')
        
        if application_field:
            # Check if this is a radio button field
            radio_inputs = application_field.find_all('input', type='radio')
            text_input = application_field.find('input', type='text')

            if radio_inputs:
                # Handle radio button options
                options = [
                    {
                        "value": input_tag.get("value"),
                        "label": span_tag.get_text(strip=True),
                    }
                    for input_tag, span_tag in zip(
                        radio_inputs,
                        application_field.find_all('span', class_='application-answer-alternative')
                    )
                ]
                field_type = "radio"
            elif text_input:
                # Handle text input fields
                options = {
                    "type": "text",
                    "name": text_input.get("name"),
                    "required": text_input.get("required") is not None,
                    "data-qa": text_input.get("data-qa")
                }
                field_type = "text"

            # Create the result dictionary for this question
            result = {
                "label": application_label,
                "type": field_type,
                "field": options
            }

            # Print the result for this question
            print(result)
label_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='application-label' and contains(text(), 'Full name')]")))

# Find the corresponding input field by navigating to the sibling 'application-field'
input_field = label_element.find_element(By.XPATH, "../div[@class='application-field']/input")

# Send keys to the input field
input_field.send_keys("John Doe")