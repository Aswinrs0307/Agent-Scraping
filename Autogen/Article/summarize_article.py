# filename: summarize_article.py
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
import string

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

def summarize_text(text, max_sentences=5):
    stop_words = set(stopwords.words('english'))
    sentences = sent_tokenize(text)
    word_frequencies = defaultdict(int)
    
    for sentence in sentences:
        for word in sentence.split():
            word = word.lower().strip(string.punctuation)
            if word not in stop_words:
                word_frequencies[word] += 1
    
    sentence_scores = defaultdict(int)
    for sentence in sentences:
        for word in sentence.split():
            word = word.lower().strip(string.punctuation)
            if word in word_frequencies:
                sentence_scores[sentence] += word_frequencies[word]
    
    sorted_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
    summary = ' '.join(sorted_sentences[:max_sentences])
    return summary

# Read the content of the article
with open("article_content.txt", "r", encoding="utf-8") as file:
    article_text = file.read()

# Summarize the article
summary = summarize_text(article_text)
print(summary)