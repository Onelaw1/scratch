import pandas as pd
import statsmodels.api as sm
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from typing import Dict, Any, List

class AnalyticsEngine:
    """
    Advanced Analytics Engine for Consulting-grade Insights.
    Uses Statsmodels for rigorous statistical testing and Scikit-learn for predictive modeling.
    """

    def __init__(self):
        pass

    def generate_descriptive_summary(self, df: pd.DataFrame) -> str:
        """
        Generates a professional descriptive summary of the dataset.
        """
        summary = df.describe().to_markdown()
        return f"### Descriptive Statistics\n\n{summary}\n"

    def run_regression_analysis(self, df: pd.DataFrame, target_col: str, predictor_cols: List[str]) -> str:
        """
        Performs OLS Regression to identify key drivers.
        Returns a summary of the regression results focusing on statistical significance (P-values).
        """
        try:
            X = df[predictor_cols]
            y = df[target_col]
            X = sm.add_constant(X)
            model = sm.OLS(y, X).fit()
            
            # Extract key insights
            significant_vars = model.pvalues[model.pvalues < 0.05].index.tolist()
            r_squared = model.rsquared
            
            insight = f"### Regression Analysis (Target: {target_col})\n"
            insight += f"- **R-squared**: {r_squared:.3f} (Explains {r_squared*100:.1f}% of variance)\n"
            insight += f"- **Significant Drivers (P < 0.05)**: {', '.join(significant_vars)}\n"
            insight += "\n#### Detailed Model Summary\n"
            insight += str(model.summary())
            return insight
        except Exception as e:
            return f"Error running regression: {str(e)}"

    def perform_clustering(self, df: pd.DataFrame, feature_cols: List[str], n_clusters: int = 3) -> str:
        """
        Performs K-Means clustering to segment data (e.g., Customer Segmentation).
        """
        try:
            X = df[feature_cols].dropna()
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            df['Cluster'] = kmeans.fit_predict(X)
            
            insight = f"### Clustering Analysis ({n_clusters} Segments)\n"
            for i in range(n_clusters):
                cluster_size = len(df[df['Cluster'] == i])
                insight += f"- **Cluster {i}**: {cluster_size} items\n"
                # Add mean values for features to describe cluster characteristics
                means = df[df['Cluster'] == i][feature_cols].mean()
                insight += f"  - Avg Characteristics: {means.to_dict()}\n"
            
            return insight
        except Exception as e:
            return f"Error performing clustering: {str(e)}"
