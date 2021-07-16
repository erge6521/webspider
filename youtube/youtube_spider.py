import json

import requests
from lxml import html
import re


def get_first_page(url):
    headers = {
        'authority': 'www.youtube.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '"Chromium";v="93", " Not;A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4575.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'service-worker-navigation-preload': 'true',
        'x-client-data': 'CNTzygE=',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'GPS=1; VISITOR_INFO1_LIVE=MHkHYfPloFE; PREF=tz=Asia.Shanghai; YSC=gT8q5kUBQ1Y',
    }

    response = requests.get(url=url, headers=headers)
    print('--------请求到视频首页-------')

    doc = html.fromstring(response.content.decode('utf-8'))
    str = doc.xpath('/html/body/script[14]/text()')

    p_next_params = re.compile('continuationEndpoint":(.*),"request"')
    p_first_request_videoID = re.compile('videoId":"(.{11})')
    re_p_next_params = re.findall(p_next_params, str[0])
    count = len(re_p_next_params)
    result_next_params = json.loads(re_p_next_params[0] + '}}')
    result_first_request_videoID = re.findall(p_first_request_videoID, str[0])
    # 获取第一次请求的videoid
    videoID = set(result_first_request_videoID)

    return count, result_next_params, videoID


def main_run(url, result_next_params, videoid):
    # 取context中的bid的值，其实就是个单点登录，每次登录值会变，但是不变也不会有问题，如果以后有问题就从这里取值，他这里其实记录的就是浏览器信息以及部分电脑信息然后生成的值
    # headers_id = {
    #     'authority': 'googleads.g.doubleclick.net',
    #     'pragma': 'no-cache',
    #     'cache-control': 'no-cache',
    #     'sec-ch-ua': '"Chromium";v="93", " Not;A Brand";v="99"',
    #     'sec-ch-ua-mobile': '?0',
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4575.0 Safari/537.36',
    #     'sec-ch-ua-platform': '"Windows"',
    #     'accept': '*/*',
    #     'origin': 'https://www.youtube.com',
    #     'x-client-data': 'CNTzygE=',
    #     'sec-fetch-site': 'cross-site',
    #     'sec-fetch-mode': 'cors',
    #     'sec-fetch-dest': 'empty',
    #     'referer': 'https://www.youtube.com/',
    #     'accept-language': 'zh-CN,zh;q=0.9',
    #     'cookie': 'id=2220a93658ca00a9||t=1626330353|et=730|cs=002213fd48ce25a6d765883954',
    # }
    #
    # response_id = requests.get('https://googleads.g.doubleclick.net/pagead/id', headers=headers)

    # print(clickTrackingParams,token)
    clickTrackingParams = result_next_params['clickTrackingParams']
    token = result_next_params['continuationCommand']['token']
    result_cookies = {
        'VISITOR_INFO1_LIVE': 'MHkHYfPloFE',
        'PREF': 'tz=Asia.Shanghai',
        'YSC': 'gT8q5kUBQ1Y',
    }

    result_headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '"Chromium";v="93", " Not;A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4575.0 Safari/537.36',
        'Content-Type': 'application/json',
        'X-Youtube-Client-Name': '1',
        'X-Youtube-Client-Version': '2.20210713.07.00',
        'X-Goog-Visitor-Id': 'CgtNSGtIWWZQbG9GRSjRrb-HBg%3D%3D',
        'sec-ch-ua-platform': '"Windows"',
        'Accept': '*/*',
        'Origin': 'https://www.youtube.com',
        'X-Client-Data': 'CNTzygE=',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'same-origin',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.youtube.com/c/%EB%BD%80%EB%AA%A8/videos',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    result_url = 'https://www.youtube.com/youtubei/v1/browse'

    result_params = (
        ('key', 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8'),
    )

    context = {'context': {
        'client': {'hl': 'zh-CN', 'gl': 'US', 'remoteHost': '154.84.1.128', 'deviceMake': '', 'deviceModel': '',
                   'visitorData': 'CgtNSGtIWWZQbG9GRSjRrb-HBg%3D%3D',
                   'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4575.0 Safari/537.36,gzip(gfe)',
                   'clientName': 'WEB', 'clientVersion': '2.20210713.07.00', 'osName': 'Windows',
                   'osVersion': '10.0',
                   'originalUrl': f'{url}', 'platform': 'DESKTOP',
                   'clientFormFactor': 'UNKNOWN_FORM_FACTOR', 'timeZone': 'Asia/Shanghai', 'browserName': 'Chrome',
                   'browserVersion': '93.0.4575.0', 'screenWidthPoints': 1920, 'screenHeightPoints': 412,
                   'screenPixelDensity': 1, 'screenDensityFloat': 1, 'utcOffsetMinutes': 480,
                   'userInterfaceTheme': 'USER_INTERFACE_THEME_LIGHT', 'connectionType': 'CONN_CELLULAR_3G',
                   'mainAppWebInfo': {'graftUrl': f'{url}',
                                      'webDisplayMode': 'WEB_DISPLAY_MODE_BROWSER',
                                      'isWebNativeShareAvailable': True}},
        'user': {'lockedSafetyMode': False},
        'request': {'useSsl': True, 'internalExperimentFlags': [], 'consistencyTokenJars': []},
        'clickTracking': {'clickTrackingParams': f'{clickTrackingParams}'}, 'adSignalsInfo': {
            'params': [{'key': 'dt', 'value': '1626330834091'}, {'key': 'flash', 'value': '0'},
                       {'key': 'frm', 'value': '0'}, {'key': 'u_tz', 'value': '480'},
                       {'key': 'u_his', 'value': '8'},
                       {'key': 'u_java', 'value': 'false'}, {'key': 'u_h', 'value': '1080'},
                       {'key': 'u_w', 'value': '1920'}, {'key': 'u_ah', 'value': '1040'},
                       {'key': 'u_aw', 'value': '1920'},
                       {'key': 'u_cd', 'value': '24'}, {'key': 'u_nplug', 'value': '3'},
                       {'key': 'u_nmime', 'value': '4'},
                       {'key': 'bc', 'value': '31'}, {'key': 'bih', 'value': '412'},
                       {'key': 'biw', 'value': '1904'},
                       {'key': 'brdim', 'value': '0,0,0,0,1920,0,1920,1040,1920,412'}, {'key': 'vis', 'value': '1'},
                       {'key': 'wgl', 'value': 'true'}, {'key': 'ca_type', 'value': 'image'}],
            'bid': 'ANyPxKouqu99e7Ce3tGBx3IS0a-CaE-0vulF_VM79c5UyhpO0IE5ahZQX5KkCYM3pEs4AhUtK_omYcGllhRrhw6SZzTS1Wun0Q'}},
        'continuation': f'{token}'}

    data = json.dumps(context)
    result = requests.post(url=result_url, headers=result_headers, params=result_params, cookies=result_cookies,
                           data=data)
    print('加载下一页完成')

    context = json.loads(result.content.decode('utf-8'))
    continuationItems = context['onResponseReceivedActions'][0]['appendContinuationItemsAction'][
        'continuationItems']
    # print(continuationItems)
    continuationItemRenderer = continuationItems.pop(-1)
    # 加个判断，防止continuationItems在pop操作后为空程序异常
    if len(continuationItems) > 0:
        for i in continuationItems:
            # print(i['gridVideoRenderer']['videoId'])
            videoid.add(i['gridVideoRenderer']['videoId'])

    return continuationItemRenderer, videoid


def get_next_page(url, result_next_params, videoid, count):
    if count == 0:
        print('------这个博主作品太少了，一页就加载完了------')
    else:
        continuationItemRenderer, videoid = main_run(url, result_next_params, videoid)
        return continuationItemRenderer, videoid


if __name__ == '__main__':
    url = 'https://www.youtube.com/c/%EB%BD%80%EB%AA%A8/videos'
    count, result_next_params, videoid = get_first_page(url)
    continuationItemRenderer, videoid = get_next_page(url, result_next_params, videoid, count)

    while True:
        if 'continuationItemRenderer' in continuationItemRenderer:
            result_next_params = continuationItemRenderer['continuationItemRenderer']['continuationEndpoint']
            continuationItemRenderer, videoid = main_run(url, result_next_params, videoid)
            # continuationItemRenderer = continuationItems.pop(-1)

        else:
            videoid.add(continuationItemRenderer['gridVideoRenderer']['videoId'])
            print('所有视频id已加载完')
            break

    print(videoid)
