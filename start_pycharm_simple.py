#!/usr/bin/env python3
"""
PyCharm专用简化启动脚本 - 农村三资数据大屏
解决PyCharm中最常见的问题：
1. 工作目录问题
2. 端口占用问题
3. 清晰的错误提示
"""

import http.server
import socketserver
import webbrowser
import os
import sys
import socket

def find_free_port(start=8000, end=8100):
    """查找空闲端口"""
    for port in range(start, end):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('localhost', port))  # 使用localhost避免防火墙问题
            s.close()
            return port
        except OSError:
            continue
    return None

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()
    
    def log_message(self, format, *args):
        # 简化日志，避免PyCharm控制台过于混乱
        pass

def main():
    # PyCharm工作目录智能处理
    script_dir = os.path.dirname(os.path.abspath(__file__))
    current_dir = os.getcwd()
    
    print("=" * 50)
    print("农村三资数据大屏 - PyCharm专用服务器")
    print("=" * 50)
    print(f"脚本目录: {script_dir}")
    print(f"当前目录: {current_dir}")
    
    # 检查是否在正确的目录
    if not os.path.exists(os.path.join(current_dir, 'index.html')):
        print("警告: 在当前目录找不到 index.html")
        print(f"切换到脚本目录: {script_dir}")
        os.chdir(script_dir)
    else:
        print("✓ 在当前目录找到 index.html，使用当前目录")
    
    # 检查关键文件
    print("\n检查关键资源文件:")
    files_to_check = [
        ('index.html', 'HTML主文件'),
        ('css/style.css', 'CSS样式'),
        ('js/main.js', 'JavaScript主文件'),
        ('lib/leaflet.js', '地图库'),
        ('lib/echarts.min.js', '图表库')
    ]
    
    all_ok = True
    for file_path, description in files_to_check:
        if os.path.exists(file_path):
            print(f"  ✓ {description}: {file_path}")
        else:
            print(f"  ✗ {description} 不存在: {file_path}")
            all_ok = False
    
    if not all_ok:
        print("\n警告: 部分关键文件缺失，页面可能无法正常显示")
        print("建议运行: python download_libs.py 下载缺失的库文件")
    
    # 查找可用端口
    port = find_free_port()
    if port is None:
        print("\n错误: 在8000-8100范围内找不到可用端口")
        print("可能的原因:")
        print("  1. 端口被其他程序占用")
        print("  2. 防火墙阻止访问")
        print("  3. 权限不足")
        print("\n解决方案:")
        print("  1. 关闭占用端口的程序")
        print("  2. 修改脚本中的端口范围")
        print("  3. 以管理员身份运行PyCharm")
        sys.exit(1)
    
    print(f"\n服务器运行在: http://localhost:{port}")
    print("按 Ctrl+C 停止服务器")
    
    # 尝试打开浏览器
    try:
        webbrowser.open(f"http://localhost:{port}")
        print("已自动打开浏览器")
    except:
        print(f"请手动访问: http://localhost:{port}")
    
    # 启动服务器
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print("\n" + "=" * 50)
            print("服务器已启动!")
            print(f"在PyCharm中访问: http://localhost:{port}")
            print("按红色停止按钮或Ctrl+C停止服务器")
            print("=" * 50 + "\n")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
        sys.exit(0)
    except Exception as e:
        print(f"\n错误: 服务器启动失败 - {e}")
        print("常见问题解决:")
        print("  1. 尝试不同的端口 (修改脚本中的端口范围)")
        print("  2. 检查防火墙设置")
        print("  3. 以管理员身份运行PyCharm")
        sys.exit(1)

if __name__ == "__main__":
    main()