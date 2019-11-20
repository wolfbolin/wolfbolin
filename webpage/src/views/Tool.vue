<template>
    <div class="wb-tool">
        <Title path="tools"></Title>
        <div class="wb-path inner">
            <el-breadcrumb separator-class="el-icon-arrow-right" class="wb-crumb">
                <template v-for="item in nav_path">
                    <el-breadcrumb-item :to="{ path: item.path }" :replace="true" :key="item.path">
                        {{item.label}}
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
                        <el-tabs type="border-card" v-model="active_box">
                            <el-tab-pane v-for="box in box_list" :key="box.name" :label="box.label" :name="box.name">
                                <el-collapse v-model="active_tool" accordion>
                                    <el-collapse-item v-for="(tool, index) in box.tool_list" :key="tool" :name="tool">
                                        <template slot="title">
                                            <p>{{box[box.tool_list[index]].title}}</p>
                                        </template>
                                        <div class="detail">
                                            <p>{{box[box.tool_list[index]].desc}}</p>
                                            <el-button type="primary" size="mini" v-on:click="open_mod" plain>
                                                加载
                                            </el-button>
                                        </div>
                                    </el-collapse-item>
                                </el-collapse>
                            </el-tab-pane>
                        </el-tabs>
                    </div>
                </el-col>
                <el-col :xs="24" :sm="18">
                    <el-card class="wb-tool">
                        <component :is="mod_now"></component>
                    </el-card>
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
                mod_now: () => import(`@/components/tool/welcome`),
                nav_path: [{path: '/tools', label: '工具箱'}],
                box_list: this.$store.state.box_list,
                tool_index: {},
                active_tool: "",
                active_box: "",
                username: "",
                password: "",
            }
        },
        methods: {
            open_mod: function () {
                console.log("Open mod: ", this.active_box, ":", this.active_tool);

                while (this.nav_path.length > 1) {
                    this.nav_path.pop()
                }
                let last_path = this.nav_path[this.nav_path.length - 1].path;
                let new_path = last_path + '/' + this.active_box;
                let path_label = this.box_list[this.active_box].label;
                this.nav_path.push({path: new_path, label: path_label});
                if (this.active_tool !== "") {
                    last_path = new_path;
                    new_path = last_path + '/' + this.active_tool;
                    path_label = this.box_list[this.active_box][this.active_tool].title;
                    this.nav_path.push({path: new_path, label: path_label});

                    this.mod_now = () => import(`@/components/tool/${this.active_tool}`);
                }
                this.$router.replace(new_path);

            },
            jump_path: function (url_path) {
                console.log("Router: ", url_path);
                let path_array = url_path.split('/');
                let path_box, path_tool = "";

                if (path_array.length >= 3) {
                    path_box = path_array[2]
                }
                if (path_array.length >= 4) {
                    path_tool = path_array[3]
                }

                if (this.box_list.hasOwnProperty(path_box)) {
                    this.active_box = path_box
                } else {
                    this.active_box = Object.keys(this.box_list)[0]
                }

                if (this.box_list[this.active_box].tool_list.includes(path_tool)) {
                    this.active_tool = path_tool;
                } else {
                    this.active_tool = ""
                }
                this.open_mod()
            }
        },
        mounted() {
            this.jump_path(this.$route.path);
        },
        watch: {
            $route() {
                this.jump_path(this.$route.path);
            }
        }
    }
</script>

<style lang="scss" scoped>
    .wb-tool {
        .wb-crumb {
            margin: 20px;
            font-size: 1.18em;
        }

        .wb-content {
            .wb-login {
                margin-bottom: 20px;

                .login-header {
                    clear: both;

                    span {
                        font-weight: 600;
                    }

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

            .wb-box {
                .detail {
                    .el-button {
                        width: 100%;
                    }
                }
            }
        }
    }
</style>