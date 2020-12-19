<template>
    <div class="wb-album">
        <section class="wb-title">
            <div class="inner">
                <p>WolfBolin</p>
                <h1>浏览相册</h1>
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
                        <div class="wb-select">
                            <el-menu @select="selectAlbum" :default-active="active_album">
                                <el-menu-item v-for="item in album_list" :index="item.name" :key="item.name">
                                    <span slot="title">{{ item.name }}</span>
                                </el-menu-item>
                            </el-menu>
                        </div>
                    </el-col>
                    <el-col :xs="24" :sm="18">
                        <el-card class="wb-album">
                            <div slot="header" class="clearfix">
                                <h2>影像展示</h2>
                            </div>
                            <el-carousel arrow="hover" ref="gallery" :height="galleryHeight">
                                <el-carousel-item v-for="photo in photo_list" :key="photo.title">
                                    <img :src="photo.thumbnail" :alt="photo.title" style="width: 100%"/>
                                </el-carousel-item>
                            </el-carousel>
                            <div class="wb-album-title">
                                <h3>影像展示</h3>
                            </div>
                            <div class="wb-album-list">
                                <el-image v-for="photo in photo_list" :key="photo.title"
                                          :src="photo.thumbnail" :preview-src-list="photo.preview" lazy>
                                </el-image>
                            </div>
                        </el-card>
                    </el-col>
                </el-row>
            </div>
        </section>
    </div>
</template>

<script>
export default {
    name: "Album",
    data() {
        return {
            token_res: "none",
            user_token: this.$store.state.user_token,
            album_list: this.$store.state.album_list,
            active_album: null,
            galleryHeight: "0px",
            photo_list: [
                {
                    "thumbnail": "/statics/img/default1.jpg",
                    "preview": ["/statics/img/default1.jpg"],
                    "title": "default1"
                },
                {
                    "thumbnail": "/statics/img/default2.jpg",
                    "preview": ["/statics/img/default2.jpg"],
                    "title": "default2"
                },
                {
                    "thumbnail": "/statics/img/default3.jpg",
                    "preview": ["/statics/img/default3.jpg"],
                    "title": "default3"
                },
                {
                    "thumbnail": "/statics/img/default4.jpg",
                    "preview": ["/statics/img/default4.jpg"],
                    "title": "default4"
                }
            ]
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
        selectAlbum: function (active_album) {
            this.active_album = active_album;
            let path_prefix = this.$route.path.split("/")[1];
            let tool_path = `/${path_prefix}/${active_album}`;
            if (this.$route.path !== tool_path) {
                this.$router.replace(tool_path);
            }
        },
        set_gallery_height: function () {
            let imageWidth = this.$refs.gallery.$el.clientWidth;
            let imageHeight = 0.5625 * imageWidth;
            this.galleryHeight = `${imageHeight}px`;
        },
    },
    mounted() {
        this.set_gallery_height();

        let active_album = this.$route.path.split("/")[2];
        if (active_album !== undefined) {
            this.active_album = active_album;
            this.selectAlbum(active_album);
        }
    },
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

    .wb-album {
        .wb-album-title {
            border-left: #91BEF0 6px solid;
        }

        .wb-album-list {
            .el-image + .el-image {
                margin-top: 16px;
            }
        }
    }
}
</style>