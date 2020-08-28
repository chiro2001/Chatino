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
								<uni-badge class="item-room-right-badge" size="small" :text="item.unread == 0 ? undefined : '' + item.unread"
								 type="error"></uni-badge>
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
	// import InDB from 'indb'

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
				// 取消未读标志
				// TODO: 真正没看到的才算做unread
				if (this.room_list.length != 0) {
					this.room_list[0].unread = 0
				}
				uni.navigateTo({
					url: '/pages/room/room?room=' + room
				})
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
				console.log("join sender", sender)
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
						this.saveData()
						let users = ''
						for (let i in data.nicks)
							users = users + data.nicks[i] + ', '
						users = users.slice(0, users.length - 2)
						this.room_list.push({
							title: this.to_join,
							text: '在线的用户: ' + users,
							time: data.time / 1000,
							unread: 0
						})
					}
				} else if (data.cmd == 'info') {
					var message = {
						// trip: data.trip,
						content: data.text,
						time: data.time / 1000,
						// username: data.trip
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
					uni.showToast({
						title: data.text,
						icon: 'none'
					})
				} else {
					var message = {
						content: "未知的命令" + data.cmd + '' + JSON.stringify(data),
						time: data.time / 1000,
						username: 'system',
					}
					this.insertSystemMessage(message)
					uni.showToast({
						title: "未知的命令" + data.cmd + '' + JSON.stringify(data),
						icon: 'none'
					})
				}
			},
			insertSystemMessage: function(message) {
				// 修改条件
				message.type = 'system'
				this.config.data.messages.push(message)
				// 触发全局事件
				uni.$emit('insertMessage', message)
				// 修改room-list的文字
				if (this.room_list.length != 0) {
					this.room_list[0].text = "系统消息: " + message.content
					this.room_list[0].time = message.time / 1
					this.room_list[0].unread++
				}
			},
			insertMessage: function(message) {
				this.config.data.messages.push(message)
				// 触发全局事件
				uni.$emit('insertMessage', message)

				// 修改room-list的文字
				if (this.room_list.length != 0) {
					this.room_list[0].text = message.username + ": " + message.content
					this.room_list[0].time = message.time / 1
					this.room_list[0].unread++
				}
			},
			onBackRoomList: function() {
				if (this.room_list.length != 0) {
					this.room_list[0].unread = 0
				}
				this.saveData()
			},
			loadData: async function() {
				// console.log('this.indb', this.indb)
				const userDB = this.idb.use('user')
				let data = await userDB.get('user')
				console.log("IndexedDB got", data)
				if (data == undefined)
					return
				this.config.data.user = data
			},
			saveData: async function() {
				// console.log('this.indb.use', this.indb.use)
				const userDB = this.idb.use('user')
				await userDB.put({
					id: 'user',
					value: this.config.data.user
				})
			},
			// 异步的启动
			onMounting: async function() {
				// 加载用户设置
				await this.loadData()
				//// 已经自动加载
				if (this.config.data.user.cookie != undefined)
					this.clickRight()
				// else if (this.config.data.user.password == undefined || this.config.data.user.username == undefined)
				else if (this.config.data.user.cookie == undefined)
					console.log('navigateTo RESUTLT', uni.navigateTo({
						url: '/pages/login',
						animationType: 'zoom-fade-out',
						animationDuration: 300,
					}))
			}
		},
		mounted: function() {
			this.ws.methods.startConnection().then((res) => {
				// console.log(res)
				if (res[0] != null) return
				this.connected = true
			})
			uni.onSocketMessage(this.parser)
			// 监听消息
			uni.$on('joinRoom', this.clickRight)
			// 监听，消除未读消息
			uni.$on('backRoomList', this.onBackRoomList)
			// if (this.room_list.length == 0) this.clickRight()
			// 保存了登录信息
			uni.showToast({
				title: '正在加载中...',
				icon: 'loading'
			})
			this.onMounting()
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
