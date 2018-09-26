<template>
    <div id="app">
        <!--祖传导航栏-->
        <div class="wb-navbar">
            <el-row class="inner">
                <el-col :span="6" class="logo">
                    <img src="./assets/WolfBolin.png"/></el-col>
                <el-col :span="18" hidden-sm-and-up>
                    <el-menu
                        :default-active="activeIndex"
                        mode="horizontal"
                        class="menu"
                        @select="handleSelect"
                        background-color="#404040"
                        text-color="#ffffff"
                        active-text-color="#0080ff">
                        <el-menu-item index="index" class="hidden-xs-only">{{ $t("i18n.index") }}</el-menu-item>
                        <el-menu-item index="gallery" class="hidden-xs-only">{{ $t("i18n.gallery") }}</el-menu-item>
                        <!--<el-menu-item index="project" class="hidden-xs-only">{{ $t("i18n.project") }}</el-menu-item>-->
                        <el-menu-item index="blog" class="hidden-xs-only">{{ $t("i18n.blog") }}</el-menu-item>
                        <el-submenu index="box" class="hidden-sm-and-up">
                            <template slot="title">菜单</template>
                            <el-menu-item index="index">{{ $t("i18n.index") }}</el-menu-item>
                            <el-menu-item index="gallery">{{ $t("i18n.gallery") }}</el-menu-item>
                            <!--<el-menu-item index="project">{{ $t("i18n.project") }}</el-menu-item>-->
                            <el-menu-item index="blog">{{ $t("i18n.blog") }}</el-menu-item>
                        </el-submenu>
                    </el-menu>
                </el-col>
            </el-row>
        </div>
        <!--此处利用路由自动呈现不同的内容-->
        <div class="wb-content">
            <div class="inner">
                <router-view/>
            </div>
        </div>
        <!--统一的页脚-->
        <footer class="wb-footer">
            <p class="copyright">CopyRight © 2018 WolfBolin. All Rights Reserved.</p>
            <a href="http://www.miitbeian.gov.cn" class="icp">湘ICP备17015330号</a>
        </footer>
    </div>
</template>

<script>
    import 'element-ui/lib/theme-chalk/display.css';

    export default {
        name: 'App',
        data() {
            return {
                activeIndex: 'index'
            }
        },
        methods: {
            handleSelect(key) {
                if (key === 'index') {
                    this.$router.push('/');
                // } else if (key === 'project') {
                //     this.$router.push('/project');
                } else if (key === 'blog') {
                    // window.location.href="http://blog.wolfbolin.com"
                    window.open("http://blog.wolfbolin.com");
                } else {
                    this.$router.push('/building');
                }
            }
        }
    }
</script>

<style lang="scss">
    @font-face {
        font-family: 'FZXY-CUT';
        src: url('../static/fonts/FZXY-CUT.ttf');
    }

    html, body {
        margin: 0;
        padding: 0;
    }

    #app {
        .wb-navbar {
            font-family: 'FZXY-CUT', sans-serif;
            background-color: #404040;
            position: fixed;
            z-index: 100;
            height: 60px;
            width: 100%;
            .inner {
                max-width: 1140px;
                margin: 0 auto;
            }
            .logo {
                padding-top: 16px;
                img {
                    height: 40px;
                }
            }
            .menu {
                float: right;
            }
            .el-menu--horizontal {
                border-bottom: none;
            }
        }

        .wb-content {
            background: url(./assets/background.jpg) no-repeat fixed top center;
            background-size: cover;
            position: relative;
        }

        .wb-footer {
            background-color: #353535;
            p, a {
                margin: 0;
                display: block;
                text-align: center;
            }
            .copyright {
                color: #888888;
                padding: 10px;
            }
            .icp {
                color: #666666;
                padding-bottom: 5px;
            }
        }
    }

</style>
