import pandas as pd
import requests
import os
import logging
from tqdm import tqdm
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def read_csv(file_path):
    """Read CSV file and return DataFrame"""
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Successfully read CSV file: {file_path}")
        return df
    except Exception as e:
        logging.error(f"Error reading CSV file: {e}")
        return None


def create_download_dir(directory):
    """Create download directory"""
    try:
        os.makedirs(directory, exist_ok=True)
        logging.info(f"Download directory created: {directory}")
    except Exception as e:
        logging.error(f"Error creating download directory: {e}")


def sanitize_filename(filename):
    """Generate a valid filename"""
    return filename.replace('/', '_').replace('\\', '_')


def download_file(url, file_path):
    """Download file and save to specified path"""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
            logging.info(f"Downloaded: {file_path}")
        else:
            logging.error(f"Failed to download {file_path}: HTTP {response.status_code}")
    except Exception as e:
        logging.error(f"Error downloading file {file_path}: {e}")


def main(csv_file, download_dir):
    """Main function"""
    df = read_csv(csv_file)
    if df is None:
        return

    create_download_dir(download_dir)

    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Downloading files"):
        download_link = row['Download Link']
        title = row['Title']
        file_name = sanitize_filename(f"{title}.pdf")
        file_path = os.path.join(download_dir, file_name)
        download_file(download_link, file_path)

    logging.info("All downloads completed.")


if __name__ == "__main__":
    # Use argparse to parse command line arguments
    parser = argparse.ArgumentParser(description="Batch download files from a CSV file.")
    parser.add_argument('csv_file', type=str, help="Path to the CSV file containing download links.")
    parser.add_argument('download_dir', type=str, help="Directory to save the downloaded files.")

    args = parser.parse_args()

    main(args.csv_file, args.download_dir)