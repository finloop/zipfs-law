"""This module contains functions for parsing the text of a book into a list of words/letters.
"""
from collections import Counter
import pandas as pd
import re

def split(text: str, words=True) -> list[str]:
    """Split a string into a list of words/letters.
    
    Args:
        text (str): The text to split.
        words (bool, optional): Whether to split into words or letters. Defaults to True.
        
    Returns:
        list[str]: The list of words/letters.
    """
    
    if words:
        return text.split()
    else:
        return list(text)

def clean(text: str) -> str:
    """Clean a string of text by removing all non-letter characters and converting to lowercase.
    
    Args:
        text (str): The text to clean.
        
    Returns:
        str: The cleaned text.
    """
    regex = re.compile(r'[^a-zA-Z\sAaĄąBbCcĆćDdEeĘęFfGgHhIiJjKkLlŁłMmNnŃńOoÓóPpRrSsŚśTtUuWwYyZzŹźŻż]')
    
    return regex.sub('', text).lower()

def count_tokens(tokens: list[str]) -> dict[str, int]:
    """Count the number of times each token appears in a list of tokens.
    
    Args:
        tokens (list[str]): The list of tokens.
        
    Returns:
        dict[str, int]: A dictionary mapping each token to its count.
    """
    counts = Counter(tokens)
    return dict(counts)

def count_to_dataframe(counts: dict[str,int]) -> pd.DataFrame:
    """Convert a dictionary of token counts to a pandas DataFrame."""
    colnames = ['token', 'count']
    df = pd.DataFrame(counts.items(), columns=colnames)
    df = df.sort_values('count', ascending=False)
    df = df.reset_index(drop=True)
    return df