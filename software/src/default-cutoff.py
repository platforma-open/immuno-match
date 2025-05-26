import pandas as pd
import numpy as np
import argparse
import os

def process_data(input_file, output_dir='.'):
    # Read the CSV file
    df = pd.read_csv(input_file)

    # Extract the 'pairing_scores' column
    pairing_values = df['pairing_scores'].values

    # Calculate 75th percentile
    pairing_75 = np.percentile(pairing_values, 75)

    # For the 75th percentile, output 0.9 if the value is greater than 0.9
    # pairing_75 = pairing_75 if pairing_75 < 0.9 else 0.9

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Write results to txt files
    output_files = {
        'pairing_75.txt': str(pairing_75)
    }

    for filename, content in output_files.items():
        output_path = os.path.join(output_dir, filename)
        with open(output_path, 'w') as f:
            f.write(content)
        print(f"Written {filename} to {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Process prediction data from a CSV file.')
    parser.add_argument('input_file', help='Path to the input CSV file containing prediction data')
    parser.add_argument('--output-dir', '-o', default='.',
                      help='Directory to save output files (default: current directory)')
    
    args = parser.parse_args()
    
    try:
        process_data(args.input_file, args.output_dir)
    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found.")
        exit(1)
    except pd.errors.EmptyDataError:
        print(f"Error: Input file '{args.input_file}' is empty.")
        exit(1)
    except KeyError:
        print("Error: Input file must contain a 'pairing_scores' column.")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        exit(1)

if __name__ == '__main__':
    main()
