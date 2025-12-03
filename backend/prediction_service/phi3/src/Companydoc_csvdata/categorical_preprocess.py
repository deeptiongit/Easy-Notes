import pandas as pd 
from tqdm import tqdm
import re
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from datasets import DatasetDict, Dataset
from datetime import datetime
import os

BASE_DIR = os.path.dirname(__file__)
data = "company-document-text.csv"
data_path = os.path.join(BASE_DIR,data)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

df = pd.read_csv(data_path)
df.head()
df = df[['text','label']]
df=df.dropna()


def preprocess_text(text):
    try:
        text = text.replace('\n', ' ')
    except:
        print(text)
        return None
    text = re.sub(r'<[^>]+>', '', text)
    
    text = re.sub(r'\s+', ' ', text)
    
    text = re.sub(r'[^\w\s$€%.,-]|(?<=\d)[.,](?=\d)|(?<=\d)[/](?=\d)', ' ', text).lower()
    
    text = text.strip()
    if len(text.split(' '))<4 :
        return None
    else:
        return text




def apply_preprocessing(df):
    preprocessed_texts = []
    for text in tqdm(df['text']):
        preprocessed_text = preprocess_text(text)
        preprocessed_texts.append(preprocessed_text)
    df['text'] = preprocessed_texts
    return df



df = apply_preprocessing(df)

label_encoder = LabelEncoder()
df['label'] = label_encoder.fit_transform(df['label'])

train_df, test_df = train_test_split(df, test_size=0.15, random_state=42)

print(f"Training set size: {len(train_df)}")
print(f"Testing set size: {len(test_df)}")

dataset_train = Dataset.from_pandas(train_df.reset_index(drop=True))
dataset_test = Dataset.from_pandas(test_df.reset_index(drop=True))

dataset = DatasetDict({
    "train": dataset_train,
    "test": dataset_test
})




text_p = []
max_length=512
def tokenize_data(example):
    try:
        return tokenizer(str(example['text']),
                         padding='max_length',
                         truncation=True,
                         max_length=max_length,
                      )
    except:
        print("Error")



dataset = dataset.map(tokenize_data ,remove_columns=["text"])


train_path = os.path.join(BASE_DIR, "train.jsonl")
test_path = os.path.join(BASE_DIR, "test.jsonl")

dataset["train"].to_json(train_path)
dataset["test"].to_json(test_path)





