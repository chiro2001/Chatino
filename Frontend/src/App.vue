<!--
 * @FileDescription: Vue主模块。
 * @Copyright: (Our Company Name), 2020
 * @Author: Chiro
 * @Email: Chiro2001@163.com
 * @Date: 2020/07/14
 * @LastEditors: Chiro
 * @LastEditTime: 2020/07/16
 -->
<template>
  <div id="app">
    <!-- 注意使用ref，引入为drawer -->
    <page-drawer ref="drawer" :initOpen="false" :items="drawerItems" />
    <index ref="index" v-if="tab == 'index'"></index>
    <users-manager ref="users_manager" v-if="tab == 'users_manager'"></users-manager>
    <br />
    <!-- <p @click="openDrawer">CLICK</p> -->
  </div>
</template>


<script>
// import HelloWorld from './components/HelloWorld.vue'
import Index from "./components/Index.vue";
import PageDrawer from "./components/pageComponents/PageDrawer.vue";
import UsersManager from "./components/UsersManager.vue";

export default {
  name: "App",
  components: {
    Index,
    UsersManager,
    PageDrawer
  },
  // props: {
  // open: Boolean
  // }
  data: function() {
    return {
      tab: "index",
      tabsTable: {
        index: this.$refs.index,
        users_manager: this.$refs.users_manager
      },
      // 传递到drawer的信息
      drawerItems: [
        {
          icon: "data_usage",
          title: "数据展示",
          items: [
            {
              text: "数据概览",
              method: this.switchTab,
              args: "index"
            }
          ]
        },
        {
          icon: "perm_data_setting",
          title: "数据管理",
          items: [
            {
              text: "用户管理",
              method: this.switchTab,
              args: "users_manager"
            },
            {
              text: "商家管理",
              method: this.showMessageToast,
              args: "未完成!"
            },
            {
              text: "订单管理",
              method: this.showMessageToast,
              args: "未完成!"
            },
            {
              text: "校友圈管理",
              method: this.showMessageToast,
              args: "未完成!"
            },
            {
              text: "轮播图管理",
              method: this.showMessageToast,
              args: "未完成!"
            }
          ]
        }
      ]
    };
  },
  methods: {
    openDrawer: function() {
      this.$refs.drawer.open();
    },
    closeDrawer: function() {
      this.$refs.drawer.close();
    },
    showMessageToast: function(text) {
      this.$toast.message(text);
    },
    switchTab: function(target) {
      this.tab = target;
      this.$refs.drawer.close();
      // 执行init函数
      // this.tabsTable[target].init();
      // this.$refs.index.init();
      this.showMessageToast(this.tabsTable['index']);
    }
  }
};
</script>

<style>
/* #app {

} */
</style>
