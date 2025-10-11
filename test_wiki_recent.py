import unittest
from wiki_recent import get_recent_changes

class TestWikiRecent(unittest.TestCase):

    def test_valid_article(self):
        """Check that a known article returns a query key."""
        data = get_recent_changes("Ball State University")
        self.assertIn("query", data)

    def test_invalid_article(self):
        """Check that a fake article still returns query with pages info."""
        data = get_recent_changes("ThisArticleDoesNotExist123456")
        self.assertIn("query", data)

    def test_redirect_article(self):
        """Check that redirects (like BSU) still return valid data."""
        data = get_recent_changes("BSU")
        self.assertIn("query", data)

unittest.main()
