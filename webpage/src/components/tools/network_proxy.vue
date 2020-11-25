<template>
    <div class="wb-proxy">
        <h2>Proxy规则</h2>
        <p v-if="user_token.length === 0">请先验证用户交互Token
            <el-button type="text" @click="check_token">检查状态</el-button>
        </p>
        <div v-if="user_token.length !== 0">
            <el-button-group class="wb-option">
                <el-button type="primary" icon="el-icon-refresh" @click="update_rule">刷新规则</el-button>
                <el-button type="primary" icon="el-icon-plus" @click="add_rule">新增规则</el-button>
                <el-button type="primary" icon="el-icon-finished" @click="commit_change">提交修改</el-button>
            </el-button-group>
            <el-table :data="proxy_rule" style="width: 100%" v-loading="loading_data" border
                      :row-class-name="row_class" ref="rule_table">
                <el-table-column prop="type" min-width="120" label="模式" sortable filter-placement="bottom"
                                 :filters="type_filters" :filter-method="table_filter"></el-table-column>
                <el-table-column prop="content" min-width="120" label="规则" sortable></el-table-column>
                <el-table-column prop="group" min-width="80" label="分组" sortable filter-placement="bottom"
                                 :filters="group_filters" :filter-method="table_filter"></el-table-column>
                <el-table-column label="操作" width="80">
                    <template slot-scope="scope">
                        <el-button size="mini" @click="edit_rule(scope.$index, scope.row)">编辑</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <el-dialog title="编辑信息" :visible.sync="show_edit_dialog" :show-close="false"
                       :close-on-click-modal="false" :close-on-press-escape="false">
                <el-form ref="form" :model="edit_data" label-width="80px">
                    <el-form-item label="规则">
                        <el-input v-model="edit_data.content"></el-input>
                    </el-form-item>
                    <el-form-item label="模式">
                        <el-select v-model="edit_data.type" placeholder="请选择模式">
                            <el-option label="MATCH" value="MATCH"></el-option>
                            <el-option label="DOMAIN" value="DOMAIN"></el-option>
                            <el-option label="DOMAIN-SUFFIX" value="DOMAIN-SUFFIX"></el-option>
                            <el-option label="DOMAIN-KEYWORD" value="DOMAIN-KEYWORD"></el-option>
                            <el-option label="GEOIP" value="GEOIP"></el-option>
                            <el-option label="IP-CIDR" value="IP-CIDR"></el-option>
                            <el-option label="SRC-IP-CIDR" value="SRC-IP-CIDR"></el-option>
                            <el-option label="DST-PORT" value="DST-PORT"></el-option>
                            <el-option label="SRC-PORT" value="SRC-PORT"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="分组">
                        <el-select v-model="edit_data.group" filterable allow-create default-first-option
                                   placeholder="请选择规则分组">
                            <el-option v-for="item in group_filters" :key="item.value"
                                       :label="item.text" :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button type="primary" @click="confirm_edit">确 定</el-button>
                    <el-button type="success" @click="cancel_edit">取 消</el-button>
                    <el-button type="danger" @click="delete_rule">删 除</el-button>
                </div>
            </el-dialog>
        </div>
    </div>
</template>

