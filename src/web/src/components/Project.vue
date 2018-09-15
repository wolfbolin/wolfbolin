<template>
  <div id="project-page">
    <div class="inner">
      <el-card class="box-card">
        <div slot="header" class="clearfix">
          <span>项目列表</span>
          <el-button style="float: right; padding: 3px 0" type="text">Github</el-button>
        </div>
        <p>此列表列举了我的全部项目</p>
        <el-table
          border
          :data="tableData"
          style="width: 100%">
          <el-table-column type="expand">
            <template slot-scope="props">
              <el-form label-position="left" inline class="demo-table-expand">
                <el-form-item label="项目名称">
                  <span>{{ props.row.name }}</span>
                </el-form-item>
                <el-form-item label="软件版本">
                  <span>{{ props.row.shop }}</span>
                </el-form-item>
                <el-form-item label="开始时间">
                  <span>{{ props.row.id }}</span>
                </el-form-item>
                <el-form-item label="结束时间">
                  <span>{{ props.row.shopId }}</span>
                </el-form-item>
                <el-form-item label="项目评分"><el-rate
                    v-model="value5"
                    disabled
                    show-score
                    text-color="#ff9900"
                    score-template="{value}"
                  class="cell-box">
                  </el-rate>
                </el-form-item>
                <el-form-item label="完成进度">
                  <el-progress :text-inside="true" :stroke-width="18" :percentage="70" class="cell-box"></el-progress>
                </el-form-item>
                <el-form-item label="项目地址">
                  <span>{{ props.row.desc }}</span>
                </el-form-item>
              </el-form>
            </template>
          </el-table-column>
          <el-table-column
            label="软件版本"
            prop="version">
          </el-table-column>
          <el-table-column
            label="项目名称"
            prop="name">
          </el-table-column>
          <el-table-column
            label="项目地址"
            prop="address">
          </el-table-column>
        </el-table>
      </el-card>
    </div>
  </div>
</template>

<script>
  export default {
    name: "Project",
    data() {
      return {
        tableData: [{
          id: '12987122',
          name: '好滋好味鸡蛋仔',
          category: '江浙小吃、小吃零食',
          desc: '荷兰优质淡奶，奶香浓而不腻',
          address: '上海市普陀区真北路',
          shop: '王小虎夫妻店',
          shopId: '10333'
        }, {
          id: '12987123',
          name: '好滋好味鸡蛋仔',
          category: '江浙小吃、小吃零食',
          desc: '荷兰优质淡奶，奶香浓而不腻',
          address: '上海市普陀区真北路',
          shop: '王小虎夫妻店',
          shopId: '10333'
        }, {
          id: '12987125',
          name: '好滋好味鸡蛋仔',
          category: '江浙小吃、小吃零食',
          desc: '荷兰优质淡奶，奶香浓而不腻',
          address: '上海市普陀区真北路',
          shop: '王小虎夫妻店',
          shopId: '10333'
        }, {
          id: '12987126',
          name: '好滋好味鸡蛋仔',
          category: '江浙小吃、小吃零食',
          desc: '荷兰优质淡奶，奶香浓而不腻',
          address: '上海市普陀区真北路',
          shop: '王小虎夫妻店',
          shopId: '10333'
        }]
      }
    }
  }
</script>

<style scoped lang="scss">
  #project-page {
    .inner {
      max-width: 960px;
      margin: 0 auto;
      padding: 60+72px 40px 72px 40px;
    }
    .demo-table-expand {
      font-size: 0;
      &.cell-box:before{
        content: '';
        display: inline-block;
        height: 100%;
        vertical-align: middle;
      }
      .cell-box{
        display: inline-block;
      }
    }
    .demo-table-expand label {
      width: 90px;
      color: #99a9bf;
    }
    .demo-table-expand .el-form-item {
      margin-right: 0;
      margin-bottom: 0;
      width: 50%;
    }
  }
</style>
