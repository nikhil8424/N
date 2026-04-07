# pip install pandas nltk scikit-learn
import pandas as pd, re, nltk
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords'); nltk.download('wordnet')
data = pd.read_csv("your_dataset.csv")   

lem = WordNetLemmatizer()
corpus = []
for t in data['text']:
    t = re.sub('[^a-zA-Z]', ' ', t).lower().split()
    t = [lem.lemmatize(w) for w in t if w not in stopwords.words('english')]
    corpus.append(" ".join(t))

X_train,X_test,y_train,y_test = train_test_split(corpus,data['label'],test_size=0.33)

cv = CountVectorizer()
X_train = cv.fit_transform(X_train)
X_test = cv.transform(X_test)

model = LogisticRegression().fit(X_train,y_train)


pred = model.predict(X_test)
print(confusion_matrix(y_test,pred))