"""
Holds gen_rss() and Item class for generating rss.
"""
from dataclasses import dataclass
from typing import List, Optional

import feedparser  # type: ignore

from .date import iso_fmt, now_local

# Begin API


@dataclass
class Item:
    """An array of items in a channel for rss feed."""

    title: str
    link: str
    description: str
    date_published: str
    channel_name: str


def gen_rss(  # pylint: disable=too-many-arguments
    items: List[Item],
    feed_title: str,
    feed_link: str,
    feed_description: str,
    language: str = "en-US",
    timezone: str = "US/Eastern",
    categories: Optional[List[str]] = None,
    ignore_errors: bool = False,
) -> str:
    """
    Convert a list of VideoInfo objects to an RSS feed.
    """

    rss_str: str = _header(
        feed_title, feed_link, feed_description, language, timezone
    )
    rss_str += _body(items, categories)
    rss_str += _footer()
    # Remove blank lines
    rss_str = "\n".join([line for line in rss_str.split("\n") if line.strip()])
    if not ignore_errors:
        feed = feedparser.parse(rss_str)
        if feed.bozo:
            raise feed.bozo_exception
    return rss_str


# Future api: def gen_rss_multi_channel(...)


# End API


def _header(
    feed_title: str,
    feed_link: str,
    feed_description: str,
    language: str,
    timezone: str,
) -> str:
    """
    Return the header for an RSS feed.
    """
    now = now_local(tz_str=timezone)
    header = f"""
<?xml version="1.0" encoding="UTF-8"?>
<rss xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#" xmlns:georss="http://www.georss.org/georss" xmlns:slash="http://purl.org/rss/1.0/modules/slash/" xmlns:sy="http://purl.org/rss/1.0/modules/syndication/" xmlns:wfw="http://wellformedweb.org/CommentAPI/" version="2.0">
   <channel>
      <title>{feed_title}</title>
      <atom:link href="{feed_link}" rel="self" type="application/rss+xml" />
      <link>https://blast.video</link>
      <description>{feed_description}</description>
      <lastBuildDate>{iso_fmt(now)}</lastBuildDate>
      <language>{language}</language>
      <sy:updatePeriod>hourly</sy:updatePeriod>
      <sy:updateFrequency>1</sy:updateFrequency>
      <generator>https://wordpress.org/?v=5.9.3</generator>
"""
    return header


def _body(items: List[Item], categories: Optional[List[str]] = None) -> str:
    """
    Return the body of an RSS feed.
    """
    if categories is None:
        categories = ["Politics", "News"]
    out: str = ""
    for item in items:
        out += f"""
      <item>
          <title><![CDATA[{item.title}]]></title>
          <link>{item.link}</link>
          <dc:creator><![CDATA[{item.channel_name}]]></dc:creator>
          <pubDate>{iso_fmt(item.date_published)}</pubDate>"""
        for category in categories:
            out += f"""
          <category><![CDATA[{category}]]></category>"""
        out += f"""
          <description><![CDATA[{item.description}]]></description>
      </item>
      """
    return out


def _footer() -> str:
    """
    Return the footer for an RSS feed.
    """
    return """
   </channel>
</rss>"""
