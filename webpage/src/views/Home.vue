<template>
    <div class="wb-home">
        <section class="wb-cover" :style="{padding: coverPadding}">
            <div ref="cover" class="inner">
                <p>嗜之越笃 技巧越工</p>
                <h1>WolfBolin</h1>
            </div>
        </section>

        <section class="wb-light-section">
            <div class="inner">
                <div class="title">
                    <p>Hello,world!</p>
                    <h2>你好,世界!</h2>
                </div>
                <div class="wb-desc">
                    <el-row v-for="(row, row_index) in home_data.section1.content" :key="row_index" class="row">
                        <el-col v-for="(col, col_index) in row" :key="col_index" :xs="24" :sm="12" class="col">
                            <h3>{{ col.title }}</h3>
                            <p>{{ col.text }}</p>
                        </el-col>
                    </el-row>
                </div>
            </div>
        </section>

        <section class="wb-blue-section">
            <div class="inner">
                <div class="title">
                    <p>{{home_data.section2.title.subtitle}}</p>
                    <h2>{{home_data.section2.title.title}}</h2>
                </div>
                <div class="wb-desc">
                    <el-carousel arrow="hover" ref="gallery" :height="galleryHeight">
                        <el-carousel-item v-for="(item, index) in home_data.section2.content" :key="index">
                            <img :src="item.src" :alt="item.title"/>
                        </el-carousel-item>
                    </el-carousel>
                </div>
            </div>
        </section>

        <section class="wb-light-section">
            <div class="inner">
                <div class="title">
                    <p>{{home_data.section3.title.subtitle}}</p>
                    <h2>{{home_data.section3.title.title}}</h2>
                </div>
                <div class="wb-desc">
                    <el-row v-for="(row, row_index) in home_data.section3.content" :key="row_index" class="row">
                        <el-col v-for="(col, col_index) in row" :key="col_index" :xs="24" :sm="12" class="col">
                            <h3>{{ col.title }}</h3>
                            <p>{{ col.text }}</p>
                        </el-col>
                    </el-row>
                </div>
            </div>
        </section>

        <section class="wb-blue-section">
            <div class="inner">
                <div class="title">
                    <p>{{home_data.section4.title.subtitle}}</p>
                    <h2>{{home_data.section4.title.title}}</h2>
                </div>
                <div class="wb-timeline" ref="timeline">
                    <ul class="tl-timeline" :style="auto_timeline">
                        <li v-for="(item, index) in home_data.section4.content" :key="index">
                            <div class="tl-direction-l" :style="auto_timeline_item" v-if="index%2!==0">
                                <div class="tl-flag-wrapper">
                                <span class="tl-flag">
                                    <a :href="item.link">{{ item.title }}</a>
                                </span>
                                    <span class="tl-time-wrapper">
                                    <span class="tl-time">{{ item.time }}</span>
                                </span>
                                </div>
                                <div class="tl-desc">{{ item.text }}</div>
                            </div>

                            <div class="tl-direction-r" :style="auto_timeline_item" v-if="index%2===0">
                                <div class="tl-flag-wrapper">
                                <span class="tl-flag">
                                    <a :href="item.link">{{ item.title }}</a>
                                </span>
                                    <span class="tl-time-wrapper">
                                    <span class="tl-time">{{ item.time }}</span>
                                </span>
                                </div>
                                <div class="tl-desc">{{ item.text }}</div>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </section>

        <section class="wb-light-section">
            <div class="inner">
                <div class="title">
                    <p>{{home_data.section5.title.subtitle}}</p>
                    <h2>{{home_data.section5.title.title}}</h2>
                </div>
                <div v-if="blog_data===null">
                    <p style="font-size: 2em; text-align: center">T_T 嘤嘤嘤，数据加载失败了</p>
                </div>
                <div class="wb-desc" v-else>
                    <el-timeline>
                        <template v-for="item in blog_data">
                            <el-timeline-item :key="item.title" :timestamp="item.time" placement="top">
                                <el-card class="wb-card">
                                    <div slot="header">
                                        <a class="title" :href="item.link">{{item.title}}</a>
                                    </div>
                                    <p>{{item.desc}}</p>
                                    <div class="tag-box">
                                        <el-tag size="small" type="info" v-for="tag in item.tags" :key="tag[0]">
                                            <a :href="tag[0]">{{tag[1]}}</a>
                                        </el-tag>
                                    </div>
                                </el-card>
                            </el-timeline-item>
                        </template>
                    </el-timeline>
                </div>
            </div>
        </section>

        <section class="wb-blue-section">
            <div class="inner">
                <div class="title">
                    <p>{{home_data.section6.title.subtitle}}</p>
                    <h2>{{home_data.section6.title.title}}</h2>
                </div>
                <div class="wb-desc">
                    <el-row class="wb-icon">
                        <el-col :lg="12" :sm="12" :xs="24" class="desc-box">
                            <p>{{home_data.section6.content.desc}}</p>
                        </el-col>
                        <el-col :lg="12" :sm="12" :xs="24">
                            <el-row>
                                <template v-for="(item, index) in home_data.section6.content.icon">
                                    <el-col :key="index" :lg="6" :sm="12" :xs="12" class="icon-box">
                                        <a :href="item.href"><img :src="item.img" :alt="item.name" class="icon"/></a>
                                    </el-col>
                                </template>
                            </el-row>
                        </el-col>
                    </el-row>
                </div>
            </div>
        </section>

        <section class="wb-light-section">
            <div class="inner">
                <div class="title">
                    <p>{{home_data.section7.title.subtitle}}</p>
                    <h2>{{home_data.section7.title.title}}</h2>
                </div>
                <div class="wb-desc">
                    <el-row v-for="(row, row_index) in home_data.section7.content" :key="row_index" class="row">
                        <el-col v-for="(col, col_index) in row" :key="col_index" :xs="24" :sm="12" class="col">
                            <h3>{{ col.title }}</h3>
                            <p>{{ col.text }}</p>
                            <p v-for="(link, index) in col.link" :key="index">
                                {{link.name}}：
                                <a :href="link.href" target="_blank">{{link.href}}</a>
                            </p>
                        </el-col>
                    </el-row>
                </div>
            </div>
        </section>

    </div>
