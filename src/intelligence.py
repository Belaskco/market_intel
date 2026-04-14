import pandas as pd
import plotly.graph_objects as go
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.preprocessing import LabelEncoder
from typing import Tuple, Optional

class MarketIntelligence:
    @staticmethod
    def calculate_spc(df: pd.DataFrame) -> Tuple[pd.DataFrame, float, float]:
        v_dia = df.groupby('dia_do_mes').size().reset_index(name='vol')
        mean = v_dia['vol'].mean()
        std = v_dia['vol'].std()
        return v_dia, mean, std

    @staticmethod
    def get_pareto_data(df: pd.DataFrame):
        rank_df = df['marca'].value_counts().reset_index(name='vendas').rename(columns={'index': 'marca'})
        rank_df['acc_perc'] = rank_df['vendas'].cumsum() / rank_df['vendas'].sum() * 100
        return rank_df

    @staticmethod
    def get_decision_logic(df: pd.DataFrame) -> Optional[str]:
        if len(df['marca'].unique()) <= 1:
            return None
        le_uf = LabelEncoder()
        df_tree = df.copy()
        df_tree['uf_code'] = le_uf.fit_transform(df_tree['uf'])
        clf = DecisionTreeClassifier(max_depth=2, random_state=42)
        clf.fit(df_tree[['dia_do_mes', 'uf_code']], df_tree['marca'])
        return export_text(clf, feature_names=['Day', 'Region_ID'])