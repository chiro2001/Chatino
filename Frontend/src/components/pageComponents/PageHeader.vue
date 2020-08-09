<!--
 * @FileDescription: AppBar的进一步封装组件。
 * @Copyright: (Our Company Name), 2020
 * @Author: Chiro
 * @Email: Chiro2001@163.com
 * @Date: 2020/07/14
 * @LastEditors: Chiro
 * @LastEditTime: 2020/07/16
 -->
<template>
  <!-- 把AppBar封装成单独组件 -->
  <mu-appbar style="width: 100%;" color="primary">
    <mu-button icon slot="left" @click="toggleDrawer()">
      <mu-icon value="menu"></mu-icon>
    </mu-button>
    {{ title }}
    <template v-if="has_menu">
      <mu-menu slot="right">
        <mu-button flat>MENU</mu-button>
        <mu-list slot="content">
          <mu-list-item button>
            <mu-list-item-content v-for="menu in menus" :key="menus.indexOf(menu)">
              <mu-list-item-title @click="menu.method(menu.args)">{{ menu.text }}</mu-list-item-title>
            </mu-list-item-content>
          </mu-list-item>
        </mu-list>
      </mu-menu>
    </template>
  </mu-appbar>
</template>

<script>
// import PageDrawer from "./PageDrawer.vue"

export default {
  props: {
    title: String,
    initedMenus: Array
  },
  data: function() {
    return {
      menus: this.initedMenus
    };
  },
  computed: {
    has_menu: function() {
      if (this.menus.length == 0) return false;
      else return true;
    }
  },
  methods: {
    toggleDrawer: function() {
      this.$parent.$parent.openDrawer();
    }
  }
};
</script>