import os, os.path, random, sqlite3, sys
import pytest

sys.path.append(os.getcwd())
from scripts.migrate import main as migrate
import helpers

sys.path.append(os.path.join(os.getcwd(), 'phonebook'))
import db
from datatypes import User, Group

seeds_user_ids = tuple(helpers.random_user_id() for _ in range(10))
seeds_module_codes = tuple(helpers.random_module_code() for _ in range(10))
seeds_user_rows = tuple(helpers.random_user_row() for _ in range(10))
seeds_group_rows = tuple(helpers.random_group_row() for _ in range(10))
seeds_group_rows_sets = tuple(helpers.random_group_rows() for _ in range(10))
seeds_stat_rows = tuple(helpers.random_stats() for _ in range(10))

def setup_function(function):
    os.environ['DB_NAME'] = 'test.db'
    migrate()

def teardown_function(function):
    os.remove('test.db')

@pytest.mark.parametrize('_id', seeds_user_ids)
def test_insert_user(_id):
    assert db.insert_user(_id) == True

@pytest.mark.parametrize('_id', seeds_user_ids)
def test_insert_user_not_unique(_id):
    assert db.insert_user(_id) == True
    assert db.insert_user(_id) is None

@pytest.mark.parametrize('code', seeds_module_codes)
def test_insert_group(code):
    assert db.insert_group(code, code, 0, 0) == True

@pytest.mark.parametrize('code', seeds_module_codes)
def test_insert_group_code_not_unique(code):
    assert db.insert_group(code, code, 0, 0) == True
    assert db.insert_group(code, code, 0, 0) is None

@pytest.mark.parametrize('user_row', seeds_user_rows)
def test_get_user(user_row):
    assert db.insert_user(*user_row) == True
    user = db.get_user(user_row[0])
    assert user is not None
    assert user == User(*user_row)

@pytest.mark.parametrize('user_row', seeds_user_rows)
def test_get_user_not_exists(user_row):
    assert db.get_user(user_row[0]) is None

@pytest.mark.parametrize('group_row', seeds_group_rows)
def test_get_group(group_row):
    assert db.insert_group(*group_row) == True
    group = db.get_group(group_row[0])
    assert group is not None
    assert group == Group(*group_row)

@pytest.mark.parametrize('group_row', seeds_group_rows)
def test_get_group_not_exists(group_row):
    assert db.get_group(group_row[0]) is None

@pytest.mark.parametrize('group_rows', seeds_group_rows_sets)
def test_get_all_groups(group_rows):
    for row in group_rows:
        assert db.insert_group(*row) == True
    groups = db.get_all_groups()
    assert len(groups) == len(group_rows)
    for row in group_rows:
        assert Group(*row) in groups

@pytest.mark.parametrize('stat_row', seeds_stat_rows)
def test_insert_stat(stat_row):
    assert db.insert_stat(*stat_row) == True

@pytest.mark.parametrize('user_row', seeds_user_rows)
def test_update_user_state(user_row):
    new_state = random.randint(0, 999)
    assert db.insert_user(*user_row) == True
    assert db.update_user_state(user_row[0], new_state) == True
    assert db.get_user(user_row[0]).state == new_state

@pytest.mark.parametrize('user_row', seeds_user_rows)
def test_update_user_state_not_exist(user_row):
    new_state = random.randint(0, 999)
    assert db.update_user_state(user_row[0], new_state) is None

@pytest.mark.parametrize('user_row', seeds_user_rows)
def test_update_user_saved_state(user_row):
    new_saved_state = helpers.random_module_code()
    assert db.insert_user(*user_row) == True
    assert db.update_user_saved_state(user_row[0], new_saved_state) == True
    assert db.get_user(user_row[0]).saved_state == new_saved_state

@pytest.mark.parametrize('user_row', seeds_user_rows)
def test_update_user_saved_state_not_exist(user_row):
    new_saved_state = helpers.random_module_code()
    assert db.update_user_saved_state(user_row[0], new_saved_state) is None