<script>
    export default {
        name: "network_clash",
        data() {
            return {
                user_token: this.$store.state.user_token,
                loading_data: false,
                show_edit_dialog: false,
                proxy_rule: [],
                type_filters: [],
                group_filters: [],
                edit_data: {},
                edit_index: -1
            }
        },
        methods: {
            check_token: function () {
                this.user_token = this.$store.state.user_token;
                if (this.user_token.length === 0) {
                    this.$message.error("请先完成用户Token验证")
                }else{
                    this.update_rule();
                }
            },
            add_rule: function () {
                this.edit_data = {
                    content: "example",
                    type: "DOMAIN",
                    group: "LAN",
                }
                this.edit_index = -1
                this.edit_mirror = {}
                this.show_edit_dialog = true;
            },
            edit_rule: function (index, row_data) {
                this.edit_data = row_data;
                this.edit_index = index;
                this.edit_mirror = this.deepCopy(row_data);
                this.show_edit_dialog = true;
            },
            confirm_edit: function () {
                this.show_edit_dialog = false;
                if (this.edit_index === -1) {
                    this.proxy_rule.unshift(this.deepCopy(this.edit_data))
                }
                this.rebuild_filter();
            },
            cancel_edit: function () {
                this.show_edit_dialog = false;
                if (this.edit_index === -1) {
                    return;
                }
                for (let key in this.edit_mirror) {
                    this.proxy_rule[this.edit_index][key] = this.edit_mirror[key];
                }
            },
            delete_rule: function () {
                this.show_edit_dialog = false;
                if (this.edit_index === -1) {
                    return;
                }
                for (let i = 0; i < this.proxy_rule.length; i++) {
                    if (this.proxy_rule[i] === this.edit_data) {
                        this.proxy_rule.splice(i, 1)
                    }
                }
                this.rebuild_filter();
            },
            update_rule: function () {
                let that = this;
                this.loading_data = true;
                let data_host = this.$store.state.host;
                let user_token = this.$store.state.user_token;
                let http_url = data_host + `/network/proxy/rule?token=${user_token}`
                this.$http.get(http_url)
                    .then(function (res) {
                        if (res.data.status === 'OK') {
                            that.proxy_rule = res.data.data;
                            that.$message('数据已刷新');

                            that.rebuild_filter();
                        }
                        that.loading_data = false;
                    })
                    .catch(function (res) {
                        console.log(res);
                        that.loading_data = false;
                    })
            },
            rebuild_filter: function () {
                let type_filters = new Set();
                let group_filters = new Set();
                for (let it of this.proxy_rule) {
                    type_filters.add(it["type"])
                    group_filters.add(it["group"])
                }
                this.type_filters = [];
                for (let it of type_filters) {
                    this.type_filters.push({
                        text: it,
                        value: it
                    })
                }
                this.group_filters = [];
                for (let it of group_filters) {
                    this.group_filters.push({
                        text: it,
                        value: it
                    })
                }
            },
            commit_change: function () {
                console.log(`Commit Change：`, this.proxy_rule)

                let that = this;
                this.loading_data = true;
                let data_host = this.$store.state.host;
                let user_token = this.$store.state.user_token;
                let http_url = data_host + `/network/proxy/rule?token=${user_token}`
                this.$http.put(http_url, this.proxy_rule)
                    .then(function (res) {
                        if (res.data.status === 'OK') {
                            that.proxy_rule = res.data.data;
                            that.$message({
                                message: '数据更新成功',
                                type: 'success'
                            });

                            that.rebuild_filter();
                        }
                        that.loading_data = false;
                    })
                    .catch(function (res) {
                        console.log(res);
                        that.loading_data = false;
                    })
            },
            row_class: function ({row}) {
                if (row.group === "REJECT") {
                    return "reject-line"
                }
                if (row.group === "DEV") {
                    return "special-line"
                }
                if (row.group === "JPN") {
                    return "yellow-line"
                }
                if (row.group !== "ACC") {
                    return "region-line"
                }
            },
            table_filter: function (value, row, column) {
                let col_key = column.property;
                let col_val = row[col_key];
                return value === col_val
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
    .wb-proxy {
        .wb-option {
            margin-bottom: 16px;
        }
    }

    .el-table {
        .special-line {
            background: #f0f9eb;
        }

        .region-line {
            background: #ecf5ff;
        }

        .reject-line {
            background: #fef0f0;
        }

        .yellow-line {
            background: #fdf6ec;
        }
    }

    .el-table-filter__bottom {
        text-align: center;
    }

    .el-table-filter__bottom button {
        margin: 0 16px;
    }
</style>