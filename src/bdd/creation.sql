CREATE DATABASE IF NOT EXISTS `veille-automatique-cyber`;

USE `veille-automatique-cyber`;

CREATE TABLE IF NOT EXISTS sources (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    lien VARCHAR(500) NOT NULL -- Lien du flux RSS
);

CREATE TABLE IF NOT EXISTS articles (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    date date NOT NULL,
    source INT NOT NULL,
    FOREIGN KEY (source) REFERENCES sources(id) ON DELETE CASCADE ON UPDATE CASCADE
);


INSERT INTO sources (nom, lien) 
VALUES ('usine-digitale', 'https://www.usine-digitale.fr/cybersecurite/rss'),
    ('Zataz', 'https://www.zataz.com/feed/');