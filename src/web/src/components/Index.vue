<template>
    <div id="index-page">
        <!--网页封面-->
        <section class="wb-cover">
            <div ref="cover" :style="{padding: coverPadding}">
                <h3>{{ $t("i18n.motto") }}</h3>
                <h1>WolfBolin</h1>
                <a>{{ $t("i18n.explore") }}</a>
            </div>
        </section>
        <!--网页第一模块-你好世界-->
        <section class="wb-white-section">
            <div class="inner">
                <div class="title">
                    <h3>WOLFBOLIN</h3>
                    <h1>{{ $t("i18n.section1_title") }}</h1>
                </div>
                <el-row :gutter="40">
                    <el-col class="item" :xs="24" :sm="12">
                        <h3>{{ $t("i18n.section1_subhead1") }}</h3>
                        <p>{{ $t("i18n.section1_content1") }}</p>
                    </el-col>
                    <el-col class="item" :xs="24" :sm="12">
                        <h3>{{ $t("i18n.section1_subhead2") }}</h3>
                        <p>{{ $t("i18n.section1_content2") }}</p>
                    </el-col>
                    <el-col class="item" :xs="24" :sm="12">
                        <h3>{{ $t("i18n.section1_subhead3") }}</h3>
                        <p>{{ $t("i18n.section1_content3") }}</p>
                    </el-col>
                    <el-col class="item" :xs="24" :sm="12">
                        <h3>{{ $t("i18n.section1_subhead4") }}</h3>
                        <p>{{ $t("i18n.section1_content4") }}</p>
                    </el-col>
                </el-row>
            </div>
        </section>
        <!--网页第二模块-凝聚时光-->
        <section class="wb-gray-section">
            <div class="inner">
                <div class="title">
                    <h3>GALLERY</h3>
                    <h1>{{ $t("i18n.section2_title") }}</h1>
                </div>
                <el-carousel :height="galleryHeight" ref="gallery">
                    <el-carousel-item v-for="(item, index) in photoGallery" :key="index">
                        <img width="100%" :src="item"/>
                    </el-carousel-item>
                </el-carousel>
            </div>
        </section>
        <!--网页第三模块-最新动向-->
        <section class="wb-white-section">
            <div class="inner">
                <div class="title">
                    <h3>TREND</h3>
                    <h1>{{ $t("i18n.section3_title") }}</h1>
                </div>
                <el-row :gutter="40">
                    <el-col class="item" :xs="24" :sm="12">
                        <h3>{{ $t("i18n.section3_subhead1") }}</h3>
                        <p>{{ $t("i18n.section3_content1") }}</p>
                    </el-col>
                    <el-col class="item" :xs="24" :sm="12">
                        <h3>{{ $t("i18n.section3_subhead2") }}</h3>
                        <p>{{ $t("i18n.section3_content2") }}</p>
                    </el-col>
                    <el-col class="item" :xs="24" :sm="12">
                        <h3>{{ $t("i18n.section3_subhead3") }}</h3>
                        <p>{{ $t("i18n.section3_content3") }}</p>
                    </el-col>
                    <el-col class="item" :xs="24" :sm="12">
                        <h3>{{ $t("i18n.section3_subhead4") }}</h3>
                        <p>{{ $t("i18n.section3_content4") }}</p>
                    </el-col>
                </el-row>
            </div>
        </section>
        <!--网页第四模块-进阶之路-->
        <section class="wb-gray-section">
            <div class="inner">
                <div class="title">
                    <h3>GROWTH</h3>
                    <h1>{{ $t("i18n.section4_title") }}</h1>
                </div>
                <ul class="timeline">
                    <li v-for="index in this.$t('i18n.section4_data')">
                        <div :class=index.class>
                            <div class="flag-wrapper">
                                <span class="flag"><a :href=index.link>{{ index.title }}</a></span>
                                <span class="time-wrapper"><span class="time">{{ index.time }}</span></span>
                            </div>
                            <div class="desc">{{ index.content }}</div>
                        </div>
                    </li>
                </ul>
            </div>
        </section>
        <!--网页第五模块-个人博客-->
        <section class="wb-white-section">
            <div class="inner">
                <div class="title">
                    <h3>BLOG</h3>
                    <h1>{{ $t("i18n.section5_title") }}</h1>
                </div>
                <el-row :gutter="40">
                    <el-col class="card" :xs="24" :sm="12" v-for="(item, index) in articleBox" :key="index">
                        <el-card>
                            <div slot="header">
                                <span>{{ item.title }}</span>
                                <el-button class="button" type="text" @click="openLink(item.link)">查看全文</el-button>
                            </div>
                            <p>{{ item.content }}</p>
                            <div>
                                <p class="blog-time">{{ item.time }}</p>
                                <template v-for="tag in item.category">
                                    <div class="blog-tag" @click="openLink(tag.link)">
                                        <el-tag>{{ tag.name }}</el-tag>
                                    </div>
                                </template>
                            </div>
                        </el-card>
                    </el-col>
                </el-row>
            </div>
        </section>
        <!--网页第六模块-与我联系-->
        <section class="wb-gray-section">
            <div class="inner">
                <div class="title">
                    <h3>LINK</h3>
                    <h1>{{ $t("i18n.section6_title") }}</h1>
                </div>
                <el-row :gutter="40">
                    <el-col class="item link-box" :xs="24" :sm="10">
                        <div class="text">
                            <h3>{{ $t("i18n.section6_subhead1") }}</h3>
                            <p>{{ $t("i18n.section6_content1") }}</p>
                        </div>
                    </el-col>
                    <el-col class="item link-box" :xs="24" :sm="14">
                        <el-row :gutter="40">
                            <el-col :xs="12" :sm="6" class="icon-box">
                                <a href="https://blog.csdn.net/qq_36731677" target="_blank">
                                    <img class="icon" src="../assets/csdn.png"/>
                                </a>
                            </el-col>
                            <el-col :xs="12" :sm="6" class="icon-box">
                                <a href="https://github.com/wolfbolin" target="_blank">
                                    <img class="icon" src="../assets/github.png"/>
                                </a>
                            </el-col>
                            <el-col :xs="12" :sm="6" class="icon-box">
                                <a href="https://space.bilibili.com/72835041/#/" target="_blank">
                                    <img class="icon" src="../assets/bilibili.png"/>
                                </a>
                            </el-col>
                            <el-col :xs="12" :sm="6" class="icon-box">
                                <a href="mailto:admin@wolfbolin.com">
                                    <img class="icon" src="../assets/gmail.png"/>
                                </a>
                            </el-col>
                        </el-row>
                    </el-col>
                </el-row>
            </div>
        </section>
        <!--网页第七模块-合作伙伴-->
        <section class="wb-white-section">
            <div class="inner">
                <div class="title">
                    <h3>FRIEND</h3>
                    <h1>{{ $t("i18n.section7_title") }}</h1>
                </div>
                <el-row :gutter="40">
                    <el-col class="item" :xs="24" :sm="12">
                        <h3>{{ $t("i18n.section7_subhead1") }}</h3>
                        <p>{{ $t("i18n.section7_content1") }}</p>
                    </el-col>
                    <el-col class="item" :xs="24" :sm="12">
                        <h3>{{ $t("i18n.section7_subhead2") }}</h3>
                        <p>{{ $t("i18n.section7_content2") }}<br/>
                            {{ $t("i18n.section7_blog") }}：
                            <a href="https://csuwangj.github.io/" target="_blank">https://csuwangj.github.io/</a><br/>
                            {{ $t("i18n.section7_blog") }}：
                            <a href="https://zickshen.github.io/" target="_blank">https://zickshen.github.io/</a></p>
                    </el-col>
                </el-row>
                <el-row :gutter="40">
                    <el-col class="item" :xs="24" :sm="12">
                        <h3>{{ $t("i18n.section7_subhead3") }}</h3>
                        <p>{{ $t("i18n.section7_content3") }}<br/>
                            {{ $t("i18n.section7_index") }}：
                            <a href="https://www.admirable.one/" target="_blank">https://www.admirable.one/</a><br/>
                            {{ $t("i18n.section7_blog") }}：
                            <a href="https://www.tail0r.com/" target="_blank">https://www.tail0r.com/</a>
                        </p>
                    </el-col>
                    <el-col class="item" :xs="24" :sm="12">
                        <h3>{{ $t("i18n.section7_subhead4") }}</h3>
                        <p>{{ $t("i18n.section7_content4") }}<br/>
                            张洺豪DragonHao：
                            <a href="http://www.dragonhao.cn/" target="_blank">http://www.dragonhao.cn/</a><br/>
                            楼远洋yylou：
                            <a href="http://www.yylou15.cn/" target="_blank">http://www.yylou15.cn/</a>
                        </p>
                    </el-col>
                </el-row>
            </div>
        </section>
    </div>
