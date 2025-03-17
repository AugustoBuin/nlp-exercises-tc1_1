import PyPDF2
import re
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import nltk
from nltk.corpus import stopwords

# Baixar stopwords do NLTK (somente na primeira execução)
nltk.download("stopwords")

# Caminho do arquivo PDF
pdf_path = "A_moreninha.pdf"


def extract_text_from_pdf(pdf_path):
    """Extrai o texto do PDF."""
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + " "
    return text


def clean_text(text):
    """Remove caracteres especiais, pontuação e números do texto."""
    text = re.sub(r"\d+", "", text)  # Remove números
    text = re.sub(r"\s+", " ", text)  # Remove múltiplos espaços
    text = re.sub(r"[^\w\s]", "", text)  # Remove pontuação
    return text.lower().strip()


def get_most_common_words(text, n=25):
    """Conta as palavras mais frequentes, removendo stopwords."""
    words = text.split()
    stop_words = set(stopwords.words("portuguese"))  # Stopwords em português
    filtered_words = [word for word in words if word not in stop_words]
    word_counts = Counter(filtered_words)
    return word_counts.most_common(n)


def plot_word_frequency(most_common_words):
    """Gera um gráfico de frequência das palavras mais usadas."""
    words, frequencies = zip(*most_common_words)  # Separar palavras e contagens
    y_pos = np.arange(len(words))

    plt.figure(figsize=(12, 6))
    plt.barh(y_pos, frequencies, color="skyblue")
    plt.yticks(y_pos, words)
    plt.xlabel("Frequência")
    plt.ylabel("Palavras")
    plt.title("25 Palavras Mais Frequentes (Sem Stopwords)")
    plt.gca().invert_yaxis()  # Inverte para colocar a palavra mais usada no topo
    plt.show()


# Executando as funções
raw_text = extract_text_from_pdf(pdf_path)
cleaned_text = clean_text(raw_text)
most_common_words = get_most_common_words(cleaned_text, 25)

# Exibir resultados
print("As 25 palavras mais comuns no texto são:")
for word, freq in most_common_words:
    print(f"{word}: {freq}")

# Gerar o gráfico
plot_word_frequency(most_common_words)
