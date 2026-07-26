#!/bin/env python
# coding: utf-8
"""生成单本元信息
Q: 如何加入风格和标签支持？
A: 参考 https://github.com/gotson/komga/issues/802

<?xml version="1.0"?>
<ComicInfo xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <Title>demoTitle</Title>
  <Series>demoSeries</Series>
  <Number>1.0</Number>
  <Summary>demoSummary</Summary>
  <Year>2024</Year>
  <Month>6</Month>
  <Day>5</Day>
  <Writer>ditkit</Writer>
  <Publisher>DK</Publisher>
  <LanguageISO>zh</LanguageISO>
  <Web>http://www.baidu.com</Web>
  <Genre>OOO,PPP,ZZZ</Genre>
  <Tags>XX,YY,ZZ</Tags>
</ComicInfo>
"""

import sys, os
import logging

import xml.etree.ElementTree as et
from lxml import etree

FILE_NAME = "ComicInfo.xml"


def download_page(url, html_path):
    from selenium import webdriver

    browser = webdriver.Chrome()
    browser.get("http://www.baidu.com/")
    with open(html_path, "w") as f:
        f.write(browser.page_source)


def prettyprint(element, **kwargs):
    xml = etree.tostring(element, pretty_print=True, **kwargs)
    print(xml.decode(), end="")


def load_comic_info(html_path):
    comic_info = {}
    html = etree.parse(html_path, etree.HTMLParser())
    prettyprint(html)


def write_xml(comic_info, file_path):
    root = et.Element(
        "ComicInfo",
        {
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
        },
    )
    for k in ("Writer", "Publisher", "Summary", "LanguageISO", "Web", "Genre", "Tags"):
        v = comic_info.get(k)
        if v:
            et.SubElement(root, k).text = v
    tree = et.ElementTree(root)
    tree.write(file_path)


def main(args):
    html_path = "test.html"
    #    download_page("http://www.baidu.com", html_path)
    load_comic_info(html_path)
    return 0

    output_dir = args.output_dir
    if not os.path.isdir(output_dir):
        logging.info("%s 不是目录!", output_dir)
        return 1

    comic_info = {
        "Writer": args.writer,
        "Publisher": args.publisher,
        "Summary": args.summary,
        "LanguageISO": "zh",
        "Genre": args.genre,
        "Tags": args.tags,
    }

    file_path = "%s/%s" % (output_dir, FILE_NAME)
    write_xml(comic_info, file_path)
    logging.info("Save %s.", file_path)
    return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        prog="komga_series_meta", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-o", "--output-dir", default=".", help="输出目录")
    parser.add_argument("-w", "--writer", default="xxx", help="发布商")
    parser.add_argument("-p", "--publisher", default="yyy", help="发布商")
    parser.add_argument("-s", "--summary", default="zzz", help="发布商")
    parser.add_argument("-g", "--genre", default="", help="系列名称")
    parser.add_argument("-t", "--tags", default="", help="系列描述")
    args = parser.parse_args()

    _format = (
        "%(asctime)s [%(process)d] %(filename)s:%(lineno)s [%(levelname)s]: %(message)s"
    )
    logging.basicConfig(level=logging.INFO, format=_format)
    sys.exit(main(args))
