# pip install pandas nltk scikit-learn
import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
nltk.download('stopwords')

data = pd.read_csv("your_dataset.csv")
text = data.iloc[:, 0].astype(str)
stop_words = stopwords.words('english')
vectorizer = CountVectorizer(
    stop_words=stop_words,
    lowercase=True
)

dtm = vectorizer.fit_transform(text)
lda = LatentDirichletAllocation(n_components=3, random_state=42)
lda.fit(dtm)

words = vectorizer.get_feature_names_out()
for i, topic in enumerate(lda.components_):
    print(f"\nTopic {i+1}:")
    print([words[i] for i in topic.argsort()[-10:]])

print("\nTopic Distribution:")
print(lda.transform(dtm))

# pip install pandas nltk wordcloud matplotlib textblob
import pandas as pd
import nltk
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from wordcloud import WordCloud
from textblob import TextBlob

nltk.download('stopwords')
data = pd.read_csv("your_dataset.csv")
text = data.iloc[:, 0].astype(str)

stop_words = set(stopwords.words('english'))
clean_text = [" ".join([word for word in t.lower().split() if word not in stop_words]) for t in text]

wc = WordCloud(width=800, height=400).generate(" ".join(clean_text))
plt.imshow(wc)
plt.axis("off")
plt.title("WordCloud")
plt.show()
s
sentiments = [TextBlob(t).sentiment.polarity for t in text]

labels = ["Positive" if s > 0 else "Negative" if s < 0 else "Neutral" for s in sentiments]

import collections
counts = collections.Counter(labels)

plt.bar(counts.keys(), counts.values())
plt.title("Sentiment Analysis")
plt.show()
