import re


def extract_string(string: str, s: str, e: str):
    return string.partition(s)[2].partition(e)[0]
