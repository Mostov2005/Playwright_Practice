def test_browser_is_available(page):
    assert page is not None
    assert page.url == "about:blank"
