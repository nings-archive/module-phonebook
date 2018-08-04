import re, urllib.parse

import db

def is_code_valid(code: str) -> bool:
    return re.match('^[A-Z]{2,3}\d{4}[A-Z]?$', code) is not None

def is_code_unique(code: str) -> bool:
    return db.get_group(code) is None

def is_url_valid(url: str) -> bool:
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
    return db.get_group_by_url(url) is None
