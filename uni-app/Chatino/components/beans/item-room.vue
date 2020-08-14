<template>
	<view>
		<uni-list>
		    <uni-list :border="true">
		        <!-- 显示圆形头像 -->
		        <uni-list-chat :avatar-circle="true" title="uni-app" avatar="https://img-cdn-qiniu.dcloud.net.cn/new-page/uni.png" note="您收到一条新的消息" time="2020-02-02 20:20" />
		        <!-- 右侧带角标 -->
		        <uni-list-chat title="uni-app" avatar="https://img-cdn-qiniu.dcloud.net.cn/new-page/uni.png" note="您收到一条新的消息" time="2020-02-02 20:20" badge-text="12"/>
		    </uni-list>
		</uni-list>
	</view>
</template>

<script>
	import divider from "../list/divider.vue"

	export default {
		name: "item-room",
		components: {
			divider,
		},
		props: {
			divider: {
				type: Boolean,
				default: true
			}
		},
		data: function() {
			return {

			};
		},
	}
</script>

<style>

</style>
