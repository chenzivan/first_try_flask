from faker import Faker
import sqlite3
fake = Faker()


res = ""

conn = sqlite3.connect("data-dev.sqlite")
c = conn.cursor()


for i in range(2, 500):
    res = 'insert into posts(body, author_id) values' + '("%s", %d)' % (fake.text(), i % 2 + 1)
    c.execute(res)

conn.commit()
conn.close()
