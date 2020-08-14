<template>
	<view>
		<uni-nav-bar left-icon="bars" right-icon="plus" @clickLeft="clickLeft" @clickRight="clickRight" title="消息列表"></uni-nav-bar>
		<uni-popup ref="popup" type="dialog">
			<uni-popup-dialog type="info" mode="input" :value="config.data.rooms.public[0]" title="输入你想加入的房间" :duration="2000"
			 :before-close="true" @close="dialogClose" @confirm="dialogConfirm"></uni-popup-dialog>
		</uni-popup>
		<view>
			<uni-list>
				<uni-list v-for="item in room_list" :key="room_list.indexOf(item)">
					<uni-list-item :ellipsis="1" :title="item.title" :note="item.text" clickable @click="onClick(item.title)">
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
				this.to_join = room
				this.ws.methods.send({
					"cmd": "join",
					"channel": room,
					"nick": "TestUser",
					"clientName": "[十字街网页版](https://crosst.chat/)",
					"clientKey": "/bG0bpXTJVKgQ58"
				}).then((res) => {
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
					if (this.to_join != undefined)
						this.room_list.push({
							title: this.to_join,
							text: data.nicks[0],
							time: data.time / 1000,
							unread: 0
						})
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
				}
			},
			insertSystemMessage: function(message) {
				this.config.data.messages.push(message)
				// 触发全局事件
				uni.$emit('insertMessage', message)
			},
			insertMessage: function(message) {
				this.config.data.messages.push(message)
				// 触发全局事件
				uni.$emit('insertMessage', message)
			}
		},
		mounted: function() {
			this.ws.methods.startConnection().then((res) => {
				console.log(res)
				if (res[0] != null) return
				this.connected = true
			})
			uni.onSocketMessage(this.parser)
			if (this.room_list.length == 0) this.clickRight()
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
