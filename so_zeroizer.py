#!/usr/bin/env python3
import sys
import os
import mmap
import time
from datetime import datetime

class Colors:
    """ANSI颜色代码"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class ArtDisplay:
    """艺术显示类"""
    @staticmethod
    def show_welcome():
        """显示艺术欢迎界面"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        welcome_art = [
            f"{Colors.CYAN}╔══════════════════════════════════════════════════╗{Colors.END}",
            f"{Colors.CYAN}║                                                  ║{Colors.END}",
            f"{Colors.MAGENTA}║              🎭 辉少专用广告去除 🎭              ║{Colors.END}",
            f"{Colors.CYAN}║                                                  ║{Colors.END}",
            f"{Colors.CYAN}║          𝘽 𝙞 𝙣 𝙖 𝙧 𝙮   𝘼 𝙧 𝙩   𝙎 𝙩 𝙪 𝙙 𝙞 𝙤          ║{Colors.END}",
            f"{Colors.CYAN}║                                                  ║{Colors.END}",
            f"{Colors.CYAN}╚══════════════════════════════════════════════════╝{Colors.END}",
            "",
            f"{Colors.YELLOW}✨ flutter黄软广告去除工具 ✨{Colors.END}",
            ""
        ]
        
        for line in welcome_art:
            print(line)
            time.sleep(0.05)

    @staticmethod
    def show_menu():
        """显示交互式菜单"""
        menu = [
            "",
            f"{Colors.BOLD}🚀 请选择操作模式：{Colors.END}",
            f"{Colors.CYAN}┌────────────────────────────────────────────┐{Colors.END}",
            f"{Colors.GREEN}│  1. 开始去除广告                          │{Colors.END}",
            f"{Colors.BLUE}│  2. 查看项目信息                        │{Colors.END}",
            f"{Colors.YELLOW}│  3. 检查系统状态                          │{Colors.END}",
            f"{Colors.RED}│  0. 退出工作室                            │{Colors.END}",
            f"{Colors.CYAN}└────────────────────────────────────────────┘{Colors.END}",
            ""
        ]
        
        for line in menu:
            print(line)
            time.sleep(0.03)
        
        while True:
            try:
                choice = input(f"{Colors.BOLD}🎯 请输入您的选择 (0-3): {Colors.END}")
                
                if choice == '1':
                    return 'start'
                elif choice == '2':
                    ArtDisplay.show_info()
                    continue
                elif choice == '3':
                    ArtDisplay.show_system_info()
                    continue
                elif choice == '0':
                    return 'exit'
                else:
                    print(f"{Colors.RED}❌ 请输入有效的选项 (0-3){Colors.END}")
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.BLUE}👋 再见！{Colors.END}")
                return 'exit'

    @staticmethod
    def show_info():
        """显示工作室信息"""
        info = [
            "",
            f"{Colors.BOLD}📋 广告去除项目信息：{Colors.END}",
            f"{Colors.CYAN}├────────────────────────────────────────────┤{Colors.END}",
            f"{Colors.WHITE}│ 🎯 使命: 用艺术优化广告                │{Colors.END}",
            f"{Colors.WHITE}│ 🔧 技术: 高级二进制处理技术                │{Colors.END}",
            f"{Colors.WHITE}│ 🎨 风格: 极简主义 + 功能美学               │{Colors.END}",
            f"{Colors.WHITE}│ 💫 理念: 愿H软没有广告          │{Colors.END}",
            f"{Colors.CYAN}└────────────────────────────────────────────┘{Colors.END}",
            ""
        ]
        
        for line in info:
            print(line)
            time.sleep(0.03)
        
        input(f"{Colors.YELLOW}⏎ 按回车键返回主菜单...{Colors.END}")
        ArtDisplay.show_welcome()
        ArtDisplay.show_menu()

    @staticmethod
    def show_system_info():
        """显示系统信息"""
        try:
            import psutil
            disk_usage = psutil.disk_usage('/')
            mem = psutil.virtual_memory()
            info = [
                "",
                f"{Colors.BOLD}📊 系统状态监测：{Colors.END}",
                f"{Colors.CYAN}├────────────────────────────────────────────┤{Colors.END}",
                f"{Colors.GREEN}│ 💾 内存: {mem.percent}% 使用中                  │{Colors.END}",
                f"{Colors.BLUE}│ 💿 存储: {disk_usage.percent}% 使用中            │{Colors.END}",
                f"{Colors.YELLOW}│ 🖥️  CPU: {psutil.cpu_percent()}% 使用中         │{Colors.END}",
                f"{Colors.MAGENTA}│ 📁 工作目录: {os.getcwd():<25} │{Colors.END}",
                f"{Colors.CYAN}└────────────────────────────────────────────┘{Colors.END}",
                ""
            ]
        except:
            info = [
                "",
                f"{Colors.BOLD}📊 系统状态监测：{Colors.END}",
                f"{Colors.CYAN}├────────────────────────────────────────────┤{Colors.END}",
                f"{Colors.YELLOW}│ ⚠️  需要安装 psutil 获取详细系统信息       │{Colors.END}",
                f"{Colors.CYAN}└────────────────────────────────────────────┘{Colors.END}",
                ""
            ]
        
        for line in info:
            print(line)
            time.sleep(0.03)
        
        input(f"{Colors.YELLOW}⏎ 按回车键返回主菜单...{Colors.END}")
        ArtDisplay.show_welcome()
        ArtDisplay.show_menu()

