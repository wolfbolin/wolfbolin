<template>
    <div class="wb-tool">
        <Title path="tools"></Title>
        <div class="wb-content inner">
            <div class="path">

            </div>
            <el-divider></el-divider>
            <div class="tool">
                <component v-if="current_component" :is="current_component"></component>
                <p v-else class="guide">请在下方选项卡中选择需要加载的工具</p>
            </div>
            <el-divider></el-divider>
            <el-row :gutter="20" class="selection">
                <el-col :xs="24" :sm="8">
                    <h2>工具说明</h2>
                    <p>{{tool_detail}}</p>
                    <el-divider></el-divider>
                    <div class="login">
                        <p>请在登录后使用该工具</p>
                        <el-input type="text" v-model="username" clearable>
                            <template slot="prepend">用户</template>
                        </el-input>
                        <el-input type="password" v-model="password" clearable>
                            <template slot="prepend">密码</template>
                        </el-input>
                        <el-button type="primary" plain>主要按钮</el-button>
                    </div>
                </el-col>
                <el-col :xs="24" :sm="16">
                    <div class="box">
                        <el-tabs v-model="active_box" @tab-click="open_box">
                            <el-tab-pane v-for="box in tool_box" :key="box.name" :label="box.label" :name="box.name">
                                <el-collapse v-model="active_tool" accordion>
                                    <el-collapse-item v-for="tool in box.tool_list" :key="tool.name" :name="tool.name">
                                        <template slot="title">
                                            <p style="margin-right: 16px">{{tool.title}}</p>
                                            <el-button v-if="active_tool" v-on:click="open_tool(box.name, tool)"
                                                       type="primary" size="mini" plain>打开工具
                                            </el-button>
                                        </template>
                                        <p>{{tool.desc}}</p>
                                    </el-collapse-item>
                                </el-collapse>
                            </el-tab-pane>
                        </el-tabs>
                    </div>
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
                active_box: "",
                active_tool: "",
                nav_path: [{path: '/tools', name: '工具箱'}],
                current_component: null,
                tool_box: this.$store.state.tool_box,
                tool_detail: "请选择工具",
                need_auth: false,
                username: "",
                password: ""
            }
        },
        methods: {
            open_path: function (url_path) {
                let path_array = url_path.split('/');

                this.nav_path = [{path: '/tools', name: '工具箱'}];

                if (path_array.length >= 3) {
                    let box_info = {};
                    for (let box of this.tool_box) {
                        if (box.name === path_array[2]) {
                            box_info = box;
                            break;
                        }
                    }
                    this.open_box(box_info);

                    if (path_array.length >= 4) {
                        let tool_info = {};
                        for (let tool of box_info.tool_list) {
                            if (tool.name === path_array[3]) {
                                tool_info = tool;
                            }
                        }
                        this.open_tool(box_info.name, tool_info)
                    } else {
                        this.current_component = null
                    }
                } else {
                    this.open_box(this.tool_box[0]);
                    this.current_component = null;
                    this.need_auth = false;
                    this.detail = "暂无说明";
                }
            },
            open_box: function (box_info) {
                console.log("open_box", box_info);
                if (box_info === {}) {
                    return 0;
                }
                this.active_box = box_info.name;

                while (this.nav_path.length > 1) {
                    this.nav_path.pop();
                }
                this.nav_path.push(
                    {
                        path: `/tools/${box_info.name}`,
                        name: box_info.label
                    }
                );
            },
            open_tool: function (box_name, tool_info) {
                console.log("open_tool", box_name, tool_info);
                if (tool_info === {}) {
                    return 0;
                }
                console.log(tool_info);
                this.need_auth = tool_info.auth;
                this.tool_detail = tool_info.detail;
                this.current_component = () => import(`@/components/tool/${tool_info.name}`);

                while (this.nav_path.length > 2) {
                    this.nav_path.pop();
                }
                this.nav_path.push(
                    {
                        path: `/tools/${box_name}/${tool_info.name}`,
                        name: tool_info.title
                    }
                );
                this.$router.replace(`/tools/${box_name}/${tool_info.name}`);
            }
        },
        watch: {
            '$route.path': function (to) {
                this.open_path(to);
            }
        },
        mounted() {
            this.open_path(this.$route.path);
        }
    }
</script>

<style lang="scss" scoped>
    .wb-tool {
            .wb-content {
            padding: 0 8px;
            .path {
                margin: 24px 0;
            }

            .tool {
                .guide {
                    text-align: center;
                    padding: 48px 0;
                }
            }

            .selection {
                margin-bottom: 36px;

                .login {
                    button {
                        margin: 16px 0;
                        width: 100%;
                        float: right;
                    }
                }

            }
        }
    }
</style>