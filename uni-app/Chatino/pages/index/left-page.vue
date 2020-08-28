<template>
	<view>
		<view class="status_bar"><!-- 这里是状态栏 --></view>
		<uni-nav-bar left-icon="back" right-icon="more" @clickLeft="clickLeft()" title="我"></uni-nav-bar>
		<view class="intro">我和关于我的一切。</view>
		<view v-if="config.data.user.username != undefined">
			用户名: {{ config.data.user.username }}
		</view>
		<button type="default" v-if="config.data.user.username == undefined" @click="login">登录</button>
		<button type="default" v-if="config.data.user.username != undefined" @click="clearCookie">清除登录信息</button>
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
			},
			login: function() {
				uni.navigateTo({
					url: '/pages/login',
					animationType: 'zoom-fade-out',
					animationDuration: 300,
				})
			}
		}
	}
</script>

<style>

</style>
