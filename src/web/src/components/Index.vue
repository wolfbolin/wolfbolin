<template>
  <div class="wb-index">
    <header class="wb-navbar">
      <el-row type="flex" justify="space-between">
        <el-col :span="8" :push="2">
          <img src="../assets/logo.png" class="wb-navbar-logo"/>
        </el-col>
        <el-col :span="16" :pull="2">
          <el-menu
            :default-active="activeIndex"
            class="wb-navbar-menu"
            mode="horizontal"
            background-color="transparent"
            text-color="#888888"
            active-text-color="#1DA1F2">
            <el-menu-item index="cover">主页</el-menu-item>
            <el-menu-item index="info">简介</el-menu-item>
            <el-menu-item index="blog">博客</el-menu-item>
            <el-menu-item index="work">动向</el-menu-item>
            <el-menu-item index="gallery">摄影</el-menu-item>
          </el-menu>
        </el-col>
      </el-row>
    </header>
    <section class="wb-cover">
      <div ref="cover" v-bind:style="{padding: coverPadding}">
        <h3>嗜之越笃 技巧越工</h3>
        <h1>WolfBolin</h1>
        <a>开始探索</a>
      </div>
    </section>
    <section class="wb-info">
      <div class="wb-body">
        <div class="wb-info-title">
          <h3>WOLFBOLIN</h3>
          <h1>很荣幸能与你相遇</h1>
        </div>
        <el-row type="flex" justify="space-around" :gutter="80">
          <el-col :span="12">
            <div class="wb-info-card">
              <h3>创建这个网站有何意义呢?</h3>
              <p>wolfbolin.com是大灰狼先生创办的个人网站，目的在于向所有线上玩家展示其对硅基生物的理解程度，
                网站的建设过程具有强烈的试验性，每一次更新对于大灰狼先生都是一次挑战，
                他永远都不知道网站会在什么时候神秘消失， 他也永远不知道你何时从这里轻轻走过。</p>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="wb-info-card">
              <h3>大灰狼先生有什么特点呢?</h3>
              <p>大灰狼先生是一位温文尔雅、礼貌谦逊的绅士。 他虽然温柔安静，但是却不喜欢宅在房间中。
                他虽然见识广泛，但他却不会经常吹嘘炫耀。 他虽然博古通今，但他却不停止学习的脚步。
                大灰狼先生正在努力成为全能小王子呢，有兴趣可以更多的关注他哟~</p>
            </div>
          </el-col>
        </el-row>
        <el-row type="flex" justify="space-around" :gutter="60">
          <el-col :span="12">
            <div class="wb-info-card">
              <h3>这个网站有多久的历史呢?</h3>
              <p>大灰狼先生坦白的告诉你，他根本计算不过来。2010年大灰狼先生着手编写网站中的相关内容。
                2012年受到世界末日的影响网站中的信息悉数丢失。2013年大灰狼又重建了他的网站。
                2014年网站因为资金受到限制被迫下线。2016年在取得充足资金支起的情况下重新恢复运行。
                2017年网站翻新逐渐使用新技术进行网站的整体更新。</p>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="wb-info-card">
              <h3>我该如何联系大灰狼先生呢?</h3>
              <p>作为漫漫硅基网络中的一角，能与你相见已经实属不易，大灰狼先生自然是愿意与天下为友。
                但是循着网线爬过来是不切实际的，他的网络带宽可能会把你压扁。
                同时因为网络中到处充斥着非碳基生物的探索活动，大灰狼先生非常担心信息被暴露。
                如果你真的想与他联系，可以试着在这里找他<a href="mailto:wolfbolin@foxmail.com">wolfbolin@foxmail.com</a>。</p>
            </div>
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
        activeIndex: 'cover',
        coverPadding: '',
        clientHeight: 0,
        titleHeight: 0
      }
    },
    mounted() {
      this.coverPadding = this.titlePadding();
    },
    methods: {
      titlePadding: function () {
        this.clientHeight = document.documentElement.clientHeight;
        this.titleHeight = this.$refs.cover.clientHeight;
        let padding = (this.clientHeight - this.titleHeight) / 2;
        return `${padding}px 0px`;
      }
    }
  }
</script>

<style>
  .wb-index {
    background: url('../assets/index-cover.jpg') no-repeat fixed top center;
    background-size: cover;
    position: relative;
  }

  .wb-body {
    max-width: 1000px;
    margin: 0 auto;
    padding: 50px 0;
  }

  .wb-navbar {
    background-color: rgba(40, 40, 40, 0.9);
    position: fixed;
    z-index: 100;
    height: 60px;
    width: 100%;
    top: 0;
    left: 0;
  }

  .wb-navbar-logo {
    float: left;
    height: 50px;
    width: 50px;
    margin: 5px 20px 5px;
    -webkit-background-size: 50px 50px;
  }

  .wb-navbar-menu {
    float: right;
    border-bottom: none;
  }

  .wb-cover {
    text-align: center;
  }

  .wb-cover h3 {
    line-height: 20px;
    font-size: 20px;
    font-weight: 200;
    letter-spacing: 2px;
    color: #888888;
    margin: 0;
  }

  .wb-cover h1 {
    line-height: 70px;
    font-size: 70px;
    font-weight: 400;
    letter-spacing: 8px;
    color: #888888;
    margin: 30px 0 20px 0;
  }

  .wb-cover a {
    display: inline-block;
    font-size: 15px;
    font-weight: 200;
    color: #888888;
    padding: .5em 1em;
    border-radius: 1000px;
    background-color: transparent;
    border: 1px solid #888888;
  }

  .wb-info {
    background-color: white;
  }

  .wb-info-title {
    text-align: center;
  }

  .wb-info-title h3 {
    color: #373737;
    font-weight: 100;
    font-size: 28px;
    line-height: 48px;
  }

  .wb-info-title h1 {
    margin-top: 0;
    color: #1DA1F2;
    font-weight: 400;
    font-size: 38px;
    line-height: 58px;
  }

  .wb-info-card h3 {
    margin: 20px 0 15px;
    color: #353535;
    letter-spacing: 1px;
    font-weight: 400;
  }

  .wb-info-card p {
    margin: 0 0 25px;
    color: #888888;
    font-weight: 400;
    font-size: 13px;
    line-height: 26px;
    word-spacing: 2px;
  }
</style>
