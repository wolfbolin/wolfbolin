<?php
/**
 * Created by PhpStorm.
 * User: wolfbolin
 * Date: 2018/1/13
 * Time: 13:23
 */
session_start();
$user = $right = null;
if(isset($_SESSION['account'])){
    $user = $_SESSION['account'];
}
if(isset($_SESSION['right'])){
    $right = $_SESSION['right'];
}
?>
<!doctype html>
<html>
<head>
    <?php
    $title = "Wolf Blog";
    $attach = "<link rel=\"stylesheet\" href=\"../include/blog/frame.css\">\n<link rel=\"stylesheet\" href=\"../include/blog/index.css\">";
    include '../include/blog/head.php';
    ?>
</head>
<body>
    <?php
    include "nav.php";
    ?>
    <section class="am-g am-g-fixed">
        <div class="am-u-md-9 am-panel am-panel-secondary wf-units">
            <div class="am-panel-hd">快速浏览</div>
            <ul class="am-list am-list-static wf-units-li">
                <?php
                include 'conn.php';
                /**
                 * 查询文章总数
                 * 根据每页十五篇文章计算页数
                 */
                $sql = "SELECT COUNT(pid) AS num FROM blog_article;";
                $res = mysqli_query($conn, $sql);
                $row = mysqli_fetch_array($res);
                $article_num = $row['num'];
                $page_num = ceil($article_num / 15.0);
                /**
                 * 获取当前页数参数
                 * 正则去除异常参数
                 */
                $page_index = 1;
                if(isset($_GET['page'])) {
                    $page_index = $_GET['page'];
                    $num_regex = "/^\d*$/";
                    if (!preg_match($num_regex, $page_index)) {
                        $page_index = 1;
                    }
                    if ($page_index < 1 || $page_index > $page_num) {
                        $page_index = 1;
                    }
                }
                /**
                 * 根据当前页数查询文章信息
                 */
                $begin_row = ($page_index-1)*15;
                $sql = "SELECT pid,title,preview,date,flux FROM blog_article ORDER BY date DESC LIMIT $begin_row,15;";
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
                include 'pagination.php';
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

