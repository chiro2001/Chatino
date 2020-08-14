<template>
	<view>
		<uni-nav-bar left-icon="back" @clickLeft="onLeftClick" right-icon="more" :title="room"></uni-nav-bar>
		<scroll-view scroll-y="true" >
			<view v-for="i in messages" :key="messages.indexOf(i)">
				<item-message :message="i"></item-message>
			</view>
		</scroll-view>
	</view>
</template>

<script>
	import ItemMessage from "../../components/beans/item-message.vue"
	import uniNavBar from "@/components/uni-nav-bar/uni-nav-bar.vue"
	import config from "@/utils/config.vue"

	export default {
		components: {
			ItemMessage,
			uniNavBar,
			config
		},
		props: {

		},
		data: function() {
			return {
				room: '',
				messages: [],
				// message_test: {
				// 	'room': 'test-room',
				// 	'username': 'test-username',
				// 	'content': "That's what I said!",
				// 	'time': 1597389265.0735579,
				// 	'type': 'text',
				// 	'visibility': 'public',
				// 	'status': 'available',
				// 	'direction': 'public',
				// 	'msg': undefined
				// },
				// system_test: {
				// 	'room': 'test-room',
				// 	'username': 'system',
				// 	'content': "John退出了房间。",
				// 	'time': 1597389265.0735579,
				// 	'type': 'system',
				// 	'visibility': 'public',
				// 	'status': 'available',
				// 	'direction': 'public',
				// 	'msg': 'exit'
				// }
			}
		},
		methods: {
			onLeftClick: function() {
				uni.navigateBack({
					animationType: "pop-out",
					animationDuration: 300
				})
			},
			insertMessage: function(message) {
				this.messages.push(message)
			}
		},
		onLoad: function(option) {
			console.log(option)
			if (option.room == undefined)
				uni.navigateBack({
					animationType: "slide-out-right",
					animationDuration: 300
				})
			else
				this.room = option.room
			// 复制全局信息
			console.log('global messages', config.data.messages)
			for (var i in config.data.messages) {
				this.messages.push(i)
				console.log('push message', i)
			}
			// 监听消息
			uni.$on('insertMessage', this.insertMessage)
		},
		mounted: function() {}
	}
</script>

<style>

</style>
