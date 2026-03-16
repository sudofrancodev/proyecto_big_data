import ast
import pandas as pd

class TagProcessor:

    def __init__(self, dataframe: pd.DataFrame, tag_column: str = "article_tags"):
        self.df = dataframe
        self.tag_column = tag_column

    def _parse_tag_string(self, tag_str):
        """
        Convierte un string tipo "['AI', 'ML']" en lista real.
        Si falla, retorna lista vacia. 
        """

        if isinstance(tag_str, list):
            return [str(tag) for tag in tag_str]
        
        if isinstance(tag_str, str):
            try:
                return [str(tag) for tag in ast.literal_eval(tag_str)]
            except (ValueError, SyntaxError):   
                return []
        
        return []
        
    
    def clean_tags(self) -> pd.DataFrame:
        """
        Limpia la columna de tags y crea una columna 'Taglist_clean'
        con texto plano separado por espacios.
        """
        self.df[self.tag_column] = self.df[self.tag_column].fillna("")

        parsed_tags = self.df[self.tag_column].apply(self._parse_tag_string)

        self.df["Taglist_clean"] = parsed_tags.apply(lambda tags: " ".join(tags))

        return self.df