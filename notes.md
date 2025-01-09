

## the lab


## to do now

add a pause for the resume to upload, maybe 15 seconds
add logic that checks if field is already filled in, if so skip
checkboxes
the application-question custom questions didn't work
perhaps have logic that doesn't fill in non-required questions
let resume autofill work and have program check if field is already filled in
fill in fields of hinge app, then see how it does on another one

## couple of avenues:

pull all questions, have an llm interpret them and generate the answer json, then have the program go back and fill stuff in
have an llm take the questions, generate the answers in json, then have a second llm take the json and the html and generate the code to fill in the fields

collect the full html blob from the application form page, tell it to extract the fields that we need to send input to

grab the application form, use the selenium thing to get all the possible elements, then have a second set of logic that goes through and thinks which elements are relevant, then of those grab the correct fields and their values to send things to

could generate all the html for each question, pass that to gpt, have it generate the code to fill in fields, then run that code


## reference

By.XPATH, f"//div[contains(@class, 'application-label') and contains(text(), '{field_label.split('✱')[0].strip()}')]"

types:

- text
- radio
- upload something -- linkedin button, resume


https://jobs.lever.co/matchgroup/354cd021-8ea8-45e9-9dea-d1f6a5a0728f/apply # lever
https://jobs.ashbyhq.com/evenup/bbc7d342-1a7f-4940-bd66-ae5c710e65ae/application # ashby job

#### Done
What do you want to do? simply take the application label, pull corresponding answer from our dict, then fill in field
if we're parsing the soup we're just looking at the text of the html, if we want to interact with the page we need the wait construct presumably
we're actually already interacting with the question objects, we just need to send the right types of inputs 

could ask to find a way that given an application-question with a corresponding field, just click into that field without needing to specify the data-qa element
can fill in text fields, after specifying the fiels very specifically to fill in
Just get a dict that has application label, application field, field type. That's it
go through and grab all the application question classes

#### Return

hitting captchas -- on choosing the location with the location being a dropdown -- return to