<template>
</template>

<script>
	export default {
		data: {
			web: {
				url: 'wss://ws.crosst.chat:35197/',
				official: 'https://crosst.chat'
			},
			rooms: {
				public: ['lounge', '公共聊天室']
			},
			user: {
				username: undefined,
				password: undefined,
				// cookie: 'sTgiHyc5cquTLx2W6tp9rzl',
				cookie: undefined,
			},
			messages: [],
			mdOptions: {
				html: false,
				xhtmlOut: false,
				breaks: true,
				langPrefix: '',
				linkify: true,
				linkTarget: '_blank" rel="noreferrer',
				typographer: true,
				quotes: `""''`,
				// 暂时取消代码高亮
				doHighlight: false,
				// 注意图片的设置
			},
			// 一些功能的设定
			settings: {
				markdown: true,
			}
		},
		methods: {

		},
	}
</script>

<style>
</style>
