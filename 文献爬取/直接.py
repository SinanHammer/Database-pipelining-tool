import requests
from bs4 import BeautifulSoup

def download_paper_by_title(paper_title):
    base_url = 'https://sci-hub.se/'
    search_url = f'{base_url}{paper_title}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()

        # 提取DOI链接
        doi_url = extract_doi_url(response.text)

        if doi_url:
            doi = doi_url.split('/')[-1]
            download_paper_by_doi(doi)
        else:
            print(f"DOI not found for the given paper title: {paper_title}")

    except requests.exceptions.HTTPError as e:
        print(f"Error searching for paper title: {e}")


def extract_doi_url(html_content):
    # 在HTML内容中提取DOI链接的方法
    # 这里可以根据Sci-Hub网页的HTML结构进行解析，提取相应的链接
    # 由于Sci-Hub可能会更改其网页结构，这个方法可能需要定期更新

    soup = BeautifulSoup(html_content, 'html.parser')
    doi_link = soup.select_one('div#doi > a[href^="https://doi.org/"]')

    if doi_link:
        return doi_link['href']

    return None


def download_paper_by_doi(doi):
    base_url = 'https://sci-hub.se/'
    url = f'{base_url}{doi}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # 提取PDF链接
        pdf_url = extract_pdf_url(response.text)

        if pdf_url:
            # 下载PDF文件
            pdf_response = requests.get(pdf_url)
            pdf_response.raise_for_status()

            # 保存PDF文件
            filename = f'{doi.replace("/", "_")}.pdf'
            with open(filename, 'wb') as f:
                f.write(pdf_response.content)

            print(f'Successfully downloaded the paper: {filename}')
        else:
            print(f"PDF URL not found for the given DOI: {doi}")

    except requests.exceptions.HTTPError as e:
        print(f'Error downloading the paper: {e}')


def extract_pdf_url(html_content):
    # 在HTML内容中提取PDF链接的方法
    # 这里可以根据Sci-Hub网页的HTML结构进行解析，提取相应的链接
    # 由于Sci-Hub可能会更改其网页结构，这个方法可能需要定期更新

    soup = BeautifulSoup(html_content, 'html.parser')
    pdf_link = soup.select_one('div#buttons > ul > li:nth-child(2) > a')

    if pdf_link:
        return pdf_link['href']

    return None


# 例子使用
paper_title = 'A new early branching armored dinosaur from the Lower Jurassic of southwester China'
download_paper_by_title(paper_title)
