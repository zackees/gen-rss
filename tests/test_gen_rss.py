"""Tests the gen_rss module."""

import unittest
from typing import List

import feedparser  # type: ignore
from gen_rss import Item, gen_rss


class RssTester(unittest.TestCase):
    """Tester for the Rss generator."""

    def test_video_list_to_rss(self):  # pylint: disable=no-self-use
        """Tests that the rss generator works with custom data that can be parsed by feedparser."""
        datetime_iso = "2020-01-01T00:00:00+00:00"
        items: List[Item] = [
            Item(
                title="test_title",
                link="test_link",
                description="test_description",
                date_published=datetime_iso,
                channel_name="test_channel_name",
            ),
        ]
        rss_str = gen_rss(
            items=items,
            feed_title="Test Feed",
            feed_link="https://blast.video/whatever/rss",
            feed_description="feed description",
        )
        print(rss_str)
        feed = feedparser.parse(rss_str)
        self.assertEqual(len(feed.entries), 1)
        item = feed.entries[0]
        self.assertEqual(item.title, "test_title")
        self.assertEqual(item.link, "test_link")
        self.assertEqual(item.description, "test_description")
        self.assertEqual(item.published, datetime_iso)
        self.assertEqual(item.author, "test_channel_name")


if __name__ == "__main__":
    unittest.main()
