<template>
	<view class="login">
		<view class="status_bar"></view>
		<view class="login-input-view">
			<view class="introduce">
				欢迎来到十字街，这是一个简洁轻小的聊天室网站。
			</view>
			<view class="warning">
				在使用本网站时，您应当遵守中华人民共和国的相关规定。如果您不在中国大陆范围内居住，您还应当同时遵守当地的法律规定。
			</view>
			<input class="login-input" v-model="username" type="text" placeholder="用户名" />
			<input class="login-input" v-model="password" type="text" placeholder="密码(可选)" password />
			<button type="default" @click="login">登录</button>
			<!-- <uni-link href="./login-help" text="登录帮助"></uni-link> -->
			<navigator url="./login-help" animation-type="zoom-fade-in" animation-duration="300">登录帮助</navigator>
		</view>
	</view>
</template>

<script>
	import config from "@/utils/config.vue"

	export default {
		data() {
			return {
				username: undefined,
				password: undefined
			}
		},
		methods: {
			login: function() {
				if (this.username == undefined) {
					uni.showToast({
						icon: 'none',
						title: '必须输入用户名'
					})
					return
				}
				this.config.data.user.username = this.username
				this.config.data.user.password = this.password
				// 触发全局事件
				uni.$emit('joinRoom')
				uni.navigateBack({
					animationType: 'zoom-fade-in',
					animationDuration: 300
				})
			}
		},
		mounted: function() {
			config.data.user.username = 'TestUser2'
			config.data.user.password = 'TestUser2'
		}
	}
</script>

<style>
	.login-input-view {
		width: 80%;
		margin: auto;
		font-size: 14px;
		/* text-indent: 2em; */
	}

	.login-input-view .introduce {
		color: #555555;
	}

	.login-input-view .warning {
		color: #DD524D;
	}

	.login-input {
		height: 32px;
	}
</style>
