<template>
    <div class="wb-dns">
        <h2>DNS解析</h2>
        <el-tabs v-model="active_domain" type="card" @tab-click="handle_click">
            <el-tab-pane v-for="domain of domain_list" :key="domain" :label="domain" :name="domain">
                <el-table :data="record_list" style="width: 100%" v-loading="loading_data" border>
                    <el-table-column prop="id" label="编号" min-width="100" sortable></el-table-column>
                    <el-table-column prop="record" min-width="80" label="记录"></el-table-column>
                    <el-table-column prop="domain" min-width="120" label="域名"></el-table-column>
                    <el-table-column prop="type" min-width="80" label="类型"></el-table-column>
                    <el-table-column prop="value" min-width="240" label="记录值"></el-table-column>
                    <el-table-column label="操作" width="80">
                        <template slot-scope="scope">
                            <el-button size="mini" @click="edit_record(scope.$index, scope.row)">编辑</el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </el-tab-pane>
            <el-tab-pane label="刷新" name="refresh"></el-tab-pane>
        </el-tabs>
    </div>
</template>

<script>
    export default {
        name: "dns",
        data() {
            return {
                active_domain: null,
                loading_data: false,
                domain_list: [],
                record_list: []
            }
        },
        methods: {
            handle_click: function (tab) {
                this.switch_host(tab.name);
            },
            switch_host: function (domain) {
                console.log("Jump to host:", domain);
                if (domain === "refresh") {
                    let that = this;
                    let data_host = this.$store.state.host;
                    this.$http.get(data_host + '/network/dns/domain')
                        .then(function (res) {
                            if (res.data.status === 'OK') {
                                console.log("域名数据源", res.data.data["source"]);
                                that.domain_list = res.data.data["domain_list"];
                                that.active_domain = that.domain_list[0];
                                that.switch_host(that.active_domain);
                            }
                        })
                        .catch(function (res) {
                            console.log(res);
                        })
                } else {
                    let that = this;
                    this.loading_data = true;
                    let data_host = this.$store.state.host;
                    this.$http.get(data_host + `/network/dns/domain/${domain}/record`)
                        .then(function (res) {
                            if (res.data.status === 'OK') {
                                console.log("记录数据源", res.data.data["source"]);
                                that.record_list = res.data.data["record_list"];
                            }
                            that.loading_data = false;
                        })
                        .catch(function (res) {
                            console.log(res);
                            that.loading_data = false;
                        })
                }
            },
            edit_record: function (index, row) {
                console.log(index, row)
            }
        },
        mounted() {
            this.switch_host("refresh");
        }
    }
</script>

<style lang="scss" scoped>
    .wb-dns {

    }

</style>