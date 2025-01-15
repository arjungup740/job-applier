

## the lab -- see if can get the whole thing working off of GPT

* feed it a list of jobs
* have it create multiple windows/fill multiple applications at once
* have some general clean ups for usability
* have another llm call go through and check the answers fill in -- for example, occasionally misses locations as well as portfolio site
* try to get something that can do ashby, greenhouse jobs


## to do now 

* come up with some next avenues


## couple of avenues:


## reference


https://jobs.lever.co/matchgroup/354cd021-8ea8-45e9-9dea-d1f6a5a0728f/apply # lever
https://jobs.ashbyhq.com/evenup/bbc7d342-1a7f-4940-bd66-ae5c710e65ae/application # ashby job

#### Done
give gpt access to the resume programmatically -- figure out this assistant thing
Try another application 
upload resume first and see what's left to fill in to reduce token counts and increase accuracy
See about getting an actual submit to work -- slow and heavy, but it does work
    employ anti-bot protections -- it detects the issue on start up
make it so that it doesn't kill the window after it finishes filling in
What do you want to do? simply take the application label, pull corresponding answer from our dict, then fill in field
if we're parsing the soup we're just looking at the text of the html, if we want to interact with the page we need the wait construct presumably
we're actually already interacting with the question objects, we just need to send the right types of inputs 

could ask to find a way that given an application-question with a corresponding field, just click into that field without needing to specify the data-qa element
can fill in text fields, after specifying the fiels very specifically to fill in
Just get a dict that has application label, application field, field type. That's it
go through and grab all the application question classes

there's conceptual and there's mechanics

#### Return

see if can handle location dropdowns -- triggers the catpcha, try again later
checkboxes - in general this might be useful, but punt for now
