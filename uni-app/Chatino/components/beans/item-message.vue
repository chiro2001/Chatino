<template>
	<view>
		<!-- <button @click="show = !show">Toggle</button> -->
		<!-- 系统消息另外有动画 -->
		<transition :name="message.type != 'system' ? 'chat-slide-' + mode : 'system-slide'">
			<view v-if="show">
				<!-- 时间 -->
				<view v-if="time" class="chat-time">
					<text>{{ showTime(message.time) }}</text>
				</view>
				<view v-if="message.type != 'system'">
					<view class="chat-receiver" v-if="mode == 'left'">
						<!-- 头像 -->
						<view v-if="head">
							<!-- <image :src="message.user.head"></image> -->
							<image src="@/static/head.png"></image>
						</view>
						<!-- 用户名 -->
						<view>
							{{ message.username }}
						</view>
						<!-- 内容 -->
						<view>
							<view class="chat-left_triangle"></view>
							<text>{{ message.content }}</text>
						</view>
						<!-- 时间 -->
						<!-- <view v-if="time">
						<text>{{ showTime(message.time) }}</text>
					</view> -->
					</view>
					<view class="chat-sender" v-if="mode == 'right'">
						<!-- 头像 -->
						<view v-if="head">
							<!-- <image :src="message.user.head"></image> -->
							<image src="@/static/head.png"></image>
						</view>
						<!-- 用户名 -->
						<view>
							{{ message.username}}
						</view>
						<!-- 内容 -->
						<view>
							<view class="chat-right_triangle"></view>
							<text>{{ message.content }}</text>
						</view>
					</view>
				</view>
				<view class="chat-notice" v-if="message.type == 'system'">
					<!-- 系统消息只显示消息内容 -->
					<text>{{ message.content }}</text>
				</view>
			</view>
		</transition>
	</view>
</template>

<script>
	/* 
	message结构
	message_test: {
		'room': 'test-room',
		'username': 'test-username',
		'content': "That's what I said!",
		'time': 1597389265.0735579,
		'type': 'text',
		'visibility': 'public',
		'status': 'available',
		'direction': 'public',
		'msg': undefined
	}
	 */
	import utils from "../../utils/utils.js"
	export default {
		components: {

		},
		props: {
			message: {
				// 消息的结构体。适配Chatino接口。
				required: true
			},
			mode: {
				// 消息模式从message就有定义
				// 消息模式：
				// simple最简单只有消息内容，只用于二人私聊
				// normal有名字、内容和识别码
				// system显示系统消息

				default: "left"
			},
			head: {
				// 是否显示头像
				default: true
			},
			time: {
				// 是否显示时间
				default: true
			}
		},
		data() {
			return {
				show: false
			}
		},
		methods: {
			showTime: utils.showTime
		},
		mounted: function() {
			// console.log(utils.showTime)
			this.show = true
		}
	}
</script>

<style>
	/* body {
		background-color: #ebebeb;
		font-family: -apple-system;
		font-family: "-apple-system", "Helvetica Neue", "Roboto", "Segoe UI", sans-serif;
	}
 */
	.chat-receiver {
		clear: both;
		font-size: 80%;
	}

	.chat-receiver view:nth-of-type(1) {
		float: left;
	}

	/* 用户名 */
	.chat-receiver view:nth-of-type(2) {
		margin: 0 50px 2px 50px;
		padding: 0px;
		color: #848484;
		font-size: 70%;
		text-align: left;
	}

	/* 内容 */
	.chat-receiver view:nth-of-type(3) {
		/* background-color: white; */
		background-color: #ebebeb;
		/*float: left;*/
		margin: 0 50px 10px 50px;
		padding: 10px 10px 10px 10px;
		border-radius: 7px;
		text-indent: -12px;
		white-space: normal;
		word-break: break-all;
		word-wrap: break-word;
	}

	/*  */

	.chat-sender {
		clear: both;
		font-size: 80%;
	}

	.chat-sender view:nth-of-type(1) {
		float: right;
	}

	.chat-sender view:nth-of-type(2) {
		margin: 0px 50px 2px 50px;
		padding: 0px;
		color: #848484;
		font-size: 70%;
		text-align: right;
	}

	.chat-sender view:nth-of-type(3) {
		/*float:right;*/
		background-color: #b2e281;
		margin: 0px 50px 10px 50px;
		padding: 10px 10px 10px 10px;
		border-radius: 7px;
	}

	.chat-sender view:first-child image,
	.chat-receiver view:first-child image {
		width: 40px;
		height: 40px;
		/*border-radius: 10%;*/
	}

	.chat-left_triangle {
		height: 0px;
		width: 0px;
		border-width: 6px;
		border-style: solid;
		border-color: transparent #ebebeb transparent transparent;
		position: relative;
		left: -22px;
		top: 3px;
	}

	.chat-right_triangle {
		height: 0px;
		width: 0px;
		border-width: 6px;
		border-style: solid;
		border-color: transparent transparent transparent #b2e281;
		position: relative;
		right: -22px;
		top: 3px;
	}

	.chat-notice {
		clear: both;
		font-size: 70%;
		color: white;
		text-align: center;
		margin-top: 15px;
		margin-bottom: 15px;
	}

	.chat-notice text {
		background-color: #cecece;
		line-height: 25px;
		border-radius: 5px;
		padding: 5px 10px;
	}

	.chat-time {
		width: 100%;
		text-align: center;
	}

	.chat-time text {
		color: #848484;
		font-size: 70%;
	}

	.chat-slide-right-enter-active {
		transition: all .3s ease;
	}

	.chat-slide-right-enter {
		transform: translateX(10px);
		opacity: 0;
	}

	.chat-slide-left-enter-active {
		transition: all .3s ease;
	}

	.chat-slide-left-enter {
		transform: translateX(-10px);
		opacity: 0;
	}

	.system-slide-enter-active {
		transition: opacity .3s;
	}

	.system-slide-enter {
		opacity: 0;
	}
</style>
