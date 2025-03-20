#!/usr/bin/env python3
"""
Data Cleaning Tool - Main Script

This script serves as the entry point for the data cleaning tool.
It handles command-line arguments, loads CSV data, applies cleaning operations,
and outputs the cleaned data.
"""

import argparse
import sys
import pandas as pd
import os
import seaborn as sns


# Import the cleaning module (to be created separately)
try:
    from data_cleaner import clean_missing_values, remove_duplicates, convert_data_types
except ImportError:
    print("Error: The cleaning module is missing. Make sure it's in the same directory.")
    sys.exit(1)

# Import the visualization module
try:
    from data_visualizer import plot_bar_chart
except ImportError:
    print("Error: The visualization module is missing. Make sure it's in the same directory.")
    sys.exit(1)

def parse_arguments():
    """Parse and validate command-line arguments."""
    parser = argparse.ArgumentParser(description='Data Cleaning Tool for CSV files')
    
    # Required argument for input file
    parser.add_argument('input_file', type=str, help='Path to the input CSV file')
    
    # Optional arguments for cleaning
    parser.add_argument('-o', '--output', type=str, help='Path to save the cleaned CSV file (if not specified, results will be displayed)')
    parser.add_argument('--handle-missing', action='store_true', help='Clean missing values')
    parser.add_argument('--remove-duplicates', action='store_true', help='Remove duplicate rows')
    parser.add_argument('--convert-types', action='store_true', help='Convert data types')
    parser.add_argument('--all', action='store_true', help='Apply all cleaning operations')
    
    # Optional arguments for visualization
    parser.add_argument('--plot-column', type=str, help='Generate a visualization for the specified column')
    parser.add_argument('--sns-style', type=str, default='darkgrid', 
                        choices=['darkgrid', 'whitegrid', 'dark', 'white', 'ticks'],
                        help='Seaborn style for plots (default: darkgrid)')
    parser.add_argument('--figsize', type=str, default='10,6', 
                        help='Figure size in inches as width,height (default: 10,6)')
    parser.add_argument('--title', type=str, help='Custom title for the plot')
    parser.add_argument('--bins', type=int, default=20, 
                        help='Number of bins for numerical data visualization (default: 20)')
    
    args = parser.parse_args()
    
    # Validate that the input file exists and is a CSV
    if not os.path.exists(args.input_file):
        parser.error(f"Input file not found: {args.input_file}")
    
    if not args.input_file.lower().endswith('.csv'):
        parser.error(f"Input file must be a CSV file: {args.input_file}")
    
    return args

def load_csv(file_path):
    """Load data from a CSV file into a pandas DataFrame."""
    try:
        print(f"Loading data from {file_path}...")
        df = pd.read_csv(file_path)
        print(f"Successfully loaded {len(df)} rows and {len(df.columns)} columns.")
        return df
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        sys.exit(1)

def save_or_display_results(df, output_path=None):
    """Save the DataFrame to a CSV file or display it."""
    if output_path:
        try:
            df.to_csv(output_path, index=False)
            print(f"Cleaned data saved to {output_path}")
        except Exception as e:
            print(f"Error saving cleaned data: {e}")
            sys.exit(1)
    else:
        # Display the first few rows of the DataFrame
        print("\nCleaned Data Preview:")
        print(df.head())
        print(f"\nTotal rows after cleaning: {len(df)}")
        print(f"Data types:\n{df.dtypes}")

def main():
    """Main function to orchestrate the data cleaning process."""
    # Parse command-line arguments
    args = parse_arguments()
    
    # Load the CSV file
    df = load_csv(args.input_file)
    
    # Apply cleaning operations based on arguments
    cleaning_applied = False
    
    if args.handle_missing or args.all:
        print("Cleaning missing values...")
        df = clean_missing_values(df)
        cleaning_applied = True
    
    if args.remove_duplicates or args.all:
        print("Removing duplicate rows...")
        df = remove_duplicates(df)
        cleaning_applied = True
    
    if args.convert_types or args.all:
        print("Converting data types...")
        df = convert_data_types(df)
        cleaning_applied = True
    
    if not cleaning_applied:
        print("No cleaning operations specified. Use --handle-missing, --remove-duplicates, --convert-types, or --all")
    
    # Save or display the results
    save_or_display_results(df, args.output)
    
    # Apply visualization operations based on arguments
    visualization_applied = False
    
    # Generate visualization if requested
    if args.plot_column:
        try:
            # Parse figsize from string to tuple
            figsize = tuple(map(int, args.figsize.split(',')))
            
            print(f"Generating visualization for '{args.plot_column}' column with style '{args.sns_style}'...")
            plot_bar_chart(
                df, 
                column_name=args.plot_column,
                sns_style=args.sns_style,
                figsize=figsize,
                title=args.title,
                bins=args.bins
            )
            visualization_applied = True
        except (TypeError, ValueError) as e:
            print(f"Error generating visualization: {e}")
        except Exception as e:
            print(f"Unexpected error during visualization: {e}")
    
    if args.plot_column and not visualization_applied:
        print("Warning: Visualization was requested but could not be completed.")
    elif visualization_applied:
        print("Visualization completed successfully.")

if __name__ == "__main__":
    main()
