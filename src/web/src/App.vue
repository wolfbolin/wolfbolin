<template>
  <div id="app">
    <router-view/>
    <footer class="wb-footer">
      <p class="wb-copyright">CopyRight © 2018 WolfBolin. All Rights Reserved.</p>
      <a href="http://www.miitbeian.gov.cn" class="wb-icp">湘ICP备17015330号</a>
    </footer>
  </div>
</template>

<script>
  export default {
    name: 'App'
  }
</script>

<style>
  @font-face {
    font-family: Raleway-Light;
    src: url('../static/Raleway-Light.ttf');
  }

  html, body {
    margin: 0;
    padding: 0;
    font-family: 'Raleway-Light', sans-serif;
  }

  .wb-footer {
    background-color: #353535;
  }

  .wb-footer p, .wb-footer a {
    margin: 0;
    display: block;
    text-align: center;
  }

  .wb-copyright {
    color: #888888;
    padding: 10px;
  }

  .wb-icp {
    color: #576b95;
    padding-bottom: 5px;
  }
</style>
