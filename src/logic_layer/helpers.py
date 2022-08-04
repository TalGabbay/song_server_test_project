import re


def look_for_pattern(pattern, response):
    match = re.search(pattern, response)
    print(match)
    return match

