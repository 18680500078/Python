#!/usr/bin/env python3
# final_cs_injector_complete.py

import os
import sys
import zipfile
import tempfile
import shutil
import subprocess
import re
import glob

class FinalInjector:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        
    def cleanup(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def extract_dex_files(self, apk_path):
        """直接从APK中提取dex文件"""
        print("📦 提取dex文件...")
        extract_dir = os.path.join(self.temp_dir, "dex_extracted")
        os.makedirs(extract_dir, exist_ok=True)
        
        try:
            with zipfile.ZipFile(apk_path, 'r') as zip_ref:
                # 提取所有dex文件
                dex_files = [f for f in zip_ref.namelist() if f.endswith('.dex')]
                for dex_file in dex_files:
                    zip_ref.extract(dex_file, extract_dir)
                    print(f"✅ 提取: {dex_file}")
            
            return extract_dir, dex_files
        except Exception as e:
            print(f"❌ 提取dex失败: {e}")
            return None, []

    def download_tool(self, url, filename):
        """下载工具"""
        tool_path = os.path.join(self.temp_dir, filename)
        
        try:
            import requests
            print(f"📥 下载 {filename}...")
            response = requests.get(url)
            with open(tool_path, 'wb') as f:
                f.write(response.content)
            return tool_path
        except Exception as e:
            print(f"❌ 下载失败: {e}")
            return None

    def decompile_dex(self, dex_path, output_dir):
        """反编译dex为smali"""
        print(f"🔧 反编译 {os.path.basename(dex_path)}...")
        
        try:
            # 下载baksmali工具
            baksmali_url = "https://bitbucket.org/JesusFreke/smali/downloads/baksmali-2.5.2.jar"
            baksmali_path = self.download_tool(baksmali_url, "baksmali.jar")
            if not baksmali_path:
                return False
            
            # 反编译dex
            cmd = ["java", "-jar", baksmali_path, "d", dex_path, "-o", output_dir]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ 反编译成功: {output_dir}")
                return True
            else:
                print(f"❌ 反编译失败: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 反编译过程出错: {e}")
            return False

    def find_target_smali(self, smali_dir, target_class):
        """查找目标smali文件"""
        print("🔍 查找目标smali文件...")
        
        # 将Java包名转换为smali路径
        smali_path = target_class.replace('.', '/') + ".smali"
        target_file = os.path.join(smali_dir, smali_path)
        
        if os.path.exists(target_file):
            print(f"✅ 找到目标文件: {target_file}")
            return target_file
        
        # 如果没找到，搜索所有smali文件
        print("⚠️  标准路径未找到，开始全局搜索...")
        for root, dirs, files in os.walk(smali_dir):
            for file in files:
                if file == os.path.basename(smali_path):
                    full_path = os.path.join(root, file)
                    print(f"✅ 深度搜索找到目标文件: {full_path}")
                    return full_path
        
        print("❌ 未找到目标smali文件")
        return None

    def inject_code_proper(self, smali_file, injection_code):
        """注入代码到正确位置 - .registers声明之后"""
        print(f"💉 向 {smali_file} 注入代码...")
        
        try:
            with open(smali_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # 备份原始文件
            backup_file = smali_file + '.bak'
            shutil.copy2(smali_file, backup_file)
            
            # 查找onCreate方法
            lines = content.split('\n')
            new_lines = []
            in_oncreate = False
            found_registers = False
            injected = False
            
            for i, line in enumerate(lines):
                new_lines.append(line)
                
                # 检查是否进入onCreate方法
                if line.strip().startswith('.method') and 'onCreate' in line:
                    print(f"✅ 找到onCreate方法: {line.strip()}")
                    in_oncreate = True
                    continue
                
                # 检查是否离开onCreate方法
                if line.strip().startswith('.end method') and in_oncreate:
                    in_oncreate = False
                    continue
                
                # 在onCreate方法内
                if in_oncreate and not injected:
                    # 查找.registers声明
                    if line.strip().startswith('.registers'):
                        found_registers = True
                        continue
                    
                    # 在.registers声明之后立即注入
                    if found_registers and line.strip() and not line.strip().startswith('.'):
                        print(f"📍 在.registers声明后立即注入 (第{i+1}行前)")
                        
                        # 添加注入代码
                        injection_lines = injection_code.split('\n')
                        for inj_line in reversed(injection_lines):
                            if inj_line.strip():
                                # 使用适当的缩进（通常是4空格）
                                indent = '    '
                                new_lines.insert(len(new_lines) - 1, f"{indent}{inj_line}")
                        
                        injected = True
            
            if injected:
                # 写入文件
                with open(smali_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(new_lines))
                
                print("✅ 代码注入完成")
                return True
            else:
                print("❌ 未找到合适的注入位置")
                # 显示方法开头部分帮助调试
                print("📄 方法开头内容:")
                for j, line in enumerate(lines[:20]):
                    print(f"  {j+1}: {line}")
                return False
                
        except Exception as e:
            print(f"❌ 注入过程出错: {e}")
            import traceback
            traceback.print_exc()
            return False

    def download_and_integrate_zip(self, zip_url, smali_dir):
        """从GitHub下载zip文件并整合到smali中"""
        print(f"📥 下载并整合zip文件: {zip_url}")
        
        try:
            import requests
            import zipfile
            
            # 下载zip文件
            response = requests.get(zip_url)
            if response.status_code != 200:
                print(f"❌ 下载失败: HTTP {response.status_code}")
                return False
            
            # 保存zip文件
            zip_path = os.path.join(self.temp_dir, "external_classes.zip")
            with open(zip_path, 'wb') as f:
                f.write(response.content)
            
            print("✅ Zip文件下载完成")
            
            # 解压zip文件
            extract_dir = os.path.join(self.temp_dir, "external_classes")
            os.makedirs(extract_dir, exist_ok=True)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            print("✅ Zip文件解压完成")
            
            # 复制smali文件到目标目录
            extracted_smali_dirs = glob.glob(os.path.join(extract_dir, "*"))
            for extracted_dir in extracted_smali_dirs:
                if os.path.isdir(extracted_dir):
                    dir_name = os.path.basename(extracted_dir)
                    target_dir = os.path.join(smali_dir, dir_name)
                    
                    # 如果目标目录不存在，直接复制
                    if not os.path.exists(target_dir):
                        shutil.copytree(extracted_dir, target_dir)
                        print(f"✅ 复制目录: {dir_name}")
                    else:
                        # 如果目标目录存在，合并文件
                        for root, dirs, files in os.walk(extracted_dir):
                            for file in files:
                                if file.endswith('.smali'):
                                    src_file = os.path.join(root, file)
                                    rel_path = os.path.relpath(root, extracted_dir)
                                    dst_dir = os.path.join(target_dir, rel_path)
                                    os.makedirs(dst_dir, exist_ok=True)
                                    dst_file = os.path.join(dst_dir, file)
                                    
                                    shutil.copy2(src_file, dst_file)
                                    print(f"✅ 复制文件: {os.path.join(rel_path, file)}")
            
            print("✅ Zip文件整合完成")
            return True
            
        except Exception as e:
            print(f"❌ Zip文件处理失败: {e}")
            import traceback
            traceback.print_exc()
            return False

    def compile_smali_to_dex(self, smali_dir, output_dex):
        """编译smali为dex"""
        print(f"🔨 编译smali为 {os.path.basename(output_dex)}...")
        
        try:
            # 下载smali工具
            smali_url = "https://bitbucket.org/JesusFreke/smali/downloads/smali-2.5.2.jar"
            smali_path = self.download_tool(smali_url, "smali.jar")
            if not smali_path:
                return False
            
            # 编译smali
            cmd = ["java", "-jar", smali_path, "assemble", smali_dir, "-o", output_dex]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ 编译成功: {output_dex}")
                return True
            else:
                print(f"❌ 编译失败: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 编译过程出错: {e}")
            return False

    def create_debug_keystore(self):
        """创建调试密钥库"""
        keystore_path = os.path.join(os.path.dirname(__file__), "debug.keystore")
        if os.path.exists(keystore_path):
            return True
        
        try:
            cmd = [
                "keytool", "-genkey", "-v",
                "-keystore", keystore_path,
                "-alias", "androiddebugkey",
                "-keyalg", "RSA",
                "-keysize", "2048",
                "-validity", "10000",
                "-storepass", "android",
                "-keypass", "android",
                "-dname", "CN=Android Debug,O=Android,C=US"
            ]
            
            result = subprocess.run(cmd, input=b'\n', capture_output=True)
            
            if result.returncode == 0:
                print("✅ 调试密钥库创建成功")
                return True
            else:
                print(f"❌ 密钥库创建失败: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 创建密钥库失败: {e}")
            return False

    def sign_apk(self, apk_path):
        """签名APK"""
        print("🔏 签名APK...")
        
        try:
            keystore_path = os.path.join(os.path.dirname(__file__), "debug.keystore")
            
            # 签名APK
            sign_cmd = [
                "jarsigner", "-verbose",
                "-keystore", keystore_path,
                "-storepass", "android",
                "-keypass", "android",
                apk_path,
                "androiddebugkey"
            ]
            
            sign_result = subprocess.run(sign_cmd, capture_output=True, text=True)
            
            if sign_result.returncode == 0:
                print(f"✅ APK签名成功: {apk_path}")
                return True
            else:
                print(f"❌ APK签名失败: {sign_result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 签名过程出错: {e}")
            return False

    def process_injection(self, apk_path, target_class, injection_code, zip_url=None):
        """主处理流程"""
        print("=" * 50)
        print("🚀 开始最终注入流程")
        print("=" * 50)
        
        # 1. 提取原始APK的dex文件
        extract_dir, dex_files = self.extract_dex_files(apk_path)
        if not extract_dir:
            return None
        
        # 2. 反编译所有dex文件
        modified_dex_files = []
        for dex_file in dex_files:
            dex_path = os.path.join(extract_dir, dex_file)
            smali_dir = os.path.join(self.temp_dir, f"smali_{os.path.splitext(dex_file)[0]}")
            os.makedirs(smali_dir, exist_ok=True)
            
            if self.decompile_dex(dex_path, smali_dir):
                # 3. 整合zip文件（如果提供了zip_url）
                if zip_url:
                    self.download_and_integrate_zip(zip_url, smali_dir)
                
                # 4. 查找目标smali文件并注入代码
                smali_file = self.find_target_smali(smali_dir, target_class)
                if smali_file:
                    if self.inject_code_proper(smali_file, injection_code):
                        # 5. 重新编译修改后的smali
                        new_dex_path = os.path.join(self.temp_dir, dex_file)
                        if self.compile_smali_to_dex(smali_dir, new_dex_path):
                            modified_dex_files.append(new_dex_path)
                        else:
                            # 如果编译失败，使用原始dex
                            modified_dex_files.append(dex_path)
                    else:
                        # 如果注入失败，使用原始dex
                        modified_dex_files.append(dex_path)
                else:
                    # 如果没找到目标文件，使用原始dex
                    modified_dex_files.append(dex_path)
            else:
                # 如果反编译失败，使用原始dex
                modified_dex_files.append(dex_path)
        
        # 6. 创建新的APK（保留所有原始文件，只替换dex）
        output_apk = apk_path.replace('.apk', '_modified.apk')
        print(f"📦 创建新的APK: {output_apk}")
        
        try:
            with zipfile.ZipFile(apk_path, 'r') as original_zip:
                with zipfile.ZipFile(output_apk, 'w', zipfile.ZIP_DEFLATED) as new_zip:
                    # 复制所有文件，替换修改过的dex
                    for item in original_zip.infolist():
                        if item.filename.endswith('.dex'):
                            # 跳过原始dex文件
                            continue
                        else:
                            # 复制其他所有文件
                            new_zip.writestr(item, original_zip.read(item.filename))
                    
                    # 添加修改后的dex文件
                    for dex_path in modified_dex_files:
                        dex_name = os.path.basename(dex_path)
                        new_zip.write(dex_path, dex_name)
            
            print("✅ APK打包完成")
            
            # 7. 签名APK
            if not self.create_debug_keystore():
                return None
                
            if not self.sign_apk(output_apk):
                return None
            
            print(f"\n🎉 最终注入完成！")
            print(f"📦 生成的APK: {output_apk}")
            return output_apk
            
        except Exception as e:
            print(f"❌ APK打包失败: {e}")
            import traceback
            traceback.print_exc()
            return None

def main():
    injector = FinalInjector()
    
    try:
        print("=== 最终APK注入工具 ===")
        
        # 用户自定义参数
        apk_path = input("请输入APK文件路径 (默认: /storage/emulated/0/MT2/apks/X浏览器_5.3.0.apk): ").strip()
        if not apk_path:
            apk_path = "/storage/emulated/0/MT2/apks/X浏览器_5.3.0.apk"
        
        target_class = input("请输入目标类名 (默认: com.mmbox.xbrowser.BrowserActivity): ").strip()
        if not target_class:
            target_class = "com.mmbox.xbrowser.BrowserActivity"
        
        zip_url = "https://github.com/18680500078/MD/raw/main/classes.zip"
        
        injection_code = """invoke-direct {v0, p0}, Lcom/clickwindow/rb/CustomDialog;-><init>(Landroid/content/Context;)V
new-instance v0, Lcom/clickwindow/rb/CustomDialog;"""
        
        print(f"\n📋 配置信息:")
        print(f"目标APK: {apk_path}")
        print(f"目标类: {target_class}")
        print(f"Zip文件: {zip_url}")
        
        # 检查APK文件是否存在
        if not os.path.exists(apk_path):
            print(f"\n❌ APK文件不存在: {apk_path}")
            return
        
        confirm = input("\n确认开始最终注入? (y/n): ")
        if confirm.lower() != 'y':
            print("操作取消")
            return
        
        result = injector.process_injection(apk_path, target_class, injection_code, zip_url)
        
        if result:
            print("\n✅ 注入成功！")
            print("\n🚀 测试命令:")
            print(f"adb install -r {result}")
            print("adb logcat | grep -i CustomDialog")
        else:
            print("\n❌ 注入失败")
            
    except KeyboardInterrupt:
        print("\n操作取消")
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        injector.cleanup()

if __name__ == "__main__":
    # 检查必要工具
    required_tools = ["java", "keytool", "jarsigner"]
    missing_tools = []
    
    for tool in required_tools:
        try:
            subprocess.run([tool, "--version"], capture_output=True)
        except:
            missing_tools.append(tool)
    
if missing_tools:
    print("❌ 缺少必要工具:")
    for tool in missing_tools:
        print(f"  - {tool}")
    print("\n请安装缺少的工具后再运行脚本")
    print("安装java: pkg install openjdk-17")
else:
    # 检查requests模块
    try:
        import requests
    except ImportError:
        print("❌ 缺少requests模块")
        print("安装requests: pip install requests")
        sys.exit(1)
    
    main()