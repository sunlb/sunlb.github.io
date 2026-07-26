#!/bin/env python
# coding: utf-8

import os, sys
import logging


def is_dir_can_zip(path):
    for postfix in (".zip", ".cbz"):
        path_zip = "%s%s" % (path, postfix)
        if os.path.exists(path_zip):
            return False, "已存在压缩包"

    files = os.listdir(path)
    if not files:
        return False, "空目录"

    for f in files:
        if not (f.endswith(".jpeg") or f.endswith(".png")):
            return False, "仅支持jpeg/png文件压缩"

    return True, "OK"


def zip_dir(root, _dir, _type):
    cmd = 'cd %s; zip -r -0 -q "%s.cbz" "%s"' % (root, _dir, _dir)
    logging.info("ZIP %s, RUN: %s", _dir, cmd)
    # os.system(cmd)


def main(args):
    input_dir, _type = args.input_dir, args.type
    for root, dirs, files in os.walk(input_dir):
        logging.info("WALK %s %s %s", root, dirs, files)
        for _dir in dirs:  # 复制dirs，可能会删除内置项
            ok, message = is_dir_can_zip("%s/%s" % (root, _dir))
            if ok:
                zip_dir(root, _dir, _type)
            else:
                logging.info("IGNORE %s, REASON: %s", _dir, message)
                dirs.remove(_dir)
    return 0


if __name__ == "__main__":
    _format = (
        "%(asctime)s [%(process)d] %(filename)s:%(lineno)s [%(levelname)s]: %(message)s"
    )
    logging.basicConfig(level=logging.INFO, format=_format)

    import argparse

    parser = argparse.ArgumentParser(
        prog="make", formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-t",
        "--type",
        choices=("test", "gen_cbz", "gen_cbz_and_clean"),
        default="test",
        help="执行类型",
    )
    parser.add_argument(
        "-i", "--input-dir", default="/Users/didi/Documents/dev/data", help="输入目录"
    )
    args = parser.parse_args()

    sys.exit(main(args))
