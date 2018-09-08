<template>
  <div id="index-page">
    <section class="wb-cover">
      <div ref="cover" v-bind:style="{padding: coverPadding}">
        <h3>嗜之越笃 技巧越工</h3>
        <h1>WolfBolin</h1>
        <a>开始探索</a>
      </div>
    </section>
    <!--网页第一个模块-->
    <section class="wb-info">
      <div class="inner">
        <div class="title">
          <h3>WOLFBOLIN</h3>
          <h1>很荣幸能与你相遇</h1>
        </div>
        <el-row :gutter="40">
          <el-col class="card" :span="12">
            <h3>创建这个网站有何意义呢?</h3>
            <p>wolfbolin.com是大灰狼先生创办的个人网站，目的在于向所有线上玩家展示其对硅基生物的理解程度，
              网站的建设过程具有强烈的试验性，每一次更新对于大灰狼先生都是一次挑战，
              他永远都不知道网站会在什么时候神秘消失， 他也永远不知道你何时从这里轻轻走过。</p>
          </el-col>
          <el-col class="card" :span="12">
            <h3>大灰狼先生有什么特点呢?</h3>
            <p>大灰狼先生是一位温文尔雅、礼貌谦逊的绅士。 他虽然温柔安静，但是却不喜欢宅在房间中。
              他虽然见识广泛，但他却不会经常吹嘘炫耀。 他虽然博古通今，但他却不停止学习的脚步。
              大灰狼先生正在努力成为全能小王子呢，有兴趣可以在不同平台关注他哟~</p>
          </el-col>
        </el-row>
        <el-row :gutter="40">
          <el-col class="card" :span="12">
            <h3>创建这个网站有何意义呢?</h3>
            <p>wolfbolin.com是大灰狼先生创办的个人网站，目的在于向所有线上玩家展示其对硅基生物的理解程度，
              网站的建设过程具有强烈的试验性，每一次更新对于大灰狼先生都是一次挑战，
              他永远都不知道网站会在什么时候神秘消失， 他也永远不知道你何时从这里轻轻走过。</p>
          </el-col>
          <el-col class="card" :span="12">
            <h3>大灰狼先生有什么特点呢?</h3>
            <p>大灰狼先生是一位温文尔雅、礼貌谦逊的绅士。 他虽然温柔安静，但是却不喜欢宅在房间中。
              他虽然见识广泛，但他却不会经常吹嘘炫耀。 他虽然博古通今，但他却不停止学习的脚步。
              大灰狼先生正在努力成为全能小王子呢，有兴趣可以在不同平台关注他哟~</p>
          </el-col>
        </el-row>
      </div>
    </section>
    <!--网页第二个模块-->
    <section class="wb-gallery">
      <div class="inner">
        <div class="title">
          <h3>GALLERY</h3>
          <h1>摄影也是生活</h1>
        </div>
        <el-carousel height="540px">
          <el-carousel-item v-for="item in photoGallery" :key="item">
            <img height="540px" :src="item"/>
          </el-carousel-item>
        </el-carousel>
      </div>
    </section>
    <!--网页第三个模块-->
    <section class="wb-work">
      <div class="inner">
        <div class="title">
          <h3>WORK</h3>
          <h1>我的最新动向</h1>
        </div>
        <el-row :gutter="40">
          <el-col class="card" :span="12">
            <h3>创建这个网站有何意义呢?</h3>
            <p>wolfbolin.com是大灰狼先生创办的个人网站，目的在于向所有线上玩家展示其对硅基生物的理解程度，
              网站的建设过程具有强烈的试验性，每一次更新对于大灰狼先生都是一次挑战，
              他永远都不知道网站会在什么时候神秘消失， 他也永远不知道你何时从这里轻轻走过。</p>
          </el-col>
          <el-col class="card" :span="12">
            <h3>大灰狼先生有什么特点呢?</h3>
            <p>大灰狼先生是一位温文尔雅、礼貌谦逊的绅士。 他虽然温柔安静，但是却不喜欢宅在房间中。
              他虽然见识广泛，但他却不会经常吹嘘炫耀。 他虽然博古通今，但他却不停止学习的脚步。
              大灰狼先生正在努力成为全能小王子呢，有兴趣可以在不同平台关注他哟~</p>
          </el-col>
        </el-row>
        <el-row :gutter="40">
          <el-col class="card" :span="12">
            <h3>创建这个网站有何意义呢?</h3>
            <p>wolfbolin.com是大灰狼先生创办的个人网站，目的在于向所有线上玩家展示其对硅基生物的理解程度，
              网站的建设过程具有强烈的试验性，每一次更新对于大灰狼先生都是一次挑战，
              他永远都不知道网站会在什么时候神秘消失， 他也永远不知道你何时从这里轻轻走过。</p>
          </el-col>
          <el-col class="card" :span="12">
            <h3>大灰狼先生有什么特点呢?</h3>
            <p>大灰狼先生是一位温文尔雅、礼貌谦逊的绅士。 他虽然温柔安静，但是却不喜欢宅在房间中。
              他虽然见识广泛，但他却不会经常吹嘘炫耀。 他虽然博古通今，但他却不停止学习的脚步。
              大灰狼先生正在努力成为全能小王子呢，有兴趣可以在不同平台关注他哟~</p>
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
        activePhoto: 0,
        photoGallery: ['./static/index-photo1.jpg', './static/index-photo2.jpg',
          './static/index-photo3.jpg', './static/index-photo4.jpg']
      }
    },
    mounted() {
      this.setCoverPadding()
    },
    methods: {
      setCoverPadding: function () {
        let clientHeight = document.documentElement.clientHeight;
        let titleHeight = this.$refs.cover.clientHeight;
        let padding = (clientHeight - titleHeight) / 2;
        this.coverPadding = `${padding}px 0px`;
      }
    }
  }
</script>

<style scoped lang="scss">
  #index-page {
    .inner {
      max-width: 960px;
      margin: 0 auto;
      padding: 36px 40px 72px 40px;
    }
    .card {
      h3 {
        color: #404040;
      }
      p {
        color: #404040;
        font-size: 13px;
        line-height: 26px;
      }
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
        border: 1px solid #404040;
      }
    }
    .wb-info {
      background-color: rgba(255, 255, 255, 0.5);
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
    .wb-gallery {
      background-color: rgba(0, 128, 255, 0.5);
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
    .wb-work {
      background-color: rgba(255, 255, 255, 0.5);
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
  }
</style>
