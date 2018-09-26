<template>
    <div id="project-page">
        <section class="wb-white-section">
            <div class="inner">
                <el-card :body-style="{ padding: '0px' }">
                    <img src="../../static/img/WordArt.png" class="image">
                    <div style="padding: 14px;">
                        <el-table
                            :data="tableData"
                            style="width: 100%"
                            border>
                            <el-table-column type="expand" label="#">
                                <template slot-scope="props">
                                    <el-form label-position="left" inline class="expand">
                                        <el-form-item label="项目名称">
                                            <span>{{ props.row.name }}</span>
                                        </el-form-item>
                                        <el-form-item label="项目地址">
                                            <a :href="props.row.url" target="_blank">
                                                {{ props.row.address }}
                                            </a>
                                        </el-form-item>
                                        <el-form-item label="起始时间">
                                            <span>{{ props.row.start }}</span>
                                        </el-form-item>
                                        <el-form-item label="结束时间">
                                            <span>{{ props.row.stop }}</span>
                                        </el-form-item>
                                        <el-form-item label="项目描述">
                                            <span>{{ props.row.describe }}</span>
                                        </el-form-item>
                                    </el-form>
                                </template>
                            </el-table-column>
                            <el-table-column
                                label="项目名称"
                                prop="name"
                                align="center">
                            </el-table-column>
                            <el-table-column
                                label="项目描述"
                                prop="describe"
                                align="center">
                            </el-table-column>
                            <el-table-column
                                label="进度"
                                align="center">
                                <template slot-scope="scope">
                                    <el-progress :percentage="scope.row.progress" status="exception"></el-progress>
                                </template>
                            </el-table-column>
                        </el-table>
                    </div>
                </el-card>
            </div>
        </section>
    </div>
</template>

<script>
    export default {
        name: "Project",
        data() {
            return {
                tableData: [{
                    name: '项目名称',
                    start: '1970-1-1',
                    stop: '1970-1-1',
                    url: 'https://wolfbolin.com',
                    address: 'https://wolfbolin.com',
                    progress: 40,
                    describe: '项目描述'
                }]
            }
        }
    }
</script>

<style scoped lang="scss">
    #project-page {
        .inner {
            max-width: 1140px;
            margin: 0 auto;
            padding: 60+72px 40px 72px 40px;
            .image{
                width: 100%;
            }
            .expand {
                font-size: 0;
                .el-form-item {
                    margin-right: 0;
                    margin-bottom: 0;
                    width: 50%;
                }
            }
        }
        .wb-white-section {
            background-color: rgba(255, 255, 255, 0.7);
            .title {
                text-align: center;
                h3 {
                    color: #404040;
                    font-weight: 100;
                    font-size: 28px;
                }
                h1 {
                    color: #66b1ff;
                    font-weight: 400;
                    font-size: 38px;
                }
            }
        }
    }
</style>
