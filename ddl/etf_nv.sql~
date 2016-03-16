
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
	%s,	#date
	%f,	#accum_net
	%f,	#unit_net
	%f,	#unit_net_chng_pct
	%f	growth_rate
);
'''
{"his_nav_list": [{"accum_net": 2.0840000000000001, "unit_net": 1.512, "unit_net_chng_pct": 2.3696999999999999, "tradedate_display2": "2014-01-22", "_id": 7409536210, "growth_rate": "2.37"}]}
