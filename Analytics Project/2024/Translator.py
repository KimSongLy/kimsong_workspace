from googletrans import Translator
import pandas as pd

# Correct the file path
file_path = r'[Enter_File_Path]'

# Read the CSV file
df = pd.read_csv(file_path)

from googletrans import Translator
translator = Translator()

# Function to translate text to English
def translate_to_english(text):

    try:
        if not text or pd.isna(text):  # Check if the text is empty or NaN
            return text
        # Detect the language and translate if not English
        detected_lang = translator.detect(text).lang
        if detected_lang != 'en':
            return translator.translate(text, src=detected_lang, dest='en').text
        else:
            return text  # Leave as-is if it's already in English
    except Exception as e:
        print(f"Error translating text: {e}")
        return text  # Return the original text in case of an error

# Apply the function to create a new column for the translation
df['column_translated'] = df['column'].apply(translate_to_english)

# Show the DataFrame
print(df.head()) 
