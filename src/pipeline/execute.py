from pathlib import Path
import pandas as pd

from preprocess import run_preprocessing

BASE_DIR = Path(__file__).resolve().parent
csv_path = BASE_DIR / "data" / "medium_final_data.csv"

#1. Cargar datos
df = pd.read_csv(csv_path)

#2. Preprocesar
df = run_preprocessing(df)

new_df = df.to_csv(BASE_DIR / "data" / "preprocessed_articles.csv", index=False)