# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests
import os
import re


class ImageDownloadPipeline(object):
    stop_count = 0

    def process_item(self, item, spider):
        if ImageDownloadPipeline.stop_count > 100:
            return item
        if 'image_urls' in item:
            images = []
            dir_path = '%s/%s' % ("download", spider.name)
            request_data = {'allow_redirects': False,
                            'auth': None,
                            'cert': None,
                            'data': {},
                            'files': {},
                            'headers': {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'},
                            'method': 'get',
                            'params': {},
                            'proxies': {},
                            'stream': True,
                            'timeout': 30,
                            'url': '',
                            'verify': True}

            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            for image_url in item['image_urls']:
                request_data['url'] = "http:" + image_url
                file_name = re.findall("[0-9a-z]*.jpg", image_url)[0]
                file_path = '%s/%s' % (dir_path, file_name)
                images.append(file_path)
                if os.path.exists(file_path):
                    continue
                with open(file_path, 'wb') as handle:
                    response = requests.request(**request_data)
                    for block in response.iter_content(1024):
                        if not block:
                            break
                        handle.write(block)
                print("download %s to %s" % (image_url, file_path))
                ImageDownloadPipeline.stop_count += 1
            item['images'] = images
            return item
