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
            <el-table :data="domain_table" :row-class-name="mark_record">>
                <el-table-column prop="index" label="序号"></el-table-column>
                <el-table-column prop="sub_domain" label="子域"></el-table-column>
                <el-table-column prop="r_type" label="类型"></el-table-column>
                <el-table-column prop="record" label="记录"></el-table-column>
                <el-table-column prop="ttl" label="TTL"></el-table-column>
                <el-table-column prop="mx" label="MX"></el-table-column>
                <el-table-column prop="status" label="状态"></el-table-column>
                <el-table-column label="操作" width="240">
                    <template slot-scope="scope">
                        <el-button v-if="scope.row !== edit_object"
                                   type="success" size="mini" @click="editRow(scope.$index, scope.row)">
                            编辑
                        </el-button>
                        <el-button v-else type="warning" size="mini" @click="saveRow(scope.$index, scope.row)">
                            保存
                        </el-button>
                        <el-button size="mini" @click="upRow(scope.$index, scope.row)">上移</el-button>
                        <el-button size="mini" @click="downRow(scope.$index, scope.row)">下移</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <div class="wb-edit">
            <el-row v-if="edit_object !== null" :gutter="20">
                <el-col :span="24">
                    <div class="edit-title">
                        <p>正在修改：{{edit_object.sub_domain}}.{{active_domain}}</p>
                        <el-switch :v-model="true" active-color="#09bb07" inactive-color="#e64340"></el-switch>
                    </div>
                </el-col>
                <el-col :span="12">
                    <el-form label-position="left" label-width="auto" :model="edit_object">
                        <el-form-item label="域名">
                            <el-input v-model="active_domain"></el-input>
                        </el-form-item>
                        <el-form-item label="类型">
                            <el-input v-model="edit_object.r_type"></el-input>
                        </el-form-item>
                        <el-form-item label="TTL">
                            <el-input v-model="edit_object.ttl"></el-input>
                        </el-form-item>
                    </el-form>
                </el-col>
                <el-col :span="12">
                    <el-form label-position="left" label-width="auto" :model="edit_object">
                        <el-form-item label="子域">
                            <el-input v-model="edit_object.sub_domain"></el-input>
                        </el-form-item>
                        <el-form-item label="记录">
                            <el-input v-model="edit_object.record"></el-input>
                        </el-form-item>
                        <el-form-item label="MX">
                            <el-input v-model="edit_object.mx"></el-input>
                        </el-form-item>
                    </el-form>
                </el-col>
                <el-col :span="24">
                    <el-button type="danger" style="width: 100%" plain>删除</el-button>
                </el-col>
            </el-row>
<!--            <el-form v-if="edit_object !== null" label-position="left" label-width="20%" :model="edit_object">-->
<!--&lt;!&ndash;                <el-form-item label="状态">&ndash;&gt;-->
<!--&lt;!&ndash;                    <el-switch&ndash;&gt;-->
<!--&lt;!&ndash;                            :v-model="true"&ndash;&gt;-->
<!--&lt;!&ndash;                            active-color="#09bb07"&ndash;&gt;-->
<!--&lt;!&ndash;                            inactive-color="#e64340">&ndash;&gt;-->
<!--&lt;!&ndash;                    </el-switch>&ndash;&gt;-->
<!--&lt;!&ndash;                </el-form-item>&ndash;&gt;-->
<!--                <el-form-item label="域名">-->
<!--                    <el-input v-model="active_domain"></el-input>-->
<!--                </el-form-item>-->
<!--&lt;!&ndash;                <el-form-item label="子域">&ndash;&gt;-->
<!--&lt;!&ndash;                    <el-input v-model="edit_object.sub_domain"></el-input>&ndash;&gt;-->
<!--&lt;!&ndash;                </el-form-item>&ndash;&gt;-->
<!--&lt;!&ndash;                <el-form-item label="类型">&ndash;&gt;-->
<!--&lt;!&ndash;                    <el-input v-model="edit_object.r_type"></el-input>&ndash;&gt;-->
<!--&lt;!&ndash;                </el-form-item>&ndash;&gt;-->
<!--&lt;!&ndash;                <el-form-item label="记录">&ndash;&gt;-->
<!--&lt;!&ndash;                    <el-input v-model="edit_object.record"></el-input>&ndash;&gt;-->
<!--&lt;!&ndash;                </el-form-item>&ndash;&gt;-->
<!--&lt;!&ndash;                <el-form-item label="TTL">&ndash;&gt;-->
<!--&lt;!&ndash;                    <el-input v-model="edit_object.ttl"></el-input>&ndash;&gt;-->
<!--&lt;!&ndash;                </el-form-item>&ndash;&gt;-->
<!--&lt;!&ndash;                <el-form-item label="MX">&ndash;&gt;-->
<!--&lt;!&ndash;                    <el-input v-model="edit_object.mx"></el-input>&ndash;&gt;-->
<!--&lt;!&ndash;                </el-form-item>&ndash;&gt;-->
<!--            </el-form>-->
        </div>
    </div>
</template>

<script>
    export default {
        name: "dns",
        data() {
            return {
                active_domain: "",
                edit_object: null,
                domain_list: ["example.com"],
                domain_table: [
                    {
                        status: "启用",
                        index: 1,
                        sub_domain: "a.t-db.cn",
                        r_type: "A",
                        record: "1.2.3.4",
                        ttl: "600",
                        mx: "",
                        edit: ""
                    }
                ]
            }
        },
        methods: {
            change_domain: function () {

            },
            mark_record: function (row) {
                let index = row.rowIndex;
                let data = row.row;
                console.log("Mark record: ", index, "=>", row);

                if (data.edit === "new") {
                    return "new-row"
                } else if (data.edit === "edit") {
                    return "edit-row"
                } else {
                    return ""
                }
            },
            editRow: function (index, data) {
                console.log("Edit domain: ", index, "=>", data);
                this.edit_object = data;

                console.log(data)
            },
            saveRow: function (index, data) {
                console.log("Edit finish: ", index, "=>", data);
                this.edit_object = null;
            },
            upRow: function () {

            },
            downRow: function () {

            }
        }
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

                .el-switch{
                    float: right;
                    margin: 1em;
                }
            }
        }
    }

</style>