<template>
    <div class="wb-title">
        <div class="inner content">
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
        padding-top: 72px;
        background: url("../../public/static/background.jpg") no-repeat 10% 10%;
        /* background 必在 background-size 前 */
        background-size: cover;

        .content {
            padding: 36px;
            h1 {
                font-size: 2.4em;
            }
            p {
                font-size: 1.38em;
            }
        }

        @media screen and (max-width: 768px) {
            .content {
                padding: 12px 12px;
                h1 {
                    font-size: 2.4em;
                }
                p {
                    font-size: 1.38em;
                }
            }
        }
    }
</style>
