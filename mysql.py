# database in terminal
# mysql based

show databases;
use bitcoin;
show tables;
create table btc 
(id int unsigned NOT NULL auto_increment,
time datetime NOT NULL,
date date NOT NULL,
tradeTime datetime NOT NULL,
tradeDate date NOT NULL,
product char(3) NOT NULL,
exchange varchar(30) NOT NULL,
last float NOT NULL,
high float NOT NULL,
low float NOT NULL,
buy float NOT NULL,
sell float NOT NULL,
vol float NOT NULL,

PRIMARY KEY (id));

CREATE INDEX exchange on btc (exchange);
ALTER TABLE btc ADD INDEX (product);
ALTER TABLE btc ADD INDEX (tradeDate);
ALTER TABLE btc ADD INDEX (date);
ALTER TABLE btc ADD UNIQUE INDEX (tradeTime);
ALTER TABLE btc ADD UNIQUE INDEX (time);

EXPLAIN btc;

INSERT INTO btc 
(time, date, tradeTime, tradeDate, product, exchange, last, high, low, buy, sell, vol)
VALUES
(NOW(), CURDATE(), '2016-06-01 10:20:30', '2016-12-31', 'BTC', 'OKCOIN', 100, 101, 99, 99.99, 100.01, 4000);

DELETE FROM btc WHERE id > 10;

import socket
socket.gethostname()
