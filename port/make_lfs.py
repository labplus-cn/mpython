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

    print("\n" + "="*60)
    print(" [错误] 无法生成 VFS 映像！")
    print(" Python 环境中缺少 littlefs-python 库，或者未安装在当前使用的 Python 中。")
    print(" 请运行以下命令将其安装到当前执行 make 的 Python 环境中：")
    print("     python -m pip install littlefs-python")
    print("="*60 + "\n")
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python make_lfs.py <source_dir> <output_bin> <total_size_bytes>")
        sys.exit(1)
    make_lfs(sys.argv[1], sys.argv[2], int(sys.argv[3]))
