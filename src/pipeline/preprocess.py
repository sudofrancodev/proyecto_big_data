import pandas as pd
import logging
from processor.TagProcessor import TagProcessor
from rocessor.TextCleaner import TextCleaner

logger = logging.getLogger(__name__)

def run_preprocessing(df: pd.DataFrame) -> pd.DataFrame:

    logger.info(f"Iniciando preprocesamiento de datos con {len(df)} registros.")

    if df.empty:
        raise ValueError("El dataframe de entrada esta vacio.")
    
    processor = TagProcessor(df)
    df = processor.clean_tags()

    cleaner = TextCleaner(df, ["title", "Taglist_clean"])
    df = cleaner.clean()

    logger.info(f"Preprocesamiento completado. Registros procesados: {len(df)}")
    
    return df