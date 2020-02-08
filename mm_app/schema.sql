/*store per game a secret mastermind game*/
CREATE TABLE IF NOT EXISTS games (
  id        INTEGER PRIMARY KEY,
  created   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  ip        TEXT, /*IP that crescrated this game*/
  game      TEXT  /*number array*/
);
