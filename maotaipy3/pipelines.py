# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import maotaipy3.deal_raw as deal_raw
import os


class Maotaipy3Pipeline(object):
    def process_item(self, item, spider):
        now = datetime.datetime.now()
        today = "%s" % datetime.date.today()
        today = today.replace('-', '')
        hour = "%02d" % now.hour

        minute = "%02d" % now.minute
        second = "%02d" % now.second
        second = "%s" % second
        pwd = os.getcwd()
        fileName = pwd + "/" +today + "_" + hour + "_" + minute + "_" + second + "_" + 'test.txt'
        with open(fileName, 'wb+') as fp:
            # fp.write(item['txt'][1].encode('utf8'))
            # fp.write(item['txt'][0].encode('utf8'))
            fp.write(item['txt'][1].encode('utf-8'))
            fp.close
        if os.path.exists(fileName):
            deal_raw.make_result(fileName)
            os.remove(fileName)
            print(fileName)
        else:
            # print("no file!")
            pass
        return item
