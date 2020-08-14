<template>
	<view>
		<view class="list-divider" :style="style_divider"></view>
	</view>
</template>

<script>
	export default {
		props: {
			width: {
				default: '100%'
			},
			height: {
				default: '1px'
			},
			color: {
				default: '#E5E5E5'
			}
		},
		data() {
			return {
				style_divider: {
					width: this.width,
					height: this.height,
					"background-color": this.color
				}
			};
		},
		mounted: function() {
			// uni.navigateTo({
			// 	url: './../room/room',
			// 	animationType: 'slide-in-left',
			// 	animationDuration: 300
			// })
		}
	}
</script>

<style>

</style>
