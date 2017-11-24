-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE database tournament;
\connect tournament;


CREATE TABLE players (
    id serial primary key,
    name text
    );

CREATE TABLE matches (
    winner integer REFERENCES players(id),
    loser integer REFERENCES players(id)
    );

-- this view I have for combining the columns winner and loser for being more comfortable
-- counting the occurence of ids.
CREATE VIEW one_column AS SELECT winner FROM matches UNION ALL SELECT loser FROM matches;

-- oh my goodness this query costed me 6 hours of life!
CREATE VIEW standings AS SELECT players.id, players.name,
            COUNT(matches.winner) AS wins,
                (SELECT COUNT(*)
                FROM one_column
                WHERE winner = players.id) AS matches
            FROM matches RIGHT JOIN players ON matches.winner = players.id
            GROUP BY players.id, matches.winner
            ORDER BY wins DESC;

