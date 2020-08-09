<!--
 * @FileDescription: 侧边栏的一个封装。
 * @Copyright: (Our Company Name), 2020
 * @Author: Chiro
 * @Email: Chiro2001@163.com
 * @Date: 2020/07/14
 * @LastEditors: Chiro
 * @LastEditTime: 2020/07/16
 -->
<template>
  <!-- 能不能把这个b注册到全局? -->
  <mu-drawer :open.sync="isopen" :docked="false">
    <!-- <div v-for="item in items" :key="items.indexOf(item)">
      <div v-for="i in item.items" :key="item.items.indexOf(i)">
        <mu-button @click="i.method(i.args)">{{ i.text }}</mu-button>
      </div>
    </div>-->
    <mu-list toggle-nested v-for="item in items" :key="items.indexOf(item)">
      <mu-list-item button nested>
        <mu-list-item-action>
          <mu-icon :value="item.icon"></mu-icon>
        </mu-list-item-action>
        <mu-list-item-title>{{ item.title }}</mu-list-item-title>
        <mu-list-item-action :ripple="false">
          <mu-icon class="toggle-icon" size="24" value="keyboard_arrow_down"></mu-icon>
        </mu-list-item-action>
        <!-- 这里不能加ripple，会影响到click的触发...这算是BUG吗 -->
        <mu-list-item :ripple="false" button slot="nested" v-for="i in item.items" :key="item.items.indexOf(i)">
          <mu-list-item-title :ripple="false" @click="i.method(i.args)">{{ i.text }}</mu-list-item-title>
          <!-- <div @click="i.method(i.args)" style='width: 100%; height: 100%'>{{ i.text }}</div> -->
        </mu-list-item>
      </mu-list-item>
    </mu-list>
  </mu-drawer>
</template>

<script>
export default {
  // name: 'page-drawer',
  props: {
    initOpen: Boolean,
    items: Array
  },
  data: function() {
    return {
      isopen: false
      // isDataShowListOpen: true,
      // isDataManageListOpen: true
    };
  },
  methods: {
    open: function() {
      this.isopen = true;
    },
    close: function() {
      this.isopen = false;
    },
    toggle: function() {
      this.isopen = !this.isopen;
    }
  },
  install: function(Vue, options) {
    console.log(options);
    Vue.prototype.PageDrawer = this;
  }
};
</script>