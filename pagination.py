import dataclasses
from typing import List


@dataclasses.dataclass
class PageSet:
    """
    Page set range.

    This range includes the start, the end and all integers between the two numbers.
    """
    start: int
    end: int


def generate_text_pagination(
    current_page: int,
    total_pages: int,
    boundaries: int,
    around: int
) -> str:
    """
    It uses the input parameters to return the pagination string representation.

    :param current_page: The current page number.
    :param total_pages: The total number of pages.
    :param boundaries: Number of pages we want to link at the beginning or end.
    :param around: Number of pages we want to link before and after the current page, exclusive.
    :return: None (It prints the pagination in the expected string format).
    """
    if current_page > total_pages:
        raise Exception("Current page shouldn't be greater than total page.")
    if any([
        current_page <= 0,
        total_pages <= 0
    ]):
        raise Exception("Pages should be integer numbers.")
    page_sets = generate_pagination(
        current_page, total_pages, boundaries, around
    )
    return pagination_to_string(page_sets)


def generate_pagination(
        current_page: int,
        total_pages: int,
        boundaries: int,
        around: int
) -> List[PageSet]:
    """
    It uses the input parameters to return the pagination ranges as PageSet objects.

    :param current_page: The current page number.
    :param total_pages: The total number of pages.
    :param boundaries: Number of pages we want to link at the beginning or end.
    :param around: Number of pages we want to link before and after the current page, exclusive.
    :return page_sets: List of page set ranges.
    """
    initial_set = PageSet(start=1, end=boundaries)
    current_page_set = PageSet(start=current_page - around, end=current_page + around)
    final_set = PageSet(start=total_pages - boundaries + 1, end=total_pages)
    page_sets = clean_page_sets([initial_set, current_page_set, final_set])
    return page_sets


def clean_page_sets(page_sets: List[PageSet]) -> List[PageSet]:
    """
    Clean overlapping page sets.

    :param page_sets: List of page set ranges.
    :return: Cleaned page sets without overlapping.
    """
    cleaned_page_sets = [page_sets[0]]
    last_index = 0

    # Find limits in the page set
    min_start = page_sets[0].start
    max_end = page_sets[-1].end

    # Clean page sets
    for i in range(1, len(page_sets)):
        if page_sets[i - 1].end >= page_sets[i].start - 1:

            # Keep the last start and update with the new end.
            start = min(cleaned_page_sets[last_index].start, page_sets[i].start)
            end = max(cleaned_page_sets[last_index].end, page_sets[i].end)

            # Update page set with minimum start and maximum end.
            cleaned_page_sets[last_index] = PageSet(
                start=max(min_start, start),
                end=min(max_end, end)
            )
        else:
            # Add a new cleaned page set
            cleaned_page_sets.append(page_sets[i])
            last_index += 1
    return cleaned_page_sets


def pagination_to_string(page_sets: List[PageSet]):
    """
    Convert a list of pagination to the expected string format.

    :param page_sets: List of page set ranges.
    :return: page sets split by ellipsis.
    """
    printed_page_sets = map(
        lambda page_set: " ".join(map(str, list(range(page_set.start, page_set.end + 1)))),
        page_sets
    )
    printed_pagination = " ... ".join(printed_page_sets)
    return printed_pagination.strip()
