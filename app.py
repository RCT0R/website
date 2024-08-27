from flask import Flask, render_template, request
import requests
import time

app = Flask(__name__)

class SimpleTranslator:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model_name}"
        self.headers = {"Authorization": f"Bearer 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"}

    def translate(self, text: str) -> str:
        payload = {"inputs": text}
        max_retries = 5
        for attempt in range(max_retries):
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            if response.status_code == 200:
                translation = response.json()[0]['translation_text']
                return translation
            elif response.status_code == 503:
                time.sleep(10)
            else:
                return f"Error: {response.status_code}, {response.text}"
        return "Failed to get translation after multiple attempts."

translator = SimpleTranslator("Helsinki-NLP/opus-mt-en-hi")

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        english_text = request.form['english_text']
        translated_text = translator.translate(english_text)
        return render_template('index.html', original_text=english_text, translated_text=translated_text)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
