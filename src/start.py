import os
import pandas as pd
from src.config import ROOT_DIR, parameters
from src.texts_processing import TextsTokenizer

tokenizer = TextsTokenizer()

stopwords = []
for filename in parameters.stopwords_files:
    stopwords_df = pd.read_csv(os.path.join(ROOT_DIR, "data", filename), sep="\t")
    stopwords += list(stopwords_df["stopwords"])

tokenizer.add_stopwords(stopwords)