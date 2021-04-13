DROP TABLE IF EXISTS players;

CREATE TABLE players (
id text,
name text
);

INSERT INTO players (id, name) VALUES
('bilbo', 'Bilbo Baggins'),
('gandalf', 'Gandalf, il mago bianco'),
('aragorn', 'Aragorn, figlio di Arathorn'),
('sauron', 'Sauron, il signore di Mordor');


DROP TABLE IF EXISTS games;
CREATE TABLE games (
   room text ,
   player1 text,
   player2 text,
   session_number int,
   show_picture int,
   results DEFAULT ''
);

INSERT INTO games
(room, player1, player2, session_number, show_picture) VALUES

('1', 'bilbo', 'gandalf_computer', 10, -1),
('2', 'bilbo', 'aragorn_computer', 10, -1),
('3', 'bilbo', 'sauron_computer', 10, -1),
('4', 'gandalf', 'bilbo_computer', 10, -1),
('5', 'gandalf', 'aragorn_computer', 10, -1),
('6', 'gandalf', 'sauron_computer', 10, -1),
('7', 'aragorn', 'gandalf_computer', 10, -1),
('8', 'aragorn', 'sauron_computer', 10, -1),
('9', 'aragorn', 'bilbo_computer', 10, -1),
('10', 'sauron', 'gandalf_computer', 10, -1),
('11', 'sauron', 'aragorn_computer', 10, -1),
('12', 'sauron', 'bilbo_computer', 10, -1);

