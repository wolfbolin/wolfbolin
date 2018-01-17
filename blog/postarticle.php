<?php
/**
 * Created by PhpStorm.
 * User: wolfbolin
 * Date: 2018/1/15
 * Time: 1:31
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
    header("location: index.php");
    exit;
}
?>
<!doctype html>
<html>
<head>
    <?php
    $title = "Wolf Blog 上传文章";
    $attach = "<link rel=\"stylesheet\" href=\"../include/blog/frame.css\">\n<link rel=\"stylesheet\" href=\"../include/blog/postarticle.css\">";
    include '../include/blog/head.php';
    ?>
</head>
<body>
    <?php
    include "nav.php";
    ?>
    <section class="am-g am-g-fixed">
        <div class="am-u-md-9 am-panel am-panel-secondary wf-article-table">
            <h1>发表新的文章</h1>
            <hr data-am-widget="divider" style="" class="am-divider am-divider-default" />
            <p>请根据提示完成表单</p>
            <form action="addarticle.php" method="post"
                  class="am-form" enctype="multipart/form-data" data-am-validator>
                <fieldset>
                    <div class="am-form-group">
                        <label for="article-title">文章标题：</label>
                        <input type="text" id="article-title" name="article-title"
                               minlength="1" placeholder="请输入文章标题" required/>
                    </div>
                    <div class="am-form-group">
                        <label for="article-date">发布日期：</label>
                        <input type="text" id="article-date" name="article-date"
                               class="am-form-field" placeholder="请选择发布日期" data-am-datepicker readonly required />
                    </div>
                    <div class="am-form-group">
                        <label for="article-file">md文件</label>
                        <input type="file" id="article-file" name="article-file"
                               accept=".md" required/>
                    </div>
                    <div class="am-form-group">
                        <label>选择分类:</label>
                        <br/>
                        <label class="am-checkbox-inline">
                            <input type="checkbox" name="tag[]" value="服务器">服务器
                        </label>
                        <label class="am-checkbox-inline">
                            <input type="checkbox" name="tag[]" value="计算机">计算机
                        </label>
                        <label class="am-checkbox-inline">
                            <input type="checkbox" name="tag[]" value="嵌入式">嵌入式
                        </label>
                        <br/>
                        <label class="am-checkbox-inline">
                            <input type="checkbox" name="tag[]" value="教程">教程
                        </label>
                        <label class="am-checkbox-inline">
                            <input type="checkbox" name="tag[]" value="题解">题解
                        </label>
                        <br/>
                        <label class="am-checkbox-inline">
                            <input type="checkbox" name="tag[]" value="C++">C++
                        </label>
                        <label class="am-checkbox-inline">
                            <input type="checkbox" name="tag[]" value="Java">Java
                        </label>
                        <label class="am-checkbox-inline">
                            <input type="checkbox" name="tag[]" value="Python">Python
                        </label>
                        <label class="am-checkbox-inline">
                            <input type="checkbox" name="tag[]" value="PHP">PHP
                        </label>
                        <label class="am-checkbox-inline">
                            <input type="checkbox" name="tag[]" value="SQL">SQL
                        </label>
                        <label class="am-checkbox-inline">
                            <input type="checkbox" name="tag[]" value="其他语言">其他语言
                        </label>
                    </div>
                    <div class="am-form-group">
                        <label for="article-preview">预览：</label>
                        <textarea type="text" id="article-data" name="article-preview"
                                  minlength="1" maxlength="512" placeholder="文章概括" required></textarea>
                    </div>
                    <div class="am-form-group">
                        <label for="article-data">备注：</label>
                        <textarea type="text" id="article-data" name="article-data"
                                  placeholder="页脚备注"></textarea>
                    </div>
                    <button class="am-btn am-btn-secondary" type="submit">提交</button>
                </fieldset>
            </form>
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
</html>

