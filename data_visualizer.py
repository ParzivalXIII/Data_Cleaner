"""
Data Visualization Module

This module provides functions to visualize data from a pandas DataFrame
using Seaborn for enhanced aesthetics.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from typing import Optional


def plot_bar_chart(df: pd.DataFrame, column_name: str, sns_style: str = 'darkgrid', 
                  figsize: tuple = (10, 6), title: Optional[str] = None, 
                  bins: int = 20) -> None:
    """
    Generate a bar chart showing the distribution of values in the specified column.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame containing the data to visualize
    column_name : str
        The name of the column to visualize
    sns_style : str, optional
        The Seaborn style to apply to the plot (default: 'darkgrid')
    figsize : tuple, optional
        The size of the figure (width, height) in inches (default: (10, 6))
    title : str, optional
        Custom title for the plot. If None, a default title will be generated.
    bins : int, optional
        Number of bins for numerical data (default: 20)
        
    Raises:
    -------
    TypeError
        If df is not a pandas DataFrame
    ValueError
        If the specified column is not present in the DataFrame
    """
    # Check if input is a DataFrame
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")
    
    # Check if column exists
    if column_name not in df.columns:
        raise ValueError(f"DataFrame must contain a '{column_name}' column")
    
    # Set the Seaborn style
    sns.set_style(sns_style)
    
    # Create the figure
    plt.figure(figsize=figsize)
    
    # Determine if the column is numeric or categorical
    is_numeric = pd.api.types.is_numeric_dtype(df[column_name])
    
    if is_numeric:
        # For numeric data, create a histogram
        ax = sns.histplot(df[column_name], kde=True, bins=bins)
        
        # Add descriptive statistics as text
        stats_text = (f"Mean: {df[column_name].mean():.2f}\n"
                      f"Median: {df[column_name].median():.2f}\n"
                      f"Std Dev: {df[column_name].std():.2f}")
        
        plt.text(0.95, 0.95, stats_text,
                 transform=ax.transAxes,
                 verticalalignment='top',
                 horizontalalignment='right',
                 bbox={'boxstyle': 'round', 'facecolor': 'white', 'alpha': 0.8})
        
        # Set labels
        plt.xlabel(column_name, fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        
    else:
        # For categorical data, create a bar chart of value counts
        value_counts = df[column_name].value_counts().reset_index()
        value_counts.columns = [column_name, 'Count']
        
        ax = sns.barplot(x=column_name, y='Count', data=value_counts)
        
        # Add count labels on top of bars
        for p in ax.patches:
            ax.annotate(f'{int(p.get_height())}', 
                       (p.get_x() + p.get_width() / 2., p.get_height()),
                       ha='center', va='bottom')
        
        # Set labels
        plt.xlabel(column_name, fontsize=12)
        plt.ylabel('Count', fontsize=12)
        plt.xticks(rotation=45)
    
    # Set title
    if title is None:
        title = f'Distribution of {column_name}'
    plt.title(title, fontsize=15)
    
    # Display the plot
    plt.tight_layout()
    plt.show()
