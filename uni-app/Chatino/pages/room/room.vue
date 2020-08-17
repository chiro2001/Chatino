<template>
	<view>
		<view class="status_bar"></view>
		<uni-nav-bar fixed left-icon="back" @clickLeft="onLeftClick" right-icon="more" :title="room"></uni-nav-bar>
		<scroll-view id="chat-scroll-view" :scroll-top="toTop" @scroll="onScroll" scroll-y="true" class="chat-window" :style="'height: ' + (style.pageHeight - style.footViewHeight - 44 - 1) + 'px'">
			<view>
				<view v-for="i in messages" :key="messages.indexOf(i)">
					<item-message :message="i" :time="i.show_time" :mode="i.username == config.data.user.username ? 'right' : 'left'"></item-message>
				</view>
			</view>
		</scroll-view>
		<!-- 加上一个分割线 -->
		<view style="height: 1px; background-color: #E5E5E5;"></view>

		<view :style="'height: ' + style.footViewHeight + 'px;'">
			<view class="chat-footer">
				<view>
					<view class="uni-form-item uni-column" :style="'background-color: #E5E5E5; width: ' + (style.pageWidth - 24 * 2 - 8 - 4) + 'px; border-radius: 12px'">
						<input maxlength="-1" v-model="input" :focus="inputFocused" @input="inputEvent" @confirm="inputEvent" @keyboardheightchange="reshapeDom"
						 adjust-position class="uni-input" :style="'height: 24px; padding-left: 12px; padding-right: 12px; '" />
					</view>
				</view>
				<view>
					<view class="chat-paperclip-button" style="height: 24px; width: 24px;">
						<uni-icons type="paperclip" size="24"></uni-icons>
					</view>
				</view>
				<view>
					<view class="chat-more-button" style="height: 24px; width: 24px;">
						<uni-icons type="plus" size="24"></uni-icons>
					</view>
				</view>
			</view>
		</view>


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
				// 聊天页面时时滚动样式
				style: {
					pageHeight: 0,
					pageWidth: 0,
					contentViewHeight: 0,
					footViewHeight: 40,
					mitemHeight: 0
				},
				// 为啥你绑定不上去啊啊啊啊啊啊
				toTop: 0,
				toTopOld: 0,
				inputFocused: false,
				// TODO: 按照是否获得输入焦点变化
				input: '',
				isBottom: true,
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
				message = this.setTimeStatus(message)
				this.messages.push(message)
				if (this.isBottom)
					this.scrollToBottom()
			},
			lastMessage: function() {
				if (this.messages.length == 0) {
					return undefined
				}
				return this.messages[this.messages.length - 1]
			},
			setTimeStatus: function(message) {
				// 查看最后消息
				let last = this.lastMessage()
				// 3分钟内不加上时间
				if (last == undefined)
					message.show_time = true
				if (last != undefined && message.time - last.time <= 3 * 60) {
					message.show_time = false
					// console.log('show_time', message)
				} else message.show_time = true
				return message
			},
			inputEvent: function(event) {
				// console.log(event)
				if (event.type == 'confirm' && event.detail.value.length != 0) {
					var sender = {
						'cmd': 'chat',
						'text': event.detail.value,
					}
					this.send(sender)
					this.input = ''
				}
				// console.log('scroll', this.toTop)
			},
			send: function(sender) {
				uni.sendSocketMessage({
					data: JSON.stringify(sender),
					fail: this.ws.methods.onError,
				})
				// console.log('after send', this.isBottom)
				if (this.isBottom)
					this.scrollToBottom()
			},
			reshapeDom: function() {
				const res = uni.getSystemInfoSync(); //获取手机可使用窗口高度     api为获取系统信息同步接口
				this.style.pageHeight = res.windowHeight;
				this.style.pageWidth = res.windowWidth;
				this.style.contentViewHeight = res.windowHeight - uni.getSystemInfoSync().screenWidth / 750 * (100) - 70; //像素   因为给出的是像素高度 然后我们用的是upx  所以换算一下 
				this.scrollToBottom(); //创建后调用回到底部方法
			},
			// scrollToBottom: function() {
			// 	// this.scroll = this.style.pageHeight
			// 	// 使用jQuery的老方法
			// 	var that = this.$("#chat-scroll-view")
			// 	that.scrollTop(this.style.pageHeight)
			// }
			scrollToBottom: function() {
				// 这个地方。。。受不了了让我偷下懒
				let maxx = 10000000000
				this.toTop = this.toTopOld
				this.$nextTick(function() {
					this.toTop = maxx
				});
			},
			onScroll: function(event) {
				// console.log('onScroll', event.detail, this.$('#chat-scroll-view').scrollTop())
				// console.log('onScroll', this.toTopOld)
				let data = event.detail
				this.toTopOld = data.scrollTop

				if (data.scrollHeight - data.scrollTop <= this.style.pageHeight - this.style.footViewHeight - 44 - 1 + 2)
					this.isBottom = true
				else this.isBottom = false
			}
		},
		onLoad: function(option) {
			// console.log(option)
			if (option.room == undefined)
				uni.navigateBack({
					animationType: "slide-out-right",
					animationDuration: 300
				})
			else
				this.room = option.room
			// 复制全局信息
			// console.log('global messages', config.data.messages)
			for (var i in config.data.messages) {
				var message = config.data.messages[i]
				message = this.setTimeStatus(message)
				this.messages.push(message)
				// console.log('push message', message)
			}
			// 监听消息
			uni.$on('insertMessage', this.insertMessage)

			this.reshapeDom()
		},
		mounted: function() {}
	}
</script>

<style>
	.chat-footer {
		padding-top: 8px;
		/* padding-bottom: 8px; */
		padding-left: 8px;
		display: flex;
		flex-direction: row;
		justify-content: flex-start;
	}
</style>
