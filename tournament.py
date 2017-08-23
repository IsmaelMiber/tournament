#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
import psycopg2, bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect(host="localhost", dbname='tournament', user="postgres", password = "123")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM matches")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM players")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT count(id) FROM players;")
    num = c.fetchone()
    conn.close()
    return num[0]
    


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO players (name) VALUES (%s)", (bleach.clean(name),))
    conn.commit()
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
    c.execute('''SELECT id, name, (select count(winner) from matches where matches.winner = id group by winner) as wins,
                (select count(*) from matches where id in (winner, loser) group by winner) as total
                from players
                group by id
                order by wins DESC''')
    players = c.fetchall()
    conn.close()
    if players[0][2] == None and players[0][3] == None and players[1][2] == None and players[1][3] == None:
        players = [(0,0,0,0), (0,0,0,0)]
    if players[0][2] == None:
        players= [(players[0][0], players[0][1], 0, players[0][3]), (players[1][0], players[1][1], players[1][2], players[1][3])]
    if players[0][3] == None:
        players= [(players[0][0], players[0][1], players[0][2], 0), (players[1][0], players[1][1], players[1][2], players[1][3])]
    if players[1][2] == None:
        players= [(players[0][0], players[0][1], players[0][2], players[0][3]), (players[1][0], players[1][1], 0, players[1][3])]
    if players[1][3] == None:
        players= [(players[0][0], players[0][1], players[0][2], players[0][3]), (players[1][0], players[1][1], players[1][2], 0)]
    return players

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    c.execute("insert into matches (winner, loser) values (%s,%s);",((winner,),(loser,)))
    conn.commit()
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
    c.execute('''SELECT id, name, (select count(winner) from matches where matches.winner = id group by winner) as wins,
                (select count(*) from matches where id in (winner, loser) group by winner) as total
                from players
                group by id
                order by wins DESC''')
    (id, name, wins, matches):
    players = c.fetchall()
    versuss = []
    conn.close();
        num = int(countPlayers())
# this section i do if statment and what below it but i wasn't know how to loop throug it so i looked on github and i take for loop idea from there.
        for player in range(0, num):
            if player % 2 == 0:
                id1 = players[player][0]
                name1 = players[player][1]
                id2 = players[player + 1][0]
                name2 = players[player + 1][1]
                pair = (id1, name1, id2, name2)
                versuss.append(pair)

        return versuss
                

















    


