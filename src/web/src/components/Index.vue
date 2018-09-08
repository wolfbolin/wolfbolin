<template>
  <div id="index-page">
    <!--网页封面-->
    <section class="wb-cover">
      <div ref="cover" v-bind:style="{padding: coverPadding}">
        <h3>嗜之越笃 技巧越工</h3>
        <h1>WolfBolin</h1>
        <a>开始探索</a>
      </div>
    </section>
    <!--网页第一模块-->
    <section class="wb-white-section">
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
    <!--网页第二模块-->
    <section class="wb-blue-section">
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
    <!--网页第三模块-->
    <section class="wb-white-section">
      <div class="inner">
        <div class="title">
          <h3>TREND</h3>
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
    <!--网页第四模块-->
    <section class="wb-blue-section">
      <div class="inner">
        <div class="title">
          <h3>GROWTH</h3>
          <h1>我的进阶之路</h1>
        </div>
        <ul class="timeline">
          <li>
            <div class="direction-l">
              <div class="flag-wrapper">
                <span class="flag"><a href="https://blog.wolfbolin.com">Blog</a></span>
                <span class="time-wrapper"><span class="time">2017/11 - 2018/4</span></span>
              </div>
              <div class="desc">每个新站长都幻想着自己的博客梦~但是大灰狼先生最终放弃了梦想，
                选择了使用简单方便的轮子
              </div>
            </div>
          </li>

          <li>
            <div class="direction-r">
              <div class="flag-wrapper">
                <span class="flag"><a href="https://github.com/wolfbolin/Caremore">Caremore</a></span>
                <span class="time-wrapper"><span class="time">2017/6 - 2017/11</span></span>
              </div>
              <div class="desc">CareMore是一款基于云计算，搭载于智能可穿戴设备，
                应用深度学习技术并结合心率进行分析的儿童安全预警系统。
              </div>
            </div>
          </li>

          <li>
            <div class="direction-l">
              <div class="flag-wrapper">
                <span class="flag">ICPC</span>
                <span class="time-wrapper"><span class="time">2016/2 - 2017/10</span></span>
              </div>
              <div class="desc">经过一年的准备，大灰狼先生参加了ICPC沈阳站的比赛，并最终收获一枚银奖。</div>
            </div>
          </li>

          <li>
            <div class="direction-r">
              <div class="flag-wrapper">
                <span class="flag"><a href="https://github.com/wolfbolin/Chattincrypted">Chattincrypted</a></span>
                <span class="time-wrapper"><span class="time">2017/7 - 2017/8</span></span>
              </div>
              <div class="desc">一款可以自己部署的加密聊天通信软件，由java+python开发运行。</div>
            </div>
          </li>

          <li>
            <div class="direction-l">
              <div class="flag-wrapper">
                <span class="flag"><a href="https://github.com/wolfbolin/Jigsaw">Jigsaw</a></span>
                <span class="time-wrapper"><span class="time">2017/6 - 2017/7</span></span>
              </div>
              <div class="desc">在校期间第一个C++实训项目，除了还能看没什么优点。</div>
            </div>
          </li>

          <li>
            <div class="direction-r">
              <div class="flag-wrapper">
                <span class="flag"><a href="">NLife</a></span>
                <span class="time-wrapper"><span class="time">2017/2 - 2017/5</span></span>
              </div>
              <div class="desc">受益于学校的自由探索项目，我带领四人开发团队尝试建立一套基于AHP法的人体健康评估模型。
                但是由于资金和能力的限制，该项目在完成了七成的工作之后搁置了，非常期待他的二次开发。
              </div>
            </div>
          </li>

          <li>
            <div class="direction-l">
              <div class="flag-wrapper">
                <span class="flag"><a href="">CSU Software</a></span>
                <span class="time-wrapper"><span class="time">2016/9 - 2016/12</span></span>
              </div>
              <div class="desc">第一个练手的网页作品，制作目的是为了参加学校组织的网页设计大赛，
                因为能力所限，页面中存在Flash技术。
              </div>
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
          <h1>我的博客</h1>
        </div>
      </div>
    </section>
    <!--网页第六模块-->
    <section class="wb-blue-section">
      <div class="inner">
        <div class="title">
          <h3>FRIEND</h3>
          <h1>我的伙伴</h1>
        </div>
        <el-row :gutter="40">
          <el-col class="card" :span="12">
            <h3>这是什么？</h3>
            <p>任何事物的学习过程都少不了同行的伙伴，任何一个人都难以掌握所有知识。
              也许你无法在Baidu、Google、Yahoo上找到合适的教学，
              也许你无法在Stack Overflow、Segment Fault、V2EX上找到合适的解答。
              但是，你还是可以问问更有智慧的伙伴呀~</p>
          </el-col>
          <el-col class="card" :span="12">
            <h3>其他伙伴</h3>
            <p>张洺豪DragonHao：<a href="http://www.dragonhao.cn/">http://www.dragonhao.cn/</a><br/>
              徐戍Haxushu：<a href="http://haxushu.coding.me/">http://haxushu.coding.me/</a></p>
          </el-col>
        </el-row>
        <el-row :gutter="40">
          <el-col class="card" :span="12">
            <h3>Frederic Chan</h3>
            <p style="margin: 0">这是一位非常文艺的软件开发者，有着优雅的编程追求。
              Admirable 是 Frederic Chan 的个人品牌。寓意为，做一个受人尊敬的人。
              Tail0r 是 Admirable.one 旗下的多人博客。
              在这里，我们分享科技、人文、兴趣、生活。
              我们一直在等待一个像你一样愿意了解我们的人。<br/>
              主页：<a href="https://www.admirable.one/">https://www.admirable.one/</a><br/>
              博客：<a href="https://www.tail0r.com/">https://www.tail0r.com/</a>
            </p>
          </el-col>
          <el-col class="card" :span="12">
            <h3>DJ !</h3>
            <p style="margin: 0">这是一位喜爱研究信息安全的小伙伴，CTF、PWN、逆向工程都是他的专业领域。
              如果有什么新奇的信息安全问题，他也许会非常感兴趣哟~<br/>
              博客：<a href="https://csuwangj.github.io/">https://csuwangj.github.io/</a><br/>
              博客：<a href="https://zickshen.github.io/">https://zickshen.github.io/</a>
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
        border: 1px solid #404040;
      }
    }
    .card {
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
    .wb-white-section {
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
    .wb-blue-section {
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
  }
</style>
