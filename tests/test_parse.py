from zipfs_law.parse import split, clean, count_tokens, histogram

def test_split():
    """Test the split function."""
    text = 'This is a test.'
    assert split(text, words=True) == ['This', 'is', 'a', 'test.']
    assert split(text, words=False) == ['T', 'h', 'i', 's', ' ', 'i', 's', ' ', 'a', ' ', 't', 'e', 's', 't', '.']
    
def test_clean():
    """Test the clean function."""
    text = 'This is a test.'
    assert clean(text) == 'this is a test'
    
def test_count_tokens():
    """Test the count_tokens function."""
    tokens = ['this', 'is', 'a', 'test', 'this', 'is', 'another', 'test']
    assert count_tokens(tokens) == {'this': 2, 'is': 2, 'a': 1, 'test': 2, 'another': 1}
    
def test_histogram():
    """Test the histogram function"""
    counts = {'this': 2, 'is': 2, 'a': 1, 'test': 2, 'another': 1}
    df = histogram(counts)
    assert df.shape == (5, 2)
    assert df['token'].tolist() == ['this', 'is', 'test', 'a', 'another']
    assert df['count'].tolist() == [2, 2, 2, 1, 1]
