-- MySQL dump 10.13  Distrib 5.7.9, for osx10.9 (x86_64)
--
-- Host: localhost    Database: zyq
-- ------------------------------------------------------
-- Server version	5.7.9

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping data for table `t_issuer`
--

LOCK TABLES `t_issuer` WRITE;
/*!40000 ALTER TABLE `t_issuer` DISABLE KEYS */;
INSERT INTO `t_issuer` VALUES ('C10102','中国工商银行股份有限公司',NULL,NULL,NULL,NULL),('C10103','中国农业银行股份有限公司',NULL,NULL,NULL,NULL),('C10104','中国银行股份有限公司',NULL,NULL,NULL,NULL),('C10105','中国建设银行股份有限公司',NULL,NULL,NULL,NULL),('C10153','宁波东海银行股份有限公司',NULL,NULL,NULL,NULL),('C10301','交通银行股份有限公司',NULL,NULL,NULL,NULL),('C10302','中信银行股份有限公司',NULL,NULL,NULL,NULL),('C10303','中国光大银行股份有限公司',NULL,NULL,NULL,NULL),('C10304','华夏银行股份有限公司',NULL,NULL,NULL,NULL),('C10305','中国民生银行股份有限公司',NULL,NULL,NULL,NULL),('C10306','广发银行股份有限公司',NULL,NULL,NULL,NULL),('C10307','平安银行股份有限公司',NULL,NULL,NULL,NULL),('C10308','招商银行股份有限公司',NULL,NULL,NULL,NULL),('C10309','兴业银行股份有限公司',NULL,NULL,NULL,NULL),('C10310','上海浦东发展银行股份有限公司',NULL,NULL,NULL,NULL),('C10315','恒丰银行股份有限公司',NULL,NULL,NULL,NULL),('C10316','浙商银行股份有限公司',NULL,NULL,NULL,NULL),('C10403','中国邮政储蓄银行股份有限公司',NULL,NULL,NULL,NULL),('C10501','汇丰银行（中国）有限公司',NULL,NULL,NULL,NULL),('C10502','东亚银行（中国）有限公司',NULL,NULL,NULL,NULL),('C10503','南洋商业银行（中国）有限公司',NULL,NULL,NULL,NULL),('C10504','恒生银行（中国）有限公司',NULL,NULL,NULL,NULL),('C10510','永亨银行（中国）有限公司',NULL,NULL,NULL,NULL),('C10513','大新银行（中国）有限公司',NULL,NULL,NULL,NULL),('C10531','花旗银行（中国）有限公司',NULL,NULL,NULL,NULL),('C10593','友利银行（中国）有限公司',NULL,NULL,NULL,NULL),('C10595','新韩银行（中国）有限公司',NULL,NULL,NULL,NULL),('C10596','企业银行（中国）有限公司',NULL,NULL,NULL,NULL),('C10597','韩亚银行（中国）有限公司',NULL,NULL,NULL,NULL),('C10621','华侨银行（中国）有限公司',NULL,NULL,NULL,NULL),('C10622','大华银行（中国）有限公司',NULL,NULL,NULL,NULL),('C10623','星展银行（中国）有限公司',NULL,NULL,NULL,NULL),('C10661','苏格兰皇家银行（中国）有限公司',NULL,NULL,NULL,NULL),('C10671','渣打银行（中国）有限公司',NULL,NULL,NULL,NULL),('C10691','法国兴业银行（中国）有限公司',NULL,NULL,NULL,NULL),('C10712','德意志银行（中国）有限公司',NULL,NULL,NULL,NULL),('C10761','澳大利亚和新西兰银行（中国）有限公司',NULL,NULL,NULL,NULL),('C10772','宁波通商银行股份有限公司',NULL,NULL,NULL,NULL),('C10781','厦门国际银行股份有限公司',NULL,NULL,NULL,NULL),('C10787','华一银行',NULL,NULL,NULL,NULL),('C10788','成都银行股份有限公司',NULL,NULL,NULL,NULL),('C10790','攀枝花市商业银行股份有限公司',NULL,NULL,NULL,NULL),('C10792','宜宾市商业银行股份有限公司',NULL,NULL,NULL,NULL),('C10793','乐山市商业银行股份有限公司',NULL,NULL,NULL,NULL),('C10794','德阳银行股份有限公司',NULL,NULL,NULL,NULL),('C10795','绵阳市商业银行股份有限公司',NULL,NULL,NULL,NULL),('C10796','南充市商业银行股份有限公司',NULL,NULL,NULL,NULL),('C10800','遂宁市商业银行股份有限公司',NULL,NULL,NULL,NULL),('C10802','北京银行',NULL,NULL,NULL,NULL),('C10803','天津银行股份有限公司',NULL,NULL,NULL,NULL),('C10804','徽商银行股份有限公司',NULL,NULL,NULL,NULL),('C10805','贵阳银行股份有限公司',NULL,NULL,NULL,NULL),('C10809','盛京银行股份有限公司',NULL,NULL,NULL,NULL),('C10810','大连银行股份有限公司',NULL,NULL,NULL,NULL),('C10811','鞍山银行股份有限公司',NULL,NULL,NULL,NULL),('C10812','抚顺银行股份有限公司',NULL,NULL,NULL,NULL),('C10813','丹东银行股份有限公司',NULL,NULL,NULL,NULL),('C10814','锦州银行股份有限公司',NULL,NULL,NULL,NULL),('C10815','营口银行股份有限公司',NULL,NULL,NULL,NULL),('C10816','阜新银行股份有限公司',NULL,NULL,NULL,NULL),('C10817','辽阳银行股份有限公司',NULL,NULL,NULL,NULL),('C10819','铁岭银行股份有限公司',NULL,NULL,NULL,NULL),('C10820','朝阳银行股份有限公司',NULL,NULL,NULL,NULL),('C10821','葫芦岛银行股份有限公司',NULL,NULL,NULL,NULL),('C10822','福建海峡银行股份有限公司',NULL,NULL,NULL,NULL),('C10823','泉州银行股份有限公司',NULL,NULL,NULL,NULL),('C10824','厦门银行股份有限公司',NULL,NULL,NULL,NULL),('C10827','广州银行股份有限公司',NULL,NULL,NULL,NULL),('C10829','珠海华润银行股份有限公司',NULL,NULL,NULL,NULL),('C10830','广东南粤银行股份有限公司',NULL,NULL,NULL,NULL),('C10831','东莞银行股份有限公司',NULL,NULL,NULL,NULL),('C10832','广西北部湾银行股份有限公司',NULL,NULL,NULL,NULL),('C10833','柳州银行股份有限公司',NULL,NULL,NULL,NULL),('C10834','沧州银行股份有限公司',NULL,NULL,NULL,NULL),('C10835','廊坊银行股份有限公司',NULL,NULL,NULL,NULL),('C10836','衡水银行股份有限公司',NULL,NULL,NULL,NULL),('C10838','焦作中旅银行股份有限公司',NULL,NULL,NULL,NULL),('C10846','洛阳银行股份有限公司',NULL,NULL,NULL,NULL),('C10847','平顶山银行股份有限公司',NULL,NULL,NULL,NULL),('C10851','郑州银行股份有限公司',NULL,NULL,NULL,NULL),('C10855','哈尔滨银行股份有限公司',NULL,NULL,NULL,NULL),('C10856','汉口银行股份有限公司',NULL,NULL,NULL,NULL),('C10859','湖北银行股份有限公司',NULL,NULL,NULL,NULL),('C10862','长沙银行股份有限公司',NULL,NULL,NULL,NULL),('C10867','吉林银行股份有限公司',NULL,NULL,NULL,NULL),('C10868','江苏银行股份有限公司',NULL,NULL,NULL,NULL),('C10869','南京银行股份有限公司',NULL,NULL,NULL,NULL),('C10871','九江银行股份有限公司',NULL,NULL,NULL,NULL),('C10872','上饶银行股份有限公司',NULL,NULL,NULL,NULL),('C10873','赣州银行股份有限公司',NULL,NULL,NULL,NULL),('C10874','江西银行股份有限公司',NULL,NULL,NULL,NULL),('C10875','内蒙古银行股份有限公司',NULL,NULL,NULL,NULL),('C10876','包商银行股份有限公司',NULL,NULL,NULL,NULL),('C10877','乌海银行股份有限公司',NULL,NULL,NULL,NULL),('C10878','鄂尔多斯银行股份有限公司',NULL,NULL,NULL,NULL),('C10879','宁夏银行股份有限公司',NULL,NULL,NULL,NULL),('C10880','石嘴山银行股份有限公司',NULL,NULL,NULL,NULL),('C10881','齐鲁银行股份有限公司',NULL,NULL,NULL,NULL),('C10882','青岛银行股份有限公司',NULL,NULL,NULL,NULL),('C10883','齐商银行股份有限公司',NULL,NULL,NULL,NULL),('C10885','河北银行股份有限公司',NULL,NULL,NULL,NULL),('C10886','唐山银行股份有限公司',NULL,NULL,NULL,NULL),('C10887','秦皇岛银行股份有限公司',NULL,NULL,NULL,NULL),('C10889','邢台银行股份有限公司',NULL,NULL,NULL,NULL),('C10891','张家口市商业银行股份有限公司',NULL,NULL,NULL,NULL),('C10894','东营银行股份有限公司',NULL,NULL,NULL,NULL),('C10895','烟台银行股份有限公司',NULL,NULL,NULL,NULL),('C10896','潍坊银行股份有限公司',NULL,NULL,NULL,NULL),('C10897','济宁银行股份有限公司',NULL,NULL,NULL,NULL),('C10898','泰安市商业银行股份有限公司',NULL,NULL,NULL,NULL),('C10899','威海市商业银行股份有限公司',NULL,NULL,NULL,NULL),('C10900','日照银行股份有限公司',NULL,NULL,NULL,NULL),('C10901','莱商银行股份有限公司',NULL,NULL,NULL,NULL),('C10902','临商银行股份有限公司',NULL,NULL,NULL,NULL),('C10903','德州银行股份有限公司',NULL,NULL,NULL,NULL),('C10904','晋商银行股份有限公司',NULL,NULL,NULL,NULL),('C10907','晋城银行股份有限公司',NULL,NULL,NULL,NULL),('C10908','长治银行股份有限公司',NULL,NULL,NULL,NULL),('C10909','晋中银行股份有限公司',NULL,NULL,NULL,NULL),('C10910','长安银行股份有限公司',NULL,NULL,NULL,NULL),('C10911','西安银行股份有限公司',NULL,NULL,NULL,NULL),('C10912','上海银行股份有限公司',NULL,NULL,NULL,NULL),('C10913','乌鲁木齐市商业银行股份有限公司',NULL,NULL,NULL,NULL),('C10917','富滇银行股份有限公司',NULL,NULL,NULL,NULL),('C10918','曲靖市商业银行股份有限公司',NULL,NULL,NULL,NULL),('C10919','玉溪市商业银行股份有限公司',NULL,NULL,NULL,NULL),('C10920','杭州银行股份有限公司',NULL,NULL,NULL,NULL),('C10921','宁波银行股份有限公司',NULL,NULL,NULL,NULL),('C10922','温州银行股份有限公司',NULL,NULL,NULL,NULL),('C10923','嘉兴银行股份有限公司',NULL,NULL,NULL,NULL),('C10924','湖州银行股份有限公司',NULL,NULL,NULL,NULL),('C10925','绍兴银行股份有限公司',NULL,NULL,NULL,NULL),('C10926','金华银行股份有限公司',NULL,NULL,NULL,NULL),('C10927','浙江稠州商业银行股份有限公司',NULL,NULL,NULL,NULL),('C10928','台州银行股份有限公司',NULL,NULL,NULL,NULL),('C10929','浙江泰隆商业银行股份有限公司',NULL,NULL,NULL,NULL),('C10930','浙江民泰商业银行股份有限公司',NULL,NULL,NULL,NULL),('C10931','重庆银行股份有限公司',NULL,NULL,NULL,NULL),('C10932','重庆三峡银行股份有限公司',NULL,NULL,NULL,NULL),('C10933','青海银行股份有限公司',NULL,NULL,NULL,NULL),('C11043','北京农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11044','天津农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11049','天津滨海农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11052','合肥科技农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11053','安徽马鞍山农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11054','淮南通商农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11074','贵州花溪农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11079','福建南安农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11080','福建晋江农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11081','福建石狮农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11096','深圳农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11122','沧州融信农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11128','武汉农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11140','长春农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11141','吉林九台农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11146','无锡农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11147','江苏江阴农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11149','江苏新沂农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11150','江苏睢宁农村商业股份有限公司',NULL,NULL,NULL,NULL),('C11153','苏州银行股份有限公司',NULL,NULL,NULL,NULL),('C11154','江苏常熟农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11155','江苏昆山农村商业银行',NULL,NULL,NULL,NULL),('C11156','江苏张家港农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11157','江苏太仓农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11158','江苏吴江农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11159','江苏海安农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11165','江苏大丰农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11166','江苏射阳农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11167','江苏仪征农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11171','江苏泰州农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11172','江苏靖江农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11173','江苏兴化农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11177','江苏泗阳农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11181','南昌农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11186','内蒙古呼和浩特金谷农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11194','宁夏黄河农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11200','山东张店农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11202','山东东营胜利农村合作银行',NULL,NULL,NULL,NULL),('C11205','山东莱州农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11207','山东寿光农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11209','山东圣泰农村合作银行',NULL,NULL,NULL,NULL),('C11212','山东邹平农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11221','上海农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11223','昆明官渡农村合作银行',NULL,NULL,NULL,NULL),('C11224','云南红塔农村合作银行',NULL,NULL,NULL,NULL),('C11227','杭州联合农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11228','浙江萧山农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11229','浙江杭州余杭农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11230','浙江富阳农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11231','浙江桐庐农村合作银行',NULL,NULL,NULL,NULL),('C11232','宁波慈溪农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11233','宁波余姚农村合作银行',NULL,NULL,NULL,NULL),('C11234','宁波鄞州农村合作银行',NULL,NULL,NULL,NULL),('C11235','浙江温州鹿城农村合作银行',NULL,NULL,NULL,NULL),('C11236','浙江温州龙湾农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11237','浙江温州瓯海农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11238','浙江乐清农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11240','浙江瑞安农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11241','浙江苍南农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11242','浙江平湖农村合作银行',NULL,NULL,NULL,NULL),('C11243','浙江禾城农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11244','湖州吴兴农村合作银行',NULL,NULL,NULL,NULL),('C11245','浙江南浔农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11246','浙江德清农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11247','浙江长兴农村合作银行',NULL,NULL,NULL,NULL),('C11248','浙江绍兴瑞丰农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11249','浙江上虞农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11250','浙江嵊州农村合作银行',NULL,NULL,NULL,NULL),('C11251','浙江新昌农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11252','浙江诸暨农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11253','绍兴恒信农村合作银行',NULL,NULL,NULL,NULL),('C11254','浙江金华成泰农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11255','浙江兰溪农村合作银行',NULL,NULL,NULL,NULL),('C11256','浙江义乌农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11257','浙江台州椒江农村合作银行',NULL,NULL,NULL,NULL),('C11258','浙江台州黄岩农村合作银行',NULL,NULL,NULL,NULL),('C11259','浙江台州路桥农村合作银行',NULL,NULL,NULL,NULL),('C11260','浙江玉环农村合作银行',NULL,NULL,NULL,NULL),('C11261','浙江天台农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11262','浙江温岭农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11263','浙江丽水莲都农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11264','浙江舟山定海海洋农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11267','重庆农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11287','江苏江南农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11288','龙江银行股份有限公司',NULL,NULL,NULL,NULL),('C11312','广州农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11313','广东顺德农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11314','东莞农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11336','江苏盐城农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11338','江苏江都农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11360','华融湘江银行',NULL,NULL,NULL,NULL),('C11376','昆仑银行股份有限公司',NULL,NULL,NULL,NULL),('C11382','江苏邳州农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11390','浙江武义农村合作银行',NULL,NULL,NULL,NULL),('C11393','江苏南通农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11402','江苏宜兴农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11404','桂林银行股份有限公司',NULL,NULL,NULL,NULL),('C11410','江苏如皋农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11417','福建上杭农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11429','黄山太平农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11432','营口沿海银行股份有限公司',NULL,NULL,NULL,NULL),('C11456','大兴安岭农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11501','亳州药都农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11521','江苏姜堰农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11546','江苏建湖农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11549','江苏民丰农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11562','江苏镇江农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11615','福建漳州农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11623','山东临淄农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11627','福建福州农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11709','广东华兴银行股份有限公司',NULL,NULL,NULL,NULL),('C11756','甘肃银行股份有限公司',NULL,NULL,NULL,NULL),('C11763','江苏泗洪农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11765','肇庆端州农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11778','攀枝花农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11788','广东南海农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11802','山西灵石农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11803','江门新会农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11804','江门融和农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11829','海口农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11865','山西寿阳农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11883','贵阳农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11891','江苏淮安农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11917','江苏盱眙农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11933','山西河津农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11940','江苏启东农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11946','青岛农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C11993','长治潞州农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12000','山西五台农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12002','潍坊农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12061','大连农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12066','山西榆次农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12086','广东清远农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12094','山东高密农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12096','佛山农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12101','珠海农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12109','贵州银行股份有限公司',NULL,NULL,NULL,NULL),('C12112','渤海银行股份有限公司',NULL,NULL,NULL,NULL),('C12123','湖北随州农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12158','山西侯马农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12162','山西乡宁农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12189','山西潞城农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12218','黄石农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12225','湖北三峡农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12240','江苏滨海农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12269','中山农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12362','新疆天山农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12395','延边农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12421','河北唐山农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12436','广东惠东农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12513','湖北荆州农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12539','广东博罗农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12582','聊城农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12588','成都农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12665','山西平遥农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12681','山东齐河农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12687','武威农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12740','包头农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12788','河北正定农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12857','菏泽农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12893','通化农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12901','中原银行股份有限公司',NULL,NULL,NULL,NULL),('C12903','山东昌邑农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C12997','济南农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C13089','新疆昌吉农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C13161','福建长乐农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C13170','朔州市平鲁区农村信用合作联社',NULL,NULL,NULL,NULL),('C20111','景德镇市商业银行股份有限公司',NULL,NULL,NULL,NULL),('C27082','兰州银行股份有限公司',NULL,NULL,NULL,NULL),('C30076','四川仪陇农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C30365','连江县农村信用合作联社',NULL,NULL,NULL,NULL),('C30368','安溪县农村信用合作联社',NULL,NULL,NULL,NULL),('C30369','泉州农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C30371','惠安县农村信用合作联社',NULL,NULL,NULL,NULL),('C30372','永春县农村信用合作联社',NULL,NULL,NULL,NULL),('C30373','德化县农村信用合作联社',NULL,NULL,NULL,NULL),('C30390','龙岩市永定区农村信用合作联社',NULL,NULL,NULL,NULL),('C30427','厦门农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C30563','广东高要农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C30564','广东四会农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C30569','肇庆市鼎湖区农村信用合作联社',NULL,NULL,NULL,NULL),('C30724','河北邢台农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C30917','郑州市市郊农村信用合作联社',NULL,NULL,NULL,NULL),('C30995','哈尔滨城郊农村信用合作联社',NULL,NULL,NULL,NULL),('C31266','长春发展农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C31271','吉林环城农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C31301','江苏紫金农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C31324','铜山县农村信用合作联社',NULL,NULL,NULL,NULL),('C31327','徐州淮海农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C31336','江苏如东农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C31347','江苏洪泽农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C31354','江苏扬州农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C31374','九江农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C31475','内蒙古伊金霍洛农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C31610','泰安市泰山区农村信用合作联社',NULL,NULL,NULL,NULL),('C31614','山东宁阳农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C31615','山东威海农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C31629','德州市德城区农村信用合作联社',NULL,NULL,NULL,NULL),('C31635','山东禹城农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C31672','大同北都农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C31682','山西盂县农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C31699','朔州市朔城区农村信用合作联社',NULL,NULL,NULL,NULL),('C31718','山西尧都农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C31732','山西泽州农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C31740','山西长治黎都农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C31741','山西襄垣农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C31745','山西壶关农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C31746','山西长子农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C31756','稷山县农村信用合作联社',NULL,NULL,NULL,NULL),('C31766','太谷县农村信用合作联社',NULL,NULL,NULL,NULL),('C31768','山西介休农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C31770','晋中经济开发区农村信用合作联社',NULL,NULL,NULL,NULL),('C31962','昆明市呈贡区农村信用合作联社',NULL,NULL,NULL,NULL),('C32076','临安市农村信用合作联社',NULL,NULL,NULL,NULL),('C32077','建德市农村信用合作联社',NULL,NULL,NULL,NULL),('C32078','淳安县农村信用合作联社',NULL,NULL,NULL,NULL),('C32080','象山县农村信用合作联社',NULL,NULL,NULL,NULL),('C32081','宁波市市区农村信用合作联社',NULL,NULL,NULL,NULL),('C32082','宁波市北仑区农村信用合作联社',NULL,NULL,NULL,NULL),('C32083','宁海县农村信用合作联社',NULL,NULL,NULL,NULL),('C32084','宁波镇海农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C32089','洞头县农村信用合作联社',NULL,NULL,NULL,NULL),('C32090','浙江平阳农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C32091','文成县农村信用合作联社',NULL,NULL,NULL,NULL),('C32092','泰顺县农村信用合作联社',NULL,NULL,NULL,NULL),('C32093','浙江嘉善农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C32094','浙江海宁农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C32095','海盐县农村信用合作联社',NULL,NULL,NULL,NULL),('C32096','桐乡市农村信用合作联社',NULL,NULL,NULL,NULL),('C32097','浙江安吉农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C32100','浙江东阳农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C32101','浙江永康农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C32102','浦江县农村信用合作联社',NULL,NULL,NULL,NULL),('C32104','磐安县农村信用合作联社',NULL,NULL,NULL,NULL),('C32106','三门县农村信用合作联社',NULL,NULL,NULL,NULL),('C32108','浙江临海农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C32109','云和县农村信用合作联社',NULL,NULL,NULL,NULL),('C32111','松阳县农村信用合作联社',NULL,NULL,NULL,NULL),('C32113','浙江青田农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C32114','龙泉市农村信用合作联社',NULL,NULL,NULL,NULL),('C32115','缙云县农村信用合作联社',NULL,NULL,NULL,NULL),('C32116','景宁畲族自治县农村信用合作联社',NULL,NULL,NULL,NULL),('C32117','岱山县农村信用合作联社',NULL,NULL,NULL,NULL),('C32118','嵊泗县农村信用合作联社',NULL,NULL,NULL,NULL),('C32119','浙江衢州柯城农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C32120','龙游县农村信用合作联社',NULL,NULL,NULL,NULL),('C32121','常山县农村信用合作联社',NULL,NULL,NULL,NULL),('C32122','开化县农村信用合作联社',NULL,NULL,NULL,NULL),('C32123','衢州市衢江农村信用合作联社',NULL,NULL,NULL,NULL),('C32125','青海西宁农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C32263','甘肃榆中农村合作银行',NULL,NULL,NULL,NULL),('C32498','山西运城农村商业银行股份有限公司',NULL,NULL,NULL,NULL),('C32546','宁波奉化农村商业银行股份有限公司',NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `t_issuer` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-01-09 11:50:46