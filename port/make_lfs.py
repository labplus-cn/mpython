# Tool to generate LittleFS v2 partition image for MicroPython
import os
import sys
import subprocess

def make_lfs(source_dir, output_bin, total_size):
    block_size = 4096
    page_size = 256
    
    # 1. 首先尝试调用定制版 mkfatfs 命令行工具 (支持 -t littlefs)
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        mkfatfs_bin = os.path.join(script_dir, "tools", "mkfatfs")
        
        # 兼容 Windows 系统的 .exe
        if not os.path.exists(mkfatfs_bin) and os.path.exists(mkfatfs_bin + ".exe"):
            mkfatfs_bin += ".exe"

        if os.path.exists(mkfatfs_bin):
            print("[make_lfs] 正在使用定制工具: %s..." % mkfatfs_bin)
            cmd = [
                mkfatfs_bin,
                "-c", source_dir if os.path.exists(source_dir) else ".",
                "-s", hex(total_size),
                "-t", "littlefs",
                "-d", "5",
                output_bin
            ]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                print("[make_lfs] 成功使用 mkfatfs 生成映像: %s" % output_bin)
                return True
            else:
                print("[make_lfs] mkfatfs 报错返回码: %d" % result.returncode)
                print("[make_lfs] mkfatfs stdout: %s" % result.stdout.decode())
                print("[make_lfs] mkfatfs stderr: %s" % result.stderr.decode())
        else:
            print("[make_lfs] 未找到 tools/mkfatfs 工具。")
    except Exception as e:
        print("[make_lfs] 运行 mkfatfs 失败:", e)

    # 2. 如果 mkfatfs 失败，尝试使用 littlefs-python 包
    try:
        from littlefs import LittleFS
        print("[make_lfs] 正在使用 Python littlefs 包生成 LittleFS 映像...")
        
        # 创建内存中的 LittleFS 对象
        lfs = LittleFS(block_size=block_size, block_count=total_size // block_size, prog_size=page_size, read_size=page_size)
        
        def add_dir(path, lfs_path):
            if lfs_path != "/":
                lfs.mkdir(lfs_path)
            for entry in os.scandir(path):
                rel_path = os.path.join(lfs_path, entry.name).replace("\\", "/")
                if entry.is_dir():
                    add_dir(entry.path, rel_path)
                elif entry.is_file():
                    with open(entry.path, 'rb') as f:
                        data = f.read()
                    with lfs.open(rel_path, 'wb') as lf:
                        lf.write(data)
                        
        if os.path.exists(source_dir):
            add_dir(source_dir, "/")
        
        with open(output_bin, 'wb') as f:
            f.write(lfs.context.buffer)
        print("[make_lfs] 成功生成 LFS 映像: %s" % output_bin)
        return True
    except ImportError:
        pass

    print("\n" + "="*60)
    print(" [错误] 无法生成 VFS 映像！")
    print(" 未找到定制的 mkfatfs 工具，且 Python 环境缺少 littlefs-python。")
    print(" 请运行以下命令将其安装到当前执行 make 的 Python 环境中：")
    print("     python -m pip install littlefs-python")
    print("="*60 + "\n")
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python make_lfs.py <source_dir> <output_bin> <total_size_bytes>")
        sys.exit(1)
    make_lfs(sys.argv[1], sys.argv[2], int(sys.argv[3]))
