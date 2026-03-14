import ast
import pandas as pd

class TagProcessor:

    def __init__(self, dataframe: pd.DataFrame, tag_column: str = "article_tags"):
        self.df = dataframe
        self.tag_column = tag_column

    def _parse_tag_string(self, tag_str: str) -> list:
        """
        Convierte un string tipo "['AI', 'ML']" en lista real.
        Si falla, retorna lista vacia. 
        """

        try:
            return ast.literal_eval(tag_str)
        except (ValueError, SyntaxError):
            return [str(tag) for tag in ast.literal_eval(tag_str)]
    
    def clean_tags(self) -> pd.DataFrame:
        """
        Limpia la columna de tags y crea una columna 'Taglist_clean'
        con texto plano separado por espacios.
        """
        self.df[self.tag_column] = self.df[self.tag_column].fillna("").astype(str)

        self.df["Taglist_clean"] = (
            self.df[self.tag_column]
            .apply(self._parse_tag_string)
            .apply(lambda x: " ".join(self._parse_tag_string(x)))
        )

        return self.df