async def test_database(context):
    await context.db.execute('CREATE TABLE some_table (id INT);')
    await context.db.execute('DROP TABLE some_table;')
