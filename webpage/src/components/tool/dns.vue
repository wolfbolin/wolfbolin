<template>
    <div class="wb-dns">
        <el-alert title="用户已登录，请谨慎操作" type="success" :closable="false"></el-alert>
        <el-alert title="请先登录后再操作" type="warning" :closable="false"></el-alert>

        <div class="wb-view">
            <el-tabs v-model="active_domain" type="card" @tab-click="change_domain">
                <template v-for="domain in domain_list">
                    <el-tab-pane :key="domain" :label="domain" :name="domain"></el-tab-pane>
                </template>
            </el-tabs>
            <div>
                <el-row :gutter="20">
                    <el-col :xs="24" :sm="8">
                        <el-button type="primary" style="width: 100%" plain @click="addRow">添加</el-button>
                    </el-col>
                    <el-col :xs="24" :sm="8">
                        <el-button type="warning" style="width: 100%" plain @click="resetTable">重置</el-button>
                    </el-col>
                    <el-col :xs="24" :sm="8">
                        <el-button type="danger" style="width: 100%" plain @click="saveTable">保存</el-button>
                    </el-col>
                </el-row>
            </div>
            <el-table :data="domain_table" :row-class-name="mark_record">>
                <el-table-column prop="code" label="编号"/>
                <el-table-column prop="sub_domain" label="子域"/>
                <el-table-column prop="r_type" label="类型"/>
                <el-table-column prop="record" label="记录"/>
                <el-table-column prop="ttl" label="TTL"/>
                <el-table-column prop="mx" label="MX"/>
                <el-table-column prop="status" label="状态"/>
                <el-table-column label="操作" width="240">
                    <template slot-scope="scope">
                        <el-button v-if="scope.$index !== edit_index"
                                   type="success" size="mini" @click="editRow(scope.$index, scope.row)">
                            编辑
                        </el-button>
                        <el-button v-else type="warning" size="mini" @click="cancelRow(scope.$index, scope.row)">
                            取消
                        </el-button>
                        <el-button size="mini" @click="upRow(scope.$index, domain_table)">上移</el-button>
                        <el-button size="mini" @click="downRow(scope.$index, domain_table)">下移</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <div class="wb-edit">
            <el-row v-if="edit_object !== null" :gutter="20">
                <el-col :span="24">
                    <div class="edit-title">
                        <p>正在修改：{{edit_object.sub_domain}}.{{active_domain}}</p>
                        <el-switch v-model="edit_object.status" active-color="#09bb07" inactive-color="#e64340"/>
                    </div>
                </el-col>
                <el-col :span="12">
                    <el-form label-position="left" label-width="auto" :model="edit_object">
                        <el-form-item label="域名">
                            <el-input v-model="active_domain" :disabled="true"/>
                        </el-form-item>
                        <el-form-item label="类型">
                            <el-input v-model="edit_object.r_type"/>
                        </el-form-item>
                        <el-form-item label="TTL">
                            <el-input v-model="edit_object.ttl"/>
                        </el-form-item>
                    </el-form>
                </el-col>
                <el-col :span="12">
                    <el-form label-position="left" label-width="auto" :model="edit_object">
                        <el-form-item label="子域">
                            <el-input v-model="edit_object.sub_domain"/>
                        </el-form-item>
                        <el-form-item label="记录">
                            <el-input v-model="edit_object.record"/>
                        </el-form-item>
                        <el-form-item label="MX">
                            <el-input v-model="edit_object.mx"/>
                        </el-form-item>
                    </el-form>
                </el-col>
                <el-col :xs="24" :sm="8">
                    <el-button type="primary" style="width: 100%" plain @click="saveRow">保存</el-button>
                </el-col>
                <el-col :xs="24" :sm="8">
                    <el-button type="warning" style="width: 100%" plain @click="resetRow">重置</el-button>
                </el-col>
                <el-col :xs="24" :sm="8">
                    <el-button type="danger" style="width: 100%" plain @click="deleteRow">删除</el-button>
                </el-col>
            </el-row>
        </div>
    </div>
