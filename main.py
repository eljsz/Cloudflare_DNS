import json
import time

from lxml import etree
import requests




# Read configuration from a local file
with open("config.json", "r",encoding='utf-8') as file:
    config_data = json.load(file)

# Extract values from the config data
auth_email = config_data["auth_email"]
auth_key = config_data["auth_key"]
zone_name = config_data["zone_name"]
record_name = config_data["record_name"]
set_url_config = config_data["set_url_config"]
record_count = config_data["record_count"]
record_type = config_data["record_type"]

def hostmonit():
    print('抓取 https://api.hostmonit.com/get_optimization_ip')
    resp = requests.post('https://api.hostmonit.com/get_optimization_ip', data=json.dumps({'key': 'iDetkOys'})).json()
    ip_list = []

    # 重新排序  CM->CU->CT
    cm_list = []
    cu_list = []
    ct_list = []

    for item in resp["info"]:
        if item["line"] == "CM":
            cm_list.append(item["ip"])
        elif item["line"] == "CU":
            cu_list.append(item["ip"])
        elif item["line"] == "CT":
            ct_list.append(item["ip"])

    for i in range(5):
        ip_list.append(cm_list[i])
        ip_list.append(cu_list[i])
        ip_list.append(ct_list[i])

    print(ip_list)
    return ip_list

def fastwork():
    print('抓取 http://cdn.fastwork.cc/cf/')
    resp = requests.get('http://cdn.fastwork.cc/cf/')
    # obj = re.compile('<table class="table table-hover">.*?</table>')
    html = etree.HTML(resp.text)
    ips = html.xpath('/html/body/div/div/table/tbody/tr/td[2]/span/text()')
    ip_list = []
    for ip in ips:
        ip_list.append(ip)
    print(ip_list)
    return ip_list


def get_public_ip():
    response = requests.get("http://4.ipw.cn")
    return response.text.strip()

if __name__ == '__main__':

    if set_url_config == 1:
        ip_list = hostmonit()
    elif set_url_config == 2:
        ip_list = fastwork()
    else:
        raise RuntimeError('请输入正确set_url_config配置')


    public_ip = get_public_ip()
    print(f"你的IP地址是：{public_ip}")
    print("欢迎关注telegram：https://t.me/+vTwBHA9RbtMwYzA9")

    response = requests.get(f"https://api.cloudflare.com/client/v4/zones?name={zone_name}", headers={
        "X-Auth-Email": auth_email,
        "X-Auth-Key": auth_key,
        "Content-Type": "application/json"
    })
    zone_data = response.json()
    zone_identifier = zone_data["result"][0]["id"]
    print(f"zone_id: {zone_identifier}")

    while record_count > 0:
        record_name_with_count = f"{record_name}{record_count}.{zone_name}"

        response = requests.get(
            f"https://api.cloudflare.com/client/v4/zones/{zone_identifier}/dns_records?name={record_name_with_count}",
            headers={
                "X-Auth-Email": auth_email,
                "X-Auth-Key": auth_key,
                "Content-Type": "application/json"
            })
        record_data = response.json()
        record_id = record_data["result"][0]["id"]
        # print(f"record_id: {record_id}")

        payload = {
            "type": record_type,
            "name": record_name_with_count,
            "content": ip_list[record_count],
            "ttl": 60,
            "proxied": False
        }
        response = requests.put(f"https://api.cloudflare.com/client/v4/zones/{zone_identifier}/dns_records/{record_id}",
                                headers={
                                    "X-Auth-Email": auth_email,
                                    "X-Auth-Key": auth_key,
                                    "Content-Type": "application/json"
                                }, json=payload)
        result = response.json()
        print(f"{record_name_with_count}域名地址更新为: {ip_list[record_count]}")
        print(f"更新结果：{result.get('success')}")

        record_count -= 1

    print("处理完成。10秒自动关闭")
    time.sleep(10)
