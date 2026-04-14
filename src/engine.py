import pandas as pd
import os
from typing import List, Optional

class DataEngine:
    """Classe responsável pela ingestão e processamento primário de dados."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_data(self) -> Optional[pd.DataFrame]:
        """Carrega o JSON e realiza o parse inicial de datas."""
        if not os.path.exists(self.file_path):
            return None
        try:
            df = pd.read_json(self.file_path)
            df['date'] = pd.to_datetime(df['date'])
            df['dia_do_mes'] = df['date'].dt.day
            return df
        except Exception as e:
            print(f"Erro na carga de dados: {e}")
            return None

    @staticmethod
    def apply_filters(df: pd.DataFrame, marcas: List[str], ufs: List[str], dias: tuple) -> pd.DataFrame:
        """Aplica filtros dinâmicos baseados na seleção do usuário."""
        mask = (df['marca'].isin(marcas)) & \
               (df['uf'].isin(ufs)) & \
               (df['dia_do_mes'].between(dias[0], dias[1]))
        return df[mask].copy()