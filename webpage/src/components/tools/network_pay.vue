<template>
    <div class="wb-pay">
        <h2>在线订单支付</h2>
        <el-row :gutter="20" class="wb-alipay">
            <el-col :xs="24" :sm="16">
                <el-form :model="order" :rules="payRule" ref="payForm"
                         label-width="80px" label-position="right"
                         class="wb-alipay-form">
                    <el-form-item label="支付渠道" prop="channel">
                        <el-radio v-model="order.channel" label="alipay" border>支付宝</el-radio>
                        <el-radio v-model="order.channel" label="wechat" border>微信</el-radio>
                    </el-form-item>
                    <el-form-item label="支付应用" prop="app">
                        <el-radio v-model="order.app" label="wolfbolin" border>WolfBolin</el-radio>
                        <el-radio v-model="order.app" label="test" border>测试项目</el-radio>
                    </el-form-item>
                    <el-form-item label="支付名目" prop="subject">
                        <el-input type="text" v-model="order.subject"></el-input>
                    </el-form-item>
                    <el-form-item label="支付金额" prop="volume">
                        <el-input v-model="order.volume">
                            <template slot="append">元(RMB)</template>
                        </el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="precreat_payment">提交</el-button>
                        <el-button @click="query_payment">刷新</el-button>
                    </el-form-item>
                </el-form>
            </el-col>
            <el-col :xs="24" :sm="8" class="wb-alipay-qrcode">
                <img v-if="order.order_status === '未创建'"
                     src="@/assets/img/QR_Code.png" alt="qrcode"/>
                <img v-else-if="order.order_status === '已支付'"
                     src="@/assets/img/done.png" alt="qrcode"/>
                <div v-else>
                    <vue-qr :text="order.order_link"></vue-qr>
                    <el-button type="primary" @click="open_channel_app" plain>打开手机应用支付</el-button>
                </div>
                <p>{{ order.volume }}元(RMB)</p>
                <p>状态：{{ order.order_status }}</p>
                <p>订单号：{{ order.order_str }}</p>
            </el-col>
        </el-row>
    </div>
</template>

<script>
import vueQr from 'vue-qr'

export default {
    components: {vueQr},
    name: "network_payment",
    data() {
        let checkVolume = (rule, value, callback) => {
            value = parseFloat(value)
            if (0 < value && value <= 1000) {
                callback()
            } else {
                callback(new Error("这个数额不合理"));
            }
        };
        return {
            timer: null,
            loading_data: false,
            qrcode_image: "",
            order: {
                app: "wolfbolin",
                volume: 0,
                subject: "",
                channel: "alipay",
                order_str: "Bill-xxxxxxxxx",
                order_link: require("../../assets/img/QR_Code.png"),
                order_status: "未创建",
            },
            payRule: {
                channel: [
                    {required: true, message: "请选择支付渠道", trigger: "blur"},
                ],
                app: [
                    {required: true, message: "请选择支付项目", trigger: "blur"},
                ],
                subject: [
                    {required: true, message: "请输入商品名称", trigger: "blur"},
                    {min: 3, max: 15, message: "3-15个字符哦", trigger: "blur"},
                ],
                volume: [
                    {required: true, message: "请输入商品金额", trigger: "change"},
                    {validator: checkVolume, trigger: "change"}
                ]
            }
        };
    },
    methods: {
        open_channel_app: function () {
            window.open(this.order.order_link)
        },
        precreat_payment: function () {
            this.$refs["payForm"].validate((valid) => {
                if (valid) {
                    console.log("Creat payment order")
                    let that = this;
                    this.loading_data = true
                    let data_host = this.$store.state.host;
                    let http_url = data_host + `/payment/${this.order.channel}`
                    this.$http.post(http_url,
                        {
                            app: this.order.app,
                            subject: this.order.subject,
                            volume: this.order.volume,
                        })
                        .then(function (res) {
                            if (res.data.status === "OK") {
                                let order_info = res.data.data
                                that.order.order_status = "已创建"
                                that.order.order_str = order_info["order_str"]
                                that.order.order_link = order_info["qrcode_link"]
                                that.timer = setInterval(that.query_payment, 2000)
                            }
                            that.loading_data = false
                        })
                        .catch(function (res) {
                            console.log(res)
                            that.loading_data = false
                        })
                }
            })
        },
        query_payment: function () {
            console.log("Query payment order")
            let that = this;
            this.loading_data = true
            let data_host = this.$store.state.host;
            let http_url = data_host + `/payment/${this.order.channel}`
            this.$http.get(http_url, {
                params: {
                    app: this.order.app,
                    order_str: this.order.order_str,
                }
            })
                .then(function (res) {
                    if (res.data.status === "OK") {
                        let order_info = res.data.data
                        console.log(order_info)
                        switch (order_info.order_status) {
                            case "NOT_EXIST":
                                that.order.order_status = "未创建";
                                break;
                            case "CREATED":
                                that.order.order_status = "已创建";
                                break;
                            case "WAITING":
                                that.order.order_status = "待支付";
                                break;
                            case "SUCCESS":
                                that.order.order_status = "已支付";
                                break;
                            case "FINISH":
                                that.order.order_status = "已终止";
                                break;
                            case "CLOSE":
                                that.order.order_status = "已关闭";
                                break;
                        }
                        if (["已支付", "已终止", "已关闭"].indexOf(that.order.order_status) !== -1) {
                            clearInterval(that.timer)
                        }
                    }
                    that.loading_data = false
                })
                .catch(function (res) {
                    console.log(res)
                    that.loading_data = false
                })
        }
    }
}
</script>

<style lang="scss">
.wb-pay {
    .wb-alipay {
        .wb-alipay-form {
            margin-top: 12px;
        }

        .wb-alipay-qrcode {
            text-align: center;
        }
    }
}
</style>