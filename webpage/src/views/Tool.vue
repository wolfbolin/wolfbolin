<template>
    <div class="wb-tool">
        <Title path="tools"></Title>
        <div class="wb-crumb inner">
            <el-breadcrumb separator-class="el-icon-arrow-right">
                <template v-for="item in nav_path">
                    <el-breadcrumb-item :to="{ path: item.path }" :replace="true" :key="item.path">
                        {{item.name}}
                    </el-breadcrumb-item>
                </template>
            </el-breadcrumb>
            <el-divider></el-divider>
        </div>

        <div class="wb-content inner">
            <el-row :gutter="20">
                <el-col :xs="24" :sm="6">
                    <el-card class="wb-login">
                        <div slot="header" class="login-header">
                            <span>登录</span>
                            <el-button type="text">忽略</el-button>
                        </div>
                        <div class="login-body">
                            <p>部分工具需要身份认证</p>
                            <el-input type="text" v-model="username" clearable>
                                <template slot="prepend">用户</template>
                            </el-input>
                            <el-input type="password" v-model="password" clearable>
                                <template slot="prepend">密码</template>
                            </el-input>
                            <el-button type="primary" plain>验证</el-button>
                        </div>
                    </el-card>
                    <div class="wb-box">
                        <el-tabs type="border-card" v-model="active_box" @tab-click="open_teb">
                            <el-tab-pane v-for="box in box_list" :key="box.name" :label="box.label" :name="box.name">
                                <el-collapse v-model="active_tool" accordion>
                                    <el-collapse-item v-for="tool in box.tool_list" :key="tool.name" :name="tool.name">
                                        <template slot="title">
                                            <p>{{tool.title}}</p>
                                        </template>
                                        <p>{{tool.desc}}</p>
                                    </el-collapse-item>
                                </el-collapse>
                            </el-tab-pane>
                        </el-tabs>
                    </div>
                </el-col>
                <el-col :xs="24" :sm="18">

                </el-col>
            </el-row>
        </div>
    </div>
</template>

<script>
    import Title from '@/components/Title.vue'

    export default {
        name: "Tool",
        components: {
            Title
        },
        data() {
            return {
                nav_path: [{path: '/tools', name: '工具箱'}],
                box: this.$store.state.tab_list,
                active_tool: "",
                active_box: "",
                username: "",
                password: ""
            }
        },
        methods: {
            open_teb: function () {

            },
            select_tool: function(tab, tool){

            },
            jump_path: function (url_path) {
                console.log("Router: ", url_path);
                let path_array = url_path.split('/');
                if (path_array.length >= 3) {
                    this.active_box = path_array[2]
                }
                if (path_array.length >= 4) {
                    this.active_tool = path_array[3]
                }
            }
        },
        mounted() {
            this.jump_path(this.$route.path);

        }
    }
</script>

<style lang="scss" scoped>
    .wb-tool {
        .wb-content {
            .wb-login {
                margin-bottom: 20px;

                .login-header {
                    clear: both;

                    button {
                        float: right;
                        padding: 3px 0;
                    }
                }

                .login-body {
                    p {
                        margin: 0;
                    }

                    .el-input {
                        margin: 10px 0;
                    }

                    button {
                        width: 100%;
                        margin-top: 20px;
                    }
                }
            }
        }
    }
</style>