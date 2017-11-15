#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("update Matches set wins = 0, matches = 0;")
    #c.execute("select * from Matches;")
    conn.commit()
    c.close()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("delete from matches;")
    c.execute("delete from players;")
    conn.commit()
    c.close()
    conn.close()



def countPlayers():
    """Returns the number of players currently registered. Not python(len),
    the database should do it"""
    conn = connect()
    c = conn.cursor()
    c.execute("select count(*) from Players;")
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
    c.execute("insert into Players (name) values (%s)", (name,))
    c.execute("select ID from Players;")
    id = c.fetchall()
    the_number = (id[-1][-1])
    c.execute("insert into Matches (ID, name, wins, matches) values (%s, %s, %s, %s)", (the_number, name, 0, 0))
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
    c.execute("select * from matches order by wins;")
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
    c.execute("select wins from matches where id = %s", (winner,))
    win = c.fetchone()[0]
    c.execute("select matches from matches where id = %s", (loser,))
    match = c.fetchone()[0]
    c.execute("update matches set wins = (%s), matches = (%s) "
              "where id = %s", ((win + 1), (match +1), winner))
    c.execute("update matches set matches = (%s) "
              "where id = %s", ((match + 1), loser))
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
    c.execute("create view comparison as select id, name, wins from Matches "
                  "group by wins, id, name "
                  "order by wins desc;")
    for x in range (0, 8, 2): # here the number of loops should be taken
        # from a query select count(id) as num or so...I'll do it later
        c.execute("select id, name, wins from comparison "
                  "limit 2 offset 0 + (%s)", (x,))
        players= c.fetchall()
        pair.append(players[0][0])
        pair.append(players[0][1])
        pair.append(players[1][0])
        pair.append(players[1][1])
        result.append(pair)
        pair = []
    return result
    conn.commit()
    c.close()
    conn.close()

