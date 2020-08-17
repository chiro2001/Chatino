<template>
	<view>
		<view class="status_bar">
			<!-- 这里是状态栏 -->
		</view>
		<uni-nav-bar fixed left-icon="bars" right-icon="plus" @clickLeft="clickLeft" @clickRight="clickRight" title="消息列表"></uni-nav-bar>
		<uni-popup ref="popup" type="dialog">
			<uni-popup-dialog type="info" mode="input" :value="config.data.rooms.public[0]" title="输入你想加入的房间" :duration="2000"
			 :before-close="true" @close="dialogClose" @confirm="dialogConfirm"></uni-popup-dialog>
		</uni-popup>
		<view>
			<uni-list>
				<uni-list v-for="item in room_list" :key="room_list.indexOf(item)">
					<uni-list-item :ellipsis="1" :title="item.title" :note="utils.limitString(item.text)" clickable @click="onClick(item.title)">
						<template slot="right">
							<view class="item-room-right">
								<text class="item-room-right-text">{{ utils.showTime(item.time) }}</text>
								<uni-badge class="item-room-right-badge" size="small" :text="item.unread" type="error"></uni-badge>
							</view>
						</template>
					</uni-list-item>
				</uni-list>
			</uni-list>
		</view>
	</view>
</template>

<script>
	import uniNavBar from "@/components/uni-nav-bar/uni-nav-bar.vue"
	import uniPopup from '@/components/uni-popup/uni-popup.vue'
	import uniPopupMessage from '@/components/uni-popup/uni-popup-message.vue'
	import uniPopupDialog from '@/components/uni-popup/uni-popup-dialog.vue'
	import config from "@/utils/config.vue"

	export default {
		components: {
			uniNavBar,
			uniPopup,
			uniPopupMessage,
			uniPopupDialog,
			config
		},
		data() {
			return {
				connected: false,
				room_list: [],
				to_join: undefined
			}
		},
		methods: {
			clickLeft: function() {
				// console.log('Visit ./left-page')
				uni.navigateTo({
					url: './left-page',
					animationType: 'slide-in-left',
					animationDuration: 300
				})
				// this.onClick()
			},
			onClick: function(room) {
				// console.log('/pages/room/room/?room=lounge')
				// url最后不能用斜杠
				console.log(uni.navigateTo({
					url: '/pages/room/room?room=' + room
				}))
			},
			clickRight: function() {
				this.$refs.popup.open()
			},
			dialogClose: function(done) {
				done()
			},
			dialogConfirm: function(done, value) {
				// console.log(value)
				this.joinRoom(value)
				done()
			},
			joinRoom: function(room) {
				if (this.room_list.length >= 1) {
					uni.showToast({
						title: "只能添加一个房间",
						icon: 'none'
					})
					return
				}
				if (!this.connected) {
					uni.showToast({
						title: "还未连接",
						icon: 'none'
					})
					return
				}
				let sender = {
					"cmd": "join",
					"channel": room,
					"clientName": "[Chatino客户端](http://chatino.chiro.work/)",
					"clientKey": "X7t4qkI5Lz+cext",
					// "clientName": "[十字街网页版](https://crosst.chat/)",
					// "clientKey": "/bG0bpXTJVKgQ58,"
				}
				if (this.config.data.user.cookie != undefined)
					sender.cookie = this.config.data.user.cookie
				if (this.config.data.user.username != undefined)
					sender.nick = this.config.data.user.username
				if (this.config.data.user.password != undefined)
					sender.password = this.config.data.user.password
				this.to_join = room
				this.ws.methods.send(sender).then((res) => {
					console.log(res)
					if (res[0] != null) return
				})
			},
			parser: function(data) {
				// console.log(data)
				data = JSON.parse(data.data)
				console.log(data)
				if (data.cmd == undefined) return
				else if (data.cmd == 'onlineSet') {
					if (this.to_join != undefined) {
						this.config.data.user.cookie = data.cookie
						this.room_list.push({
							title: this.to_join,
							text: data.nicks[0],
							time: data.time / 1000,
							unread: 0
						})
					}
				} else if (data.cmd == 'info') {
					var message = {
						trip: data.trip,
						content: data.text,
						time: data.time / 1000,
						username: 'system'
					}
					this.insertSystemMessage(message)
				} else if (data.cmd == 'chat') {
					var message = {
						trip: data.trip,
						content: data.text,
						time: data.time / 1000,
						role: data.level,
						username: data.nick
					}
					this.insertMessage(message)
				} else if (data.cmd == 'onlineRemove') {
					var message = {
						username: data.nick,
						time: data.time / 1000,
						content: data.nick + "退出聊天室"
					}
					this.insertSystemMessage(message)
				} else if (data.cmd == "onlineAdd") {
					var message = {
						username: data.nick,
						time: data.time / 1000,
						content: data.nick + "加入聊天室"
					}
					this.insertSystemMessage(message)
				} else if (data.cmd == "warn") {
					var message = {
						username: 'system',
						time: data.time / 1000,
						content: data.text,
					}
					this.insertSystemMessage(message)
				} else {
					var message = {
						content: "未知的命令" + data.cmd + '' + JSON.stringify(data),
						time: data.time / 1000,
						username: 'system',
					}
					this.insertSystemMessage(message)
				}
			},
			insertSystemMessage: function(message) {
				// 修改条件
				message.type = 'system'
				this.config.data.messages.push(message)
				// 触发全局事件
				uni.$emit('insertMessage', message)
				// 修改room-list的文字
				this.room_list[0].text = "系统消息: " + message.content
			},
			insertMessage: function(message) {
				this.config.data.messages.push(message)
				// 触发全局事件
				uni.$emit('insertMessage', message)
				
				this.room_list[0].text = message.username + ": " + message.content
			}
		},
		mounted: function() {
			this.ws.methods.startConnection().then((res) => {
				console.log(res)
				if (res[0] != null) return
				this.connected = true
			})
			uni.onSocketMessage(this.parser)
			// 监听消息
			uni.$on('joinRoom', this.clickRight)
			// if (this.room_list.length == 0) this.clickRight()
			// 保存了登录信息
			if (this.config.data.user.cookie != undefined)
				this.clickRight()
			else if (this.config.data.user.password == undefined || this.config.data.user.username == undefined)
				uni.navigateTo({
					url: '/pages/login',
					animationType: 'zoom-fade-out',
					animationDuration: 300,
				})
		}
	}
</script>

<style>
	.item-room-right {
		display: flex;
		flex-direction: column;
		align-items: flex-end;
	}

	.item-room-right-text {
		font-size: 10px;
		color: #999999;
	}

	.item-room-right-badge {}
</style>
