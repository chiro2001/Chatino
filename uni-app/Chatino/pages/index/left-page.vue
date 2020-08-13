<template>
	<view>
		<uni-nav-bar left-icon="back" right-icon="more" @clickLeft="clickLeft()" title="我"></uni-nav-bar>
		 <view class="status_bar"><!-- 这里是状态栏 --></view>
		<view class="intro">我和关于我的一切。</view>
	</view>
</template>

<script>
	import uniNavBar from "@/components/uni-nav-bar/uni-nav-bar.vue"
	
	export default {
		components: {
			uniNavBar,
		},
		data() {
			return {
				
			}
		},
		methods: {
			clickLeft: function() {
				// console.log('Visit ./left-page')
				uni.navigateBack({
					animationType: "slide-out-left",
					animationDuration: 300
				})
			}
		}
	}
</script>

<style>

</style>
