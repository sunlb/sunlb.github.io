#!/bin/env python3
# coding: utf-8

import os, sys
import logging
import shutil
import re


def move_file(src_file, dst_dir, mode):
    logging.info("%s: '%s' -> '%s'", mode, src_file, dst_dir)
    if mode == "run":
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        shutil.move(src_file, dst_dir)


def main(args):
    input_dir, output_dir, _format = args.input_dir, args.output_dir, args.format
    for _dir in (input_dir, output_dir):
        if not os.path.exists(_dir):
            logging.info("NOT EXISTS %s", _dir)
            return 1

    for sub_dir in sorted(os.listdir(input_dir)):
        sub_dir_path = "%s/%s" % (input_dir, sub_dir)
        if not os.path.isdir(sub_dir_path):
            logging.info("IGNORE %s", sub_dir_path)
            continue
        split_by = "_"
        re_string = (
            r"^\d+%s.*\.(jpg|jpeg)$" % split_by
        )  # 匹配格式：数字序号_XX.jpg或jpeg
        for f in sorted(os.listdir(sub_dir_path)):
            if re.match(re_string, f, re.IGNORECASE):  # 不区分大小写
                index_ = f.index(split_by)
                prefix_index = (int(f[:index_]) - 1) // 10
                src_file = "%s/%s" % (sub_dir_path, f)
                dst_dir_name = _format % (prefix_index, prefix_index + 1)
                dst_dir = "%s/%s" % (output_dir, dst_dir_name)
                move_file(src_file, dst_dir, args.mode)

    return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        prog="kmg_split_dir", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-m", "--mode", choices=("test", "run"), default="test", help="执行类型"
    )
    parser.add_argument("-f", "--format", default="%02d1-%02d0", help="分目录格式")
    parser.add_argument(
        "-i",
        "--input-dir",
        default="tmp",
        help="输入目录，默认待整理图片位于该目录的子目录，暂不支持递归",
    )
    parser.add_argument("-o", "--output-dir", default=".", help="输出目录")
    args = parser.parse_args()

    _format = (
        "%(asctime)s [%(process)d] %(filename)s:%(lineno)s [%(levelname)s]: %(message)s"
    )
    logging.basicConfig(level=logging.INFO, format=_format)
    sys.exit(main(args))
