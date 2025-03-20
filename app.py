from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from llama_index.core import SimpleDirectoryReader
from llama_index.llms.ollama import Ollama

app = Flask(__name__)

# Function to scrape a web page
def scrape_website(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = ' '.join([p.text for p in soup.find_all('p')])  # Extract paragraphs
            return text
        else:
            return "Failed to fetch the webpage."
    except Exception as e:
        return str(e)

# Function to summarize scraped data using LLM
def summarize_text(text):
    llm = Ollama(model="llama3")  # Ensure you have Ollama installed
    summary = llm.complete(text[:4000])  # Limit input to 4000 characters
    return summary

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        scraped_text = scrape_website(url)
        summary = summarize_text(scraped_text)
        return jsonify({'scraped_text': scraped_text, 'summary': summary})
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
