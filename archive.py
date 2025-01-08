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