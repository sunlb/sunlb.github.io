# coding: utf-8
"""
XPATH: https://www.cnblogs.com/mxjhaima/p/13775844.html
"""

import os, sys
import logging
import collections
import datetime
import xml.etree.ElementTree as et

from lxml import etree


# 处理toptoon
def process_toptoon(url, html):
    infos = collections.defaultdict(list)
    for k, _xpath in (
        ("desc", '//div[@class="desc"]'),
        ("title", '//div[@class="box"]/div[@class="title"]'),
        ("subTitle", '//div[@class="box"]/div[@class="subTitle"]'),
        ("tags", '//div[@class="hashTag"]/a'),
        ("writer", '//div[@class="etc"]/span'),
    ):
        for i in html.xpath(_xpath):
            infos[k].append(i.text)
            # print(k, i.sourceline, i.text)

    def get_summary(infos):
        summary = []
        if len(infos["desc"]) >= 1:
            summary.append(infos["desc"][0])
        summary.append("")
        for title, sub_title in zip(infos["title"], infos["subTitle"]):
            summary.append("%s\t%s" % (title, sub_title))
        return "\n".join(summary)

    comic_info = {
        "Summary": get_summary(infos),
        "Writer": infos["writer"],
        "Publisher": "顶通-TOPTOON",
        "Tags": ",".join(infos["tags"]),
        "Web": url,
        "LanguageISO": "zh",
    }
    return comic_info


# 处理toomics
def process_toomics(url, html):
    # Writer
    _e = html.xpath('//span[@class="writer"]//*')
    writers = [i.text for i in _e]

    # Summary
    _e = html.xpath('//meta[@name="description"]')
    summary = _e[0].get("content")

    comic_info = {
        "Summary": summary,
        "Writer": ",".join(writers),
        "Publisher": "玩漫-TOOMICS",
        "Web": url,
        "LanguageISO": "zh",
    }
    return comic_info


def download_html(url, html_path):
    start = datetime.datetime.now()
    logging.info("download_html: %s ...", url)
    browser = webdriver.Safari()
    browser.get(url)
    with open(html_path, "w") as f:
        f.write(browser.page_source)
    logging.info(
        "donwload_html DONE, save to %s, spend %s.",
        html_path,
        datetime.datetime.now() - start,
    )


def parse_html(url, html_path):
    logging.info("parse_html: %s ...", html_path)
    html = etree.parse(html_path, etree.HTMLParser(encoding="utf-8"))

    comic_info = {}
    for website, func in (
        ("toptoon", process_toptoon),
        ("toomics", process_toomics),
    ):
        if website in url:
            comic_info = func(url, html)
            break

    logging.info("parse_html DONE.")
    return comic_info


def write_xml(comic_info, file_path):
    logging.info("write_xml %s", comic_info)
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
    tree.write(file_path, encoding="utf-8")
    logging.info("write_xml DONE, save to %s.", file_path)


def main(args):
    url, tmp_dir, output_dir, mode = (
        args.input_url,
        args.tmp_dir,
        args.output_dir,
        args.mode,
    )
    for _dir in (tmp_dir, output_dir):
        if not os.path.exists(_dir):
            os.makedirs(_dir)

    html_path = "%s/%s.html" % (
        tmp_dir,
        url.replace(":", "").replace("//", "_").replace(".", "_").replace("/", "_"),
    )
    if mode != "ignore_download":
        download_html(url, html_path)
    comic_info = parse_html(url, html_path)
    if comic_info:
        write_xml(comic_info, "%s/ComicInfo.xml" % output_dir)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        prog="komga_series_meta", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-i",
        "--input-url",
        default="https://toomics.com/sc/webtoon/episode/toon/5809",
        help="输出目录",
    )
    parser.add_argument("-t", "--tmp-dir", default="tmp", help="临时目录")
    parser.add_argument("-o", "--output-dir", default="tmp", help="输出目录")
    parser.add_argument(
        "-m",
        "--mode",
        choices=("default", "ignore_download"),
        default="ignore_download",
        help="执行类型",
    )
    args = parser.parse_args()

    _format = (
        "%(asctime)s [%(process)d] %(filename)s:%(lineno)s [%(levelname)s]: %(message)s"
    )
    logging.basicConfig(level=logging.INFO, format=_format)
    sys.exit(main(args))
