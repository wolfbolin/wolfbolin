<template>
    <div class="wb-dns">
        <el-alert v-if="role === 'admin'" title="用户已登录，请谨慎操作" type="success" :closable="false"></el-alert>
        <el-alert v-else title="请先登录后再操作" type="warning" :closable="false"></el-alert>
        <el-table :data="tableData" style="width: 100%" lazy :load="loadRecord"
                  :tree-props="{children: 'children', hasChildren: 'hasChildren'}">>
            <el-table-column prop="index" label="序号"></el-table-column>
            <el-table-column prop="domain" label="域名"></el-table-column>
            <el-table-column prop="type" label="类型"></el-table-column>
            <el-table-column prop="record" label="记录"></el-table-column>
            <el-table-column prop="ttl" label="TTL"></el-table-column>
            <el-table-column prop="mx" label="MX"></el-table-column>
            <el-table-column prop="status" label="状态"></el-table-column>
            <el-table-column label="操作" width="240">
                <template slot-scope="scope">
                    <el-button type="success" size="mini" @click="editRow(scope.$index, scope.row)">编辑</el-button>
                    <el-button size="mini" @click="upRow(scope.$index, scope.row)">上移</el-button>
                    <el-button size="mini" @click="downRow(scope.$index, scope.row)">下移</el-button>
                </template>
            </el-table-column>
        </el-table>
        <div>
            <div class="editLine">
                <p>域名</p>
                <el-input v-model="domain" placeholder="子域名"></el-input>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "dns",
        data() {
            return {
                role: "",
                tableData: [
                    {
                        index: 1,
                        domain: "a.t-db.cn",
                        type: "A",
                        record: "1.2.3.4",
                        ttl: "600",
                        mx: "",
                        status: "开启"
                    }
                ],
                domain: ""
            }
        },
        methods: {
            loadRecord: function () {

            },
            editRow: function () {

            },
            upRow: function () {

            },
            downRow: function () {

            }
        }
    }
</script>

<style lang="scss" scoped>
    .editLine {

    }
</style>