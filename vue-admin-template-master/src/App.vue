<template>
    <div id="app" >
        <router-view v-if="isRouterAlive"></router-view>
        <div class="global-loading" v-show="isShowLoading">
            <Spin size="large"></Spin>
        </div>
    </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
    name: 'App',
    methods: {
        reload() {
            this.isRouterAlive = false
            // eslint-disable-next-line
            this.$nextTick(function () {
                this.isRouterAlive = true
            })
        },
    },
    provide() {
        return {
            reload: this.reload,
        }
    },
    data() {
        return {
            isRouterAlive: true,
            keepAliveData: ['manage'],
        }
    },
    computed: {
        ...mapState([
            'isShowLoading',
        ]),
    },
}
</script>

<style>
body {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}
li, ul, p, div, body, html, table {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
html, body {
    height: 100%;
    overflow: hidden;
}
li {
    list-style: none;
}
#app {
    height: 100%;
}
/* loading */
.global-loading {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(255,255,255,.5);
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>