</template>

<script>
    export default {
        name: 'Home',
        data() {
            return {
                coverPadding: '',
                galleryHeight: '',
                auto_timeline: '',
                auto_timeline_item: '',
                home_data: this.$store.state.home_data,
                blog_data: this.$store.state.blog_data,
            }
        },
        methods: {
            set_cover_padding: function () {
                // 设置封面内边距
                let clientHeight = document.documentElement.clientHeight;
                let titleHeight = this.$refs.cover.clientHeight;
                let padding = ((clientHeight - titleHeight) / 2);
                this.coverPadding = `${padding}px 0px`;
            },
            set_gallery_height: function () {
                let imageWidth = this.$refs.gallery.$el.clientWidth;
                let imageHeight = 0.5625 * imageWidth;
                this.galleryHeight = `${imageHeight}px`;
            },
            set_timeline_width: function () {
                let boxWidth = this.$refs.timeline.clientWidth;
                if (boxWidth > 960) {
                    boxWidth = 960;
                }
                if (boxWidth >= 768) {
                    let itemWidth = boxWidth / 2 - 30;
                    this.auto_timeline = `width: ${boxWidth}px`;
                    this.auto_timeline_item = `width: ${itemWidth}px`;
                } else {
                    this.auto_timeline = "";
                    this.auto_timeline_item = "";
                }
            },
            get_blog_selection: function () {
                if (this.blog_data) {
                    return 0;
                }
                let that = this;
                let data_host = this.$store.state.host;
                this.$http.get(data_host + '/webpage/blog/selection')
                    .then(function (res) {
                        if (res.data.status === 'OK') {
                            console.log("博客数据源", res.data.data["source"]);
                            that.blog_data = res.data.data["rss_info"];
                            that.$store.state.blog_data = res.data.data;
                        } else {
                            that.$store.state.blog_data = null;
                        }
                    })
                    .catch(function (res) {
                        console.log(res);
                        that.$store.state.blog_data = null;
                    })
            },
        },
        mounted() {
            this.set_cover_padding();
            this.set_gallery_height();
            this.set_timeline_width();
            this.get_blog_selection();
        },
    }
