#imports for gemini
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv
import os
#imports for data extraction
import csv
#imports for data analysis/visualization

#add feature to download prompt history as you go, can this remember conversation history?

#to overwrite previous prompthistory file
if os.path.exists("prompt_history.csv"):
    os.remove("prompt_history.csv")

data = [["Prompts", "Response"]]

#model
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")
print("Enter '~~~' to stop prompting")
prompt = input("Enter your prompt: ") #gain input from user

while(prompt != "~~~"):

    context = ""
    for row in data[1:]:
        context += "Previous Prompt: " + row[0] + " | Previous Response: " + row[1] + "\n"
        response = model.generate_content(["Use the following context to answer this prompt:\n" + context + "Prompt: " + prompt], 
                                      safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    })

    print(response.text)
    data.append([prompt] + [response.text]) #add prompt to history as well as the response to it
    prompt = input("Enter your prompt: ") #gain input from user

print("You can review your prompt history now!")
#create csv file from the list we have
file_path = os.path.join("./", "prompt_history.csv")
with open(file_path, mode='w', newline="", encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(data)