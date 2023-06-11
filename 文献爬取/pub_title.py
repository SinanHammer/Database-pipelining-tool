import requests
from bs4 import BeautifulSoup

def search_doi_by_title(title):
    query_url = f'https://api.crossref.org/works?query.title={title.replace(" ", "+")}&rows=1'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

    try:
        response = requests.get(query_url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if 'items' in data and len(data['items']) > 0:
            item = data['items'][0]
            if 'DOI' in item:
                return item['DOI']

    except requests.exceptions.HTTPError as e:
        print(f'Error searching DOI: {e}')

    return None


def download_paper(doi):
    base_url = 'https://sci-hub.se/'
    url = f'{base_url}{doi}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # 提取PDF链接
        pdf_url = extract_pdf_url(response.text)

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
    # 在HTML内容中提取PDF链接的方法
    # 这里可以根据Sci-Hub网页的HTML结构进行解析，提取相应的链接
    # 由于Sci-Hub可能会更改其网页结构，这个方法可能需要定期更新

    # 一个简单的示例：
    start_index = html_content.find('href="') + 6
    end_index = html_content.find('">[下载]')
    pdf_url = html_content[start_index:end_index]

    return pdf_url


# 使用示例
paper_title = 'New Specimens of Scutellosaurus Lawleri Colbert, 1981, from the Lower Jurassic Kayenta Formation in Arizona Elucidate the Early Evolution of Thyreophoran Dinosaurs'
doi = search_doi_by_title(paper_title)

if doi:
    download_paper(doi)
else:
    print('DOI not found for the given paper title.')
