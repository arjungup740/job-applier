

## the lab


## to do now


see if can handle location dropdowns
the citizenship textarea field
checkboxes
logic that doesn't fill in non-required questions -- certainly not demographic ones
make it so that it doesn't kill the window after it finishes filling in




## couple of avenues:

ultimately could grab the question elements and html, pass to llm to parse the questions and generate an answer dict, then pass that answer dict to the program that goes and fills in the fields

## reference


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

there's conceptual and there's mechanics

#### Return

hitting captchas -- on choosing the location with the location being a dropdown -- return to