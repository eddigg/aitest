from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Training data (hardcoded for MVP)
commands = [
    ("turn on the lights", "turn_on_lights"),
    ("switch on lights", "turn_on_lights"),
    ("turn off the lights", "turn_off_lights"),
    ("switch off lights", "turn_off_lights"),
    ("play music", "play_music"),
    ("start music", "play_music"),
    ("stop music", "stop_music"),
    ("pause music", "stop_music"),
    ("hello there", "unknown")
]
texts, intents = zip(*commands)

# Train classifier
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)
clf = LogisticRegression()
clf.fit(X, intents)

def classify_intent(text: str) -> str:
    X_test = vectorizer.transform([text])
    intent = clf.predict(X_test)[0]
    confidence = clf.predict_proba(X_test).max()
    return intent if confidence > 0.5 else "unknown"