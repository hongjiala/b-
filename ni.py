import requests
import bilibili.community.service.dm.v1_pb2 as Danmaku
import google.protobuf.text_format as text_format


url = 'https://api.bilibili.com/x/v2/dm/web/history/seg.so'
params = {
    'type':1,           #弹幕类型
    'oid':144541892,    #cid
    'date':'2020-01-21' #弹幕日期
}
cookies = {
    'SESSDATA':'xxx'
}
resp = requests.get(url,params,cookies=cookies)
data = resp.content

danmaku_seg = Danmaku.DmSegMobileReply()
danmaku_seg.ParseFromString(data)

print(text_format.MessageToString(danmaku_seg.elems[0],as_utf8=True))