import pandas as pd
import ast
from pathlib import Path

class MediumCSVRepository:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def save_incremental(self, rows: list[dict]) -> pd.DataFrame:

        """
        Guarda artículos incrementalmente en CSV evitando duplicados.

        Parameters
        ----------
        rows : list[dict]
            Nuevos artículos a persistir.

        Returns
        -------
        pd.DataFrame
            DataFrame final consolidado.
        """
        if not rows:
            raise ValueError("No hay datos para guardar")
        
        df_new = pd.DataFrame(rows)

        try:
            if self.path.exists():
                df_old = pd.read_csv(self.path, converters={"article_tags": ast.literal_eval})
                df_final = (
                    pd.concat([df_old, df_new])
                    .drop_duplicates(subset=["link"])
                )
            else:
                df_final = df_new

        
            df_final.to_csv(self.path, index=False)
            return df_final
        
        except Exception as e:
            raise RuntimeError(
                f"Error guardando datos en {self.path}"
            ) from e

    
