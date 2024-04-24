import requests
import re
import cv2  # 导入OpenCV库
# 定义组播地址和端口
urls_udp = "/udp/239.77.0.1:5146"
# 定义fofa链接
fofa_url = 'https://fofa.info/result?qbase64=InVkcHh5IiAmJiBwcm90b2NvbD0iaHR0cCIgJiYgY2l0eT0iR3Vhbmd6aG91IiAmJiBzZXJ2ZXI9PSJ1ZHB4eSAxLjAtMjUuMCAocHJvZCkgc3RhbmRhcmQgW0xpbnV4IDUuMTAuMTk0IHg4Nl82NF0i'
fofa_url_gd = 'https://fofa.info/result?qbase64=InVkcHh5IiAmJiBwcm90b2NvbD0iaHR0cCIgJiYgcmVnaW9uPSJHdWFuZ2RvbmciICYmIHNlcnZlcj09InVkcHh5IDEuMC0yNS4wIChwcm9kKSBzdGFuZGFyZCBbTGludXggNS4xMC4xOTQgeDg2XzY0XSI%3D'
fofa_url_fs = 'https://fofa.info/result?qbase64=InVkcHh5IiAmJiBwcm90b2NvbD0iaHR0cCIgJiYgY2l0eT0iRm9zaGFuIiAmJiBzZXJ2ZXI9PSJ1ZHB4eSAxLjAtMjUuMCAocHJvZCkgc3RhbmRhcmQgW0xpbnV4IDUuMTAuMTk0IHg4Nl82NF0i'
# 尝试从fofa链接提取IP地址和端口号，并去除重复项
def extract_unique_ip_ports(fofa_url):
    try:
        response = requests.get(fofa_url)
        html_content = response.text
        # 使用正则表达式匹配IP地址和端口号
        middle = re.findall(r'Array.*</script>', html_content)
        print(middle)
        ips_ports = re.findall(r'(\d+\.\d+\.\d+\.\d+:\d+)',middle[0])
        return ips_ports if ips_ports else None
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return None

# 检查视频流的可达性
def check_video_stream_connectivity(ip_port, urls_udp):
    try:
        # 构造完整的视频URL
        video_url = f"http://{ip_port}{urls_udp}"
        # 用OpenCV读取视频
        cap = cv2.VideoCapture(video_url)
        
        # 检查视频是否成功打开
        if not cap.isOpened():
            print(f"视频URL {video_url} 无效")
            return None
        else:
            # 读取视频的宽度和高度
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            print(f"视频URL {video_url} 的分辨率为 {width}x{height}")
            # 检查分辨率是否大于0
            if width > 0 and height > 0:
                return ip_port  # 返回有效的IP和端口
            # 关闭视频流
            cap.release()
    except Exception as e:
        print(f"访问 {ip_port} 失败: {e}")
    return None

# 更新文件中的IP地址和端口号
def update_files(accessible_ip_port,ip_port_pattern,ip_port_repl,files_to_update):
    global updated_content
    for file_info in files_to_update:
        try:
            # 读取原始文件内容
            response = requests.get(file_info['url'])
            if updated_content:
                file_content = updated_content
            else:
                file_content = response.text

            # 替换文件中的IP地址和端口号
            # 假设文件中的IP地址和端口号格式为 http://IP:PORT
            #ip_port_pattern = r'(http://\d+\.\d+\.\d+\.\d+:\d+)'
            updated_content = re.sub(ip_port_pattern, ip_port_repl, file_content)
            print(updated_content)
            # 保存更新后的内容到新文件
            with open(file_info['filename'], 'w', encoding='utf-8') as file:
                file.write(updated_content)

            print(f"文件 {file_info['filename']} 已更新并保存。")
        except requests.RequestException as e:
            print(f"无法更新文件 {file_info['filename']}，错误: {e}")

def findtheone(unique_ips_ports):
    if unique_ips_ports:
        print("提取到的唯一IP地址和端口号：")
        for ip_port in unique_ips_ports:
            print(ip_port)
    
    # 测试每个IP地址和端口号，直到找到一个可访问的视频流
        valid_ip = None
        for ip_port in unique_ips_ports:
            valid_ip = check_video_stream_connectivity(ip_port, urls_udp)
            if valid_ip:
                break  # 找到有效的IP后，不再继续循环

        if valid_ip:
            print(f"找到可访问的视频流服务: {valid_ip}")\

        else:
            print("没有找到可访问的视频流服务。")
    else:
        print("没有提取到IP地址和端口号。")
    return valid_ip


# 提取唯一的IP地址和端口号
unique_ips_ports = extract_unique_ip_ports(fofa_url)
print(unique_ips_ports)
unique_ips_ports_fs = extract_unique_ip_ports(fofa_url_fs)
print(unique_ips_ports_fs)
unique_ips_ports_gd = extract_unique_ip_ports(fofa_url_gd)
print(unique_ips_ports_gd)

valid_ip = findtheone(unique_ips_ports)
print(valid_ip)
valid_ip_fs = findtheone(unique_ips_ports_fs)
print(valid_ip_fs)
valid_ip_gd = findtheone(unique_ips_ports_gd)
print(valid_ip_gd)
# 定义需要更新的文件列表
files_to_update = [
    {'url': 'https://mirror.ghproxy.com/https://raw.githubusercontent.com/jaccong/loong/main/9.txt', 'filename': '9.txt'}
]

#定义正则
ip_port_pattern = r'(\[GZ\]\,http://\d+\.\d+\.\d+\.\d+:\d+)'
ip_port_pattern_fs = r'(\[FS\]\,http://\d+\.\d+\.\d+\.\d+:\d+)'
ip_port_pattern_gd = r'(\[GD\]\,http://\d+\.\d+\.\d+\.\d+:\d+)'
ip_port_repl = f'[GZ],http://{valid_ip}'
ip_port_repl_fs = f'[FS],http://{valid_ip_fs}'
ip_port_repl_gd = f'[GD],http://{valid_ip_gd}'

# 更新文件中的IP地址和端口号
updated_content = ''
update_files(valid_ip,ip_port_pattern,ip_port_repl,files_to_update)
update_files(valid_ip_fs,ip_port_pattern_fs,ip_port_repl_fs,files_to_update)
update_files(valid_ip_gd,ip_port_pattern_gd,ip_port_repl_gd,files_to_update)

