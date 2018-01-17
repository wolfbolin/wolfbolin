<?php
/**
 * Created by PhpStorm.
 * User: wolfbolin
 * Date: 2018/1/15
 * Time: 2:03
 */
/**
 * 利用session验证用户和权限
 */
session_start();
$user = $right = null;
if(isset($_SESSION['account'])){
    $user = $_SESSION['account'];
}
if(isset($_SESSION['right'])){
    $right = $_SESSION['right'];
}
if($user == null ||$right == null){
    http_response_code(404);
    exit;
}
/**
 * 获取表单数据
 */
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $article_title = test_post('article-title');
    $article_date = test_post('article-date');
    $article_file = $_FILES["article-file"];
    $article_tag = implode(" / ", $_POST['tag']);
    $article_preview = test_post('article-preview');
    $article_data = test_post('article-data');
    if(empty($article_title)||empty($article_date)||empty($article_preview)){
        http_response_code(403);
        exit;
    }
}else{
    http_response_code(403);
    exit;
}
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
/**
 * 连接数据库
 * 分配PID
 * 保存信息在数据库中
 */
echo "正在保存信息到数据库..."."<br/>";
include 'conn.php';
$PID = uniqid('',true);
//暂时放弃了时分秒的功能
$sql = "INSERT INTO blog_article(pid, title, date, preview, content, tag, flux, data) "
."VALUES(\"$PID\",\"$article_title\",\"$article_date 08:00:00\""
.", \"$article_preview\", \"md_$PID.md\", \"$article_tag\", 0,\"$article_data\");";

$res = mysqli_query($conn, $sql);
if(!$res){
    echo $sql."<br/>";
    echo "发生数据库错误".mysqli_error($conn)."<br/>";
    http_response_code(500);
    exit;
}
/**
 * 保存文件在本地
 */
echo "正在保存文件到本地..."."<br/>";
$file_name = "md_".$PID.".md";
rename($article_file['tmp_name'], "cache/".$file_name);
exec("python3 md2html-php.py ".$file_name." 2>&1",$arr,$ret);
if($ret != 0){
    echo "保存文件时发生错误";
    print_r($arr);
    echo "<br/>";
    exit;
    //此处可以加入数据库回滚操作
}
/**
 * 尝试跳转到文章
 */
echo "文章上传成功，正在跳转..."."<br/>";
header("location: article.php?PID=$PID");
?>