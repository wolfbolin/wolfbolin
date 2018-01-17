<?php
/**
 * Created by PhpStorm.
 * User: wolfbolin
 * Date: 2018/1/15
 * Time: 21:09
 */
$mysql_host = "127.0.0.1"; //mysql主机地址
$mysql_user = "wolfbolin"; //mysql 登录账户
$mysql_passwd = "wolfbolin.com"; //mysql登录密码
$mysql_database = "wolfbolin";
$conn = new mysqli($mysql_host, $mysql_user, $mysql_passwd, $mysql_database);
if ($conn->connect_error) {
    http_response_code(500);
    exit;
}
?>