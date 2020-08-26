<template>
    <div class="wb-ip">
        <h2>IP信息</h2>
        <p>IP: {{ip}}</p>
        <el-button size="small" type="primary" @click="check_ip_info">刷新信息</el-button>
    </div>
</template>

<script>
    export default {
        name: "network_ip",
        data() {
            return {
                ip: "0.0.0.0"
            }
        },
        methods: {
            check_ip_info: function () {
                let that = this;
                let data_host = this.$store.state.host;
                let http_url = data_host + `/network/info/ip`
                this.$http.get(http_url)
                    .then(function (res) {
                        if (res.data.status === 'OK') {
                            that.$message('数据已更新');
                            that.ip = res.data.data;
                        }
                    })
                    .catch(function (res) {
                        console.log(res);
                    })
            }
        },
        mounted() {
            this.check_ip_info();
        }
    }
</script>

<style scoped>

</style>