</template>

<script>
    export default {
        name: "dns",
        data() {
            return {
                active_domain: "",
                edit_index: -1,
                edit_object: null,
                domain_list: ["example.com"],
                source_table: [],
                domain_table: [
                    {
                        code: 132423,
                        status: true,
                        sub_domain: "testA",
                        r_type: "A",
                        record: "1.2.3.4",
                        ttl: "600",
                        mx: "",
                        edit: ""
                    }, {
                        code: 156456,
                        status: true,
                        sub_domain: "testB",
                        r_type: "A",
                        record: "4.5.6.7",
                        ttl: "600",
                        mx: ""
                    },
                ]
            }
        },
        methods: {
            change_domain: function () {

            },
            resetTable: function(){

            },
            saveTable: function(){

            },
            addRow: function () {
                console.log("Add row: ", this.domain_table.length);
                let newObj = {
                    code: 0,
                    status: true,
                    sub_domain: "",
                    r_type: "",
                    record: "",
                    ttl: "",
                    mx: ""
                };
                this.edit_index = this.domain_table.length;
                this.edit_object = this.deepCopy(newObj);
                this.domain_table.push(newObj);
            },
            editRow: function (index, data) {
                console.log("Edit row: ", index, "=>", data);
                this.edit_index = index;
                this.edit_object = this.deepCopy(data);
            },
            cancelRow: function (index, data) {
                console.log("Cancel edit: ", index, "=>", data);
                this.edit_index = -1;
                this.edit_object = null;
            },
            saveRow: function () {
                console.log("Save edit: ", this.edit_index, "=>", this.edit_object);
                this.domain_table[this.edit_index] = this.edit_object;
                this.edit_index = -1;
                this.edit_object = null;
            },
            resetRow: function () {
                console.log("Reset edit: ", this.edit_index, "=>", this.edit_object);
                this.edit_object = this.deepCopy(this.domain_table[this.edit_index]);
            },
            deleteRow: function () {
                console.log("Delete edit: ", this.edit_index, "=>", this.edit_object);
                this.domain_table.splice(this.edit_index, 1);
                this.edit_index = -1;
                this.edit_object = null;
            },
            upRow: function (index, table) {
                console.log("Up row: ", index);
                if (index <= 0) {
                    return 0;
                }
                let tmp_obj = {};
                for (let key in table[index]) {
                    tmp_obj[key] = table[index][key];
                    table[index][key] = table[index - 1][key];
                }
                for (let key in table[index]) {
                    table[index - 1][key] = tmp_obj[key];
                }
            },
            downRow: function (index, table) {
                console.log("Down row: ", index);
                if (index >= table.length - 1) {
                    return 0;
                }
                let tmp_obj = {};
                for (let key in table[index]) {
                    tmp_obj[key] = table[index][key];
                    table[index][key] = table[index + 1][key];
                }
                for (let key in table[index]) {
                    table[index + 1][key] = tmp_obj[key];
                }
            },
            mark_record: function (row) {
                let index = row.rowIndex;
                console.log("Mark record: ", index, "=>", row);

                if (index >= this.source_table.length) {
                    return "new-row";
                } else {
                    for (let key in this.source_table[index]) {
                        // console.log(this.source_table[index][key], this.domain_table[index][key]);
                        if (this.source_table[index][key] !== this.domain_table[index][key]) {
                            return "edit-row";
                        }
                    }
                }
                return "";
            },
            deepCopy: function (obj) {
                return JSON.parse(JSON.stringify(obj));
            }
        },
        mounted() {
            this.active_domain = this.domain_list[0];
            this.source_table = this.deepCopy(this.domain_table);
        },
    }
</script>

<style lang="scss">
    .wb-dns {
        .wb-view {
            .edit-row {
                background: #fdf5e6;
            }

            .new-row {
                background: #e6f8e6;
            }
        }

        .wb-edit {
            margin: 20px;

            .edit-title {
                p {
                    display: inline-block;
                }

                .el-switch {
                    float: right;
                    margin: 1em;
                }
            }
        }
    }

</style>