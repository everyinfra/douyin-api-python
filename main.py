"""Douyin API in Python: search Douyin (China's TikTok) videos, then pull a video's comments.

  python main.py search 咖啡 --out videos.csv
  python main.py comments https://www.douyin.com/video/<id> --out comments.csv
"""
import argparse

from everyinfra import call, report


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search", help="videos for a keyword (Chinese keywords work best)")
    s.add_argument("keyword")
    c = sub.add_parser("comments", help="comments of one video")
    c.add_argument("url", help="video URL")
    for x in (s, c):
        x.add_argument("--out", help="write .csv or .json")
    a = p.parse_args()

    if a.cmd == "search":
        data = call("douyin", "search", {"keyword": a.keyword})
    else:
        data = call("douyin", "comments", {"url": a.url})
    report(data, a.out)


if __name__ == "__main__":
    main()
