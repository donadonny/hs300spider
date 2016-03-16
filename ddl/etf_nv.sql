
use hs300;


CREATE TABLE IF NOT EXISTS `etf_nv` (
  `id` int(10) unsigned NOT NULL,
  `date` varchar(12) NOT NULL,
  `accum_net` FLOAT NOT NULL DEFAULT '0.0',
  `unit_net` FLOAT NOT NULL DEFAULT '0.0',
  `unit_net_chng_pct` FLOAT NOT NULL DEFAULT '0.0',
  `growth_rate` varchar(12) NOT NULL,
  PRIMARY KEY (`id`,`date`)
);

sql_template = '''
insert into etf_nv values(
	%d,	#ID
	'%s',	#date
	%f,	#accum_net
	%f,	#unit_net
	%f,	#unit_net_chng_pct
	'%s'	#growth_rate
);
'''


create table IF NOT EXISTS `summary`(
  `id` int unsigned NOT NULL,
  `date` varchar(12) NOT NULL,
  `high_price` FLOAT NOT NULL DEFAULT '0.0',
  `low_price` FLOAT NOT NULL DEFAULT '0.0',
  `open_price` FLOAT NOT NULL DEFAULT '0.0',
  `close_price` FLOAT NOT NULL DEFAULT '0.0',
  `last_close_price` FLOAT NOT NULL DEFAULT '0.0',
  `price_change` FLOAT NOT NULL DEFAULT '0.0',
  `amount` FLOAT NOT NULL DEFAULT '0.0',
  `volume` FLOAT NOT NULL DEFAULT '0.0',
  PRIMARY KEY (`id`,`date`)
);

sql_template = '''
insert into summary values(
	%d,	#ID
	'%s',	#date
	%f,	#high_price
	%f,	#low_price
	%f,	#open_price
	%f,	#close_price
	%f,	#last_close_price
	%f,	#price_change
	%f,	#amount
	%f	#volume
);
'''
