CREATE DATABASE IF NOT EXISTS `veille-automatique-cyber`;

USE `veille-automatique-cyber`;

CREATE TABLE IF NOT EXISTS sources (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    lien VARCHAR(500) NOT NULL -- Lien du flux RSS
);
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS articles (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    date date NOT NULL,
    source INT NOT NULL,
    link VARCHAR(500) NOT NULL,
    FOREIGN KEY (source) REFERENCES sources(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS frise (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL
);



CREATE TABLE IF NOT EXISTS liste_perso(
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS linkListeArticle(
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    id_article INT NOT NULL,
    id_liste INT NOT NULL,
    FOREIGN KEY (id_article) REFERENCES articles(id),
    FOREIGN KEY (id_liste) REFERENCES liste_perso(id)
);

CREATE TABLE IF NOT EXISTS linkUserListe(
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    id_user INT NOT NULL,
    id_liste_perso INT NOT NULL,
    FOREIGN KEY (id_liste_perso) REFERENCES liste_perso(id),
    FOREIGN KEY (id_user) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS linkFrise (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    id_frise INT NOT NULL,
    valeur VARCHAR(255) NOT NULL,
    date_publi DATE NOT NULL,
    FOREIGN KEY (id_frise) REFERENCES frise(id),
);

INSERT INTO sources (nom, lien) 
VALUES ('Usine Digitale', 'https://www.usine-digitale.fr/cybersecurite/rss'),
    ('Zataz', 'https://www.zataz.com/feed/'),
    ('Siecle digitale','https://siecledigital.fr/cybersecurite/feed/'),
    ('Cybersécurité-info','https://cybersecurite-info.fr//feed/'),
    ('IT-Connect','https://www.it-connect.fr/feed/'),
    ('Zdnet','https://www.zdnet.fr/feeds/rss/actualites/cybersecurite-3900046206q.htm'),
    ('Futura Sciences','https://www.futura-sciences.com/rss/actualites.xml');