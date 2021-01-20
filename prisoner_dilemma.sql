DROP TABLE IF EXISTS players;

CREATE TABLE players (
id text,
name text
);

INSERT INTO players (id, name) VALUES 
('gs9', 'Paola'),
('xp6', 'Chloé'),
('na8', 'Margot'),
('bn9', 'Olivier');


DROP TABLE IF EXISTS games;
CREATE TABLE games (
   room text ,
   player1 text,
   player2 text,
   session_number int,
   show_picture int,
   session_played int,
   results text
);

INSERT INTO games 
(room, player1, player2, session_number, show_picture, session_played, results) VALUES

('1', 'gs9', 'xp6', 25, 1, 0, ''),
('2', 'gs9', 'na8', 25, 1, 0, ''),
('3', 'gs9', 'bn9', 25, 1, 0, ''),
('4', 'xp6', 'na8', 25, 1, 0, ''),
('5', 'xp6', 'bn9', 25, 1, 0, ''),
('6', 'na8', 'bn9', 25, 1, 0, '');
