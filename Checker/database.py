import sqlite3

DATABASE = 'database.db'


def create_database():
    # Connect to the database
    conn = sqlite3.connect(DATABASE)
    # Create a cursor
    c = conn.cursor()
    # Create a table
    c.execute("""CREATE TABLE IF NOT EXISTS accounts (
        steam_id text PRIMARY KEY,
        steam_name text,
        game_bans text,
        num_game_bans text,
        steam_vac text,
        num_vac_bans text,
        discord_id text
    )""")
    # commit our command
    conn.commit()
    # close our connection
    conn.close()


# add a steam account to the database
def add_account(steam_id, steam_name, game_bans, num_game_bans, steam_vac, num_vac_bans, discord_id):

    if check_account(steam_id):
        update_status(steam_id, steam_name, game_bans, num_game_bans, steam_vac, num_vac_bans, discord_id)
    else:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?, ?)", (steam_id, steam_name, game_bans, num_game_bans,
                                                                        steam_vac, num_vac_bans, discord_id))
        conn.commit()
        conn.close()


# Check if steam account is in the database
def check_account(steam_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT steam_id FROM accounts WHERE steam_id=?", (steam_id,))
    row = c.fetchone()
    conn.close()

    if row:
        return True
    else:
        return False


# Get all steam_id from database
def get_accounts():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT steam_id FROM accounts")
    rows = c.fetchall()
    conn.close()

    if rows:
        return [i[0] for i in rows]
    else:
        return None


# Update the status of a steam account
def update_status(steam_id, steam_name, game_bans, num_game_bans, steam_vac, num_vac_bans, discord_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("UPDATE accounts SET steam_name=?, game_bans=?, num_game_bans=?, steam_vac=?, num_vac_bans=?, discord_id=?"
              "WHERE steam_id=?", (steam_name, game_bans, num_game_bans, steam_vac, num_vac_bans, discord_id, steam_id))
    conn.commit()
    conn.close()


# remove a steam account from the database
def remove_account(steam_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM accounts WHERE steam_id=?", (steam_id,))
    conn.commit()
    conn.close()


def get_steamid(steam_name):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT steam_id FROM users WHERE steam_name=?", (steam_name,))
    row = c.fetchone()
    conn.close()

    if row:
        return row[0]
    else:
        return None


def get_vac_status(steam_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT steam_vac FROM users WHERE steam_id=?", (steam_id,))
    row = c.fetchone()
    conn.close()

    if row:
        return row[0]
    else:
        return None


def get_game_bans(steam_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT game_bans FROM users WHERE steam_id=?", (steam_id,))
    row = c.fetchone()
    conn.close()

    if row:
        return row[0]
    else:
        return None


# Get all steam_id for every discord_id
def get_steamid_from_discord(discord_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT steam_id FROM accounts WHERE discord_id=?", (discord_id,))
    rows = c.fetchall()
    conn.close()

    if rows:
        return [i[0] for i in rows]
    else:
        return None


# Get discord_id from steam_id
def get_discord_id(steam_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT discord_id FROM accounts WHERE steam_id=?", (steam_id,))
    row = c.fetchone()
    conn.close()

    if row:
        return row[0]
    else:
        return None


# Get the number of accounts per discord_id
def get_num_accounts():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT discord_id, COUNT(*) FROM accounts GROUP BY discord_id")
    rows = c.fetchall()
    conn.close()

    if rows:
        return rows
    else:
        return None


# Get every unique discord_id
def get_discord_id_list():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT DISTINCT discord_id FROM accounts")
    rows = c.fetchall()
    conn.close()

    if rows:
        return [i[0] for i in rows]
    else:
        return None


# Get the number of different discord_id
def get_num_discord_id():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT DISTINCT discord_id FROM accounts")
    rows = c.fetchall()
    conn.close()

    if rows:
        return rows
    else:
        return None