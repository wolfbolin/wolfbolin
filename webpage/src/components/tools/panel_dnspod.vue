<template>
    <div class="wb-dns">
        <h2>DNS解析</h2>
        <p v-if="password.length === 0">请先验证用户交互Token
            <el-button type="text" @click="check_token">检查状态</el-button>
        </p>
        <el-tabs v-model="active_domain" type="card" @tab-click="handle_tab_click" v-if="password.length !== 0">
            <el-tab-pane v-for="domain of domain_list" :key="domain" :label="domain" :name="domain"></el-tab-pane>
            <el-tab-pane label="刷新" name="refresh-force"></el-tab-pane>
            <el-button-group class="wb-option">
                <el-button type="primary" icon="el-icon-refresh" @click="refresh_record(active_domain)">刷新记录</el-button>
                <el-button type="primary" icon="el-icon-plus" @click="add_record">新增记录</el-button>
                <el-button type="warning" icon="el-icon-sort" v-if="edit_record_order"
                           @click="edit_record_order = ~edit_record_order">编辑顺序
                </el-button>
                <el-button type="primary" icon="el-icon-sort" v-if="~edit_record_order"
                           @click="edit_record_order = ~edit_record_order">编辑顺序
                </el-button>
                <el-button type="primary" icon="el-icon-finished" @click="commit_change">提交修改</el-button>
            </el-button-group>
            <p class="wb-version">数据版本：{{data_version_info}}</p>
            <el-table :data="record_list" style="width: 100%" v-loading="loading_data"
                      :row-class-name="row_class" :cell-class-name="cell_class" border>
                <el-table-column prop="id" label="编号" min-width="100" sortable></el-table-column>
                <el-table-column prop="record" min-width="120" label="记录"></el-table-column>
                <el-table-column prop="domain" min-width="120" label="域名"></el-table-column>
                <el-table-column prop="type" min-width="80" label="类型"></el-table-column>
                <el-table-column prop="ttl" min-width="80" label="TTL"></el-table-column>
                <el-table-column prop="value" min-width="200" label="记录值"></el-table-column>
                <template v-if="edit_record_order">
                    <el-table-column label="操作" width="200">
                        <template slot-scope="scope">
                            <el-button-group>
                                <el-button type="primary" icon="el-icon-plus"
                                           @click="record_up(scope.$index)">上移
                                </el-button>
                                <el-button type="primary" icon="el-icon-finished"
                                           @click="record_down(scope.$index)">下移
                                </el-button>
                            </el-button-group>
                        </template>
                    </el-table-column>
                </template>
                <template v-if="~edit_record_order">
                    <el-table-column label="操作" width="80">
                        <template slot-scope="scope">
                            <el-button size="mini" @click="edit_record(scope.$index, scope.row)">编辑</el-button>
                        </template>
                    </el-table-column>
                </template>
            </el-table>
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
                            <el-option label="CNAME" value="CNAME"></el-option>
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
                    <el-form-item label="TTL">
                        <el-input v-model="edit_data.ttl" type="number" placeholder="120~3600s"></el-input>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button type="primary" @click="confirm_edit">确 定</el-button>
                    <el-button type="success" @click="cancel_edit">取 消</el-button>
                    <el-button type="warning" @click="rollback_edit" v-if="edit_index !== -1">回 滚</el-button>
                    <el-button type="danger" @click="delete_record"
                               v-if="edit_index !== -1 && edit_data.edit !== 'deleted'">删 除
                    </el-button>
                    <el-button type="danger" @click="delete_record"
                               v-if="edit_index !== -1 && edit_data.edit === 'deleted'">恢 复
                    </el-button>
                </div>
            </el-dialog>
        </el-tabs>
    </div>
</template>

