DROP TABLE IF EXISTS players;

CREATE TABLE players (
id text,
name text
);

INSERT INTO players (id, name) VALUES 
('gs9', 'Bilbo'),
('xp6', 'Gandalf'),
('na8', 'Aragorn'),
('bn9', 'Sauron');


DROP TABLE IF EXISTS games;
CREATE TABLE games (
   room text ,
   player1 text,
   player2 text,
   session_number int,
   show_picture text,
   results DEFAULT ''
);

INSERT INTO games 
(room, player1, player2, session_number, show_picture) VALUES

('1', 'gs9', 'xp6', 25, 5),
('2', 'gs9', 'na8', 25, 0),
('3', 'gs9', 'bn9', 25, 10),
('4', 'xp6', 'na8', 25, 5),
('5', 'xp6', 'bn9', 25, 5),
('6', 'na8', 'bn9', 25, 20);
