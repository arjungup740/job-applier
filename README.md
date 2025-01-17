Easily apply given a list of urls from jobs.leverl.co. As of this writing v4_multiple_jobs.py is the latest version.

Currently, the bot fills out each application and leaves the browser open for the user to review everything before manually submitting (occasionally the LLM still misses things ). As I build the system out more and gain more confidence with it, eventually you could imagine it submitting the applications automatically.

There's a couple more avenues we could explore:

* a bot to find urls to feed into the system
* Fully automating the process and having it submit
* expanding to be able to handle ashby, greenhouse, etc.
* a more general purpose bot that can use gpt to intuit the structure and fill out any form
* parallelize

The basic structure is as follows:

* Initialize WebDriver with enhanced anti-detection options
* get the application questions from the page (parsing the html structure and searching for the previously determined relevant fields)
* if there is a button to upload a resume (there usually is) upload the resume. This will typically trigger some sort of auto-fill of some fields on the site's part.
* Collect the remaining fields that are empty
* pass them, plus my resume, plus some additional information about me, to gpt to fill in the rest
* Have a second AI pass to check the generated answers and see if any fields are missing or can be further filled in (empirically this was better than just one step)
* Leave the browser open so the user can review everything quickly before submitting!

Cuing up 5 jobs and then quickly skimming them over before submitting, I was able to submit them much faster than sequentially filling out every single one.