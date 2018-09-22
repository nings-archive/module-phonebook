import re, urllib.parse

import db

def is_code_valid(code: str) -> bool:
    """Returns if the given code is a valid NUS module code"""
    return re.match('^[A-Z]{2,3}\d{4}[A-Z]?$', code) is not None

def is_code_unique(code: str) -> bool:
    """Returns if the given code will be unique when added to the db"""
    return db.get_group(code) is None

def is_url_valid(url: str) -> bool:
    """Returns if the given url is a valid telegram group invite link."""
    fragments = urllib.parse.urlparse(url)
    return (
        fragments.scheme == 'https'
        and fragments.netloc == 't.me'
        and re.match('^/joinchat/[A-z\d]+$', fragments.path) is not None
        and fragments.params == ''
        and fragments.query == ''
        and fragments.fragment == ''
    )

def is_url_unique(url: str) -> bool:
    """Returns if the given url will be unique when added to the db"""
    return db.get_group_by_url(url) is None
