# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd


class StoreInfoPipeline(object):
    def process_item(self, item, spider):
        return item


class XlsxWriterPipeline:
    def __init__(self):
        self.df = None
        self.output_filename = None

    def open_spider(self, spider):
        self.output_filename = "results/%s.xlsx" % spider.name

    def close_spider(self, spider):
        if spider.name == "maac":
            if self.df[self.df.url_2.notna()].isnull:
                self.df = self.df.drop("url_2", 1)
            self.df.to_excel(self.output_filename, index=False, sheet_name='MAAC Clubs', freeze_panes=(1, 0))
        else:
            self.df.to_excel(self.output_filename, index=False, freeze_panes=(1, 0))

    def process_item(self, item, spider):
        if type(item) != dict:
            item_dict = vars(item)['_values']
        else:
            item_dict = item

        if self.df is None:
            self.df = pd.DataFrame([item_dict], columns=item_dict.keys())
        self.df = self.df.append(item_dict, ignore_index=True)

        return item