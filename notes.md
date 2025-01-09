* * * 

## the lab

Do we need the label element? Or just the field to fill it out? we don't need to find the label element to fill it out necessarily.. just the field element

## to do now

can't handle radio buttons or checkboxes
the application-question custom questions didn't work

## couple of avenues:

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

could ask to find a way that given an application-question with a corresponding field, just click into that field without needing to specify the data-qa element
can fill in text fields, after specifying the fiels very specifically to fill in
Just get a dict that has application label, application field, field type. That's it
go through and grab all the application question classes

#### Return

hitting captchas -- on choosing the location with the location being a dropdown -- return to