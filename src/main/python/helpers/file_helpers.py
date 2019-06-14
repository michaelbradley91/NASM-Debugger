"""
This module contains functions to help manage files.
"""
import codecs
import string


def read_file_text(path: str) -> str:
    """
    Read the text portion of a file. This will ignore characters it cannot decode
    and characters that cannot be printed.
    :param path: the path to the file to read.
    :return: the text context.
    """
    with codecs.open(path, 'r', encoding='utf-8', errors='ignore') as file:
        text = file.read()

    return str.join("", (c for c in text if c in string.printable))