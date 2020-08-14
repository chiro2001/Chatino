import moment from "moment"

export default {
	showTime: function(utime) {
		moment.locale('zh-cn')
		// 注意是毫秒数
		var result = moment(utime * 1000).calendar()
		return result
	}
}