import re
import requests


def download_paper(doi):
    # base_url = 'https://sci-hub.se/'
    base_url = 'https://shuobolife.com/sci-hub-2/'
    url = f'{base_url}{doi}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # 提取PDF链接
        pdf_url = extract_pdf_url(response.text)

        if pdf_url is None:
            pdf_url = extract_backup_pdf_url(response.text)

        if pdf_url is None:
            raise ValueError('PDF URL not found')

        # 下载PDF文件
        pdf_response = requests.get(pdf_url)
        pdf_response.raise_for_status()

        # 保存PDF文件
        filename = f'{doi.replace("/", "_")}.pdf'
        with open(filename, 'wb') as f:
            f.write(pdf_response.content)

        print(f'Successfully downloaded the paper: {filename}')

    except requests.exceptions.HTTPError as e:
        print(f'Error downloading the paper: {e}')


def extract_pdf_url(html_content):
    # 提取PDF链接的方法
    script_pattern = r"location\.href\s*=\s*'(.+?)'"
    script_match = re.search(script_pattern, html_content, re.IGNORECASE)

    if script_match:
        script_url = script_match.group(1)
        if script_url.startswith('http://'):
            return script_url

    return None


def extract_backup_pdf_url(html_content):
    # 提取备用PDF链接的方法
    backup_pattern = r'<a\s+href="(.+?)"\s*class="icon icon-dl">'
    backup_match = re.search(backup_pattern, html_content, re.IGNORECASE)

    if backup_match:
        backup_url = backup_match.group(1)
        if backup_url.startswith('http://'):
            return backup_url

    return None


# 使用示例
doi = 'https://doi.org/10.7554/eLife.75248'
download_paper(doi)
