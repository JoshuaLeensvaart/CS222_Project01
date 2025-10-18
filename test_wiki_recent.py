import unittest
from wiki_recent import get_wikipedia_data 


class TestWikiRecent(unittest.TestCase):

    def test_valid_article(self):
        """Check that a real article returns valid query data."""
        data = get_wikipedia_data("Ball State University")
        self.assertIn("query", data)

    def test_redirect_article(self):
        """Check that a redirect still returns valid data."""
        data = get_wikipedia_data("USA")
        self.assertIn("query", data)

    def test_invalid_article(self):
        """Check that a fake article still returns a query object."""
        data = get_wikipedia_data("ThisArticleDoesNotExist123456")
        self.assertIn("query", data)

unittest.main()