class ArtisticProgress:
    """艺术进度条类"""
    def __init__(self, total, length=40):
        self.total = total
        self.length = length
        self.current = 0
        self.start_time = time.time()
        self.art_frames = ['🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘']
        self.frame_index = 0
        
    def update(self, increment=1, found_count=0):
        """更新艺术进度条"""
        self.current += increment
        percent = min(100, (self.current / self.total) * 100)
        
        # 计算统计信息
        elapsed = time.time() - self.start_time
        speed = self.current / elapsed if elapsed > 0 else 0
        
        # 艺术动画帧
        art_frame = self.art_frames[self.frame_index]
        self.frame_index = (self.frame_index + 1) % len(self.art_frames)
        
        # 创建艺术进度条
        filled = int(self.length * percent / 100)
        bar = f"{Colors.GREEN}▓{Colors.END}" * filled + f"{Colors.WHITE}░{Colors.END}" * (self.length - filled)
        
        # 清空并输出
        sys.stdout.write('\r\033[K')
        sys.stdout.write(
            f"{art_frame} {Colors.CYAN}{bar} {Colors.MAGENTA}{percent:5.1f}% "
            f"{Colors.YELLOW}│ {Colors.BLUE}🚀 {speed:.1f}项/秒 "
            f"{Colors.YELLOW}│ {Colors.GREEN}🎯 {found_count}处{Colors.END}"
        )
        sys.stdout.flush()
        
    def complete(self, total_found):
        """完成艺术进度条"""
        elapsed = time.time() - self.start_time
        sys.stdout.write('\r\033[K')
        
        print(f"{Colors.GREEN}✅ {Colors.BOLD}广告去除完成!{Colors.END}")
        print(f"{Colors.CYAN}   ⏱️  耗时: {elapsed:.1f}s {Colors.YELLOW}│ 🎯 修改: {total_found}处{Colors.END}")
        print(f"{Colors.MAGENTA}   ✨ 辉少专用广告去除!{Colors.END}")

class SOZeroizer:
    def __init__(self):
        self.so_file_path = "/storage/emulated/0/MT2/apks/libapp.so"
        self.strings_to_zero = [
            b"playmoviead", b"movie_ad", b"recommend_page",
            b"loading_page", b"appicon_9", b"index_page_promt",
            b"product_banner", b"home_suspend_", b"bannerImageUrl",
            b"/product", b"/darknet", b"/ai", b"/square",
            b"/SharePage", b"/domain/app.version"
        ]
        self.total_changes = 0

    def check_file(self):
        """检查文件是否存在"""
        if not os.path.exists(self.so_file_path):
            print(f"{Colors.RED}❌ 错误: 文件不存在{Colors.END}")
            return False
        
        file_size = os.path.getsize(self.so_file_path)
        print(f"{Colors.BLUE}📁 文件: {os.path.basename(self.so_file_path)}")
        print(f"{Colors.BLUE}📊 大小: {file_size/1024/1024:.1f} MB{Colors.END}")
        return True

    def create_backup(self):
        """创建备份文件"""
        backup_path = self.so_file_path + '.bak'
        if not os.path.exists(backup_path):
            try:
                import shutil
                shutil.copy2(self.so_file_path, backup_path)
                print(f"{Colors.GREEN}✅ 备份已创建: {os.path.basename(backup_path)}{Colors.END}")
                return True
            except Exception as e:
                print(f"{Colors.RED}❌ 备份失败: {e}{Colors.END}")
                return False
        else:
            print(f"{Colors.YELLOW}⚠️  备份文件已存在{Colors.END}")
            return True

    def process_strings(self):
        """艺术化处理广告"""
        try:
            progress = ArtisticProgress(len(self.strings_to_zero))
            
            with open(self.so_file_path, 'r+b') as f:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE) as mm:
                    
                    print(f"\n{Colors.BOLD}🎨 开始去除广告...{Colors.END}\n")
                    time.sleep(1)
                    
                    for i, target_string in enumerate(self.strings_to_zero):
                        target_len = len(target_string)
                        found_count = 0
                        
                        # 搜索并置零
                        pos = 0
                        while True:
                            found_pos = mm.find(target_string, pos)
                            if found_pos == -1:
                                break
                            
                            mm[found_pos:found_pos+target_len] = b'\x00' * target_len
                            found_count += 1
                            self.total_changes += 1
                            pos = found_pos + target_len
                        
                        progress.update(1, self.total_changes)
                        time.sleep(0.1)
                    
                    mm.flush()
                    progress.complete(self.total_changes)
                    return True
                    
        except Exception as e:
            print(f"\n{Colors.RED}❌ 处理失败: {e}{Colors.END}")
            return False

    def run(self):
        """运行艺术工作室"""
        # 显示欢迎界面和菜单
        ArtDisplay.show_welcome()
        choice = ArtDisplay.show_menu()
        
        if choice == 'exit':
            return True
        
        # 检查文件
        if not self.check_file():
            return False
        
        # 创建备份
        if not self.create_backup():
            print(f"{Colors.RED}❌ 无法继续，备份创建失败{Colors.END}")
            return False
        
        # 开始处理
        success = self.process_strings()
        
        if success and self.total_changes > 0:
            # 播放完成提示音
            try:
                os.system("termux-tts-speak '艺术创作完成' 2>/dev/null")
            except:
                pass
        
        return success

def main():
    """主函数"""
    try:
        zeroizer = SOZeroizer()
        zeroizer.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.BLUE}👋 再见！{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}❌ 发生错误: {e}{Colors.END}")

if __name__ == "__main__":
    main()