<script>
    export default {
        name: "dns",
        data() {
            return {
                username: this.$store.state.username,
                password: this.$store.state.password,
                active_domain: null,
                loading_data: false,
                show_edit_dialog: false,
                edit_record_order: false,
                data_version_info: "",
                domain_list: [],
                record_list: [],
                tag_input_key: "",
                original_data: {},
                edit_id: 0,
                edit_data: {},
                edit_index: 0,
                edit_mirror: {}
            }
        },
        methods: {
            check_token: function () {
                this.username = this.$store.state.username;
                this.password = this.$store.state.password;
                if (this.password.length === 0) {
                    this.$message.error("请先完成用户Token验证")
                }else{
                    this.switch_host("refresh");
                }
            },
            handle_tab_click: function (tab) {
                if (tab.name === "refresh-force") {
                    this.switch_host("refresh", "true");
                } else {
                    this.switch_host(tab.name);
                }
            },
            switch_host: function (domain, force = "false") {
                console.log("Jump to host:", domain);
                if (domain === "refresh") {
                    let that = this;
                    let data_host = this.$store.state.host;
                    let http_url = data_host + `/network/dns/domain?user=${this.username}&pass=${this.password}&refresh=${force}`
                    this.$http.get(http_url)
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
                    this.refresh_record(domain, "false")
                }
            },
            refresh_record: function (domain, force = "true") {
                let that = this;
                this.loading_data = true;
                let data_host = this.$store.state.host;
                let http_url = data_host + `/network/dns/domain/${domain}/record?user=${this.username}&pass=${this.password}&refresh=${force}`
                this.$http.get(http_url)
                    .then(function (res) {
                        if (res.data.status === 'OK') {
                            console.log("记录数据源", res.data.data["source"]);
                            that.data_version_info = res.data.data["source"];
                            that.record_list = res.data.data["record_list"];
                            that.$message('数据已刷新');

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
            },
            add_record: function () {
                this.edit_id = 0
                this.edit_data = {
                    id: "0",
                    domain: this.active_domain,
                    edit: "none",
                    record: "example",
                    status: "enable",
                    type: "A",
                    ttl: "600",
                    value: "127.0.0.1",
                }
                this.edit_index = -1
                this.edit_mirror = {}
                this.show_edit_dialog = true;
            },
            edit_record: function (index, row_data) {
                this.show_edit_dialog = true;
                this.edit_id = row_data["id"];
                this.edit_data = row_data;
                this.edit_index = index;
                this.edit_mirror = this.deepCopy(row_data);
            },
            confirm_edit: function () {
                if (this.edit_index === -1) {
                    this.record_list.push(this.deepCopy(this.edit_data))
                }
                this.show_edit_dialog = false;
            },
            cancel_edit: function () {
                this.show_edit_dialog = false;
                if (this.edit_index === -1) {
                    return;
                }
                for (let key in this.edit_mirror) {
                    this.record_list[this.edit_index][key] = this.edit_mirror[key];
                }
            },
            rollback_edit: function () {
                if (this.edit_index === -1) {
                    return;
                }
                let that_data = this.record_list[this.edit_index]
                that_data["edit"] = "none"
                this.$set(this.record_list, this.edit_index, that_data)
                for (let key in this.original_data[this.edit_id]) {
                    this.record_list[this.edit_index][key] = this.original_data[this.edit_id][key];
                }
            },
            delete_record: function () {
                if (this.edit_index === -1) {
                    return;
                }
                if (this.edit_data["edit"] === "deleted") {
                    let that_data = this.record_list[this.edit_index]
                    that_data["edit"] = ""
                    this.$set(this.record_list, this.edit_index, that_data)
                } else {
                    let that_data = this.record_list[this.edit_index]
                    that_data["edit"] = "deleted"
                    this.$set(this.record_list, this.edit_index, that_data)
                }
            },
            record_up: function (index) {
                if (index === 0) {
                    return;
                }
                let temp = this.record_list[index]
                this.$set(this.record_list, index, this.record_list[index - 1])
                this.$set(this.record_list, index - 1, temp)
            },
            record_down: function (index) {
                if (index === this.record_list.length - 1) {
                    return;
                }
                let temp = this.record_list[index]
                this.$set(this.record_list, index, this.record_list[index + 1])
                this.$set(this.record_list, index + 1, temp)
            },
            commit_change: function () {
                console.log(`Commit Change ${this.active_domain}：`, this.record_list)

                let that = this;
                this.loading_data = true;
                let data_host = this.$store.state.host;
                let http_url = data_host + `/network/dns/domain/${this.active_domain}/record?user=${this.username}&pass=${this.password}`
                this.$http.put(http_url, this.record_list)
                    .then(function (res) {
                        if (res.data.status === 'OK') {
                            console.log("记录数据源", res.data.data["source"]);
                            that.data_version_info = res.data.data["source"];
                            that.record_list = res.data.data["record_list"];
                            that.$message({
                                message: '数据更新成功',
                                type: 'success'
                            });

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
            },
            row_class: function ({row}) {
                if (row.record === "www") {
                    return "split-line"
                }

                if (row["edit"] === "deleted") {
                    return "deleted-row"
                }
                if (row.id === "0") {
                    row["edit"] = "none"
                    return "success-row"
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
            cell_class: function (cell_info) {
                let this_cell_class = ""
                let col_key = cell_info.column.property;
                if (col_key === "value") {
                    this_cell_class += "ellipsis_cell "
                }
                return this_cell_class
            },
            deepCopy: function (item) {
                return JSON.parse(JSON.stringify(item))
            }
        },
        mounted() {
            this.check_token()
        }
    }
</script>

<style lang="scss">
    .wb-dns {
        .wb-option {
            margin: 8px 0;
        }

        .wb-version {
            display: inline-block;
            margin-left: 16px;
        }
    }

    .el-table .split-line {
        background: #f4f4f5;
    }

    .el-table .success-row {
        background: #f0f9eb;
    }

    .el-table .warning-row {
        background: oldlace;
    }

    .el-table .deleted-row {
        background: #fef0f0;
    }

    .ellipsis_cell .cell {
        white-space: nowrap;
    }

</style>
