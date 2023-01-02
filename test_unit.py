import unittest

from pagination import PageSet, generate_text_pagination, clean_page_sets, pagination_to_string

param_list = [
    ((4, 5, 1, 0), "1 ... 4 5"),
    ((4, 10, 2, 2), '1 2 3 4 5 6 ... 9 10'),
    ((1, 9, 1, 3), '1 2 3 4 ... 9'),
    ((5, 15, 1, 1), '1 ... 4 5 6 ... 15'),
    ((5, 10, 5, 5), '1 2 3 4 5 6 7 8 9 10'),
    ((5, 9999999999999999, 1, 0), '1 ... 5 ... 9999999999999999'),
    ((3, 5, 0, 0), ' ... 3 ... '),
    ((3, 5, 0, 10), '1 2 3 4 5'),
    ((3, 5, 10, 0), '1 2 3 4 5'),
]

pages_zero_or_negative = [
    (0, 0, 1, 1),
    (1, 0, 1, 1),
    (0, 1, 1, 1),
    (-1, 1, 1, 1),
    (1, -1, 1, 1),
]


class TestPagination(unittest.TestCase):

    def test_generate_pagination(self):
        """
        Given: Input parameters

        When: User generates text pagination

        Then: The correct string representation is calculated.
        """
        for input_value, expected_output in param_list:
            with self.subTest():
                self.assertEqual(generate_text_pagination(*input_value), expected_output)

    def test_current_page_greater_than_total_pages_error(self):
        """
        Given: A current_page greater than the total_pages.

        When: User generates text pagination

        Then: It raises an exception
        """
        self.assertRaises(Exception, generate_text_pagination, 9, 8, 1, 3)

    def test_page_is_not_positive(self):
        """
        Given: A current_page greater than the total_pages.

        When: User generates text pagination

        Then: It raises an exception
        """
        for input_values in pages_zero_or_negative:
            with self.subTest():
                self.assertRaises(Exception, generate_text_pagination, *input_values)

    def test_clean_page_sets_with_one_start_gap(self):
        """
        Given: A page set list with a gap between the first and the middle page set.

        When: Cleaning the page sets.

        Then: It will keep the first page set and join the last and the middle page set.
        """
        page_sets = [
            PageSet(start=1, end=2),
            PageSet(start=5, end=7),
            PageSet(start=6, end=9)
        ]
        new_page_sets = clean_page_sets(page_sets)
        self.assertEqual(len(new_page_sets), 2)
        self.assertEqual(new_page_sets[0].start, 1)
        self.assertEqual(new_page_sets[0].end, 2)
        self.assertEqual(new_page_sets[1].start, 5)
        self.assertEqual(new_page_sets[1].end, 9)

    def test_clean_page_sets_with_one_end_gap(self):
        """
        Given: A page set list with a gap between the middle and the last page set.

        When: Cleaning the page sets.

        Then: It will keep the last page set and join the first and the middle page set.
        """
        page_sets = [
            PageSet(start=1, end=5),
            PageSet(start=5, end=7),
            PageSet(start=10, end=13)
        ]
        new_page_sets = clean_page_sets(page_sets)
        self.assertEqual(len(new_page_sets), 2)
        self.assertEqual(new_page_sets[0].start, 1)
        self.assertEqual(new_page_sets[0].end, 7)
        self.assertEqual(new_page_sets[1].start, 10)
        self.assertEqual(new_page_sets[1].end, 13)

    def test_clean_page_sets_with_two_gaps(self):
        """
        Given: A page set list with two gaps.

        When: Cleaning the page sets.

        Then: It will keep the page sets unchanged.
        """
        page_sets = [
            PageSet(start=1, end=3),
            PageSet(start=5, end=7),
            PageSet(start=10, end=13)
        ]
        new_page_sets = clean_page_sets(page_sets)
        self.assertEqual(len(new_page_sets), 3)
        self.assertEqual(new_page_sets[0].start, 1)
        self.assertEqual(new_page_sets[0].end, 3)
        self.assertEqual(new_page_sets[1].start, 5)
        self.assertEqual(new_page_sets[1].end, 7)
        self.assertEqual(new_page_sets[2].start, 10)
        self.assertEqual(new_page_sets[2].end, 13)

    def test_clean_page_sets_with_no_gaps(self):
        """
        Given: A page set list with no gaps.

        When: Cleaning the page sets.

        Then: It will join all the page sets in one resulting page set.
        """
        page_sets = [
            PageSet(start=1, end=3),
            PageSet(start=-1, end=15),
            PageSet(start=10, end=16)
        ]
        new_page_sets = clean_page_sets(page_sets)
        self.assertEqual(len(new_page_sets), 1)
        self.assertEqual(new_page_sets[0].start, 1)
        self.assertEqual(new_page_sets[0].end, 16)


class TestHelpers(unittest.TestCase):

    def test_one_page_set(self):
        """
        Given: One page set.

        When: Converting it to string.

        Then: It returns only numbers split by space.
        """
        page_sets = [
            PageSet(start=1, end=3),
        ]
        pagination_string = pagination_to_string(page_sets)
        self.assertEqual(pagination_string, "1 2 3")

    def test_two_page_sets(self):
        """
        Given: Two page sets.

        When: Converting it to string.

        Then: It returns numbers split by space and page sets split by ellipsis.
        """
        page_sets = [
            PageSet(start=1, end=3),
            PageSet(start=5, end=6),
        ]
        pagination_string = pagination_to_string(page_sets)
        self.assertEqual(pagination_string, "1 2 3 ... 5 6")

    def test_three_page_sets(self):
        """
        Given: Three page sets.

        When: Converting it to string.

        Then: It returns numbers split by space and page sets split by ellipsis.
        """
        page_sets = [
            PageSet(start=1, end=2),
            PageSet(start=4, end=4),
            PageSet(start=6, end=8),
        ]
        pagination_string = pagination_to_string(page_sets)
        self.assertEqual(pagination_string, "1 2 ... 4 ... 6 7 8")
