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
		}
	}
</script>

<style>
</style>
