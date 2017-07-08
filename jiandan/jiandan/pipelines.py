# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import re
import urllib
import socket
socket.setdefaulttimeout(0.1)


class ImageDownloadPipeline(object):
    stop_count = 0

    def process_item(self, item, spider):
        if ImageDownloadPipeline.stop_count > 100:
            return item

        if 'image_urls' in item:
            # 指定下载后保存的目录download
            dir_path = '%s/%s' % ("download", spider.name)

            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            for image_url in item['image_urls']:
                file_name = re.findall("[0-9a-z]*.jpg", image_url)
                if len(file_name) != 0:
                    file_name = file_name[0]
                file_path = '%s/%s' % (dir_path, file_name)

                if os.path.exists(file_path):
                    continue

                image_url = "http:" + image_url
                try:
                    urllib.urlretrieve(image_url, file_path)
                except socket.timeout:
                    print('urlretrieve timeout when fetching %s' % image_url)
                except Exception:
                    print('unknown exception')

                print("download %s to %s" % (image_url, file_path))

                ImageDownloadPipeline.stop_count += 1
            return item
