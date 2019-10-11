<template>
    <div id="app">
        <!-- 祖传导航栏 -->
        <header class="wb-nav">
            <div class="inner">
                <div class="float-left">
                    <img v-if="user_agent==='pc'" src="./assets/logo_nav.png" alt="logo"/>
                    <img v-if="user_agent==='phone'" src="./assets/logo_nav-s.png" alt="logo"/>
                </div>
                <div class="float-right">
                    <ul class="menu">
                        <li v-for="item in nav_list" :key="item.id" :class="item.class">
                            <a href="javascript:void(0);" v-on:click="page_switch(item.href)">{{ item.label }}</a>
                        </li>
                    </ul>
                </div>
            </div>
        </header>

        <router-view/>

        <!-- 祖传页脚 -->
        <footer class="wb-footer">
            <div class="inner">
                <p class="copyright" v-if="user_agent==='pc'">
                    CopyRight © 2017-2020 WolfBolin.All Rights Reserved.
                </p>
                <p class="copyright" v-if="user_agent==='phone'">
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
                user_agent: 'pc',
                nav_list: [
                    {"id": "index", "href": "/", "name": "index", "label": "主页", "class": ""},
                    {"id": "note", "href": "/note", "name": "", "label": "笔记", "class": ""},
                    {"id": "blog", "href": "/blog", "name": "", "label": "博客", "class": ""},
                    {"id": "album", "href": "/album", "name": "", "label": "相册", "class": ""},
                    {"id": "tools", "href": "/tools", "name": "tools", "label": "工具", "class": ""}
                ],
            }
        },
        methods: {
            page_switch: function (path) {
                if (this.$route.path !== path) {
                    this.$router.push(path);
                }
                for (let item of this.nav_list) {
                    if (this.$route.name === item.name) {
                        item.class = 'active';
                    } else {
                        item.class = '';
                    }
                }
            },
            set_nav_logo: function () {
                let clientWidth = document.documentElement.clientWidth;
                if (clientWidth < 768) {
                    this.user_agent = "phone"
                } else {
                    this.user_agent = "pc"
                }
            }
        },
        watch: {
            '$route.path': function (to) {
                this.page_switch(to);
            }
        },
        mounted: function () {
            console.log(
                " __          __   _  __ ____        _ _  \n" +
                " \\ \\        / /  | |/ _|  _ \\      | (_)  \n" +
                "  \\ \\  /\\  / /__ | | |_| |_) | ___ | |_ _ __  \n" +
                "   \\ \\/  \\/ / _ \\| |  _|  _ < / _ \\| | | '_ \\  \n" +
                "    \\  /\\  / (_) | | | | |_) | (_) | | | | | |  \n" +
                "     \\/  \\/ \\___/|_|_| |____/ \\___/|_|_|_| |_|  \n" +
                "=================================================");
            console.log("Designed by WolfBolin ~ \nContact me at: mailto@wolfbolin.com");
            this.page_switch(this.$route.path);
            this.set_nav_logo();
        }
    }
</script>

<style lang="scss">
    html, body {
        margin: 0;
        padding: 0;
    }

    .inner {
        max-width: 1140px;
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
            color: #91BEF0;
            padding: 10px;
            display: block;
            text-align: center;
        }

        .icp {
            margin: 0;
            color: #91BEF0;
            display: block;
            text-align: center;
            padding-bottom: 5px;
        }
    }
</style>

