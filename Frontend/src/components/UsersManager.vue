<!--
 * @FileDescription: 用户数据管理组件。
 * @Copyright: (Our Company Name), 2020
 * @Author: Chiro
 * @Email: Chiro2001@163.com
 * @Date: 2020/07/19
 * @LastEditors: Chiro
 * @LastEditTime: 2020/07/19
 -->
 <template>
  <div class="app-index">
    <page-header title="用户数据管理" :initedMenus="menus" />
    <mu-flex class="demo-linear-progress" v-if="loading == true">
      <mu-linear-progress color="secondary"></mu-linear-progress>
    </mu-flex>
    <br />
    <mu-container>
      <h2>用户数据统计</h2>
      <mu-divider></mu-divider>
      <br />
      <h3>总体信息</h3>
      <div style="display: flex; flex-wrap: wrap">
        <mu-button color="primary" class="paike-button">男女比例</mu-button>
        <mu-button color="primary" class="paike-button">活跃用户查询</mu-button>
        <mu-button color="primary" class="paike-button">用户地域分布</mu-button>
      </div>
    </mu-container>
  </div>
</template>

<script>
import "muse-ui/dist/muse-ui.css";
import PageHeader from "./pageComponents/PageHeader";

export default {
  name: "app-index",
  props: {},
  components: {
    PageHeader
  },
  data: function() {
    return {
      menus: [
        {
          text: "刷新",
          method: this.refreshData
        }
      ],
      loading: true
    };
  },
  methods: {
    // 切换到这个标签页的时候执行
    init: function() {
      // this.refreshData();
      this.$toast.message('Inited.');
    },
    refreshData: function() {
      // this.sleep(1);
      this.loading = false
    },
    sleep: function(time) {
      var startTime = new Date().getTime() + parseInt(time, 10);
      while (new Date().getTime() < startTime) {
        console.log("");
      }
    }
  }
};
</script>

<style lang="less">
.paike-data-card {
  margin-left: 1px;
  margin-top: 3px;
  // height: 220px;
}
.paike-button {
  margin-right: 10px;
}
</style>