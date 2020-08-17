<template>
	<view>
		<view class="status_bar"><!-- 这里是状态栏 --></view>
		<uni-nav-bar left-icon="back" right-icon="more" @clickLeft="clickLeft()" title="我"></uni-nav-bar>
		<view class="intro">我和关于我的一切。</view>
		<button type="default" @click="clearCookie">清除登录信息</button>
	</view>
</template>

<script>
	import uniNavBar from "@/components/uni-nav-bar/uni-nav-bar.vue"
	import config from "@/utils/config.vue"
	
	export default {
		components: {
			uniNavBar,
		},
		data() {
			return {
				
			}
		},
		methods: {
			clickLeft: function() {
				// console.log('Visit ./left-page')
				uni.navigateBack({
					animationType: "slide-out-left",
					animationDuration: 300
				})
			},
			clearCookie: function() {
				this.config.data.user.cookie = undefined
				uni.showToast({
					title: '完成'
				})
			}
		}
	}
</script>

<style>

</style>
