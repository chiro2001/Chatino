<template>
	<view>
		<uni-nav-bar left-icon="bars" right-icon="more" @clickLeft="clickLeft()" title="消息列表"></uni-nav-bar>
		<!-- <view class="intro">消息列表。</view> -->
		<view>
			<item-room></item-room>
			<item-room></item-room>
		</view>
	</view>
</template>

<script>
	import uniNavBar from "@/components/uni-nav-bar/uni-nav-bar.vue"
	import ItemRoom from "@/components/beans/item-room.vue"
	
	export default {
		components: {
			uniNavBar,
			ItemRoom
		},
		data() {
			return {
				
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
			}
		}
	}
</script>

<style>

</style>
