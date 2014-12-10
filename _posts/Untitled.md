# 会议纪要(December 10, 2014):

* (1)把HTTP header uuid和deviceid去除(token替代)
* (2)列表请求中各种list改为data_list，并去除data级
<pre>
{
	count:
	total:
	data_list:[xx,xx,xx]
	next_cursor:
}
</pre>
* (3)user list 添加user_id
* (4)bind不用传递token，不管是否已经绑定，统一成功，并返回token（关注结果）
* (5)公告点赞API确定（按照荣木已写的API）
* (6)APP点赞操作 本地加1或减1
* (7)APP点赞数只需在进入公告列表时更新
* (8)公告列表断点显示（被动加载），若最后一条存在断点，则不显示
* (9)APP 每个DeviceId 对应一个DB
* (10)添加登录和注销API接口（用于推送）
* (11)API列表统一逆序，如cursor＝100，则返回0到100的数据
* (12)token = (DeviceId＋UUID+bind时间戳)	(某种加密算法)
