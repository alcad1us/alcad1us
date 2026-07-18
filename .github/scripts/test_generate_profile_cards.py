import unittest
from collections import Counter
from datetime import UTC, datetime
from xml.etree import ElementTree

import generate_profile_cards as cards


PROFILE = {
    "public_repos": 4,
    "followers": 7,
    "created_at": "2022-12-16T00:00:00Z",
}
REPOSITORIES = [
    {"fork": False, "stargazers_count": 3, "forks_count": 1},
    {"fork": False, "stargazers_count": 2, "forks_count": 0},
    {"fork": True, "stargazers_count": 99, "forks_count": 99},
]


class ProfileCardTests(unittest.TestCase):
    def test_language_totals_are_aggregated(self):
        totals = cards.aggregate_languages([{"Python": 20}, {"Python": 5, "C": 10}])
        self.assertEqual(totals, Counter({"Python": 25, "C": 10}))

    def test_account_age_handles_pre_anniversary_date(self):
        now = datetime(2026, 7, 18, tzinfo=UTC)
        self.assertEqual(cards.account_age_years(PROFILE["created_at"], now), 3)

    def test_stats_exclude_fork_stars(self):
        svg = cards.render_stats(PROFILE, REPOSITORIES)
        self.assertIn("TOTAL STARS", svg)
        self.assertIn(">5</text>", svg)
        self.assertNotIn(">104</text>", svg)

    def test_language_card_escapes_names(self):
        svg = cards.render_languages(Counter({"C & C++": 10}))
        self.assertIn("C &amp; C++", svg)

    def test_highlight_card_contains_account_age(self):
        svg = cards.render_highlights(PROFILE, REPOSITORIES)
        self.assertIn("YEARS ON GITHUB", svg)

    def test_all_cards_are_valid_xml(self):
        rendered = (
            cards.render_stats(PROFILE, REPOSITORIES),
            cards.render_languages(Counter({"Python": 20, "C": 10})),
            cards.render_highlights(PROFILE, REPOSITORIES),
        )
        for svg in rendered:
            ElementTree.fromstring(svg)


if __name__ == "__main__":
    unittest.main()
