<?php
/**
 * Created by PhpStorm.
 * User: wolfbolin
 * Date: 2018/1/14
 * Time: 18:36
 */
?>
<div class="am-panel am-panel-secondary">
    <div class="am-panel-hd">资料卡</div>
    <div class="am-panel-bd">
        <a href="" class="wf-introduction">
            <img class="am-circle" src="../include/blog/logo-inverse.jpg" width="60" height="60"/>
            <span>WolfBolin</span>
        </a>
    </div>
    <footer class="am-panel-footer wf-data">
        <?php
        $sql = "SELECT COUNT(pid) AS num FROM blog_article;";
        $res = mysqli_query($conn, $sql);
        $row = mysqli_fetch_array($res);
        $article_num = $row['num'];
        $sql = "SELECT SUM(flux) as flux FROM blog_article;";
        $res = mysqli_query($conn, $sql);
        $row = mysqli_fetch_array($res);
        ?>
        <p>文章：<span><?php echo $article_num?></span></p>
        <p>阅读：<span><?php echo $row['flux']?></span></p>
    </footer>
</div>
<div class="am-panel am-panel-secondary">
    <div class="am-panel-hd">文章分类</div>
    <div class="am-panel-bd">
        <a class="am-btn am-btn-default am-round
        wf-tag" href="list.php?tag=服务器">服务器</a>
        <a class="am-btn am-btn-default am-round
        wf-tag" href="list.php?tag=计算机">计算机</a>
        <a class="am-btn am-btn-default am-round
        wf-tag" href="list.php?tag=嵌入式">嵌入式</a>
        <a class="am-btn am-btn-default am-round
        wf-tag" href="list.php?tag=教程">教程</a>
        <a class="am-btn am-btn-default am-round
        wf-tag" href="list.php?tag=题解">题解</a>
        <a class="am-btn am-btn-default am-round
        wf-tag" href="list.php?tag=C%2B%2B">C++</a>
        <a class="am-btn am-btn-default am-round
        wf-tag" href="list.php?tag=Java">Java</a>
        <a class="am-btn am-btn-default am-round
        wf-tag" href="list.php?tag=Python">Python</a>
        <a class="am-btn am-btn-default am-round
        wf-tag" href="list.php?tag=PHP">PHP</a>
        <a class="am-btn am-btn-default am-round
        wf-tag" href="list.php?tag=SQL">SQL</a>
        <a class="am-btn am-btn-default am-round
        wf-tag" href="list.php?tag=其他语言">其他语言</a>
    </div>
</div>
<div class="am-panel am-panel-secondary">
    <div class="am-panel-hd">最新文章</div>
    <ul class="am-list am-list-static wf-recent">
        <?php
        $sql = "SELECT pid,title FROM blog_article ORDER BY date DESC LIMIT 10;";
        $res = mysqli_query($conn, $sql);
        while ($row = mysqli_fetch_array($res)){
            ?>
            <li><a href="article.php?PID=<?php echo $row['pid'];?>"><?php echo $row['title'];?></a></li>
            <?php
        }
        ?>
    </ul>
</div>
