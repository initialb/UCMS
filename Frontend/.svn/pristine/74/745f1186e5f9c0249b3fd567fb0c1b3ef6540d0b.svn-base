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
	PROD_ID int(11) NOT NULL AUTO_INCREMENT COMMENT 'PK',
	LEGAL_GROUP varchar(4) NOT NULL COMMENT '机构名',
	PROD_CODE varchar(100) NOT NULL COMMENT '产品代码',
	PROD_NAME varchar(300) NOT NULL COMMENT '产品名称',
	CURRENCY varchar(10) NOT NULL COMMENT '币种',
	TENOR varchar(50) COMMENT '期限（天）',
	ISSUE_DATE date COMMENT '发行日期',
	END_DATE date COMMENT '结束日期',
	VALUE_DATE date COMMENT '起息日',
	MATURITY_DATE date COMMENT '到期日',
	COUPONTYPE varchar(10) COMMENT '收益类型',
	REDEEMABLE varchar(1) COMMENT '是否可赎回',
	PRESERVABLE varchar(1) COMMENT '是否保本',
	PLEDGEABLE varchar(1) COMMENT '是否保证收益',
	YIELD decimal(10,5) COMMENT '预期收益',
	RISK varchar(100) COMMENT '风险类型',
	STATUS varchar(100) COMMENT '产品状态',
	REMARK varchar(1000) COMMENT '备注',
	UPDATE_DATE datetime COMMENT '更新时间',
	PRIMARY KEY (PROD_ID)
	);




序号	银行	产品	代码	币种	期限（天）	预期收益	产品起始	产品到期	是否可赎回	是否保收益	是否保本	风险级别	产品建议	产品状态	同类产品平均收益