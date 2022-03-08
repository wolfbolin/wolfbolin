<template>
    <div class="wb-ip">
        <h2>K-V存储信息</h2>
        <p v-if="password.length === 0">请先验证用户交互Token
            <el-button type="text" @click="check_token">检查状态</el-button>
        </p>
        <div v-if="password.length !== 0">
            <el-tabs v-model="active_group" type="card" @tab-click="handle_tab">
                <el-tab-pane v-for="group of kv_group" :key="group" :label="group" :name="group"></el-tab-pane>
                <el-tab-pane label="刷新" name="refresh"></el-tab-pane>
            </el-tabs>
            <el-table :data="record_list" style="width: 100%" v-loading="loading_data" border>
                <el-table-column prop="kid" label="编号" min-width="20" sortable></el-table-column>
                <el-table-column prop="app" min-width="20" label="APP"></el-table-column>
                <el-table-column prop="key" min-width="30" label="键"></el-table-column>
                <el-table-column prop="val" label="值"></el-table-column>
                <el-table-column width="80">
                    <template slot="header">
                        操作
                        <el-button icon="el-icon-plus" size="mini" circle></el-button>
                    </template>
                    <template slot-scope="scope">
                        <el-button size="mini" @click="edit_record(scope.row)">编辑</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
    </div>
</template>

<script>
export default {
    name: "network_ip",
    data() {
        return {
            username: this.$store.state.username,
            password: this.$store.state.password,
            kv_group: [],
            record_list: [],
            loading_data: false,
            active_group: null
        }
    },
    methods: {
        check_token: function () {
            this.username = this.$store.state.username;
            this.password = this.$store.state.password;
            if (this.password.length === 0) {
                this.$message.error("请先完成用户Token验证")
            }else{
                this.switch_group("refresh");
            }
        },
        handle_tab: function (tab) {
            if (tab.name === "refresh") {
                this.switch_group("refresh");
            } else {
                this.switch_group(tab.name);
            }
        },
        switch_group: function (group) {
            console.log("Switch group:", group)
            if (group === "refresh") {
                let that = this;
                let data_host = this.$store.state.host;
                let http_url = data_host + `/network/k-v/groups?user=${this.username}&pass=${this.password}`
                this.$http.get(http_url)
                    .then(function (res) {
                        if (res.data.status === 'OK') {
                            console.log("分组信息", res.data.data);
                            that.kv_group = res.data.data;
                            that.active_group = that.kv_group[0];
                            that.switch_group(that.active_group);
                        }
                    })
                    .catch(function (res) {
                        console.log(res);
                    })
            } else {
                this.refresh_record(group)
            }
        },
        refresh_record: function (group) {
            console.log("Refresh record:", group)
            let that = this;
            this.loading_data = true;
            let data_host = this.$store.state.host;
            let http_url = data_host + `/network/k-v/group/${group}/record?user=${this.username}&pass=${this.password}`
            this.$http.get(http_url)
                .then(function (res) {
                    if (res.data.status === 'OK') {
                        console.log("分组记录量", res.data.data.length);
                        that.record_list = res.data.data;
                        that.$message('数据已刷新');
                    }
                    that.loading_data = false;
                })
                .catch(function (res) {
                    console.log(res);
                    that.loading_data = false;
                })
        },
        edit_record: function (rowData) {
            console.log(rowData)
            rowData.edit = true
        }
    },
    mounted() {
        this.check_token()
    }
}
</script>

<style>

</style>