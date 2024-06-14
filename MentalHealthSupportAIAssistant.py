from openai import OpenAI
from playsound import playsound
import warnings
import os
warnings.filterwarnings("ignore", category = DeprecationWarning)

def text2speech(prompt):
    if not os.path.exists(str(os.getcwd())+"\\AudioFiles"):
        # Create the directory
        os.makedirs(str(os.getcwd())+"\\AudioFiles")
        
    os.chdir(str(os.getcwd())+"\\AudioFiles")
    fileList = os.listdir()
    numFiles = len(fileList)
    newFileName = "audio"+str(numFiles)+".mp3"
    
    response = client.audio.speech.create(
        model="tts-1-hd",
        voice="nova",
        input=prompt
        )
    response.stream_to_file(newFileName)
    playsound(newFileName)
# Initialize the OpenAI client
client = OpenAI(api_key="ENTERAPIKEY")

# Open the file to be uploaded
with open("dataset.json", "rb") as open_file:
    # Upload the file to OpenAI
    data_file = client.files.create(file=open_file, purpose='assistants')

# Create an AI assistant
ai_assistant = client.beta.assistants.create(
    name="Serena",
    instructions="You are an application with special expertise in"
        "providing resources and guidance for managing stress,"
        "practicing mindfulness, or seeking professional help when needed"
        "You are required to ask for more details on why the user feels the"
        "way that they feel"
        "You are also required to name specific activities and resources that can"
        "aid in the users specific mental health issues"
        "You are also required to suggest seeking professional help"
        "when the users issues seem to require it"
        "Your voice is relaxing, and helps people feel comfortable"
        "Your voice is seductive",
    model="gpt-3.5-turbo",
    tools=[{"type": "file_search"}],
)
endProgram = False
while endProgram != True:
    # Prompt the user for input
    prompt = input("Enter a prompt: ")

    # Create a thread with the user prompt
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # Print thread ID and assistant ID
    print("\n############################################")
    print("Thread id:", thread.id)
    print("Assistant id:", ai_assistant.id)
    print("############################################\n")

    # Create and poll a run for the thread
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=ai_assistant.id
    )

    # If run is completed, print user and assistant messages
    if run.status == "completed":
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        
        print("User:", messages.data[1].content[0].text.value)

        ###### AI RESPONSE
        print("Assistant:", messages.data[0].content[0].text.value)
        text2speech( messages.data[0].content[0].text.value)
        print("\n############################################")
        print("Run id:", run.id)
    else:
        print(run.status)
        
    if prompt == "exit" or prompt == "quit":
        endProgram = True
        
