import yomu


SERIES = yomu.get_series_posts()


def test_get_series_posts():
    assert len(SERIES) > 0


def test_youtube_video():
    # https://therenegadecoder.com/code/how-to-invert-a-dictionary-in-python/
    assert not yomu.get_youtube_video(SERIES[-1]).is_text()


def test_get_challenge():
    # https://therenegadecoder.com/code/how-to-invert-a-dictionary-in-python/
    assert yomu.get_challenge(SERIES[-1].title).is_text()


def test_get_notebook():
    # https://therenegadecoder.com/code/how-to-invert-a-dictionary-in-python/
    assert yomu.get_notebook(SERIES[-1].title).is_text()


def test_get_test():
    # https://therenegadecoder.com/code/how-to-invert-a-dictionary-in-python/
    assert yomu.get_test(SERIES[-1].title).is_text()
