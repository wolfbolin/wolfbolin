<?php
/**
 * Created by PhpStorm.
 * User: wolfbolin
 * Date: 2018/1/15
 * Time: 20:38
 */
session_start();
$account_regex = "/^[A-Za-z0-9._]{5,20}$/";
$password_regex = "/^[A-Za-z0-9`~!@#$%^&*-=+,.]{5,30}$/";
$action = $accountID = $password = "";
/**
 * 获取表单数据
 * 校验表单数据
 * 登录或登出
 */
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $action = test_post("action");
    $accountID = test_post("accountID");
    $password = test_post("password");
    if(strcmp($action,'login')==0){
        //nothing to do.
    }elseif (strcmp($action,'logout')==0){
        unset($_SESSION['account']);
        unset($_SESSION['right']);
        echo '{"result":"success"}';
        exit;
    }else{
        echo '{"result":"action error"}';
        exit;
    }

    if(!preg_match($account_regex, $accountID)){
        echo '{"result":"account error"}';
        exit;
    }
    if(!preg_match($password_regex, $password)){
        echo '{"result":"password error"}';
        exit;
    }
}else{
    http_response_code(403);
    exit;
}
/**
 * 连接数据库
 * 查询用户信息
 * 记录登录状态
 * 返回登录结果
 */
include 'conn.php';

$sql = "SELECT * FROM user_table WHERE account='$accountID' AND password='$password';";
$res = mysqli_query($conn, $sql);
if(!$res){
    echo '{"result":"'.mysqli_error($conn).'"}';
    mysqli_close($conn);
    exit;
}
if($row = mysqli_fetch_array($res)){
    $_SESSION['account'] = $accountID;
    $_SESSION['right'] = $row['right'];
    echo '{"result":"success"}';
}else{
    echo '{"result":"authentication failure"}';
}
mysqli_close($conn);

function test_post($key) {
    if(!isset($_POST[$key])){
        return "";
    }
    $data = $_POST[$key];
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
}
?>