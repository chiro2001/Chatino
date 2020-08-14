<template>
</template>

<script>
	import config from "@/utils/config"
	export default {
		data: {
			ws: undefined,
			task: undefined,
			// is_open: false,
			// 暂时什么都不做，可以替换这个函数
			// on_message: function(data) {}
		},
		methods: {
			startConnection: function() {
				this.task = uni.connectSocket({
					url: config.data.web.url,
				})
				// 是一个Promise
				uni.onSocketOpen(this.onOpen)
				uni.onSocketError(this.onError)
				// uni.onSocketMessage(this.onMessage)
				return this.task
			},
			onOpen: function(res) {
				uni.showToast({
					title: '连接成功',
				})
				// this.is_open = true;
			},
			onError: function(res) {
				uni.showToast({
					title: '网络错误',
					icon: 'none',
				})
			},
			onClose: function() {
				uni.showToast({
					title: "连接已关闭",
					icon: 'none'
				})
			},
			close: function(code, reason) {
				uni.closeSocket({
					code: code,
					reason: reason,
					complete: () => {}
				})
			},
			send: function(data) {
				return uni.sendSocketMessage({
					data: JSON.stringify(data),
				})
			},
			// onMessage: function(data) {
			// 	this.on_message(data)
			// }
		}
	}
</script>

<style>
</style>
