from openai import OpenAI
from openai.types.beta.threads.message_create_params import (
    Attachment,
    AttachmentToolFileSearch,
)
import os

filename = "Resume_AGupta_2024.pdf"
prompt = "Extract the content from the file provided without altering it. Just output its exact content and nothing else."

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

prompt = f"""You are a personal assistant helping to fill a web form job application. Given the dictionary of fields and the corresponding html, use the information in the resume to generate a json object of answers that a program can use to fill in the fields
                Here is an example of the dictionary you should produce: {sample_fields}
                Do not answer any demographic questions -- don't even include them in the json
                Here is the dictionary of fields and their input types: {questions_and_types_dict}. Only produce json for the fields that are in this dictionary, though you may use the example dictionary to help you with information if needed.
                """


client = OpenAI(api_key=os.environ.get("MY_OPENAI_KEY"))

pdf_assistant = client.beta.assistants.create(
    model="gpt-4o",
    description="An assistant to extract the contents of PDF files.",
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

messages_cursor = client.beta.threads.messages.list(thread_id=thread.id)
messages = [message for message in messages_cursor]

# Output text
res_txt = messages[1].content[0].text.value
print(res_txt)