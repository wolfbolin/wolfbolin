<template>
<div class="wb-clash">
    <h2>IP信息</h2>
    <el-form :model="bin" label-width="120px">
        <el-form-item label="Clash配置">
            <el-input v-model="bin.data" :autosize="{ minRows: 6, maxRows: 10 }"
                      type="textarea" placeholder="Please input"/>
        </el-form-item>
        <el-form-item label="可选部分">
            <el-checkbox-group v-model="bin.part">
                <el-checkbox label="显示规则" name="type"/>
                <el-checkbox label="显示节点" name="type"/>
            </el-checkbox-group>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" @click="render">渲染图像</el-button>
        </el-form-item>
    </el-form>

    <div class="chart">
        <div class="sankey" id="sankey" ref="sankey"></div>
    </div>
</div>
</template>

<script>
const yaml = require('js-yaml');
import * as echarts from 'echarts/core';
import {TitleComponent, TooltipComponent} from 'echarts/components';
import {SankeyChart} from 'echarts/charts';

import {CanvasRenderer} from 'echarts/renderers';

echarts.use([TitleComponent, TooltipComponent, SankeyChart, CanvasRenderer]);

export default {
    name: "util_clash",
    data() {
        return {
            bin: {
                data: "",
                part: []
            },
            panel: null,
            option: {},
            nodes: [],
            links: []
        }
    },
    methods: {
        render: function () {
            this.parserYaml()
            this.showChart()
        },
        parserYaml: function () {
            console.log("Parse yaml")
            let showRuleFlag = false
            let showNodeFlag = false

            let userCheck = new Set(Object.values(this.bin.part))
            if (userCheck.has("显示规则")) {
                showRuleFlag = true
            }
            if (userCheck.has("显示节点")) {
                showNodeFlag = true
            }

            //处理配置文件
            let linkDict = {}
            let nodeList = new Set()
            let config = yaml.load(this.bin.data)

            // 处理策略中的关系
            config["proxy-groups"].forEach(item => {
                let node_name = item["name"]
                nodeList.add(node_name)
            })
            config["proxy-groups"].forEach(item => {
                let node_name = item["name"]
                linkDict[node_name] ??= {}
                item["proxies"].forEach(target => {
                    if (nodeList.has(target)) {
                        nodeList.add(target)
                    }
                    linkDict[node_name][target] ??= 0
                    linkDict[node_name][target] += 1
                })
            })

            // 处理规则中的关系
            if (showRuleFlag) {
                config["rules"].forEach(item => {
                    let rule = item.split(",")
                    let source = rule[1]
                    let target = rule[2]

                    nodeList.add(source)
                    nodeList.add(target)
                    linkDict[source] ??= {}
                    linkDict[source][target] ??= 0
                    linkDict[source][target] += 1
                })
            }

            // 处理节点中的关系
            if (showNodeFlag) {
                config["proxies"].forEach(item => {
                    let node_name = item["name"]
                    nodeList.add(node_name)
                })
            }

            // 转换数据类型
            this.nodes = []
            this.links = []
            nodeList.forEach(item => {
                this.nodes.push({"name": item, "itemStyle": {"color": this.lightColorGen()}})
            })
            Object.entries(linkDict).forEach(([source, targets]) => {
                Object.entries(targets).forEach(([target, value]) => {
                    if (nodeList.has(target)) {
                        this.links.push({
                            source: source,
                            target: target,
                            value: value
                        })
                    }
                })
            })
        },
        initChart: function () {
            let chartDom = this.$refs.sankey
            chartDom.style.height = chartDom.clientWidth * 0.618 + "px"
            this.panel = echarts.init(chartDom);
        },
        showChart: function () {
            console.log("Load visualization")
            this.option = this.$store.state.visual_clash
            this.option.series[0].data = this.nodes
            this.option.series[0].links = this.links
            this.panel.setOption(this.option)
        },
        lightColorGen: function () {
            const {random} = Math
            const mH = 360  // 色相环角度范围
            const mS = 10  // 饱和度范围
            const mL = 10 // 亮度范围
            const H = ~~(mH * random())
            const S = ~~(mS * random()) + 95
            const L = ~~(mL * random()) + 45
            return `HSL(${H}, ${S}%, ${L}%)`;
        }
    },
    mounted() {
        this.initChart()
    }
}
</script>

<style scoped>

</style>