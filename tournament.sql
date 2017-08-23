-- Creating Database Called 'tournament'
-- COMMAND THAT USED TO CREATE MY DATABASE IN psql -> CREATE DATABASE tournament;

-- Creating TWO Tables In 'tournament' Database
-- First Table: Table for players has TWO coloumns.
-- 1st col called 'id' type serial for unique number and constraint 'primary key'.
-- 2nd col called 'full_name' type text.
CREATE TABLE players(id serial primary key, name text);

-- Second Table: Table for matches has THREE coloumns.
-- 1st col called 'id_player' type integer and it is FK(Foregien Key) from players table col (id).
-- 2st col called 'winner' type integer. as FK for 'id' in players table.
-- 3st col called 'loser' type integer. as FK for 'id' in players table.
CREATE TABLE matches(id serial primary key,  winner integer references players(id), loser integer references players(id));