<template>
    <div class="wb-dns">
        <h2>DNS解析</h2>
        <el-tabs v-model="active_domain" type="card" @tab-click="handle_click">
            <el-tab-pane v-for="domain of domain_list" :key="domain" :label="domain" :name="domain">
                <el-table :data="record_list" style="width: 100%" border
                          v-loading="loading_data" :row-class-name="row_class">
                    <el-table-column prop="id" label="编号" min-width="100" sortable></el-table-column>
                    <el-table-column prop="record" min-width="80" label="记录"></el-table-column>
                    <el-table-column prop="domain" min-width="120" label="域名"></el-table-column>
                    <el-table-column prop="type" min-width="80" label="类型"></el-table-column>
                    <el-table-column prop="value" min-width="240" label="记录值"></el-table-column>
                    <el-table-column prop="edit" min-width="80" label="编辑"></el-table-column>
                    <el-table-column label="操作" width="80">
                        <template slot-scope="scope">
                            <el-button size="mini" @click="edit_record(scope.$index, scope.row)">编辑</el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </el-tab-pane>
            <el-tab-pane label="刷新" name="refresh"></el-tab-pane>
        </el-tabs>
        <el-dialog title="编辑信息" :visible.sync="show_edit_dialog" :show-close="false"
                   :close-on-click-modal="false" :close-on-press-escape="false">
            <el-form ref="form" :model="edit_data" label-width="80px">
                <el-form-item label="编号">
                    <el-input v-model="edit_data.id" disabled></el-input>
                </el-form-item>
                <el-form-item label="记录">
                    <el-input v-model="edit_data.record"></el-input>
                </el-form-item>
                <el-form-item label="域名">
                    <el-input v-model="edit_data.domain" disabled></el-input>
                </el-form-item>
                <el-form-item label="类型">
                    <el-select v-model="edit_data.type" placeholder="请选择解析类型">
                        <el-option label="A" value="A"></el-option>
                        <el-option label="CHAME" value="CHAME"></el-option>
                        <el-option label="MX" value="MX"></el-option>
                        <el-option label="TXT" value="TXT"></el-option>
                        <el-option label="AAAA" value="AAAA"></el-option>
                        <el-option label="SRV" value="SRV"></el-option>
                        <el-option label="显性URL" value="显性URL"></el-option>
                        <el-option label="隐性URL" value="隐性URL"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="记录值">
                    <el-input v-model="edit_data.value"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button type="primary" @click="confirm_edit">确 定</el-button>
                <el-button type="success" @click="cancel_edit">取 消</el-button>
                <el-button type="warning" @click="rollback_record">回 滚</el-button>
                <el-button type="danger" @click="delete_record" v-if="edit_data.edit !== 'deleted'">删 除</el-button>
                <el-button type="danger" @click="delete_record" v-if="edit_data.edit === 'deleted'">恢 复</el-button>
            </div>
        </el-dialog>
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
                record_list: [],
                original_data: {},
                show_edit_dialog: false,
                edit_id: 0,
                edit_data: {},
                edit_index: 0,
                edit_mirror: {},
                edited_list: new Set(),
                delete_list: new Set()
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

                                // 重建数据索引
                                that.original_data = {}
                                for (let item of that.record_list) {
                                    that.original_data[item.id] = JSON.parse(JSON.stringify(item));
                                    item["edit"] = "none"
                                }
                            }
                            that.loading_data = false;
                        })
                        .catch(function (res) {
                            console.log(res);
                            that.loading_data = false;
                        })
                }
            },
            edit_record: function (index, row_data) {
                this.show_edit_dialog = true;
                this.edit_id = row_data["id"];
                this.edit_data = row_data;
                this.edit_index = index;
                this.edit_mirror = this.deepCopy(row_data);
            },
            cancel_edit: function () {
                this.show_edit_dialog = false;
                for(let key in this.edit_mirror){
                    this.record_list[this.edit_index][key] = this.edit_mirror[key];
                }
            },
            rollback_record: function () {
                let that_data = this.record_list[this.edit_index]
                that_data["edit"] = "none"
                this.$set(this.record_list, this.edit_index, that_data)
                for (let key in this.original_data[this.edit_id]) {
                    this.record_list[this.edit_index][key] = this.original_data[this.edit_id][key];
                }
            },
            delete_record: function () {
                if(this.edit_data["edit"] === "deleted"){
                    let that_data = this.record_list[this.edit_index]
                    that_data["edit"] = ""
                    this.$set(this.record_list, this.edit_index, that_data)
                }else{
                    let that_data = this.record_list[this.edit_index]
                    that_data["edit"] = "deleted"
                    this.$set(this.record_list, this.edit_index, that_data)
                }
            },
            confirm_edit: function () {
                this.show_edit_dialog = false;
            },

            row_class: function ({row}) {

                console.log(row["edit"])
                if (row["edit"] === "deleted") {
                    return "deleted-row"
                }

                // 比对数据
                let old_data = this.original_data[row.id];
                row["edit"] = "none"
                for (let key of Object.keys(old_data)) {
                    if (old_data[key] !== row[key]) {
                        row["edit"] = "edited";
                        return "warning-row"
                    }
                }
                return ""
            },
            deepCopy: function (item) {
                return JSON.parse(JSON.stringify(item))
            }
        },
        mounted() {
            this.switch_host("refresh");
        }
    }
</script>

<style lang="scss">
    .el-table .warning-row {
        background: oldlace;
    }

    .el-table .deleted-row {
        background: #fef0f0;
    }

</style>