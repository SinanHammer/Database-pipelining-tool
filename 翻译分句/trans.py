import re
import requests
import random
import json
from hashlib import md5
from nltk import sent_tokenize


class BaiduTranslator:
    def __init__(self, appid, appkey):
        self.appid = appid
        self.appkey = appkey
        self.endpoint = 'http://api.fanyi.baidu.com'
        self.path = '/api/trans/vip/translate'
        self.url = self.endpoint + self.path

    def translate(self, query, from_lang, to_lang):
        salt = random.randint(32768, 65536)
        sign = self.make_md5(self.appid + query + str(salt) + self.appkey)

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {
            'appid': self.appid,
            'q': query,
            'from': from_lang,
            'to': to_lang,
            'salt': salt,
            'sign': sign
        }

        r = requests.post(self.url, params=payload, headers=headers)
        result = r.json()
        return result

    def make_md5(self, s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    def split_sentences(self, text):
        sentences = re.split(r'[.;]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences

    def translate_text(self, text, from_lang, to_lang):
        sentences = self.split_sentences(text)
        translations = []
        for i, sentence in enumerate(sentences):
            result = self.translate(sentence, from_lang, to_lang)
            print(result)
            translations.append(result)
            print(f"原句{i+1}：{sentence}")
            print(f"翻译结果{i+1}：{result['trans_result'][0]['dst']}")


        return translations

    def translate_file(self, filename, from_lang, to_lang):
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()

        return self.translate_text(text, from_lang, to_lang)


# 示例用法
appid = '20230610001707561'
appkey = 'ytNd96IV5s3_FgA_r0ln'
translator = BaiduTranslator(appid, appkey)

filename = '1.txt'
from_lang = 'en'
to_lang = 'zh'

translations = translator.translate_file(filename, from_lang, to_lang)
