from pagination import generate_text_pagination


if __name__ == '__main__':
    current_page = int(input("Insert the current_page value: "))
    total_pages = int(input("Insert the total_pages value: "))
    boundaries = int(input("Insert the boundaries value: "))
    around = int(input("Insert the around value: "))
    print(generate_text_pagination(current_page, total_pages, boundaries, around))
