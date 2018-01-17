<?php
/**
 * Created by PhpStorm.
 * User: wolfbolin
 * Date: 2018/1/16
 * Time: 14:21
 */
session_start();
$user = $right = null;
if(isset($_SESSION['account'])){
    $user = $_SESSION['account'];
}
if(isset($_SESSION['right'])){
    $right = $_SESSION['right'];
}
/**
 * 获取连接中的标签tag
 * 处理参数，防止数据库注入
 */
$tag = null;
if(isset($_GET['tag'])){
    $tag = $_GET['tag'];
    $tag = trim($tag);
    $tag = stripslashes($tag);
    $tag = htmlspecialchars($tag);
}
?>
<!doctype html>
<html>
<head>
    <?php
    $title = "Wolf Blog 文章列表";
    $attach = "<link rel=\"stylesheet\" href=\"../include/blog/frame.css\">\n<link rel=\"stylesheet\" href=\"../include/blog/list.css\">";
    include '../include/blog/head.php';
    ?>
</head>
<body>
<?php
include "nav.php";
?>
<section class="am-g am-g-fixed">
    <div class="am-u-md-9 am-panel am-panel-secondary wf-units">
        <div class="am-panel-hd">
            <?php
            if(empty($tag)) {
                echo "文章列表";
            }else{
                echo $tag."相关文章";
            }
            ?>
        </div>
        <ul class="am-list am-list-static wf-units-li">
        <?php
        include 'conn.php';
        /**
         * 根据tag来显示文章，无tag时显示所有文章
         */
        if(empty($tag)){
            /**
             * 无tag的查询
             * 不分页，全部显示
             */
            $sql = "SELECT pid,title,preview,date,flux FROM blog_article ORDER BY date DESC;";
            $res = mysqli_query($conn, $sql);
            while ($row = mysqli_fetch_array($res)){
                ?>
                <li>
                    <a href="article.php?PID=<?php echo $row['pid']?>">
                        <h2><?php echo $row['title']?></h2>
                        <p><?php echo $row['preview']?></p>
                        <span class="am-icon-clock-o"><?php echo $row['date']?></span>
                        <span class="am-icon-book"><?php echo $row['flux']?></span>
                    </a>
                </li>
                <?php
            }
        }else{
            /**
             * 防止+号的错误输入
             * 有tag的查询
             */
            $tag = str_replace("+","[+]", $tag);
            $sql = "SELECT pid,title,preview,date,flux FROM blog_article WHERE tag REGEXP \"$tag\" ORDER BY date DESC;";
            $res = mysqli_query($conn, $sql);
            if(!$res){
                echo mysqli_error($conn);
                http_response_code(500);
                exit;
            }
            while ($row = mysqli_fetch_array($res)){
                ?>
                <li>
                    <a href="article.php?PID=<?php echo $row['pid']?>">
                        <h2><?php echo $row['title']?></h2>
                        <p><?php echo $row['preview']?></p>
                        <span class="am-icon-clock-o"><?php echo $row['date']?></span>
                        <span class="am-icon-book"><?php echo $row['flux']?></span>
                    </a>
                </li>
                <?php
            }
        }
        ?>
        </ul>
    </div>
    <div class="am-u-md-3">
        <?php
        include "sidebar.php";
        ?>
    </div>
</section>
</body>
<script src="../include/js/jquery.min.js"></script>
<script src="../include/js/amazeui.min.js"></script>
<script src="../include/blog/frame.js"></script>
</html>