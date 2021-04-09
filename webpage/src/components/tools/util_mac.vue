<template>
    <div class="wb-mac">
        <h2>MAC地址格式转换</h2>
        <p>请输入任意格式MAC地址</p>
        <el-input placeholder="请输入MAC地址" v-model="mac_input" @input="user_typing">
            <el-button slot="append" @click="format_mac">转换</el-button>
        </el-input>
        <p>转换结果</p>
        <el-row :gutter="20">
            <el-col :xs="24" :sm="12">
                <el-input placeholder="请输入MAC地址" v-model="mac_output[0]" readonly>
                    <el-button slot="append" :data-clipboard-text="mac_output[0]">复制</el-button>
                </el-input>
            </el-col>
            <el-col :xs="24" :sm="12">
                <el-input placeholder="请输入MAC地址" v-model="mac_output[1]" readonly>
                    <el-button slot="append" :data-clipboard-text="mac_output[1]">复制</el-button>
                </el-input>
            </el-col>
            <el-col :xs="24" :sm="12">
                <el-input placeholder="请输入MAC地址" v-model="mac_output[2]" readonly>
                    <el-button slot="append" :data-clipboard-text="mac_output[2]">复制</el-button>
                </el-input>
            </el-col>
            <el-col :xs="24" :sm="12">
                <el-input placeholder="请输入MAC地址" v-model="mac_output[3]" readonly>
                    <el-button slot="append" :data-clipboard-text="mac_output[3]">复制</el-button>
                </el-input>
            </el-col>
        </el-row>
    </div>
</template>

<script>
export default {
    name: "util_mac",
    data() {
        return {
            mac_input: "",
            mac_output: ["","","",""]
        }
    },
    methods: {
        user_typing: function (text) {
            if (text.length === 17) {
                console.log("MAC Input:", text)
                this.format_mac()
            }
        },
        format_mac: function () {
            this.mac_input = this.mac_input.trim()
            console.log(this.mac_input)
            let regex_res = this.mac_input.match(/([0-9a-fA-F]{1,2}([.:-])){5}([0-9a-fA-F]{1,2})/)
            if(regex_res === null){
                this.$message.error("这貌似不是一个有效的MAC")
                return
            }
            console.log(regex_res)

            let mac_string = regex_res[0]
            let split_char = regex_res[2]
            let bit_list = mac_string.split(split_char)

            this.mac_output[0] = bit_list.map(x => x.toLowerCase()).join(".")
            this.mac_output[1] = bit_list.map(x => x.toUpperCase()).join(".")
            this.mac_output[2] = bit_list.map(x => x.toLowerCase()).join("-")
            this.mac_output[3] = bit_list.map(x => x.toUpperCase()).join("-")
        }
    }
}
</script>

<style scoped>
.el-col {
    margin-bottom: 16px;
}
</style>