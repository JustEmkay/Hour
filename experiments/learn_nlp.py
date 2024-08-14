import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Sample text
text = "This is a sample text. It contains some numbers, like 123 and special characters! @#"

# Remove HTML tags
text = re.sub(r'<.*?>', '', text)

# Remove special characters and punctuation
text = text.translate(str.maketrans('', '', string.punctuation))

# Lowercasing
text = text.lower()

# Tokenization
words = nltk.word_tokenize(text)

# Remove stop words
stop_words = set(stopwords.words('english'))
words = [word for word in words if word not in stop_words]

# Stemming
stemmer = PorterStemmer()
words = [stemmer.stem(word) for word in words]

# Lemmatization (requires spaCy)
import spacy
nlp = spacy.load('en_core_web_sm')
doc = nlp(text)
words = [token.lemma_ for token in doc]

print(words)
