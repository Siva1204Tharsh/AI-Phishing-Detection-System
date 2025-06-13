import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib

# Load SMS Spam Dataset

df = pd.read_csv("https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv", sep='\t', names=["label", "message"])
df['label'] = df['label'].map({'ham': 0, 'spam': 1})

print(df.head())

# Save the dataset file .csv from dataframe
df.to_csv("sms.csv", index=False)



# Train/test split
X_train, X_test, y_train, y_test = train_test_split(df['message'], df['label'], test_size=0.2)

# Build model
model = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),
    ('clf', RandomForestClassifier(n_estimators=100))     
])

model.fit(X_train, y_train)
print(classification_report(y_test, model.predict(X_test)))

# # Save model
# joblib.dump(model, "../backend/model/phishing_model.pkl")


