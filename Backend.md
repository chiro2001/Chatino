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
        - start: {token/username}
            - 提供方式：
                - {username, password}：在这里login
                - {token}：已经login了
                - {username}：打开匿名
            - 打开ws接口，提供密码之后就不再需要密码
            - 如果不提供密码，必须提供临时username
        - online: {room}
            - 返回room中的在线用户的用户信息
            - 用户users: 【】
                - user: {username, trip, head}
        - help: {room}
            - 在room显示帮助信息
        - join: {room}
            - 加入讨论，开始接收这个room的消息
            - 接收到join消息则加入在线用户列表的信息
        - chat: {room, type, content}
            - 发送消息
            - 消息类型：{text, image}

*其他数据传输*(**使用GET**)
- login: {username, password}
    - 登录即注册
    - 名字会和密码直接绑定
    - 不输入密码就不会绑定
    - 登录后返回token
- info
    - 查询房中他人信息: {username, room}
        - ->{username, trip, info: {head, email, motto}}
    - 设置自己的信息: {token, head, email, motto}
- destroy: {token}
    - 注销该绑定
    - 注销之后所以有关记录内容清除（待定）
- history:
    - 提供时间 {token, room, startTime, stopTime, limit, offset}
    - 按条查询 {token, room, limit, offset}
    - 查询聊天历史记录
    - 能看到给你的私聊

*数据结构和储存*
- 消息
    - {room, type, content, time, 
    username, visibility, status, direction}
- 用户
    - {username, password(md5), 
    trip(password(md5) -> map),
    role,
    info: {head, email, motto}}
- logs
    - {type, data}
- token
    - 已经登录成功的用户对应token，对应单次登录有效
    - 匿名状态对应也有token
    - {username, trip, token}

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