#!/usr/bin/env python3
"""
Data Cleaning Module

This module provides functions for cleaning pandas DataFrames, including
handling missing values, removing duplicates, and converting data types.
Each function takes a DataFrame as input and returns a cleaned DataFrame.
"""

import pandas as pd
import numpy as np


def clean_missing_values(df):
    """
    Detect and handle missing values in a DataFrame.
    
    This function identifies columns with missing values and applies appropriate
    strategies to handle them:
    - Numeric columns: Fill with median
    - Categorical/text columns: Fill with mode (most frequent value)
    - Date columns: Fill with previous or next value (forward fill, then backward fill)
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The input DataFrame to clean
        
    Returns:
    --------
    pandas.DataFrame
        A DataFrame with missing values handled
    """
    # Create a copy to avoid modifying the original DataFrame
    cleaned_df = df.copy()
    
    # Get information about missing values
    missing_info = cleaned_df.isnull().sum()
    columns_with_missing = missing_info[missing_info > 0].index.tolist()
    
    # If no missing values, return the original DataFrame
    if not columns_with_missing:
        return cleaned_df
    
    # Handle missing values based on data type
    for column in columns_with_missing:
        # Get the data type of the column
        dtype = cleaned_df[column].dtype
        
        # Handle numeric columns (fill with median)
        if np.issubdtype(dtype, np.number):
            median_value = cleaned_df[column].median()
            cleaned_df[column].fillna(median_value, inplace=True)
        
        # Handle datetime columns (forward fill then backward fill)
        elif pd.api.types.is_datetime64_dtype(dtype):
            cleaned_df[column].fillna(method='ffill', inplace=True)
            cleaned_df[column].fillna(method='bfill', inplace=True)
        
        # Handle categorical/object columns (fill with mode)
        else:
            mode_value = cleaned_df[column].mode()[0]
            cleaned_df[column].fillna(mode_value, inplace=True)
    
    return cleaned_df


def remove_duplicates(df):
    """
    Identify and remove duplicate rows from a DataFrame.
    
    This function checks for duplicate rows and removes them, keeping only
    the first occurrence.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The input DataFrame to clean
        
    Returns:
    --------
    pandas.DataFrame
        A DataFrame with duplicate rows removed
    """
    # Create a copy to avoid modifying the original DataFrame
    cleaned_df = df.copy()
    
    # Get the original row count
    original_count = len(cleaned_df)
    
    # Remove duplicates, keeping the first occurrence
    cleaned_df.drop_duplicates(inplace=True)
    
    # Get the new row count
    new_count = len(cleaned_df)
    
    # Calculate the number of duplicates removed
    duplicates_removed = original_count - new_count
    
    # If duplicates were found, reset the index
    if duplicates_removed > 0:
        cleaned_df.reset_index(drop=True, inplace=True)
    
    return cleaned_df


def convert_data_types(df):
    """
    Convert data types in a DataFrame to more appropriate types.
    
    This function attempts to convert:
    - Object columns that contain numbers to numeric types
    - Object columns that contain dates to datetime types
    - Object columns with few unique values to categorical types
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The input DataFrame to clean
        
    Returns:
    --------
    pandas.DataFrame
        A DataFrame with optimized data types
    """
    # Create a copy to avoid modifying the original DataFrame
    cleaned_df = df.copy()
    
    # Process each column
    for column in cleaned_df.columns:
        # Skip columns that are already numeric or datetime
        if pd.api.types.is_numeric_dtype(cleaned_df[column]) or pd.api.types.is_datetime64_dtype(cleaned_df[column]):
            continue
        
        # Try to convert object columns to numeric
        if cleaned_df[column].dtype == 'object':
            # Check if column can be converted to numeric
            try:
                numeric_column = pd.to_numeric(cleaned_df[column])
                cleaned_df[column] = numeric_column
                continue
            except (ValueError, TypeError):
                pass
            
            # Check if column can be converted to datetime
            try:
                datetime_column = pd.to_datetime(cleaned_df[column])
                cleaned_df[column] = datetime_column
                continue
            except (ValueError, TypeError):
                pass
            
            # Convert to categorical if the column has few unique values
            # (less than 50% of total rows and fewer than 100 unique values)
            unique_count = cleaned_df[column].nunique()
            if unique_count < min(100, len(cleaned_df) * 0.5):
                cleaned_df[column] = cleaned_df[column].astype('category')
    
    return cleaned_df