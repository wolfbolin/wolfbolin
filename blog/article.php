<?php
/**
 * Created by PhpStorm.
 * User: wolfbolin
 * Date: 2018/1/14
 * Time: 14:13
 */
/**
 * 利用session验证用户和权限
 */
session_start();
$user = $right = $PID = null;
if(isset($_SESSION['account'])){
    $user = $_SESSION['account'];
}
if(isset($_SESSION['right'])){
    $right = $_SESSION['right'];
}
/**
 * 获取连接中的文章参数
 * 处理参数，防止数据库注入
 * 无参数的链接将被转向404
 */
if(isset($_GET['PID'])){
    $PID = $_GET['PID'];
    $PID = trim($PID);
    $PID = stripslashes($PID);
    $PID = htmlspecialchars($PID);
}else{
    http_response_code(404);
    exit;
}
/**
 * 连接数据库
 * 从数据库中获取文章内容
 * 处理文章不存在的情况
 */
include 'conn.php';
$sql = "SELECT * FROM blog_article WHERE PID=\"$PID\";";
$res = mysqli_query($conn, $sql);
if(!$res){
    http_response_code(500);
    exit;
}
if($row = mysqli_fetch_array($res)){
    $article_title = $row['title'];
    $article_date = $row['date'];
    $article_content = $row['content'];
    $article_tag = $row['tag'];
    $article_flux = $row['flux']+1;
    $article_data = $row['data'];
}else{
    http_response_code(404);
    exit;
}
/**
 * 记录访问量
 */
$sql = "UPDATE blog_article SET flux=flux+1 WHERE PID=\"$PID\";";
$res = mysqli_query($conn, $sql);
if(!$res){
    http_response_code(500);
    exit;
}
?>
<!doctype html>
<html>
<head>
    <?php
    $title = $article_title;
    $attach = "<link rel=\"stylesheet\" href=\"../include/blog/frame.css\">\n<link rel=\"stylesheet\" href=\"../include/blog/article.css\">";
    include '../include/blog/head.php';
    ?>
</head>
<body>
    <?php
    include "nav.php";
    ?>
    <section class="am-g am-g-fixed">
        <div class="am-u-md-9 am-panel am-panel-secondary">
            <!-- Article.Different from the home page -->
            <div class="wf-article-title">
                <h1><?php echo $article_title?></h1>
                <span class="am-icon-clock-o"><?php echo $article_date?></span>
                <span class="am-icon-book"><?php echo $article_flux?></span>
                <?php
                if(!empty($article_tag)){
                    ?>
                    <span class="am-icon-tags"><?php echo $article_tag?></span>
                    <?php
                }
                ?>
            </div>
            <hr data-am-widget="divider" style="" class="am-divider am-divider-default" />
            <div class="wf-article-content">
                <?php
                include "data/html/md_$PID.html";
                ?>
            </div>
            <!-- Article End -->
        </div>
        <div class="am-u-md-3">
            <?php
            include "sidebar.php";
            ?>
        </div>
    </section>
    <?php
    include "../include/footer.html";
    ?>
</body>
<script src="../include/js/jquery.min.js"></script>
<script src="../include/js/amazeui.min.js"></script>
<script src="../include/blog/frame.js"></script>
<link rel="stylesheet" href="../include/css/highlight-github.css">
<script src="../include/js/highlight.pack.js"></script>
<script>hljs.initHighlightingOnLoad();</script>
</html>
