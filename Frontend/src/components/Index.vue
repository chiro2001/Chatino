<!--
 * @FileDescription: 主页组件。
 * @Copyright: (Our Company Name), 2020
 * @Author: Chiro
 * @Email: Chiro2001@163.com
 * @Date: 2020/07/14
 * @LastEditors: Chiro
 * @LastEditTime: 2020/07/19
 -->
 <template>
  <div class="app-index">
    <page-header title="派小侠后台管理主页" :initedMenus="menus" />
    <br />
    <mu-container>
      <div>
        <mu-alert color="info">
          <mu-icon left value="info"></mu-icon>这是管理公告
        </mu-alert>
      </div>
      <br />
      <div>
        <div style="display: flex; flex-wrap: wrap">
          <!-- 用户数据概览 -->
          <div>
            <mu-card class="paike-data-card">
              <mu-card-title title="用户"></mu-card-title>
              <mu-card-text>
                用户总数: 7389545348
                <br />今日活跃: 104325432
              </mu-card-text>
              <mu-card-actions>
                <mu-button flat>用户管理</mu-button>
              </mu-card-actions>
            </mu-card>
          </div>
          <!-- 外卖订单数据概览 -->
          <div>
            <mu-card class="paike-data-card">
              <mu-card-title title="外卖订单"></mu-card-title>
              <mu-card-text>
                已开启的订单: 73895
                <br />正在进行的订单: 1043
              </mu-card-text>
              <mu-card-actions>
                <mu-button flat>订单管理</mu-button>
              </mu-card-actions>
            </mu-card>
          </div>
          <!-- 财务数据概览 -->
          <div>
            <mu-card class="paike-data-card">
              <mu-card-title title="财务"></mu-card-title>
              <mu-card-text>
                本月总收入: 4879321
                <br />本月总支出: 43
              </mu-card-text>
              <mu-card-actions>
                <mu-button flat>财务管理</mu-button>
              </mu-card-actions>
            </mu-card>
          </div>
        </div>
      </div>
    </mu-container>
  </div>
</template>

<script>
import "muse-ui/dist/muse-ui.css";
import PageHeader from "./pageComponents/PageHeader";

export default {
  name: "Index",
  props: {},
  components: {
    PageHeader
  },
  data: function() {
    return {
      menus: [
        {
          text: "菜单1",
          method: function() {
            console.log("Nothing but a menu.");
          }
        }
      ]
    };
  },
  methods: {
    // 切换到这个标签的时候执行
    init: function() {}
  }
  // data() {
  //   return {
  //     open: false,
  //   };
  // }
};
</script>

<style lang="less">
.paike-data-card {
  margin-left: 1px;
  margin-top: 3px;
  // height: 220px;
}
</style>