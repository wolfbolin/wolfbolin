<template>
    <div class="wb-tool">
        <section class="wb-title">
            <div class="inner">
                <p>WolfBolin</p>
                <h1>在线工具箱</h1>
            </div>
        </section>
        <section class="wb-content">
            <div class="inner">
                <el-row :gutter="20">
                    <el-col :xs="24" :sm="6">
                        <div class="wb-part">
                            <el-card class="wb-login">
                                <div slot="header" class="login-header">
                                    <span>网络验证</span>
                                </div>
                                <div class="login-body">
                                    <el-input type="text" placeholder="请输入账户"
                                              v-model="username" autofocus clearable>
                                        <template slot="prepend">用户</template>
                                    </el-input>
                                    <el-input type="password" placeholder="请输入秘钥" v-model="password"
                                              @keyup.enter.native="check_token" clearable>
                                        <template slot="prepend">秘钥</template>
                                    </el-input>
                                    <el-checkbox v-model="keep_token">保存秘钥</el-checkbox>
                                    <el-button type="primary" plain @click="check_token">验证</el-button>
                                    <p>网络连接
                                        <i class="el-icon-loading" style="color: orange"
                                           v-if="connected === 'Unknown'"></i>
                                        <i class="el-icon-circle-check" style="color: green"
                                           v-if="connected === 'OK'"></i>
                                        <i class="el-icon-circle-close" style="color: red"
                                           v-if="connected === 'Error'"></i>
                                    </p>
                                    <p>身份验证
                                        <i class="el-icon-loading" style="color: orange"
                                           v-if="token_res === 'Unknown'"></i>
                                        <i class="el-icon-circle-check" style="color: green"
                                           v-if="token_res === 'OK'"></i>
                                        <i class="el-icon-circle-close" style="color: red"
                                           v-if="token_res === 'Error'"></i>
                                    </p>
                                </div>

                            </el-card>
                        </div>
                        <div class="wb-part">
                            <el-tabs type="border-card" v-model="active_box">
                                <el-tab-pane v-for="box of box_list" :key="box.label" :label="box.name"
                                             :name="box.label">
                                    <el-collapse v-model="active_tool" @change="open_mod" accordion>
                                        <el-collapse-item v-for="tool in box.tool_list" :key="tool.label"
                                                          :title="tool.name" :name="tool.label">
                                            <div>{{ tool.desc }}</div>
                                        </el-collapse-item>
                                    </el-collapse>
                                </el-tab-pane>
                            </el-tabs>
                        </div>
                    </el-col>
                    <el-col :xs="24" :sm="18">
                        <el-card class="wb-tool">
                            <component :is="active_mod"/>
                        </el-card>
                    </el-col>
                </el-row>
            </div>
        </section>
    </div>
</template>

<script>
export default {
    name: "Tool",
    data() {
        return {
            connected: "Unknown",
            token_res: "Unknown",
            keep_token: false,
            username: this.$store.state.username,
            password: this.$store.state.password,
            active_box: null,
            active_tool: null,
            active_mod: () => import(`@/components/tools/welcome`),
            acl_tools: []
        }
    },
    methods: {
        check_token: function () {
            let that = this;
            let data_host = this.$store.state.host;
            this.$http.get(data_host + `/webpage/tool/acl?user=${this.username}&pass=${this.password}`)
                .then(function (res) {
                    if (res.data.status === 'OK') {
                        that.token_res = "OK"
                        that.$store.commit("setData", {key: "username", val: that.username})
                        that.$store.commit("setData", {key: "password", val: that.password})
                        if (that.keep_token) {
                            that.$cookies.set("username", that.username)
                            that.$cookies.set("password", that.password)
                        }
                        that.acl_tools = res.data.data
                    } else {
                        that.keep_token = false
                        that.token_res = "Error"
                        that.$store.commit("setData", {key: "username", val: ""})
                        that.$store.commit("setData", {key: "password", val: ""})
                    }
                })
                .catch(function (res) {
                    that.token_res = "Error"
                    that.$store.commit("setData", {key: "password", val: ""})
                    console.log(res);
                })
        },
        open_mod: function (label) {
            let box_label = this.active_box;
            let tool_label = this.active_tool;
            let path_prefix = this.$route.path.split("/")[1];
            let tool_path = `/${path_prefix}/${box_label}/${tool_label}`;
            if (label === "") {
                this.active_mod = () => import(`@/components/tools/welcome`)
            } else {
                this.active_mod = () => import(`@/components/tools/${box_label}_${tool_label}`);
            }
            if (this.$route.path !== tool_path) {
                this.$router.replace(tool_path);
            }
        },
        check_path: function (path_now) {
            let path_list = path_now.split("/")
            let box_label = path_list[2];
            let tool_label = path_list[3];
            this.active_box = box_label;
            this.active_tool = tool_label;
            if (this.active_tool === undefined || this.active_tool === "") {
                this.active_mod = () => import(`@/components/tools/welcome`)
            } else {
                this.active_mod = () => import(`@/components/tools/${box_label}_${tool_label}`);
            }
        },
        check_service: function () {
            let that = this;
            let data_host = this.$store.state.host;
            this.$http.get(data_host + `/generate_204`)
                .then(function () {
                    that.connected = "OK"
                })
                .catch(function () {
                    that.connected = "Error"
                })
        },
        read_user_config: function () {
            let username = this.$cookies.get("username")
            let password = this.$cookies.get("password")
            if (username !== null && password !== null) {
                this.keep_token = true
                this.username = username
                this.password = password
                this.$store.commit("setData", {key: "username", val: this.username})
                this.$store.commit("setData", {key: "password", val: this.password})
                this.check_token()
            }
        },
    },
    mounted() {
        if (this.$route.path.split("/").length < 3) {
            let new_path = `${this.$route.path}/${this.box_list[0]["label"]}`;
            this.$router.replace(new_path);
        }
        this.check_path(this.$route.path);
        this.check_service();  // 检查服务器连通性
        this.read_user_config(); // 检查用户存储
    },
    computed: {
        box_list: function () {
            let tool_config = this.$store.state.tool_data
            let box_list = []
            let box_index = {}
            for(let box of tool_config["box_list"]){
                box_index[box["label"]] = box_list.length
                box["tool_list"] = []
                box_list.push(box)
            }
            for(let tool of tool_config["tool_list"]){
                if(tool["mode"] === "basic"){
                    box_list[box_index[tool["box"]]]["tool_list"].push(tool)
                }
                if(tool["mode"] === "acl" && this.acl_tools.indexOf(tool["label"]) !== -1){
                    box_list[box_index[tool["box"]]]["tool_list"].push(tool)
                }
            }
            return box_list
        }
    },
    watch: {
        $route() {
            this.check_path(this.$route.path);
        }
    }
}
</script>

<style lang="scss" scoped>
.wb-title {
    padding: 36px;

    @media screen and (min-width: 768px) {
        background: url("~@/assets/img/cover.jpg") no-repeat;
        background-position-y: 40%;
        /* background 必在 background-size 前 */
        background-size: cover;
    }
}

.wb-content {
    padding: 18px 0;

    .wb-part {
        margin-bottom: 16px;
    }

    .wb-login {
        .login-body {
            .el-input {
                margin-bottom: 8px;
            }

            .el-button {
                width: 100%;
                margin: 6px 0;
            }
        }
    }
}
</style>