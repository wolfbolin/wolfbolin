<template>
    <div class="building-page">
      <div class="inner">
        <img class="building" src="../assets/building.png"/>
      </div>
    </div>
</template>

<script>
    export default {
        name: "Building"
    }
</script>

<style scoped lang="scss">
  .building-page{
    .inner {
      max-width: 960px;
      margin: 0 auto;
      padding: 36px 40px 72px 40px;
    }
    .building{
      display: block;
      margin: 100px auto 40px auto;
    }
  }

</style>
