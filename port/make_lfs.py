# Tool to generate LittleFS v2 partition image for MicroPython
import os
import sys
import subprocess

def make_lfs(source_dir, output_bin, total_size):
    block_size = 4096
    page_size = 256
    
    # 1. 尝试使用 littlefs-python 包 (如果用户环境已通过 pip install littlefs-python 安装)
    try:
        from littlefs import LittleFS
        print("[make_lfs] 正在使用 Python littlefs 包生成 LittleFS v2 映像...")
        
        # 创建内存中的 LittleFS 对象
        lfs = LittleFS(block_size=block_size, block_count=total_size // block_size, page_size=page_size)
        
        # 递归写入文件
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
        
        # 写入生成的二进制文件
        with open(output_bin, 'wb') as f:
            f.write(lfs.context.buffer)
        print("[make_lfs] 成功生成 LFS 映像: %s" % output_bin)
        return True
    except ImportError:
        pass

    # 2. 尝试调用系统的 mklittlefs 命令行工具
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        mklittlefs_bin = os.path.join(script_dir, "tools", "mklittlefs", "mklittlefs")
        if not os.path.exists(mklittlefs_bin):
            mklittlefs_bin = "mklittlefs"  # 找不到则降级回系统 PATH 中的工具
            print("[make_lfs] 未检测到内置工具，尝试调用系统 PATH 中的 mklittlefs...")
        else:
            print("[make_lfs] 正在使用内置工具: %s..." % mklittlefs_bin)
            
        cmd = [
            mklittlefs_bin,
            "-c", source_dir if os.path.exists(source_dir) else ".", # 若源目录不存在则打包当前空文件夹
            "-p", str(page_size),
            "-b", str(block_size),
            "-s", str(total_size),
            output_bin
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print("[make_lfs] 成功使用 %s 生成映像: %s" % (os.path.basename(mklittlefs_bin), output_bin))
            return True
        else:
            print("[make_lfs] %s 报错: %s" % (os.path.basename(mklittlefs_bin), result.stderr.decode()))
    except FileNotFoundError:
        print("[make_lfs] 找不到 mklittlefs 工具。")
        
    print("\n[错误] 无法生成 VFS 映像！")
    print("请安装以下任意一种工具以继续编译：")
    print("1. 安装 Python 包（推荐）：pip install littlefs-python")
    print("2. 安装系统工具：下载 mklittlefs 二进制文件并加入 PATH 环境变量。")
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python make_lfs.py <source_dir> <output_bin> <total_size_bytes>")
        sys.exit(1)
    make_lfs(sys.argv[1], sys.argv[2], int(sys.argv[3]))
