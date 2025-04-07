import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from transformers import pipeline
import stanza
from .utils import extract_keywords_stanza, calculate_semantic_similarity_stanza

class PromptTracker:
    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
        
        stanza.download('en')
        self.nlp = stanza.Pipeline('en')

        self.data_columns = [
            "prompt", "prompt_timestamp", "word_count", "char_count", "key_topics", 
            "deleted_words_percent", "added_words_num", "semantic_similarity", "change_summary"
        ]
        self.data = pd.DataFrame(columns=self.data_columns)

    def track(self, prompt):
        prompt_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        word_count = len(prompt.split())
        char_count = len(prompt)
        key_topics = extract_keywords_stanza(prompt, self.nlp)
        deleted_words_percent = 0
        added_words_num = 0
        semantic_similarity = 0
        change_summary = ""

        if self.data.empty:
            change_summary = "This is the first prompt."
        else:
            previous_prompt = self.data.iloc[-1]["prompt"]
            previous_prompt_words = set(previous_prompt.split())
            current_prompt_words = set(prompt.split())

            deleted_words = previous_prompt_words - current_prompt_words
            added_words = current_prompt_words - previous_prompt_words

            if previous_prompt_words:
                deleted_words_percent = round((len(deleted_words) / len(previous_prompt_words)) * 100, 2)

            added_words_num = len(added_words)
            semantic_similarity = calculate_semantic_similarity_stanza(previous_prompt, prompt, self.nlp)

            change_summary = self.model.generate_content(
                ["Summarize changes in about 30 words. Previous: '" + previous_prompt + "' Current: '" + prompt + "'"],
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                },
            ).text.replace(",", " ")

        new_row = pd.DataFrame({
            "prompt": [prompt],
            "prompt_timestamp": [prompt_timestamp],
            "word_count": [word_count],
            "char_count": [char_count],
            "key_topics": [key_topics],
            "deleted_words_percent": [deleted_words_percent],
            "added_words_num": [added_words_num],
            "semantic_similarity": [semantic_similarity],
            "change_summary": [change_summary]
        })

        self.data = pd.concat([self.data, new_row], ignore_index=True)
        
        # ADD HERE: Build context and generate & print model response
        # Create conversation context using all previous prompts
        context = "\n".join([f"[{i+1}] {row}" for i, row in enumerate(self.data["prompt"].tolist())])
        structured_prompt = (
            f"Here is the conversation so far:\n{context}\n\n"
            f"Respond thoughtfully to the following prompt:\n{prompt}"
        )
        response = self.model.generate_content(
            [structured_prompt],
            safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                },
        ).text
        print("Model response:", response)


    def save_prompt_history(self, filename="prompt_history.csv"):
        file_path = os.path.join("./", filename)
        self.data.to_csv(file_path, index=False, encoding='utf-8')
