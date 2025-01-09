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