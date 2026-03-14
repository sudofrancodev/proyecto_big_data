from pathlib import Path
import pandas as pd

from pipeline.preprocess import run_preprocessing
from pipeline.train import train_model
from pipeline.train import show_recommendations

BASE_DIR = Path(__file__).resolve().parent
csv_path = BASE_DIR / "data" / "clean_articles.csv"

#1. Cargar datos
df = pd.read_csv(csv_path)

#2. Preprocesar
df = run_preprocessing(df)

#3. Entrenar modelo
model = train_model(df)

show_recommendations(model, article_index=10)

#def search(query):
#    return model.search(query)

#if __name__ == "__main__":
#    while True:
#        q = input("Buscar: ")
#        results = search(q)
#        print(results[["title", "link"]])