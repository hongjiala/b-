# （本文首发在“程序员coding”公众号）
import requests
import re
import datetime

# content_list存放所有弹幕
content_list = []
# 爬取开始日期和结束日期范围内的弹幕
begin = datetime.date(2023, 12, 28)
end = datetime.date(2024, 1, 2)
for i in range((end - begin).days + 1):
    day = begin + datetime.timedelta(days=i)
    url = f'https://api.bilibili.com/x/v2/dm/wbi/web/seg.so?type=1&oid=197711172&date={day}'
    #https://api.bilibili.com/x/v2/dm/wbi/web/seg.so?type=1&oid=197711172&date={day}
   # https://data.bilibili.com/v2/log/web?content_type=pbrequest&logid=021436&disable_compression=true
    #https://api.bilibili.com/x/v2/dm/wbi/web/seg.so?type=1&oid=197711172&pid=328492664&segment_index=1&pull_mode=1&ps=0&pe=120000&web_location=1315873&w_rid=511786ca2def7ab9f99a158854bd8a6d&wts=1727352151
    headers  = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
    'cookie': 'buvid3=7851D727-0603-DEB3-0DBC-A6D9FD86B03983207infoc; b_nut=1697274283; i-wanna-go-back=-1; b_ut=7; _uuid=3F689CC5-89F6-CC6A-2E10C-103ABF7ECF3ED83882infoc; enable_web_push=DISABLE; buvid4=FE9D0F06-9BA6-F0CF-A43B-314E5575F9BA84676-023101417-dx%2FaaQBcjhGgMGKEShEHKA%3D%3D; header_theme_version=CLOSE; rpdid=|(YYRJuuu|l0J\'uYm~k~RJYm; hit-dyn-v2=1; buvid_fp_plain=undefined; FEED_LIVE_VERSION=V_WATCHLATER_PIP_WINDOW3; SESSDATA=ce961b97%2C1728468941%2C24cb7%2A42CjBJS_A94oms2hTZAqEpN2duzi8MS4AZtUSy31xmx2pgzQi8j834Jb265QXMpMtXhmASVnBsQ1RkclJZVmtveDRTUnBvOHdDRUhaMl9qcGkwQlJpcWl1TmtGUkFFZ0dfS1BKYnlpN0RYLTQ5bFpDcWlTSmIzQl90cWFNaHZVS1lHQU9vTnE3eWF3IIEC; bili_jct=cf26bc61caebdd9487b54b2b1501823f; DedeUserID=651103095; DedeUserID__ckMd5=136d77eaa57d2fdc; sid=5oha8ief; CURRENT_BLACKGAP=0; CURRENT_FNVAL=16; LIVE_BUVID=AUTO4417241206523669; PVID=6; CURRENT_QUALITY=64; fingerprint=100536d50ea8f1aa9c35d0618c12347e; buvid_fp=26a110e14381cd91f161c9f49cd5d368; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjczOTcxNzQsImlhdCI6MTcyNzEzNzkxNCwicGx0IjotMX0.c-RTCvvUpkMrg1FIvfzlirG1lQxR53O_Gx5E2_e4gCQ; bili_ticket_expires=1727397114; b_lsid=A4A1067A9_1922E24E0A1; home_feed_column=4; bp_t_offset_651103095=981454431486738432; browser_resolution=511-928',
}
    response = requests.get(url=url, headers=headers)
    response.encoding = 'utf-8'

    temp_list = re.findall('[\u4e00-\u9fa5]+', response.text)
    content_list.extend(temp_list)
    print("爬取", day, "日弹幕,获取到：", len(temp_list), "条弹幕，已经增加到总列表。总列表共有", len(content_list),
          "条弹幕。")

# 保存数据
content = '\n'.join(content_list)
with open('弹幕.txt', mode='a', encoding='utf-8') as f:
    f.write(content)
print("保存完成")

