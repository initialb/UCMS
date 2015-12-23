-- Create Database UCMS
SHOW DATABASES;
CREATE DATABASE UCMS;
USE UCMS;

-- Create user ucms for localhost and remote login
CREATE USER 'ucms'@'localhost' IDENTIFIED BY 'ucms';
GRANT ALL PRIVILEGES ON *.* TO 'ucms'@'localhost' WITH GRANT OPTION;
CREATE USER 'ucms'@'%' IDENTIFIED BY 'ucms';
GRANT ALL PRIVILEGES ON *.* TO 'ucms'@'%' WITH GRANT OPTION;


DROP TABLE PRODUCT;
CREATE TABLE PRODUCT (
	PROD_ID int(11) NOT NULL AUTO_INCREMENT COMMENT 'System Prod ID',
	LEGAL_GROUP varchar(4) NOT NULL COMMENT 'Institution Name',
	PROD_CODE varchar(100) NOT NULL, -- Product code by institutions
	PROD_NAME varchar(300) NOT NULL, -- Product name by institutions
	CURRENCY varchar(3) NOT NULL, -- Currency Type
	TENOR varchar(50) COMMENT '期限（天）', -- Tenor
	VALUE_DATE date, -- 起息日
	MATURITY_DATE date, -- 到期日
	REDEEMABLE varchar(1), -- 是否可赎回
	PRESERVABLE varchar(1), -- 是否保本
	PLEDGEABLE varchar(1), -- 是否保证收益
	ISSUE_DATE date, -- 发行日期
	YIELD decimal(10,5), -- 预期收益
	RISK varchar(100) COMMENT '风险类型',
	STATUS varchar(100), -- 产品状态
	REMARK varchar(1000),
	UPDATE_DATE datetime,
	PRIMARY KEY (PROD_ID)
	);




序号	银行	产品	代码	币种	期限（天）	预期收益	产品起始	产品到期	是否可赎回	是否保收益	是否保本	风险级别	产品建议	产品状态	同类产品平均收益