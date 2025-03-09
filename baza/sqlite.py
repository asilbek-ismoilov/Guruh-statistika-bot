import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS USERS(
        full_name TEXT,
        telegram_id NUMBER unique);
              """
        self.execute(sql, commit=True)

    def create_table_group_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS GROUPS(
            full_name TEXT,
            telegram_id INTEGER,
            add_id INTEGER DEFAULT 0,
            group_id INTEGER,
            UNIQUE(telegram_id, group_id)
        );
        """
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())


    def add_user(self, telegram_id:int, full_name:str):

        sql = """
        INSERT INTO Users(telegram_id, full_name) VALUES(?, ?);
        """
        self.execute(sql, parameters=(telegram_id, full_name), commit=True)

    def add_group_user(self, telegram_id: int, full_name: str, add_id: int, group_id: int):
        sql = """
        INSERT OR IGNORE INTO GROUPS(telegram_id, full_name, add_id, group_id) VALUES(?, ?, ?, ?);
        """
        self.execute(sql, (telegram_id, full_name, add_id, group_id), commit=True)

    def get_user_by_id(self, telegram_id: int, group_id: int):
        sql = "SELECT * FROM GROUPS WHERE telegram_id = ? AND group_id = ?;"
        return self.execute(sql, (telegram_id, group_id), fetchone=True)
    
    def get_added_count(self, adder_id: int, group_id: int):
        sql = "SELECT COUNT(*) FROM GROUPS WHERE add_id = ? AND group_id = ?;"
        result = self.execute(sql, (adder_id, group_id), fetchone=True)
        return result[0] if result else 0
    
    def delete_group_user(self, telegram_id: int, group_id: int):
        sql = "DELETE FROM GROUPS WHERE telegram_id = ? AND group_id = ?;"
        self.execute(sql, (telegram_id, group_id), commit=True)
    
    def select_all_users(self):
        sql = """
        SELECT * FROM Users;
        """
        return self.execute(sql, fetchall=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def all_users_id(self):
        return self.execute("SELECT telegram_id FROM Users;", fetchall=True)
        
    def all_added_count(self, group_id: int):

        # Avval guruhdagi barcha foydalanuvchilarni olamiz
        sql_users = """
        SELECT telegram_id, full_name 
        FROM GROUPS 
        WHERE group_id = ? 
        GROUP BY telegram_id, full_name;
        """
        users = self.execute(sql_users, (group_id,), fetchall=True)

        # Har bir foydalanuvchi uchun qo'shgan odamlar sonini hisoblaymiz
        result = []
        for user in users:
            telegram_id, full_name = user
            sql_count = """
            SELECT COUNT(*) 
            FROM GROUPS 
            WHERE add_id = ? AND group_id = ?;
            """
            invite_count = self.execute(sql_count, (telegram_id, group_id), fetchone=True)[0] or 0
            result.append((telegram_id, full_name, invite_count))

        # Natijani invite_count bo'yicha kamayib borish tartibida saralaymiz
        result.sort(key=lambda x: x[2], reverse=True)
        return result
    
    def top_added_count(self, group_id: int):
        """
        Eng ko‘p odam qo‘shgan 10 ta foydalanuvchini to‘g‘ridan-to‘g‘ri SQL so‘rovi bilan qaytaradi.
        """
        sql = """
        SELECT 
            g.telegram_id, 
            g.full_name, 
            COUNT(inv.add_id) AS invite_count
        FROM GROUPS g
        LEFT JOIN (
            SELECT add_id
            FROM GROUPS
            WHERE group_id = ? AND add_id <> 0
        ) inv ON g.telegram_id = inv.add_id
        WHERE g.group_id = ?
        GROUP BY g.telegram_id, g.full_name
        ORDER BY invite_count DESC
        LIMIT 10;
        """
        return self.execute(sql, (group_id, group_id), fetchall=True)
        
def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")