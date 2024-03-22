import sqlite3


class DB:
    def __init__(self):
        self.con = sqlite3.connect('darkshop.db')
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS products(id integer primary key autoincrement, title varchar("
                         "100), price integer, content text)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS basket(user_id integer ,"
                         "product_id integer, amount integer)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS users(user_id integer, balance integer)")
        self.con.commit()

    def get_all_products(self) -> list:
        res = self.cur.execute("SELECT id, title, price FROM products").fetchall()
        return res

    def create_product(self, title: str, price: int) -> None:
        self.cur.execute(f"INSERT INTO products(title, price) VALUES('{title}', '{price}')")
        self.con.commit()

    def add_user(self, user_id: int) -> None:
        is_user_exists = self.cur.execute(f"SELECT balance FROM users WHERE user_id={user_id}").fetchone()
        if is_user_exists:
            self.cur.execute(f"UPDATE users SET balance=15000 WHERE user_id={user_id}")
        else:
            self.cur.execute(f"INSERT INTO users(user_id, balance) VALUES ({user_id}, 15000)")
        self.con.commit()

    def get_product_info(self, title):
        return self.cur.execute(f"SELECT title, price FROM products WHERE title='{title}'").fetchone()

    def make_message(self, title):
        res = self.get_product_info(title)
        msg = ''
        if not res:
            return 'br0, w3 607 0nly 600d pr0duc7...'
        msg += f'T1tl3 - {res[0]}\npr1c3 - {res[1]}$'
        return msg

    def buy_product(self, user_id, title):
        product_price, product_content = self.cur.execute(f"SELECT price, content FROM products WHERE title = '{title}'").fetchone()
        user_balance = self.cur.execute(f"SELECT balance FROM users WHERE user_id = {user_id} ").fetchone()[0]
        if user_balance >= product_price:
            self.cur.execute(f"UPDATE users SET balance={user_balance - product_price} WHERE user_id={user_id}")
            self.con.commit()
            return f'5ucc355ful purch453\nB4l4nc3 - {user_balance - product_price}$\n\n{product_content}'
        return f'1n5uff1c13n7 fund5 🤡'

    def get_balance(self, user_id: int):
        return "br0, y0u'r3 br0k3 - " + \
               str(self.cur.execute(f"SELECT balance FROM users WHERE user_id={user_id}").fetchone()[0]) + '$'
