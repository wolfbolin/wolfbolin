<template>
    <div class="wb-index">
        <section class="wb-cover" :style="{padding: coverPadding}">
            <div ref="cover" class="inner">
                <p>{{page_date.section0.title.subtitle}}</p>
                <h1>{{page_date.section0.title.title}}</h1>
            </div>
        </section>

        <section class="wb-light-section">
            <div class="inner">
                <div class="title">
                    <p>{{page_date.section1.title.subtitle}}</p>
                    <h2>{{page_date.section1.title.title}}</h2>
                </div>
                <div class="wb-desc">
                    <el-row v-for="(row, row_index) in page_date.section1.content" :key="row_index" class="row">
                        <el-col v-for="(col, col_index) in row" :key="col_index" :xs="24" :sm="12" class="col">
                            <h3>{{ col.title }}</h3>
                            <p>{{ col.text }}</p>
                        </el-col>
                    </el-row>
                </div>
            </div>
        </section>

        <section class="wb-deep-section">
            <div class="inner">
                <div class="title">
                    <p>{{page_date.section2.title.subtitle}}</p>
                    <h2>{{page_date.section2.title.title}}</h2>
                </div>
                <div class="wb-desc">
                    <el-carousel arrow="hover" ref="gallery" :height="galleryHeight">
                        <el-carousel-item v-for="(item, index) in page_date.section2.content" :key="index">
                            <img :src="item.src" :alt="item.title"/>
                        </el-carousel-item>
                    </el-carousel>
                </div>
            </div>
        </section>

        <section class="wb-light-section">
            <div class="inner">
                <div class="title">
                    <p>{{page_date.section3.title.subtitle}}</p>
                    <h2>{{page_date.section3.title.title}}</h2>
                </div>
                <div class="wb-desc">
                    <el-row v-for="(row, row_index) in page_date.section3.content" :key="row_index" class="row">
                        <el-col v-for="(col, col_index) in row" :key="col_index" :xs="24" :sm="12" class="col">
                            <h3>{{ col.title }}</h3>
                            <p>{{ col.text }}</p>
                        </el-col>
                    </el-row>
                </div>
            </div>
        </section>

        <section class="wb-deep-section">
            <div class="inner">
                <div class="title">
                    <p>{{page_date.section4.title.subtitle}}</p>
                    <h2>{{page_date.section4.title.title}}</h2>
                </div>
                <div class="wb-timeline" ref="timeline">
                    <ul class="tl-timeline" :style="auto_timeline">
                        <li v-for="(item, index) in page_date.section4.content" :key="index">
                            <div class="tl-direction-l" :style="auto_timeline_l" v-if="index%2!==0">
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

                            <div class="tl-direction-r" :style="auto_timeline_r" v-if="index%2===0">
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
                    <p>{{page_date.section5.title.subtitle}}</p>
                    <h2>{{page_date.section5.title.title}}</h2>
                </div>
                <div v-if="blog_selection===null">
                    <p style="font-size: 2em; text-align: center">T_T 嘤嘤嘤，数据加载失败了</p>
                </div>
                <div class="wb-desc" v-else>
                    <!--                                        <el-card class="wb-card" v-for="item in blog_selection" :key="item.title">-->
                    <!--                                            <div slot="header">-->
                    <!--                                                <a class="title" :href="item.link">{{item.title}}</a>-->
                    <!--                                                <div class="tag-box">-->
                    <!--                                                    <el-tag size="small" type="info" v-for="tag in item.tags" :key="tag[0]">-->
                    <!--                                                        <a :href="tag[0]">{{tag[1]}}</a>-->
                    <!--                                                    </el-tag>-->
                    <!--                                                </div>-->
                    <!--                                            </div>-->
                    <!--                                            <p>{{item.desc}}</p>-->
                    <!--                                            <p class="card-time">{{item.time}}</p>-->
                    <!--                                        </el-card>-->
                    <el-timeline class="wb-timeline">
                        <template v-for="item in blog_selection">
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

        <section class="wb-deep-section">
            <div class="inner">
                <div class="title">
                    <p>{{page_date.section6.title.subtitle}}</p>
                    <h2>{{page_date.section6.title.title}}</h2>
                </div>
                <div class="wb-desc">
                    <el-row class="wb-icon">
                        <el-col :lg="12" :sm="12" :xs="24" class="desc-box">
                            <p>{{page_date.section6.content.desc}}</p>
                        </el-col>
                        <el-col :lg="12" :sm="12" :xs="24">
                            <el-row>
                                <template v-for="(item, index) in page_date.section6.content.icon">
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
                    <p>{{page_date.section7.title.subtitle}}</p>
                    <h2>{{page_date.section7.title.title}}</h2>
                </div>
                <div class="wb-desc">
                    <el-row v-for="(row, row_index) in page_date.section7.content" :key="row_index" class="row">
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
        name: 'Index',
        data() {
            return {
                coverPadding: '',
                galleryHeight: '',
                auto_timeline: '',
                auto_timeline_l: '',
                auto_timeline_r: '',
                page_date: this.$store.state.index_data,
                blog_selection: this.$store.state.blog_selection,
            }
        },
        methods: {
            set_cover_padding: function () {
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
                    this.auto_timeline_l = `width: ${itemWidth}px`;
                    this.auto_timeline_r = `width: ${itemWidth}px`;
                } else {
                    this.auto_timeline = "";
                    this.auto_timeline_l = "";
                    this.auto_timeline_r = "";
                }
            },
            get_blog_selection: function () {
                if (this.blog_selection) {
                    return 0;
                }
                let that = this;
                let host = this.$store.state.host;
                this.$http.get(host + '/webPage/blogSelection')
                    .then(function (res) {
                        if (res.data.status === 'success') {
                            // console.log(res.data.data);
                            that.blog_selection = res.data.data;
                            that.$store.state.blog_selection = res.data.data;
                        } else {
                            that.$store.state.blog_selection = null;
                        }
                    })
                    .catch(function (res) {
                        console.log(res);
                        that.$store.state.blog_selection = null;
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
    @import "../../public/static/timeline.css";

    @font-face {
        font-family: bmxuyuanx;
        src: url('../../public/static/BMXY-WolfBolin.ttf')
    }

    @font-face {
        font-family: fzxiyuanx;
        src: url('../../public/static/FZXY.ttf')
    }

    .wb-index {
        font-family: fzxiyuanx, sans-serif;
        background: url("../../public/static/cover.jpg") no-repeat fixed top;
        /* background 必在 background-size 前 */
        background-size: cover;
        position: relative;
    }

    .wb-cover {
        text-align: center;

        p {
            font-size: 2em;
            color: #2E2E2E;
            line-height: 40px;
            font-weight: 400;
            letter-spacing: 2px;
        }

        h1 {
            color: #2E2E2E;
            font-size: 6em;
            font-weight: 400;
            line-height: 90px;
            margin: 30px 0 20px;
            letter-spacing: 8px;
            font-family: bmxuyuanx, sans-serif;
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

    .wb-light-section {
        padding: 4em 0;
        background-color: #FFFFFF;

        .title {
            text-align: center;

            p {
                color: #404040;
                font-size: 1.5em;
                font-weight: 100;
                margin-bottom: 1rem;
            }

            h2 {
                color: #91BEF0;
                font-size: 3em;
                font-weight: 400;
                margin-bottom: 0.8em;
            }
        }
    }

    .wb-deep-section {
        padding: 4em 0;
        background-color: #91BEF0;

        .title {
            text-align: center;

            p {
                color: #404040;
                font-size: 1.5em;
                font-weight: 100;
                margin-bottom: 1rem;
            }

            h2 {
                color: white;
                font-size: 3em;
                font-weight: 400;
                margin-bottom: 0.8em;
            }
        }
    }

    .wb-desc {
        h3 {
            font-size: 1.5em;
            font-weight: 500;
            margin-bottom: .5em;
        }

        p {
            font-size: 1.35em;
            line-height: 1.5;
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
            font-size: 1.35em;
        }

        .tl-time {
            font-size: 1.15em;
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

<style>
    .el-timeline-item__timestamp{
        font-size: 20px;
    }
</style>
