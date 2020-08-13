<template>
	<view>
		<view class="item-room">
			<view class="item-room-left">
				<view class="item-room-title">Title</view>
				<view class="item-room-text">text</view>
			</view>
			<view class="item-room-right">
				<view class="item-room-time">00:00</view>
				<!-- <view class="item-room-unread">
				<view class="item-room-unread-num">2</view>
			</view> -->
				<uni-badge text="1" type="error"></uni-badge>
			</view>
		</view>
		<divider v-if="divider"></divider>
	</view>
</template>

<script>
	import divider from "../list/divider.vue"

	export default {
		name: "item-room",
		components: {
			divider,
		},
		props: {
			divider: {
				type: Boolean,
				default: true
			}
		},
		data: function() {
			return {

			};
		},
	}
</script>

<style>
	.item-room {
		min-height: 48px;
		display: flex;
		padding: 3%;
		flex-direction: row;
		justify-content: space-between;
	}

	/* 右对齐 */
	.item-room-right {
		display: flex;
		flex-direction: column;
		align-items: flex-end;
	}

	/* .item-room-unread {
		height: 20px;
		width: 20px;
		border-radius: 20px;
		background-color: red;
	}

	.item-room-unread-num {
		height: 20px;
		line-height: 20px;
		display: block;
		color: white;
		text-align: center;
		font-size: 10px;
	} */

	.item-room-title {
		color: black;
		font-size: 20px;
	}

	.item-room-text {
		color: grey;
		font-size: 16px;
	}

	.item-room-time {
		color: grey;
		font-size: 16px;
	}
</style>
