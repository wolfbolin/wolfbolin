<template>
    <div class="wb-title">
        <div class="content inner">
            <h1>{{title}}</h1>
            <p>{{desc}}</p>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Title",
        props: {
            path: String
        },
        data() {
            return {
                title: "",
                desc: "",
            }
        },
        methods: {
            set_description: function () {
                let page_data = this.$store.state.title_data;
                for (let item of page_data) {
                    if (item.path === this.path) {
                        this.title = item.title;
                        this.desc = item.desc;
                        break;
                    }
                }
            }
        },
        mounted() {
            this.set_description()
        }
    }
</script>

<style lang="scss" scoped>

    .wb-title {
        padding-top: 60px;

        @media screen and (min-width: 768px) {
            background: url("../../public/static/title.jpg") no-repeat;
            /* background 必在 background-size 前 */
            background-size: cover;
        }

        .content {
            padding: 8px;
        }
    }
</style>
