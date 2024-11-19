# Imports for gemini
import google.generativeai as genai
from dotenv import load_dotenv
import os
# Imports for data extraction
import csv
# Imports for interface
from tkinter import *
from tkinter import ttk, messagebox

# Load environment variables for API configuration
load_dotenv()

# Configure the Generative Model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize data for prompt history
data = [["Prompts", "Response"]]

# Function to generate a response and update the prompt history
def generate_response():
    prompt = prompt_entry.get()
    if prompt.strip() == "":
        messagebox.showinfo("Input Error", "Please enter a prompt.")
        return
    
    # Combine data into a single string for context
    context = "\n".join([f"Prompt: {row[0]} | Response: {row[1]}" for row in data[1:]])  # Skip header
    full_prompt = f"Use the following context to answer this prompt:\n{context}\nPrompt: {prompt}"
    
    # Generate response
    response = model.generate_content(full_prompt).text
    response_text.delete(1.0, END)  # Clear previous response
    response_text.insert(END, response)  # Insert new response
    data.append([prompt, response])  # Append prompt and response to history
    prompt_entry.delete(0, END)

# Function to save the prompt history (append to existing file)
def save_history():
    file_path = os.path.join("./", "prompt_history.csv")
    with open(file_path, mode="a", newline="") as file:  # 'a' mode to append
        writer = csv.writer(file)
        writer.writerows(data)
    messagebox.showinfo("Save Successful", "Prompt history appended to prompt_history.csv")

# Function to clear the prompt history CSV file
def clear_history():
    file_path = os.path.join("./", "prompt_history.csv")
    if os.path.exists(file_path):
        os.remove(file_path)
        messagebox.showinfo("Clear Successful", "Prompt history file cleared.")
    else:
        messagebox.showinfo("No File", "No prompt history file to clear.")

# Function to save prompt history and exit the program
def save_and_exit():
    file_path = os.path.join("./", "prompt_history.csv")
    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)
    messagebox.showinfo("Exit Program", "Prompt history saved. Exiting the program.")
    root.destroy()  # Close the tkinter window

# Initialize the main window
root = Tk()
root.title("Prompt Generator")
root.geometry("600x500")

# Create widgets
Label(root, text="Enter your prompt:").pack(pady=10)
prompt_entry = Entry(root, width=50)
prompt_entry.pack(pady=5)

Button(root, text="Generate Response", command=generate_response).pack(pady=5)

Label(root, text="Response:").pack(pady=10)

# Frame for the response text and scrollbar
response_frame = Frame(root)
response_frame.pack(pady=5, fill=BOTH, expand=True)

# Text widget with scrollbar for response display
response_text = Text(response_frame, wrap=WORD, height=10, width=70)
response_text.pack(side=LEFT, fill=BOTH, expand=True)

response_scrollbar = Scrollbar(response_frame, command=response_text.yview)
response_scrollbar.pack(side=RIGHT, fill=Y)
response_text.config(yscrollcommand=response_scrollbar.set)

# Buttons for different save options
Button(root, text="Save Prompt History", command=save_history).pack(pady=5)
Button(root, text="Clear Prompt History", command=clear_history).pack(pady=5)
Button(root, text="Exit Program", command=save_and_exit).pack(pady=5)

# Run the tkinter main loop
root.mainloop()