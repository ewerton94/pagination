import unittest

from pagination import PageSet, generate_text_pagination, clean_page_sets, pagination_to_string

param_list = [
    ((4, 5, 1, 0), "1 ... 4 5"),
    ((4, 10, 2, 2), '1 2 3 4 5 6 ... 9 10'),
    ((1, 9, 1, 3), '1 2 3 4 ... 9'),
    ((5, 15, 1, 1), '1 ... 4 5 6 ... 15'),
    ((5, 10, 5, 5), '1 2 3 4 5 6 7 8 9 10'),
    ((5, 9999999999999999, 1, 0), '1 ... 5 ... 9999999999999999'),
    ((3, 5, 0, 0), '... 3 ...'),
    ((3, 5, 0, 10), '1 2 3 4 5'),
    ((3, 5, 10, 0), '1 2 3 4 5'),
    ((1, 10, 3, 1), '1 2 3 ... 8 9 10'),
    ((10, 10, 4, 1), '1 2 3 4 ... 7 8 9 10'),
    ((2, 10, 0, 1), '1 2 3 ...'),
    ((2, 10, 0, 3), '1 2 3 4 5 ...'),
    ((9, 10, 0, 1), '... 8 9 10'),
    ((1, 10, 0, 15), '1 2 3 4 5 6 7 8 9 10'),
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


class TestCleanPageSets(unittest.TestCase):

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
        expected_page_sets = [
            PageSet(start=1, end=2),
            PageSet(start=5, end=9)
        ]
        new_page_sets = clean_page_sets(page_sets)
        self.assertEqual(new_page_sets, expected_page_sets)

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
        expected_page_sets = [
            PageSet(start=1, end=7),
            PageSet(start=10, end=13)
        ]
        new_page_sets = clean_page_sets(page_sets)
        self.assertEqual(new_page_sets, expected_page_sets)

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
        expected_page_sets = [
            PageSet(start=1, end=3),
            PageSet(start=5, end=7),
            PageSet(start=10, end=13)
        ]
        new_page_sets = clean_page_sets(page_sets)
        self.assertEqual(new_page_sets, expected_page_sets)

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
        expected_page_sets = [
            PageSet(start=1, end=16),
        ]
        new_page_sets = clean_page_sets(page_sets)
        self.assertEqual(new_page_sets, expected_page_sets)

    def test_clean_page_sets_boundaries_greater_than_around_and_current_page_at_start(self):
        """
        Given: A page set list with boundaries greater than around and current page at start.

        When: Cleaning the page sets.

        Then: it should consider the boundaries number.
        """
        page_sets = [
            # current_page = 1; total_pages = 10
            PageSet(start=1, end=3),  # boundaries = 3
            PageSet(start=0, end=2),  # around = 1
            PageSet(start=8, end=10)  # boundaries = 3
        ]
        expected_page_sets = [
            PageSet(start=1, end=3),
            PageSet(start=8, end=10),
        ]
        new_page_sets = clean_page_sets(page_sets)
        self.assertEqual(new_page_sets, expected_page_sets)

    def test_clean_page_sets_boundaries_greater_than_around_and_current_page_at_end(self):
        """
        Given: A page set list with boundaries greater than around and current page at end.

        When: Cleaning the page sets.

        Then: it should consider the boundaries number.
        """
        page_sets = [
            # current_page = 10; total_pages = 10
            PageSet(start=1, end=3),  # boundaries = 3
            PageSet(start=9, end=11),  # around = 1
            PageSet(start=8, end=10)  # boundaries = 3
        ]
        expected_page_sets = [
            PageSet(start=1, end=3),
            PageSet(start=8, end=10),
        ]
        new_page_sets = clean_page_sets(page_sets)
        self.assertEqual(new_page_sets, expected_page_sets)

    def test_clean_page_sets_boundaries_smaller_than_around_and_current_page_at_start(self):
        """
        Given: A page set list with boundaries smaller than around and current page at start.

        When: Cleaning the page sets.

        Then: it should keep the maximum number of pages, starting at page 1.
        """
        page_sets = [
            # current_page = 1; total_pages = 10
            PageSet(start=1, end=1),  # boundaries = 1
            PageSet(start=-2, end=4),  # around = 3
            PageSet(start=10, end=10)  # boundaries = 1
        ]
        expected_page_sets = [
            PageSet(start=1, end=4),
            PageSet(start=10, end=10),
        ]
        new_page_sets = clean_page_sets(page_sets)
        self.assertEqual(new_page_sets, expected_page_sets)

    def test_clean_page_sets_boundaries_smaller_than_around_and_current_page_at_end(self):
        """
        Given: A page set list with boundaries smaller than around and current page at end.

        When: Cleaning the page sets.

        Then: it should keep the maximum number of pages, ending at page 10.
        """
        page_sets = [
            # current_page = 10; total_pages = 10
            PageSet(start=1, end=1),  # boundaries = 1
            PageSet(start=7, end=13),  # around = 3
            PageSet(start=10, end=10)  # boundaries = 3
        ]
        expected_page_sets = [
            PageSet(start=1, end=1),
            PageSet(start=7, end=10),
        ]
        new_page_sets = clean_page_sets(page_sets)
        self.assertEqual(new_page_sets, expected_page_sets)


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

    def test_show_only_first_pages(self):
        """
        Given: One page set with first pages and another without values to show.

        When: Converting it to string.

        Then: It returns the first pages and ends with ...
        """
        page_sets = [
            PageSet(start=1, end=3),
            PageSet(start=4, end=3),
        ]
        pagination_string = pagination_to_string(page_sets)
        self.assertEqual(pagination_string, "1 2 3 ...")

    def test_show_only_last_pages(self):
        """
        Given: One page set without values to show and another with last pages.

        When: Converting it to string.

        Then: It starts with ... and returns the last pages.
        """
        page_sets = [
            PageSet(start=1, end=0),
            PageSet(start=3, end=4),

        ]
        pagination_string = pagination_to_string(page_sets)
        self.assertEqual(pagination_string, "... 3 4")

    def test_show_only_middle_pages(self):
        """
        Given: Two page sets without values to show and another with the middle pages.

        When: Converting it to string.

        Then: It starts with ..., returns the middle pages and ends with ...
        """
        page_sets = [
            PageSet(start=1, end=0),
            PageSet(start=3, end=4),
            PageSet(start=6, end=5),

        ]
        pagination_string = pagination_to_string(page_sets)
        self.assertEqual(pagination_string, "... 3 4 ...")

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
