<template>
  <div id="index-page">
    <!--网页封面-->
    <section class="wb-cover">
      <div ref="cover" v-bind:style="{padding: coverPadding}">
        <h3>{{ $t("i18n.motto") }}</h3>
        <h1>WolfBolin</h1>
        <a>{{ $t("i18n.explore") }}</a>
      </div>
    </section>
    <!--网页第一模块-->
    <section class="wb-white-section">
      <div class="inner">
        <div class="title">
          <h3>WOLFBOLIN</h3>
          <h1>{{ $t("i18n.section1_title") }}</h1>
        </div>
        <el-row :gutter="40">
          <el-col class="item" :span="12">
            <h3>{{ $t("i18n.section1_subhead1") }}</h3>
            <p>{{ $t("i18n.section1_content1") }}</p>
          </el-col>
          <el-col class="item" :span="12">
            <h3>{{ $t("i18n.section1_subhead2") }}</h3>
            <p>{{ $t("i18n.section1_content2") }}</p>
          </el-col>
        </el-row>
        <el-row :gutter="40">
          <el-col class="item" :span="12">
            <h3>{{ $t("i18n.section1_subhead3") }}</h3>
            <p>{{ $t("i18n.section1_content3") }}</p>
          </el-col>
          <el-col class="item" :span="12">
            <h3>{{ $t("i18n.section1_subhead4") }}</h3>
            <p>{{ $t("i18n.section1_content4") }}</p>
          </el-col>
        </el-row>
      </div>
    </section>
    <!--网页第二模块-->
    <section class="wb-blue-section">
      <div class="inner">
        <div class="title">
          <h3>GALLERY</h3>
          <h1>{{ $t("i18n.section2_title") }}</h1>
        </div>
        <el-carousel height="540px">
          <el-carousel-item v-for="item in photoGallery" :key="item">
            <img height="540px" :src="item"/>
          </el-carousel-item>
        </el-carousel>
      </div>
    </section>
    <!--网页第三模块-->
    <section class="wb-white-section">
      <div class="inner">
        <div class="title">
          <h3>TREND</h3>
          <h1>{{ $t("i18n.section3_title") }}</h1>
        </div>
        <el-row :gutter="40">
          <el-col class="item" :span="12">
            <h3>{{ $t("i18n.section3_subhead1") }}</h3>
            <p>{{ $t("i18n.section3_content1") }}</p>
          </el-col>
          <el-col class="item" :span="12">
            <h3>{{ $t("i18n.section3_subhead2") }}</h3>
            <p>{{ $t("i18n.section3_content2") }}</p>
          </el-col>
        </el-row>
        <el-row :gutter="40">
          <el-col class="item" :span="12">
            <h3>{{ $t("i18n.section3_subhead3") }}</h3>
            <p>{{ $t("i18n.section3_content3") }}</p>
          </el-col>
          <el-col class="item" :span="12">
            <h3>{{ $t("i18n.section3_subhead4") }}</h3>
            <p>{{ $t("i18n.section3_content4") }}</p>
          </el-col>
        </el-row>
      </div>
    </section>
    <!--网页第四模块-->
    <section class="wb-blue-section">
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
    <!--网页第五模块-->
    <section class="wb-white-section">
      <div class="inner">
        <div class="title">
          <h3>BLOG</h3>
          <h1>{{ $t("i18n.section5_title") }}</h1>
        </div>
        <el-row :gutter="40" v-for="index in Math.ceil(articleBox.length/2)" :key="index">
          <el-col class="card" :span="12">
            <el-card>
              <div slot="header">
                <span>{{ articleBox[2*(index-1)].title }}</span>
                <el-button class="button" type="text" @click="openLink(articleBox[2*(index-1)].link)">查看全文</el-button>
              </div>
              <p>{{ articleBox[2*(index-1)].content }}</p>
              <div>
                <p class="blog-time">{{ articleBox[2*(index-1)].time }}</p>
                <template v-for="item in articleBox[2*(index-1)].category">
                  <div class="blog-tag" @click="openLink(item.link)">
                    <el-tag>{{ item.name }}</el-tag>
                  </div>
                </template>
              </div>
            </el-card>
          </el-col>

          <el-col class="card" :span="12" v-if="(2*index-1) < articleBox.length">
            <el-card>
              <div slot="header">
                <span>{{ articleBox[2*index-1].title }}</span>
                <el-button class="button" type="text" @click="openLink(articleBox[2*index-1].link)">查看全文</el-button>
              </div>
              <p>{{ articleBox[2*index-1].content }}</p>
              <div>
                <p class="blog-time">{{ articleBox[2*index-1].time }}</p>
                <template v-for="item in articleBox[2*index-1].category">
                  <div class="blog-tag" @click="openLink(item.link)">
                    <el-tag>{{ item.name }}</el-tag>
                  </div>
                </template>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </section>
    <!--网页第六模块-->
    <section class="wb-blue-section">
      <div class="inner">
        <div class="title">
          <h3>LINK</h3>
          <h1>{{ $t("i18n.section6_title") }}</h1>
        </div>
        <el-row :gutter="40">
          <el-col class="item link-box" :span="10">
            <div class="text">
              <h3>{{ $t("i18n.section6_subhead1") }}</h3>
              <p>{{ $t("i18n.section6_content1") }}</p>
            </div>
          </el-col>
          <el-col class="item link-box icon-box" :span="14">
            <a href="https://blog.csdn.net/qq_36731677" target="_blank">
              <img class="icon" src="../assets/csdn.png"/>
            </a>
            <a href="https://github.com/wolfbolin" target="_blank">
              <img class="icon" src="../assets/github.png"/>
            </a>
            <a href="https://space.bilibili.com/72835041/#/" target="_blank">
              <img class="icon" src="../assets/bilibili.png"/>
            </a>
            <a href="mailto:admin@wolfbolin.com">
              <img class="icon" src="../assets/gmail.png"/>
            </a>
          </el-col>
        </el-row>
      </div>
    </section>
    <!--网页第七模块-->
    <section class="wb-white-section">
      <div class="inner">
        <div class="title">
          <h3>FRIEND</h3>
          <h1>{{ $t("i18n.section7_title") }}</h1>
        </div>
        <el-row :gutter="40">
          <el-col class="item" :span="12">
            <h3>{{ $t("i18n.section7_subhead1") }}</h3>
            <p>{{ $t("i18n.section7_content1") }}</p>
          </el-col>
          <el-col class="item" :span="12">
            <h3>{{ $t("i18n.section7_subhead2") }}</h3>
            <p>{{ $t("i18n.section7_content2") }}<br/>
              {{ $t("i18n.section7_blog") }}：
              <a href="https://csuwangj.github.io/" target="_blank">https://csuwangj.github.io/</a><br/>
              {{ $t("i18n.section7_blog") }}：
              <a href="https://zickshen.github.io/" target="_blank">https://zickshen.github.io/</a></p>
          </el-col>
        </el-row>
        <el-row :gutter="40">
          <el-col class="item" :span="12">
            <h3>{{ $t("i18n.section7_subhead3") }}</h3>
            <p>{{ $t("i18n.section7_content3") }}<br/>
              {{ $t("i18n.section7_index") }}：
              <a href="https://www.admirable.one/" target="_blank">https://www.admirable.one/</a><br/>
              {{ $t("i18n.section7_blog") }}：
              <a href="https://www.tail0r.com/" target="_blank">https://www.tail0r.com/</a>
            </p>
          </el-col>
          <el-col class="item" :span="12">
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
      this.setCoverPadding();
      this.updateArticle();
    },
    methods: {
      setCoverPadding: function () {
        let clientHeight = document.documentElement.clientHeight;
        let titleHeight = this.$refs.cover.clientHeight;
        let padding = (clientHeight - titleHeight) / 2;
        this.coverPadding = `${padding}px 0px`;
      },
      openLink: function (url) {
        window.open(url);
      },
      updateArticle: function () {
        let that = this;
        this.$http.get('http://localhost:63344/server/getArticle.php')
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

  #index-page {
    .inner {
      max-width: 960px;
      margin: 0 auto;
      padding: 36px 40px 72px 40px;
    }
    .wb-cover {
      text-align: center;
      h3 {
        line-height: 20px;
        font-size: 20px;
        font-weight: 200;
        letter-spacing: 2px;
        color: #404040;
        margin: 0;
      }
      h1 {
        line-height: 70px;
        font-size: 70px;
        font-weight: 400;
        letter-spacing: 8px;
        color: #404040;
        margin: 30px 0 20px 0;
      }
      a {
        display: inline-block;
        font-size: 15px;
        font-weight: 200;
        color: #404040;
        padding: .5em 1em;
        border-radius: 1000px;
        background-color: transparent;
        border: 0.5px solid #404040;
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
        color: #0080ff;
        text-decoration: none;
      }
    }
    .icon-box {
      text-align: center;
    }
    .link-box {
      height: 250px;
      &:before {
        content: '';
        display: inline-block;
        height: 100%;
        vertical-align: middle;
      }
      .text {
        display: inline-block;
        vertical-align: middle;
      }
      .icon {
        display: inline-block;
        vertical-align: middle;
        margin: 2%;
        border-radius: 25%;
        width: 100px;
        height: 100px;
      }
    }
    .card {
      padding: 20px;
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
          color: #0080ff;
          font-weight: 400;
          font-size: 38px;
        }
      }
    }
    .wb-blue-section {
      background-color: rgba(0, 128, 255, 0.7);
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
    }
  }
</style>
