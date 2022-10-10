import utils.sql


def on_startup():
    print('*START*')
    with utils.sql.database as db:
        db.create_table()
