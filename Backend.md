## Chatino 后端

### 整体架构

- 对外接口：ws/wss
- 命令解释器
- 扩展命令模块


### 技术细节

*WebSocket*

*命令*
- 格式
    - 基本格式`{"cmd": ..., "args": {...}}`
    - 命令：    
        - start: {password/username}
            - 打开ws接口，提供密码之后就不再需要密码
            - 如果不提供密码，必须提供临时username
        - help: {room}
            - 在room显示帮助信息
        - join: {room}
            - 加入讨论，开始接收这个room的消息
        - chat: {room, type, content}
            - 发送消息
            - 消息类型：{text, image}

*其他数据传输*
- login: {password}
    - 登录即注册
    - 名字会和密码直接绑定
    - 不输入密码就不会绑定
- destroy: {password}
    - 注销该绑定
- history: {room, startTime, stopTime}
    - 查询聊天历史记录

*数据结构和储存*
- 消息
    - {room, type, content, time, username, status}
- 用户
    - {username, password(md5), trip(password(md5) -> map)}
- logs
    - {type, data}

*性能提升*
- 暂无

*插件MOD*
- 插件可以从ws的连接获取username
- 放在命令处理阶段，定义cmd和args，定义处理函数
- 处理函数的定义：
    - 按照python包定义
    - import之后访问main函数
    - 参数：cmd, args
    - 操作：发出消息
    - 返回值：无/数据 -> 写入日志
        - 返回不是None的时候，在聊天室输出错误信息（调试模式已经打开）
- 可以从A岛导入trip：
    - 指定串号去发含有指定颜表情的回复即可