</script>

<style lang="scss" scoped>
    @import "~@/assets/css/timeline.css";

    @font-face {
        font-family: bmxuyuanx;
        src: url('~@/assets/ttf/BMXY-WolfBolin.ttf')
    }

    .wb-home {
        background: url("~@/assets/img/cover.jpg") no-repeat fixed top;
        /* background 必在 background-size 前 */
        background-size: cover;
        position: relative;
    }

    //////////////////// 封面 ////////////////////

    .wb-cover {
        text-align: center;

        p {
            font-size: 2em;
            color: #2E2E2E;
            font-weight: 100;
            line-height: 48px;
            letter-spacing: 2px;
        }

        h1 {
            color: #2E2E2E;
            font-size: 6em;
            font-weight: 400;
            line-height: 90px;
            margin: 30px 0 20px;
            letter-spacing: 8px;
        }

        @media screen and (max-width: 768px) {
            p {
                font-size: 1em;
            }

            h1 {
                font-size: 3em;
                letter-spacing: 2px;
            }
        }
    }

    //////////////////// 分段样式 ////////////////////

    .wb-light-section {
        padding: 4em 0;
        background-color: #FFFFFF;

        .title {
            text-align: center;

            p {
                color: #404040;
                font-size: 2em;
                font-weight: 100;
                letter-spacing: .1em;
            }

            h2 {
                color: #91BEF0;
                font-size: 3em;
                font-weight: 400;
                letter-spacing: .3em;
            }
        }
    }

    .wb-blue-section {
        padding: 4em 0;
        background-color: #91BEF0;

        .title {
            text-align: center;

            p {
                color: #404040;
                font-size: 2em;
                font-weight: 100;
                letter-spacing: .1em;
            }

            h2 {
                color: white;
                font-size: 3em;
                font-weight: 400;
                letter-spacing: .3em;
            }
        }
    }

    .wb-desc {
        max-width: 970px;
        margin: 0 auto;

        h3 {
            margin: 20px 0 15px;
            color: #373737;
            letter-spacing: 1px;
            font-weight: 400;
        }

        p {
            font-weight: 100;
            line-height: 26px;
            word-spacing: 2px;
        }

        img {
            width: 100%;
        }

        a {
            color: #91BEF0;
        }

        .row {
        }

        .col {
            padding: 0 15px;
            margin-bottom: 2em;
        }

        .wb-icon {
            .desc-box {
                padding: 15px 15px 15px 26px;
            }

            .icon-box {
                margin: 1em 0;
                text-align: center;
            }

            .icon {
                display: inline-block;
                vertical-align: middle;
                border-radius: 25%;
                width: 100px;
                height: 100px;
            }
        }
    }

    .wb-timeline {
        .tl-desc {
            font-size: 1em;
        }

        .tl-time {
            font-size: 1.15em;
            line-height: 1.15em;
        }

        .tl-flag:before {
            border: 4px solid #91BEF0;
        }

        .tl-flag a {
            font-size: 1.15em;
        }

        .wb-card {
            margin: 15px;

            .title {
                color: #91BEF0;
                font-size: 1.38em;
                text-decoration: none;
            }

            p {
                font-size: 1.15em;
                word-break: break-all;
            }

            .tag-box {
                padding-top: 20px;

                .el-tag {
                    margin-right: 0.5em;

                    a {
                        color: #909399;
                        font-size: 1.15em;
                        text-decoration: none;
                    }
                }
            }
        }
    }
</style>