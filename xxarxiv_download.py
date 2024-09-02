import pandas as pd
import requests
import os
import logging
from tqdm import tqdm

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_csv(file_path):
    """读取 CSV 文件并返回 DataFrame"""
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Successfully read CSV file: {file_path}")
        return df
    except Exception as e:
        logging.error(f"Error reading CSV file: {e}")
        return None


def create_download_dir(directory):
    """创建下载目录"""
    try:
        os.makedirs(directory, exist_ok=True)
        logging.info(f"Download directory created: {directory}")
    except Exception as e:
        logging.error(f"Error creating download directory: {e}")


def sanitize_filename(filename):
    """生成合法的文件名"""
    return filename.replace('/', '_').replace('\\', '_')


def download_file(url, file_path):
    """下载文件并保存到指定路径"""
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
    """主函数"""
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
    # 配置 CSV 文件路径和下载目录
    csv_file = './arxiv_download/biorxiv_download.csv'  # 替换为你的 CSV 文件路径
    download_dir = 'biorxiv'

    main(csv_file, download_dir)