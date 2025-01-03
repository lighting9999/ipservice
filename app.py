from flask import Flask, request, jsonify
import os
from ipip import IP, IPX

app = Flask(__name__)

def create_https_link(ip, location):
    """
    构建一个指向在线 IP 地理位置查询服务的 HTTPS 链接。
    
    :param ip: 要查询的 IP 地址。
    :param location: 查询到的地理位置信息。
    :return: 返回一个包含 IP 和地理位置信息的 HTTPS 链接字符串。
    """
    base_url = "https://example.com/ipinfo"  # 替换为实际的服务 URL
    return f"{base_url}?ip={ip}&location={location}"

@app.route('/api/ip-location', methods=['GET'])
def find_ip_location():
    ip_address = request.args.get('ip')
    if not ip_address:
        return jsonify({"error": "IP address is required"}), 400

    try:
        # 加载 IPv4 数据文件
        ipv4_data_path = os.path.abspath("mydata4vipday2.dat")
        IP.load(ipv4_data_path)
        result = IP.find(ip_address)

        # 如果 IPX 数据可用，则也尝试加载和查找
        try:
            ipv4x_data_path = os.path.abspath("mydata4vipday2.datx")
            IPX.load(ipv4x_data_path)
            result_x = IPX.find(ip_address)
            if isinstance(result_x, dict) and 'location' in result_x:
                result = result_x['location']
        except Exception as ex:
            print(f"Loading IPX data failed: {ex}")

        # 根据查找结果构建 HTTPS 链接
        if result != "N/A":
            https_link = create_https_link(ip_address, result)
            return jsonify({"ip": ip_address, "location_link": https_link})
        else:
            return jsonify({"error": "无法找到 IP 地址的相关信息"}), 404

    except Exception as ex:
        print(f"An error occurred while finding IP location: {ex}")
        return jsonify({"error": "查询过程中发生错误"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=443)