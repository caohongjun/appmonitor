"""
简单的Web服务器
功能：
1. 提供静态文件服务（web目录和data目录）
2. 提供API接口触发AI分析
"""

import os
import json
import subprocess
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


class MyHandler(SimpleHTTPRequestHandler):
    """自定义请求处理器"""

    def __init__(self, *args, **kwargs):
        # 设置根目录为项目根目录
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)

    def do_POST(self):
        """处理POST请求（API接口）"""
        parsed_path = urlparse(self.path)

        # API: 触发分析
        if parsed_path.path == '/api/analyze':
            self.handle_analyze()
            return

        # API: 触发爬取
        if parsed_path.path == '/api/scrape':
            self.handle_scrape()
            return

        # API: 触发检测
        if parsed_path.path == '/api/detect':
            self.handle_detect()
            return

        # 其他POST请求返回404
        self.send_error(404, "Not Found")

    def do_GET(self):
        """处理GET请求（静态文件 + API）"""
        parsed_path = urlparse(self.path)

        # API: 健康检查
        if parsed_path.path == '/health':
            self.send_json_response({'status': 'ok', 'message': 'Server is running'})
            return

        # 忽略 favicon 请求
        if parsed_path.path == '/favicon.ico':
            self.send_response(204)
            self.end_headers()
            return

        # 忽略 Chrome 安全检查请求
        if parsed_path.path.startswith('/.well-known/'):
            self.send_response(204)
            self.end_headers()
            return

        # API: 获取实际存在的日期列表
        if parsed_path.path == '/api/dates':
            self.handle_get_dates()
            return

        # API: 获取实际存在的新上榜产品日期列表
        if parsed_path.path == '/api/detector/dates':
            self.handle_get_new_apps_dates()
            return

        # API: 获取分析结果
        if parsed_path.path.startswith('/api/analysis/'):
            self.handle_get_analysis(parsed_path)
            return

        # 默认使用父类处理（静态文件）
        return super().do_GET()

    def handle_analyze(self):
        """处理分析请求"""
        try:
            # 读取请求数据
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            app_id = data.get('app_id')
            platform = data.get('platform')

            if not app_id or not platform:
                self.send_json_response({'error': '缺少参数'}, 400)
                return

            print(f"\n{'='*60}")
            print(f"📥 收到分析请求:")
            print(f"   App ID: {app_id}")
            print(f"   Platform: {platform}")
            print(f"{'='*60}\n")

            # 在后台线程中执行分析
            def run_analysis():
                project_root = os.path.dirname(os.path.abspath(__file__))
                venv_python = os.path.join(project_root, 'venv', 'bin', 'python')
                analyzer_script = os.path.join(project_root, 'modules', 'analyzer.py')

                # 确保logs目录存在
                log_dir = os.path.join(project_root, 'logs')
                os.makedirs(log_dir, exist_ok=True)

                print(f"🚀 启动分析进程...")
                print(f"   项目根目录: {project_root}")
                print(f"   Python路径: {venv_python}")
                print(f"   Python存在: {os.path.exists(venv_python)}")
                print(f"   脚本路径: {analyzer_script}")
                print(f"   脚本存在: {os.path.exists(analyzer_script)}")
                print(f"   工作目录: {os.getcwd()}")
                print(f"   App ID: {app_id}")
                print(f"   Platform: {platform}")

                # 检查环境变量
                api_key = os.environ.get('ANTHROPIC_API_KEY')
                if api_key:
                    print(f"   ✓ ANTHROPIC_API_KEY 已设置 (长度: {len(api_key)})")
                else:
                    print(f"   ⚠️  ANTHROPIC_API_KEY 未设置")

                # 构建命令
                cmd = [
                    venv_python,
                    analyzer_script,
                    '--app-id', app_id,
                    '--platform', platform
                ]
                print(f"   执行命令: {' '.join(cmd)}")

                try:
                    # 使用subprocess.Popen获取实时输出
                    # 重要：传递当前进程的环境变量（包括ANTHROPIC_API_KEY）
                    import sys
                    process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        cwd=project_root,
                        env=os.environ.copy(),  # 传递环境变量
                        bufsize=1
                    )

                    print(f"\n📝 分析进程输出 (PID: {process.pid}):")
                    print(f"{'='*60}")

                    # 实时打印输出
                    for line in process.stdout:
                        print(line, end='')
                        sys.stdout.flush()

                    # 等待进程结束
                    return_code = process.wait()

                    print(f"{'='*60}")
                    if return_code == 0:
                        print(f"✓ 分析完成: {app_id}")
                    else:
                        print(f"✗ 分析失败: {app_id} (返回码: {return_code})")

                except FileNotFoundError as e:
                    print(f"\n✗ 文件未找到: {e}")
                    print(f"   请检查虚拟环境是否正确安装")
                except Exception as e:
                    print(f"\n✗ 分析异常: {e}")
                    import traceback
                    print(traceback.format_exc())

            # 启动后台线程
            thread = threading.Thread(target=run_analysis, daemon=True)
            thread.start()

            # 立即返回成功响应
            self.send_json_response({
                'success': True,
                'message': f'分析任务已启动: {app_id}'
            })

        except Exception as e:
            print(f"✗ 处理分析请求失败: {e}")
            self.send_json_response({'error': str(e)}, 500)

    def handle_scrape(self):
        """处理爬取请求"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            date = data.get('date')
            platform = data.get('platform')
            category = data.get('category')

            if not date:
                self.send_json_response({'error': '缺少date参数'}, 400)
                return

            print(f"\n{'='*60}")
            print(f"📥 收到爬取请求:")
            print(f"   Date: {date}")
            print(f"   Platform: {platform or '全部'}")
            print(f"   Category: {category or '全部'}")
            print(f"{'='*60}\n")

            def run_scrape():
                project_root = os.path.dirname(os.path.abspath(__file__))
                venv_python = os.path.join(project_root, 'venv', 'bin', 'python')
                scraper_script = os.path.join(project_root, 'modules', 'scraper.py')

                cmd = [venv_python, scraper_script, '--date', date]
                if platform:
                    cmd.extend(['--platform', platform])
                if category:
                    cmd.extend(['--category', category])

                print(f"🚀 启动爬取进程...")
                print(f"   执行命令: {' '.join(cmd)}")

                try:
                    process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        cwd=project_root,
                        env=os.environ.copy(),
                        bufsize=1
                    )

                    print(f"\n📝 爬取进程输出 (PID: {process.pid}):")
                    print(f"{'='*60}")

                    for line in process.stdout:
                        print(line, end='')

                    return_code = process.wait()

                    print(f"{'='*60}")
                    if return_code == 0:
                        print(f"✓ 爬取完成: {date}")
                    else:
                        print(f"✗ 爬取失败: {date} (返回码: {return_code})")

                except Exception as e:
                    print(f"\n✗ 爬取异常: {e}")
                    import traceback
                    print(traceback.format_exc())

            thread = threading.Thread(target=run_scrape, daemon=True)
            thread.start()

            self.send_json_response({
                'success': True,
                'message': f'爬取任务已启动: {date}'
            })

        except Exception as e:
            print(f"✗ 处理爬取请求失败: {e}")
            self.send_json_response({'error': str(e)}, 500)

    def handle_detect(self):
        """处理检测请求"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            date = data.get('date')
            force = data.get('force', False)

            print(f"\n{'='*60}")
            print(f"📥 收到检测请求:")
            print(f"   Date: {date or '今天'}")
            print(f"   Force: {force}")
            print(f"{'='*60}\n")

            def run_detect():
                project_root = os.path.dirname(os.path.abspath(__file__))
                venv_python = os.path.join(project_root, 'venv', 'bin', 'python')
                detector_script = os.path.join(project_root, 'modules', 'detector.py')

                cmd = [venv_python, detector_script]
                if date:
                    cmd.extend(['--date', date])
                if force:
                    cmd.append('--force')

                print(f"🚀 启动检测进程...")
                print(f"   执行命令: {' '.join(cmd)}")

                try:
                    process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        cwd=project_root,
                        env=os.environ.copy(),
                        bufsize=1
                    )

                    print(f"\n📝 检测进程输出 (PID: {process.pid}):")
                    print(f"{'='*60}")

                    for line in process.stdout:
                        print(line, end='')

                    return_code = process.wait()

                    print(f"{'='*60}")
                    if return_code == 0:
                        print(f"✓ 检测完成")
                    else:
                        print(f"✗ 检测失败 (返回码: {return_code})")

                except Exception as e:
                    print(f"\n✗ 检测异常: {e}")
                    import traceback
                    print(traceback.format_exc())

            thread = threading.Thread(target=run_detect, daemon=True)
            thread.start()

            self.send_json_response({
                'success': True,
                'message': '检测任务已启动'
            })

        except Exception as e:
            print(f"✗ 处理检测请求失败: {e}")
            self.send_json_response({'error': str(e)}, 500)

    def handle_get_dates(self):
        """获取实际存在的日期列表"""
        try:
            import os
            from datetime import datetime, timedelta
            
            data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'raw')
            dates = []
            
            if os.path.exists(data_dir):
                # 遍历 data/raw 目录下的所有日期文件夹
                for item in os.listdir(data_dir):
                    item_path = os.path.join(data_dir, item)
                    if os.path.isdir(item_path):
                        # 验证是有效的日期格式
                        try:
                            datetime.strptime(item, '%Y-%m-%d')
                            dates.append(item)
                        except ValueError:
                            pass
            
            # 按日期排序（最新的在前）
            dates.sort(reverse=True)
            
            self.send_json_response({
                'dates': dates
            })
            
        except Exception as e:
            print(f"✗ 获取日期列表失败: {e}")
            self.send_json_response({'error': str(e)}, 500)

    def handle_get_new_apps_dates(self):
        """获取实际存在的新上榜产品日期列表"""
        try:
            import os
            from datetime import datetime
            
            data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'new_apps')
            dates = []
            
            if os.path.exists(data_dir):
                for item in os.listdir(data_dir):
                    item_path = os.path.join(data_dir, item)
                    if os.path.isfile(item_path) and item.endswith('.json'):
                        date_str = item.replace('.json', '')
                        try:
                            datetime.strptime(date_str, '%Y-%m-%d')
                            dates.append(date_str)
                        except ValueError:
                            pass
            
            dates.sort(reverse=True)
            
            self.send_json_response({
                'dates': dates
            })
            
        except Exception as e:
            print(f"✗ 获取新上榜产品日期列表失败: {e}")
            self.send_json_response({'error': str(e)}, 500)

    def handle_get_analysis(self, parsed_path):
        """获取分析结果"""
        try:
            # 从URL提取app_id
            path_parts = parsed_path.path.split('/')
            app_id = path_parts[-1] if len(path_parts) > 0 else None

            if not app_id:
                self.send_json_response({'error': '缺少app_id'}, 400)
                return

            # 解析查询参数
            query_params = parse_qs(parsed_path.query)
            platform = query_params.get('platform', [None])[0]
            date = query_params.get('date', [None])[0]

            if not platform:
                self.send_json_response({'error': '缺少platform参数'}, 400)
                return

            # 如果没有提供日期，使用今天
            if not date:
                from datetime import datetime
                date = datetime.now().strftime('%Y-%m-%d')

            # 构建文件路径
            project_root = os.path.dirname(os.path.abspath(__file__))
            analysis_file = os.path.join(project_root, 'data', 'analysis', date, f'{app_id}.json')

            if not os.path.exists(analysis_file):
                self.send_json_response({'error': '分析结果不存在'}, 404)
                return

            # 读取并返回分析结果
            with open(analysis_file, 'r', encoding='utf-8') as f:
                result = json.load(f)

            self.send_json_response(result)

        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)

    def send_json_response(self, data, status=200):
        """发送JSON响应"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def end_headers(self):
        """添加CORS头"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()


def run_server(port=8000):
    """启动服务器"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, MyHandler)

    print("=" * 60)
    print("🚀 Web服务器已启动")
    print("=" * 60)
    print(f"访问地址: http://localhost:{port}/web/")
    print(f"API地址: http://localhost:{port}/api/")
    print("=" * 60)
    print("功能：")
    print("  - 静态文件服务（web目录和data目录）")
    print("  - API接口：")
    print("    POST /api/analyze - 触发AI分析")
    print("    POST /api/scrape - 触发榜单爬取")
    print("    POST /api/detect - 触发新上榜检测")
    print("    GET  /api/analysis/<app_id> - 获取分析结果")
    print("    GET  /health - 健康检查")
    print("=" * 60)

    # 检查环境变量
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if api_key:
        print(f"✓ ANTHROPIC_API_KEY 已设置 (长度: {len(api_key)})")
    else:
        print("⚠️  警告: ANTHROPIC_API_KEY 未设置")
        print("   AI 分析功能可能无法正常工作")
        print("   解决方案: export ANTHROPIC_API_KEY='your-key'")

    print("=" * 60)
    print("按 Ctrl+C 停止服务器")
    print("")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")


if __name__ == '__main__':
    run_server()
