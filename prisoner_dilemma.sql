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

('1', 'bilbo', 'gandalf', 25, 0),
('2', 'bilbo', 'aragorn', 25, 0),
('3', 'bilbo', 'sauron', 25, 0),
('4', 'gandalf', 'aragorn', 25, 0),
('5', 'gandalf', 'sauron', 25, 0),
('6', 'aragorn', 'sauron', 25, 0);

