import re
import unicodedata
import pandas as pd
from langdetect import detect, LangDetectException as Lang
from deep_translator import GoogleTranslator


class TextCleaner:

    def __init__(self, dataframe: pd.DataFrame, text_columns: list[str]):
        missing = [col for col in text_columns if col not in dataframe.columns]
        if missing:
            raise ValueError(f"Columns not found in dataframe: {missing}")

        self.translator = GoogleTranslator(source="auto", target="en")
        self.df = dataframe
        self.text_columns = text_columns


    def _remove_emojis(self, text: str) -> str:
        """
        Elimina emojis y simbolos unicode extendidos.
        """

        return re.sub(r'[^\x00-\x7F]+', ' ', text)
    

    def _normalize_unicode(self, text: str) -> str:
        """
        Normaliza caracteres Unicode (acentos, etc.)
        """

        text = unicodedata.normalize("NFKD", text)
        return text.encode("ascii", "ignore").decode("utf-8")


    def _clean_text(self, text: str) -> str:
        if not isinstance(text, str):
            return ""
        
        # Normalizar unicode
        text = self._normalize_unicode(text)

        # Eliminar emojis y simbolos extraños
        text = self._remove_emojis(text)

        # Eliminar caracteres especiales pero conservar letras y numeros
        text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

        # Normalizar espacios
        text = re.sub(r"\s+", " ", text).strip()

        return text


    def clean(self) -> pd.DataFrame:
        for col in self.text_columns:
            self.df[col] = self.df[col].fillna("").astype(str).apply(self._clean_text)
        return self.df


    def _detect_language(self, text: str) -> str:
        try:
            return detect(text)
        except Lang:
            return "unknown"
        
    def _translate_if_needed(self, text: str, target_lang: str) -> str:
        if not text.strip():
            return text
        if self._detect_language(text) != target_lang:
            try:
                return self.translator.translate(text)
            except Exception as e:
                print(f"Error traduciendo texto: {e}")
                return text
        return text
    
    def normalize_language(self, target_lang: str = "en") -> pd.DataFrame:

        for col in self.text_columns:
            self.df[col] = self.df[col].apply(lambda x: self._translate_if_needed(x, target_lang))
        return self.df