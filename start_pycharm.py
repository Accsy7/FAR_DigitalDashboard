#!/usr/bin/env python3
"""
PyCharm专用启动脚本 - 农村三资数据大屏
专门优化以在PyCharm中稳定运行
"""

import http.server
import socketserver
import webbrowser
import os
import sys
import socket
import argparse
import logging
from typing import Optional

def setup_logging(verbose: bool = False):
    """配置适合PyCharm的日志"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.StreamHandler(sys.stdout)  # 确保输出到PyCharm控制台
        ]
    )

def find_free_port(start: int = 8000, end: int = 8100) -> Optional[int]:
    """查找空闲端口，PyCharm友好的实现"""
    for port in range(start, end + 1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('localhost', port))  # 绑定到localhost，避免防火墙问题
            sock.close()
            logging.debug(f"端口 {port} 可用")
            return port
        except OSError as e:
            logging.debug(f"端口 {port} 不可用: {e}")
            continue
    return None

class PyCharmHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """针对PyCharm优化的HTTP处理器"""
    
    def end_headers(self):
        # 添加必要的HTTP头
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        # 安全头
        self.send_header('X-Content-Type-Options', 'nosniff')
        super().end_headers()
    
    def log_message(self, format, *args):
        """在PyCharm中显示有用的日志信息"""
        message = format % args
        # 过滤掉favicon.ico等常见请求的日志，减少干扰
        if 'favicon.ico' not in message:
            logging.debug(f"HTTP请求: {self.address_string()} - {message}")

def resolve_pycharm_working_dir() -> str:
    """
    解决PyCharm中的工作目录问题
    PyCharm可能设置不同的工作目录，需要智能处理
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 检查是否在PyCharm中运行（通过环境变量判断）
    pycharm_env = os.environ.get('PYCHARM_HOSTED', '0')
    
    if pycharm_env == '1' or 'pycharm' in sys.executable.lower():
        logging.info("检测到在PyCharm环境中运行")
        # 在PyCharm中，保持当前目录为项目根目录
        # 但需要确保能访问到所有资源
        current_dir = os.getcwd()
        
        # 检查关键文件是否存在
        required_files = ['index.html', 'lib/leaflet.js', 'css/style.css']
        missing_files = []
        
        for file in required_files:
            if not os.path.exists(os.path.join(current_dir, file)):
                missing_files.append(file)
        
        if missing_files:
            logging.warning(f"在当前目录找不到文件: {missing_files}")
            logging.info(f"切换到脚本目录: {script_dir}")
            os.chdir(script_dir)
            return script_dir
        else:
            logging.info(f"使用PyCharm设置的工作目录: {current_dir}")
            return current_dir
    else:
        # 不在PyCharm中，使用脚本目录
        os.chdir(script_dir)
        return script_dir

def main():
    """主函数 - 专门为PyCharm优化"""
    parser = argparse.ArgumentParser(
        description='农村三资数据大屏 - PyCharm专用启动脚本',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--port', type=int, help='指定服务器端口')
    parser.add_argument('--no-browser', action='store_true', 
                       help='不自动打开浏览器（PyCharm调试时有用）')
    parser.add_argument('--verbose', action='store_true', 
                       help='显示详细日志（调试用）')
    parser.add_argument('--host', default='localhost', 
                       help='绑定主机 (默认: localhost，避免防火墙问题)')
    
    args = parser.parse_args()
    setup_logging(args.verbose)
    
    logging.info("=" * 50)
    logging.info("农村三资数据大屏 - PyCharm专用服务器")
    logging.info("=" * 50)
    
    # 解决PyCharm工作目录问题
    working_dir = resolve_pycharm_working_dir()
    logging.info(f"工作目录: {working_dir}")
    
    # 显示关键文件存在性检查
    logging.info("检查关键资源文件...")
    key_files = {
        'HTML主文件': 'index.html',
        'CSS样式': 'css/style.css',
        'JavaScript主文件': 'js/main.js',
        '地图库': 'lib/leaflet.js',
        '图表库': 'lib/echarts.min.js'
    }
    
    for name, path in key_files.items():
        if os.path.exists(path):
            logging.info(f"  ✓ {name}: {path}")
        else:
            logging.warning(f"  ✗ {name} 不存在: {path}")
    
    # 确定端口
    if args.port:
        port = args.port
        # 检查端口是否可用
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((args.host, port))
            sock.close()
            logging.info(f"使用指定端口: {port}")
        except OSError as e:
            logging.error(f"端口 {port} 不可用: {e}")
            logging.info("尝试寻找其他可用端口...")
            port = find_free_port(8000, 8100)
            if port is None:
                logging.error("找不到可用端口，请检查端口占用情况")
                sys.exit(1)
    else:
        port = find_free_port(8000, 8100)
        if port is None:
            logging.error("在8000-8100范围内找不到可用端口")
            logging.info("建议：")
            logging.info("  1. 关闭占用端口的其他程序")
            logging.info("  2. 使用 --port 参数指定其他端口")
            logging.info("  3. 检查防火墙设置")
            sys.exit(1)
    
    # 服务器信息
    server_url = f"http://{args.host}:{port}"
    logging.info(f"服务器地址: {server_url}")
    logging.info("按 Ctrl+C 停止服务器")
    
    # 在PyCharm中，有时自动打开浏览器不是最佳选择
    if not args.no_browser:
        try:
            logging.info("正在打开浏览器...")
            webbrowser.open(server_url)
        except Exception as e:
            logging.warning(f"无法自动打开浏览器: {e}")
            logging.info(f"请手动访问: {server_url}")
    else:
        logging.info(f"请手动访问: {server_url}")
    
    # 启动服务器
    Handler = PyCharmHTTPRequestHandler
    socketserver.TCPServer.allow_reuse_address = True
    
    try:
        with socketserver.TCPServer((args.host, port), Handler) as httpd:
            logging.info("服务器已启动，等待连接...")
            
            # PyCharm友好提示
            print("\n" + "=" * 50)
            print("服务器运行中!")
            print(f"访问地址: {server_url}")
            print("在PyCharm中:")
            print("  • 控制台输出会显示请求日志（如果启用verbose）")
            print("  • 按红色停止按钮或Ctrl+C停止服务器")
            print("  • 可以点击链接直接访问")
            print("=" * 50 + "\n")
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        logging.info("\n服务器已停止（用户中断）")
        print("\n服务器已停止。")
        sys.exit(0)
    except PermissionError:
        logging.error("权限不足，请尝试:")
        logging.error("  1. 在PyCharm中以管理员身份运行")
        logging.error("  2. 使用1024以上的端口号")
        logging.error("  3. 检查防火墙设置")
        sys.exit(1)
    except Exception as e:
        logging.error(f"服务器启动失败: {e}")
        logging.error("常见问题解决:")
        logging.error("  1. 端口被占用: 使用 --port 指定其他端口")
        logging.error("  2. 防火墙阻止: 检查防火墙设置")
        logging.error("  3. 权限不足: 以管理员身份运行")
        sys.exit(1)

if __name__ == "__main__":
    main()