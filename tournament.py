#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

''' The enhanced way to connect to database and cursor at a same time:
    
    def connect(database_name="tournament"):
        try: 
            db = psycopg2.connect("dbname={}".format(database_name))
            c = db.cursor()
            return db, c
        except:
            print("some error message")
    
    Then the functions should look like this:
    
    def register_player(name):
        db, c = connect()
        
        query = "insert into players (name) values (%s);"
        parameter = (name,)
        c.execute(query, parameter)
        
        db.commit()
        db.close()
'''


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM matches;")
    conn.commit()
    c.close()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("TRUNCATE matches;")  # truncate equals to delete from, but is quicker
    c.execute("DELETE FROM players;")
    conn.commit()
    c.close()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered. Not python(len),
    the database should do it"""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT count(*) FROM players;")
    number = c.fetchone()[0]
    conn.commit()
    c.close()
    conn.close()
    return number


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    query = "INSERT INTO players (name) VALUES (%s)"
    param = (name,)
    c.execute(query, param)
    conn.commit()
    c.close()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    query = "SELECT * FROM standings;"
    c.execute(query)
    result = c.fetchall()
    conn.commit()
    c.close()
    conn.close()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.


    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    c.execute("insert into matches (winner, loser) values ((%s), (%s))", (winner, loser))
    conn.commit()
    c.close()
    conn.close()

 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    c = conn.cursor()
    result = []
    pair = []
    c.execute("SELECT COUNT(*) FROM standings;")
    players_count = c.fetchone()[0]

    for x in range(0, players_count, 2):
        c.execute("SELECT id, name, wins FROM standings "
                  "LIMIT 2 OFFSET 0 + (%s)", (x,))
        players = c.fetchall()
        pair.append(players[0][0])
        pair.append(players[0][1])
        pair.append(players[1][0])
        pair.append(players[1][1])
        result.append(pair)
        pair = []
    return result
    c.close()
    conn.close()

