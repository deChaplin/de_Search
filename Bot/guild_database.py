import sqlite3

DATABASE = 'database.db'


def create_database():
    # Connect to the database
    conn = sqlite3.connect(DATABASE)
    # Create a cursor
    c = conn.cursor()
    # Create a table
    c.execute("""CREATE TABLE IF NOT EXISTS guilds (
        guild_id text PRIMARY KEY,
        guild_prefix text
    )""")
    # commit our command
    conn.commit()
    # close our connection
    conn.close()


# Add a guild id and prefix to the database
def add_guild(guild_id, guild_prefix):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    # Create a table
    c.execute("INSERT INTO guilds VALUES (?, ?)", (guild_id, guild_prefix))
    conn.commit()
    conn.close()


# Remove a guild from the database
def remove_guild(guild_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    # Create a table
    c.execute("DELETE FROM guilds WHERE guild_id=?", (guild_id,))
    conn.commit()
    conn.close()


# Check if guild is in the database
def check_guild(guild_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    # Create a table
    c.execute("SELECT guild_id FROM guilds WHERE guild_id=?", (guild_id,))
    row = c.fetchone()
    conn.close()

    if row:
        return True
    else:
        return False


# Update the prefix of a guild
def update_prefix(guild_id, guild_prefix):
    if check_guild(guild_id):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        # Create a table
        c.execute("UPDATE guilds SET guild_prefix=? WHERE guild_id=?", (guild_prefix, guild_id))
        conn.commit()
        conn.close()
    else:
        add_guild(guild_id, guild_prefix)


# Get the prefix of a guild
def get_prefix(guild_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    # Create a table
    c.execute("SELECT guild_prefix FROM guilds WHERE guild_id=?", (guild_id,))
    row = c.fetchone()
    conn.close()

    return row[0]


# Get the number of guilds in the database
def get_num_guilds():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    # Create a table
    c.execute("SELECT COUNT(*) FROM guilds")
    row = c.fetchone()
    conn.close()

    if row is not None:
        return row[0]
    else:
        return 0