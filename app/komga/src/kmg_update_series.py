#!/bin/env python
# coding: utf-8
"""生成系列元信息
示例：
{
    "version": "1.0.0",
    "metadata": {
        "type": "comicSeries",
        "publisher": "UnkownPublisher",
        "imprint": "",
        "name": "UndefineName",
        "comicid": "1",
        "year": 2024,
        "description_text": "",
        "description_formatted": "Name",
        "volume": 1,
        "booktype": "TPB",
        "age_rating": "All",
        "comic_image": "",
        "total_issues": 999,
        "publication_run": "",
        "status": 0
    }
}
"""

import sys, os
import json
import logging

BOOKTYPE = ("Select", "TPB", "HC", "GN", "Digital", "One-Shot", "Print")
AGE_RATING = ("All", "9+", "12+", "15+", "17+", "Adult")
STATUS = {
    "ENDED": 0,
    "CONTINUING": 1,
}

SERIES_JSON = {
    "version": "1.0.0",
    "metadata": {
        "type": "comicSeries",
        "publisher": "UnkownPublisher",
        "imprint": "",
        "name": "NoName",
        "comicid": "1",
        "year": 2024,
        "description_text": "",
        "description_formatted": "",  # 比description_text优先显示
        "volume": 1,  # 如果>1，则year附加到name后面
        "booktype": "TPB",
        "age_rating": "Adult",
        # "collects": "unused",
        "comic_image": "",
        "total_issues": 999,
        "publication_run": "",
        "status": 0,  # 0-ENDED, 1-CONTINUING
    },
}


def load_file_or_string(description):
    real_description = ""
    if (description.endswith(".txt") or description.endswith(".md")) and os.path.exists(
        description
    ):
        with open(description) as f:
            real_description = f.read()
    else:
        real_description = description.replace("\\n", "\n")
    return real_description


def main(args):
    output_dir = args.output_dir
    with open("%s/series.json" % output_dir, "w") as outfile:
        meta = SERIES_JSON["metadata"]
        meta["publisher"] = args.publisher
        meta["name"] = args.name
        meta["description_formatted"] = load_file_or_string(args.description)
        meta["age_rating"] = args.age_rating
        meta["status"] = STATUS[args.status]
        json.dump(SERIES_JSON, outfile, indent=4, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        prog="komga_series_meta", formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-p", "--publisher", default="", help="发布商")
    parser.add_argument("-n", "--name", default="", help="系列名称")
    parser.add_argument("-y", "--year", default="", help="系列名称")
    parser.add_argument("-v", "--volumn", default="1", help="系列名称")
    parser.add_argument("-d", "--description", default="", help="系列描述")
    parser.add_argument(
        "-a", "--age_rating", choices=AGE_RATING, default="All", help="分级"
    )
    parser.add_argument(
        "-s", "--status", choices=STATUS.keys(), default="CONTINUING", help="连载状态"
    )
    parser.add_argument("output_dir", help="输出目录")
    args = parser.parse_args()

    _format = (
        "%(asctime)s [%(process)d] %(filename)s:%(lineno)s [%(levelname)s]: %(message)s"
    )
    logging.basicConfig(level=logging.INFO, format=_format)
    sys.exit(main(args))
