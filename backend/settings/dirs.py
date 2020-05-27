import pathlib

PROJECT_DIR = pathlib.Path(__file__).parents[2]  # is 2 level deep
MEDIA_DIR = PROJECT_DIR / "media"
SETTINGS_DIR = PROJECT_DIR / "settings"
SQL_DATABASE = PROJECT_DIR / "db.sqlite"
SQL_TEST_DATABASE = PROJECT_DIR / "test_db.sqlite"