</template>

<script>
    export default {
        name: "Index",
        data() {
            return {
                coverPadding: '',
                galleryHeight: '',
                photoGallery: ['./static/img/index-photo1.jpg', './static/img/index-photo2.jpg',
                    './static/img/index-photo3.jpg', './static/img/index-photo4.jpg'],
                articleBox: [{
                    title: '示例标题一',
                    link: 'https://blog.wolfbolin.com',
                    content: '假设这里有一篇很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长的文章介绍',
                    time: '1970-00-00 00:08:00',
                    category: [
                        {
                            name: '标签一',
                            link: 'https://blog.wolfbolin.com'
                        }
                    ]
                }, {
                    title: '示例标题二',
                    link: 'https://blog.wolfbolin.com',
                    content: '假设这里有一篇很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长的文章介绍',
                    time: '1970-00-00 00:08:00',
                    category: [
                        {
                            name: '标签二',
                            link: 'https://blog.wolfbolin.com'
                        }
                    ]
                }]
            }
        },
        mounted() {
            this.updateArticle();
            this.setCoverPadding();
            this.setGalleryHeight();
        },
        methods: {
            openLink: function (url) {
                window.open(url);
            },
            setCoverPadding: function () {
                let clientHeight = document.documentElement.clientHeight;
                let titleHeight = this.$refs.cover.clientHeight;
                let padding = (clientHeight - titleHeight) / 2;
                this.coverPadding = `${padding}px 0px`;
            },
            setGalleryHeight: function () {
                let imageWidth = this.$refs.gallery.$el.clientWidth;
                let imageHeight = 0.5625 * imageWidth;
                this.galleryHeight = `${imageHeight}px`;
            },
            updateArticle: function () {
                let that = this;
                this.$http.get('https://wolfbolin.com/server/getArticle.php')
                    .then(function (response) {
                        if (response.data.result === 'AC') {
                            that.articleBox = response.data.card;
                        } else {
                            that.$notify({
                                title: '警告',
                                message: '服务器异常，博客文章更新失败',
                                type: 'warning',
                                position: 'bottom-right'
                            });
                        }
                    })
                    .catch(function (err) {
                        that.$notify.error({
                            title: '错误',
                            message: '您似乎与服务器断开链接，博客文章更新失败',
                            position: 'bottom-right'
                        });
                    });
            }
        }
    }
