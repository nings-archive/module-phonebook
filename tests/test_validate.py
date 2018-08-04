import os, os.path, sqlite3, sys
import pytest

sys.path.append(os.path.join(os.getcwd()))
from scripts.migrate import main as migrate
import helpers

sys.path.append(os.path.join(os.getcwd(), 'phonebook'))
import db, validate
from datatypes import User, Group

seeds_module_codes = tuple(helpers.random_module_code() for _ in range(10))
seeds_valid_codes = (
    'GER1000', 'CS1101S', 'UWC2101D', 'CM1401', 'USS2105',
    'LSM2241', 'LSM2232', 'UQF2101I', 'CS1231', 'MA1101R'
)
seeds_invalid_codes = (
    'A123456', '', '1000GER', '999', 'COMPBIO',
    'USS', 'ST2131/MA2216', '7', '0.667', '*'
)
seeds_urls = tuple(helpers.random_url() for _ in range(10))
seeds_invalid_urls = (
    'google.com', 'https://regex101.com', 'localhost', '127.0.0.1',
    '8.8.8.8', 'https://gist.github.com/nifl/1178878', 'example.com',
    'sourceacademy.nus.edu.sg', 'ningyuan.io',
    'https://coursemology.org/courses/1345/'
)

def setup_function(function):
    os.environ['DB_NAME'] = 'test.db'
    migrate()

def teardown_function(function):
    os.remove('test.db')

@pytest.mark.parametrize('code', seeds_module_codes)
def test_is_code_unique_true(code):
    assert validate.is_code_unique(code) is True

@pytest.mark.parametrize('code', seeds_module_codes)
def test_is_code_unique_false(code):
    assert db.insert_group(code, helpers.random_url(), 0, 0)
    assert validate.is_code_unique(code) is False

@pytest.mark.parametrize('code', seeds_valid_codes)
def test_is_code_valid_true(code):
    assert validate.is_code_valid(code) is True

@pytest.mark.parametrize('code', seeds_invalid_codes)
def test_is_code_valid_false(code):
    assert validate.is_code_valid(code) is False

@pytest.mark.parametrize('url', seeds_urls)
def test_is_url_unique_true(url):
    assert validate.is_url_unique(url) is True

@pytest.mark.parametrize('url', seeds_urls)
def test_is_url_unique_false(url):
    assert db.insert_group(helpers.random_module_code(), url, 0, 0)
    assert validate.is_url_unique(url) is False

@pytest.mark.parametrize('url', seeds_urls)
def test_is_url_valid_true(url):
    assert validate.is_url_valid(url) is True

@pytest.mark.parametrize('url', seeds_invalid_urls)
def test_is_url_valid_false(url):
    assert validate.is_url_valid(url) is False
