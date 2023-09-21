from PyPDF2 import PdfReader
import re


# 打开PDF文件
pdf_file = "2023.pdf"
pdf = PdfReader(pdf_file)

# 获取PDF文档的元数据信息
metadata = pdf.metadata

# 输出文档信息，注意使用 modification_date 而不是 mod_date
print("Author:", metadata.author)
print("Creator:", metadata.creator)
print("Producer:", metadata.producer)
print("Subject:", metadata.subject)
print("Title:", metadata.title)
print("Creation Date:", metadata.creation_date)
print("Modification Date:", metadata.modification_date)


# 获取PDF文档的所有文本内容
all_text = ""
for page in pdf.pages:
    all_text += page.extract_text()

with open("1.txt", 'w') as f:
    f.write(all_text)


# 编写正则表达式来匹配DOI
doi_pattern = r"10\.\d{4,}/\S+"
doi_matches = re.findall(doi_pattern, all_text)

# 输出匹配到的DOI
if doi_matches:
    for doi in doi_matches:
        print("DOI:", doi)
else:
    print("No DOI found in the document.")
