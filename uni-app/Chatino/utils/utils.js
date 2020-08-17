import moment from "moment"

export default {
	showTime: function(utime) {
		moment.locale('zh-cn')
		// 注意是毫秒数
		var result = moment(utime * 1000).calendar()
		return result
	},
	
	limitString: function(string) {
		if (string.length > 15)
			string  = string.slice(0, 15) + '...'
		string = string.replace('\n', '')
		return string
	}
}