</script>

<style scoped lang="scss">
    @import "../../static/css/timeline.css";
    @font-face {
        font-family: 'BMXY-EN';
        src: url('../../static/fonts/BMXY-EN.ttf') format("truetype");
    }
    @font-face {
        font-family: 'FZXY-CUT';
        src: url('../../static/fonts/FZXY-CUT.ttf');
    }

    #index-page {
        font-family: 'FZXY-CUT', sans-serif;
        .inner {
            max-width: 1140px;
            margin: 0 auto;
            padding: 36px 40px 72px 40px;
        }
        .wb-cover {
            text-align: center;
            @media only screen and (max-width: 767px) {
                h3 {
                    font-size: 1em;
                }
                h1 {
                    font-size: 3em;
                }
            }
            @media only screen and (min-width: 768px) {
                h3 {
                    font-size: 1.5em;
                }
                h1 {
                    font-size: 6em;
                }
            }
            h3 {
                line-height: 40px;
                font-weight: 400;
                letter-spacing: 2px;
                color: #404040;
                margin: 0;
            }
            h1 {
                font-family: 'BMXY-EN', sans-serif;
                line-height: 90px;
                font-weight: 400;
                letter-spacing: 8px;
                color: #404040;
                margin: 30px 0 20px 0;
            }
            a {
                display: inline-block;
                font-size: 15px;
                font-weight: 400;
                color: #404040;
                padding: .5em 1em;
                border-radius: 1000px;
                background-color: transparent;
                border: 1px solid #404040;
                cursor: pointer;
            }
        }
        .item {
            h3 {
                color: #404040;
            }
            p {
                color: #404040;
                line-height: 26px;
            }
            a {
                color: #66b1ff;
                text-decoration: none;
            }
        }
        .link-box {
            &:before {
                content: '';
                display: inline-block;
                height: 100%;
                vertical-align: middle;
            }
            .icon-box {
                text-align: center;
                margin-bottom: 30px;
            }
            .text {
                display: inline-block;
                vertical-align: middle;
            }
            .icon {
                display: inline-block;
                vertical-align: middle;
                border-radius: 25%;
                width: 100px;
                height: 100px;
            }
        }
        .card {
            padding: 20px 0;
            .button {
                float: right;
                padding: 3px 0
            }
            .blog-time {
                display: inline-block;
            }
            .blog-tag {
                float: right;
                margin: 10px 2px;
                cursor: pointer;
            }
        }
        .wb-white-section {
            background-color: rgba(255, 255, 255, 0.7);
            .title {
                text-align: center;
                h3 {
                    color: #404040;
                    font-weight: 100;
                    font-size: 28px;
                }
                h1 {
                    color: #66b1ff;
                    font-weight: 400;
                    font-size: 38px;
                }
            }
        }
        .wb-gray-section {
            background-color: rgba(204, 204, 204, 0.7);
            .title {
                text-align: center;
                h3 {
                    color: #404040;
                    font-weight: 100;
                    font-size: 28px;
                }
                h1 {
                    color: #ffffff;
                    font-weight: 400;
                    font-size: 38px;
                }
            }
        }
        .timeline {
            .time, .desc {
                font-size: 0.9em;
            }
            @media screen and (max-width: 660px) {
                .desc {
                    background: rgba(245, 245, 245, 0.9);
                    border-radius: 10px;
                }
            }
        }
    }
</style>
