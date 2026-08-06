import os


def generate_header() -> str:
    term_width = os.get_terminal_size().columns

    if term_width < 60:
        width = term_width
    elif term_width < 120:
        width = term_width // 2
    else:
        width = term_width // 3

    width = max(width, 48)
    inner = width - 2

    lines = [
        "-~*=*~" * int(width / 5.8),
        f"|{'PROSTY  Auto clicker'.center(inner)}|",
        f"\\{'w Pythonie'.center(inner)}/",
        f"/{' ' * inner}\\",
        f"|{'- zrobił Bartosz Zakrzewski'.center(inner)}|",
        f"\\{'<https://github.com/BartekDeveloper>'.center(inner)}/",
        "-~*=*~" * int(width / 5.8),
    ]

    return "\n".join(lines)
