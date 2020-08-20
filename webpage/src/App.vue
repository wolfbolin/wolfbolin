<template>
    <div id="app">
        <!-- 祖传导航栏 -->
        <header class="wb-nav">
            <div class="inner">
                <div class="float-left">
                    <img :src="logo_src" alt="logo"/>
                </div>
                <div class="float-right">
                    <ul class="menu">
                        <li v-for="item in nav_list" :key="item.id" :class="item.class">
                            <a href="javascript:void(0);" v-on:click="switch_page(item.href)">{{ item.label }}</a>
                        </li>
                    </ul>
                </div>
            </div>
        </header>

        <!-- 页面内容 -->
        <router-view/>

        <!-- 祖传页脚 -->
        <footer class="wb-footer">
            <div class="inner">
                <p class="copyright" v-if="run_env==='desktop'">
                    CopyRight © 2017-2020 WolfBolin.All Rights Reserved.
                </p>
                <p class="copyright" v-if="run_env==='phone'">
                    CopyRight © 2017-2020 WolfBolin.<br/>All Rights Reserved.
                </p>
                <a href="http://www.miitbeian.gov.cn" class="icp">豫ICP备19033794号</a>
            </div>
        </footer>
    </div>
</template>

<script>
    export default {
        name: 'app',
        data() {
            return {
                run_env: "desktop",
                logo_src: "",
                nav_list: [
                    {"id": "index", "href": "/", "label": "主页", "class": ""},
                    // {"id": "note", "href": "/note", "label": "笔记", "class": ""},
                    // {"id": "blog", "href": "http://blog.wolfbolin.com", "label": "博客", "class": ""},
                    // {"id": "album", "href": "/album", "label": "相册", "class": ""},
                    // {"id": "tools", "href": "/tools", "label": "工具", "class": ""}
                ],
            }
        },
        methods: {
            app_init: function () {
                console.log(
                    " __          __   _  __ ____        _ _  \n" +
                    " \\ \\        / /  | |/ _|  _ \\      | (_)  \n" +
                    "  \\ \\  /\\  / /__ | | |_| |_) | ___ | |_ _ __  \n" +
                    "   \\ \\/  \\/ / _ \\| |  _|  _ < / _ \\| | | '_ \\  \n" +
                    "    \\  /\\  / (_) | | | | |_) | (_) | | | | | |  \n" +
                    "     \\/  \\/ \\___/|_|_| |____/ \\___/|_|_|_| |_|  \n" +
                    "=================================================");
                console.log("Designed by WolfBolin ~ \nContact me at: mailto@wolfbolin.com");
                // 确定后台服务地址
                if (window.location.host.indexOf("localhost") !== -1) {
                    this.$store.commit("modify_host", "http://127.0.0.1:12880");
                } else if (window.location.host.indexOf("127.0.0.1") !== -1) {
                    this.$store.commit("modify_host", "http://127.0.0.1:12880");
                } else {
                    this.$store.commit("modify_host", "http://core.wolfbolin.com");
                }
                console.log("Connect to:", this.$store.state.host);
                // 设置激活导航栏
                this.set_active_nav()
                let clientWidth = document.documentElement.clientWidth;
                if (clientWidth < 768) {
                    this.logo_src = require("@/assets/img/logo_nav-s.png");
                } else {
                    this.logo_src = require("@/assets/img/logo_nav.png");
                }
            },
            switch_page: function (path) {
                console.log("switch_page:", path);
                if (this.$route.path !== path) {
                    this.$router.push(path);
                }
                this.set_active_nav()
            },
            set_active_nav: function () {
                let path_prefix = this.$route.path.split("/")[1];
                path_prefix = "/" + path_prefix;
                for (let item of this.nav_list) {
                    if (path_prefix === item.href) {
                        item.class = 'active';
                    } else {
                        item.class = '';
                    }
                }
            }
        },
        watch: {
            '$route.path': function (to) {
                this.switch_page(to);
            }
        },
        mounted: function () {
            this.app_init();
        }
    }
</script>

<style lang="scss">
    html, body {
        margin: 0;
        padding: 0;
    }

    .inner {
        max-width: 1180px;
        margin: 0 auto;
    }

    .wb-nav {
        width: 100%;
        height: 64px;
        z-index: 100;
        position: fixed;
        font-weight: 200;
        background-color: #404040;

        .menu {
            margin: 0 1em;
        }

        .float-left {
            float: left;

            img {
                height: 40px;
                padding-top: 15px;
            }

            @media screen and (max-width: 768px) {
                img {
                    padding: 15px 10px;
                }
            }
        }

        .float-right {
            float: right;

            .active {
                color: #91BEF0;
                border-bottom: 4px solid #91BEF0;
            }

            li {
                height: 60px;
                color: white;
                display: inline-block;
                text-align: -webkit-match-parent;
            }

            a {
                color: inherit;
                padding: 0 20px;
                line-height: 60px;
                text-decoration: none;
            }

            @media screen and (max-width: 768px) {
                a {
                    padding: 0 5px;
                }
            }
        }


    }

    .wb-footer {
        background-color: #505050;

        .copyright {
            margin: 0;
            color: #B0B0B0;
            padding: 10px;
            display: block;
            text-align: center;
        }

        .icp {
            margin: 0;
            color: #B0B0B0;
            display: block;
            text-align: center;
            padding-bottom: 5px;
        }
    }
</style>

