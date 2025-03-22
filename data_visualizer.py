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
    # Adjust figsize to avoid overly tall plots
    max_height = figsize[0] * 1.5  # Limit height to 1.5x width
    adjusted_figsize = (figsize[0], min(figsize[1], max_height))
    fig, ax = plt.subplots(figsize=adjusted_figsize)
    
    # Determine if the column is numeric or categorical
    is_numeric = pd.api.types.is_numeric_dtype(df[column_name])
    
    if is_numeric:
        # For numeric data, create a histogram
        ax = sns.histplot(df[column_name], kde=True, bins=bins)
        
        # Add descriptive statistics as text
        stats_text = (f"Mean: {df[column_name].mean():.2f}\n"
                      f"Median: {df[column_name].median():.2f}\n"
                      f"Std Dev: {df[column_name].std():.2f}")
        
        ax.text(0.95, 0.95, stats_text,
                 transform=ax.transAxes,
                 verticalalignment='top',
                 horizontalalignment='right',
                 bbox={'boxstyle': 'round', 'facecolor': 'white', 'alpha': 0.8})
        
        # Set labels
        ax.set_xlabel(column_name, fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        
    else:
        # For categorical data, create a bar chart of value counts
        value_counts = df[column_name].value_counts().reset_index()
        value_counts.columns = [column_name, 'Count']
        
        # ✅ Optional: limit to top N categories (e.g., 50) for better readability
        top_n = 50
        value_counts = value_counts.head(top_n)

        sns.barplot(x=column_name, y='Count', data=value_counts, ax=ax)
        
        # Add count labels on top of bars
        for p in ax.patches:
            ax.annotate(f'{int(p.get_height())}', 
                       (p.get_x() + p.get_width() / 2., p.get_height()),
                       ha='center', va='bottom')
        
        # Set labels
        ax.set_xlabel(column_name, fontsize=12)
        ax.set_ylabel('Count', fontsize=12)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    
    # Set title
    if title is None:
        title = f'Distribution of {column_name}'
    ax.set_title(title, fontsize=15)
    
    # Display the plot
    fig.tight_layout()
    return fig
    
def plot_histogram(df, column_name, sns_style='darkgrid', figsize=(10, 6), title=None, bins=20):
    sns.set_style(sns_style)
    fig, ax = plt.subplots(figsize=figsize)
    sns.histplot(df[column_name], kde=True, bins=bins, ax=ax)

    if title is None:
        title = f'Histogram of {column_name}'
    ax.set_title(title, fontsize=15)
    ax.set_xlabel(column_name)
    ax.set_ylabel('Frequency')

    fig.tight_layout()
    return fig

def plot_pie_chart(df, column_name, title=None):
    value_counts = df[column_name].value_counts()
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%', startangle=140)
    ax.axiis('equal')
    if title is None:
        title = f'Distribution of {column_name}'
    ax.set_title(title, fontsize=15)
    return fig