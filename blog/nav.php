<nav class="am-topbar wf-topbar">
    <h1 class="am-topbar-brand">
        <a href="#" class="am-text-ir">WolfBolin</a>
    </h1>

    <button class="am-topbar-btn am-topbar-toggle am-btn am-btn-sm am-btn-success am-show-sm-only" data-am-collapse="{target: '#doc-topbar-collapse'}"><span class="am-sr-only">导航切换</span> <span class="am-icon-bars"></span></button>

    <div class="am-collapse am-topbar-collapse" id="doc-topbar-collapse">
        <ul class="am-nav am-nav-pills am-topbar-nav">
            <?php
            $php_self = substr($_SERVER['PHP_SELF'],strrpos($_SERVER['PHP_SELF'],'/')+1);
            ?>
            <li <?php if($php_self==="index.php")echo "class=\"am-active\""?>><a href="index.php">博客首页</a></li>
            <li <?php if($php_self==="list.php")echo "class=\"am-active\""?>><a href="list.php">文章列表</a></li>
            <li class="am-dropdown" data-am-dropdown>
                <a class="am-dropdown-toggle" data-am-dropdown-toggle href="javascript:;">
                    标签分类 <span class="am-icon-caret-down"></span>
                </a>
                <ul class="am-dropdown-content">
                    <li class="am-dropdown-header">按平台</li>
                    <li><a href="list.php?tag=服务器">服务器</a></li>
                    <li><a href="list.php?tag=计算机">计算机</a></li>
                    <li><a href="list.php?tag=嵌入式">嵌入式</a></li>
                    <li class="am-divider"></li>
                    <li class="am-dropdown-header">按类型</li>
                    <li><a href="list.php?tag=教程">教程</a></li>
                    <li><a href="list.php?tag=题解">题解</a></li>
                    <li class="am-divider"></li>
                    <li class="am-dropdown-header">按语言</li>
                    <li><a href="list.php?tag=C%2B%2B">C++</a></li>
                    <li><a href="list.php?tag=Java">Java</a></li>
                    <li><a href="list.php?tag=Python">Python</a></li>
                    <li><a href="list.php?tag=PHP">PHP</a></li>
                    <li><a href="list.php?tag=SQL">SQL</a></li>
                    <li><a href="list.php?tag=其他语言">其他语言</a></li>
                </ul>
            </li>
            <?php
            if($user === "wolfbolin" && $right === "root"){?>
                <li <?php if($php_self==="postarticle.php")echo "class=\"am-active\""?>><a href="postarticle.php">发布博客</a></li>
            <?php
            }
            ?>
        </ul>
        <!--暂无该功能
        <div class="am-topbar-right">

            <form class="am-topbar-form am-topbar-left am-form-inline" role="search">
                <div class="am-form-group">
                    <input type="text" class="am-form-field am-input-sm" placeholder="搜索">
                </div>
            </form>
            <div class="am-dropdown" data-am-dropdown="{boundary: '.am-topbar'}">
                <button class="am-btn am-btn-secondary am-topbar-btn am-btn-sm am-dropdown-toggle" data-am-dropdown-toggle>其他 <span class="am-icon-caret-down"></span></button>
                <ul class="am-dropdown-content">
                    <li><a href="#">注册</a></li>
                    <li><a href="#">随便看看</a></li>
                </ul>
            </div>
        </div>-->
        <div class="am-topbar-right">
            <?php
            if($user === "wolfbolin"){
                //多用户时此处需要修改为根据不同用户显示不同头像
                ?>
                <img class="am-circle wf-avatar" src="../include/blog/logo-inverse.jpg"/>
                <button class="am-btn am-btn-success am-topbar-btn am-btn-sm" id="logout-btn">注销</button>
                <?php
            }else{
                ?>
                <button class="am-btn am-btn-primary am-topbar-btn am-btn-sm" id="login-modal-btn">登录</button>
                <?php
            }
            ?>
        </div>
    </div>
</nav>
<div class="am-modal am-modal-prompt" tabindex="-1" id="login-modal">
    <div class="am-modal-dialog">
        <div class="am-modal-hd">Wolfbolin.com</div>
        <div class="am-modal-bd">
            请使用帐号密码登录
            <input type="text" class="am-modal-prompt-input"
                   placeholder="用户名" required/>
            <input type="password" class="am-modal-prompt-input"
                   placeholder="密码" required/>
        </div>
        <div class="am-modal-footer">
            <span class="am-modal-btn" data-am-modal-cancel>取消</span>
            <span class="am-modal-btn" data-am-modal-confirm>登录</span>
        </div>
    </div>
</div>
<div class="am-modal am-modal-loading am-modal-no-btn" tabindex="-1" id="wf-loading">
    <div class="am-modal-dialog">
        <div class="am-modal-hd" id="wf-loading-text">登录中...</div>
        <div class="am-modal-bd">
            <span class="am-icon-spinner am-icon-spin"></span>
        </div>
    </div>
</div>
<div class="am-modal am-modal-alert" tabindex="-1" id="wf-alert">
    <div class="am-modal-dialog">
        <div class="am-modal-hd">Wolfbolin.com</div>
        <div class="am-modal-bd" id="wf-alert-text">
            Hello world！
        </div>
        <div class="am-modal-footer">
            <span class="am-modal-btn">确定</span>
        </div>
    </div>
</div>
<header class="am-g wf-header">
    <div class="am-g-fixed am-u-md-12 am-u-lg-centered wf-header-title">
        <h1>Wolf Blog</h1>
        <h3>一只软件萌新的进阶之路</h3>
    </div>
</header>