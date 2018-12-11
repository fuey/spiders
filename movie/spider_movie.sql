/*
Navicat MySQL Data Transfer

Source Server         : 本地连接
Source Server Version : 50636
Source Host           : localhost:3306
Source Database       : read_rank

Target Server Type    : MYSQL
Target Server Version : 50636
File Encoding         : 65001

Date: 2018-12-11 21:01:27
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for spider_movie
-- ----------------------------
DROP TABLE IF EXISTS `spider_movie`;
CREATE TABLE `spider_movie` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `rank_no` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `img_url` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `title` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `star_num` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `director` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `main_role` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `type` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `nation` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `language` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `release_date` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `length` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `alternate_name` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `summary` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `data_source` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
