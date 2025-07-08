import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

def train_model():
    df = pd.read_csv("data/network_logs.csv")

    if 'threat_detected' not in df.columns:
        raise ValueError("❌ CSV file must include a 'threat_detected' column.")

    df['threat_detected'] = df['threat_detected'].astype(int)
    df['event_type'] = df['event_type'].astype('category').cat.codes
    df['device_id'] = df['device_id'].astype('category').cat.codes

    X = df[['device_id', 'event_type']]
    y = df['threat_detected']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)

    print("✅ Model trained.")
    return model