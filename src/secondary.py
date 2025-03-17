import PyPDF2
import re
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import nltk
from nltk.corpus import stopwords

# Downloads stopwords from NLTK (1st Execution Only)
nltk.download("stopwords")

# PDF File Path
pdf_path = "metamorfose.pdf"


def extract_text_from_pdf(pdf_path):
    """Extracts PDF text."""
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + " "
    return text


def clean_text(text):
    """Removes especial characters, punctuations and numbers from text."""
    text = re.sub(r"\d+", "", text)  # Removes numbers
    text = re.sub(r"\s+", " ", text)  # Removes multiple spaces
    text = re.sub(r"[^\w\s]", "", text)  # Removes pontuação
    return text.lower().strip()


def get_most_common_words(text, n=25):
    """Counts most frequent words and removes stopwords."""
    words = text.split()
    stop_words = set(stopwords.words("portuguese"))  # Stopwords in Portuguese
    filtered_words = [word for word in words if word not in stop_words]
    word_counts = Counter(filtered_words)
    return word_counts.most_common(n)


def plot_word_frequency(most_common_words):
    """generates a frequency graph about the most used words."""
    words, frequencies = zip(*most_common_words)  # Separates words and counts
    y_pos = np.arange(len(words))

    plt.figure(figsize=(12, 6))
    plt.barh(y_pos, frequencies, color="skyblue")
    plt.yticks(y_pos, words)
    plt.xlabel("Frequência")
    plt.ylabel("Palavras")
    plt.title("25 Palavras Mais Frequentes (Sem Stopwords)")
    plt.gca().invert_yaxis()  # Inverts so the most used word is at the top
    plt.show()


def analyze_text(text):
    """Counts unique words and calculates text diversity."""
    words = text.split()
    total_words = len(words)
    unique_words = len(set(words))
    diversity = unique_words / total_words * 100  # Percentage of unique words
    return total_words, unique_words, diversity


# Executes Functions
raw_text = extract_text_from_pdf(pdf_path)
cleaned_text = clean_text(raw_text)
most_common_words = get_most_common_words(cleaned_text, 25)
total_words, unique_words, diversity = analyze_text(cleaned_text)

# Show Results
print("As 25 palavras mais comuns no texto são:")
for word, freq in most_common_words:
    print(f"{word}: {freq}")

# Generates Graphs
plot_word_frequency(most_common_words)

# Displays Text Analysis
print(f"Total de palavras: {total_words}")
print(f"Palavras únicas: {unique_words}")
print(f"Diversidade lexical: {diversity:.2f}%")
