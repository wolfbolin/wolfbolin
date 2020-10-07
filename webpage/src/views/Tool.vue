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
                                    <span>身份验证</span>
                                </div>
                                <div class="login-body">
                                    <el-input type="password" placeholder="请输入秘钥" v-model="user_token"
                                              @keyup.enter.native="check_token" autofocus clearable>
                                        <el-button slot="append" type="primary" @click="check_token" plain>验证
                                        </el-button>
                                    </el-input>
                                </div>
                                <div class="login-alert">
                                    <el-alert title="Token验证成功" type="success"
                                              v-if="token_res === 'success'"></el-alert>
                                    <el-alert title="Token验证失败" type="error"
                                              v-if="token_res === 'error'"></el-alert>
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
            token_res: "none",
            user_token: this.$store.state.user_token,
            active_box: null,
            active_tool: null,
            active_mod: () => import(`@/components/tools/welcome`),
            box_list: this.$store.state.tool_data
        }
    },
    methods: {
        check_token: function () {
            let that = this;
            let data_host = this.$store.state.host;
            this.$http.get(data_host + `/webpage/check/token?token=${this.user_token}`)
                .then(function (res) {
                    if (res.data.data === 'Success') {
                        that.token_res = "success"
                        that.$store.commit("setData", {key: "user_token", val: that.user_token})
                    } else {
                        that.token_res = "error"
                        that.$store.commit("setData", {key: "user_token", val: ""})
                    }
                })
                .catch(function (res) {
                    that.token_res = "error"
                    that.$store.commit("setData", {key: "user_token", val: ""})
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
        }
    },
    mounted() {
        if (this.$route.path.split("/").length < 3) {
            let new_path = `${this.$route.path}/${this.box_list[0]["label"]}`;
            this.$router.replace(new_path);
        }
        this.check_path(this.$route.path);
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
        .login-alert {
            margin-top: 16px;
        }
    }
}
</style>