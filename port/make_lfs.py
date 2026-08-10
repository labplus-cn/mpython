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
            
            # 部分版本的 mkfatfs 在成功生成映像后可能会返回非 0 状态码
            # 因此我们以“输出文件是否存在且大小正确”作为最终的成功判定标准
            if os.path.exists(output_bin) and os.path.getsize(output_bin) == total_size:
                if result.returncode != 0:
                    print("[make_lfs] mkfatfs 成功生成映像 (警告: 返回码为 %d): %s" % (result.returncode, output_bin))
                else:
                    print("[make_lfs] 成功使用 mkfatfs 生成映像: %s" % output_bin)
                return True
            else:
                print("[make_lfs] mkfatfs 执行失败！返回码: %d" % result.returncode)
                print("[make_lfs] mkfatfs stdout: %s" % result.stdout.decode())
                print("[make_lfs] mkfatfs stderr: %s" % result.stderr.decode())
        else:
            print("[make_lfs] 未找到 tools/mkfatfs 工具。")
    except Exception as e:
        print("[make_lfs] 运行 mkfatfs 失败:", e)

    print("\n" + "="*60)
    print(" [错误] 无法使用 mkfatfs 生成 VFS 映像！")
    print(" 请检查 tools/mkfatfs 是否存在，或者检查执行日志。")
    print("="*60 + "\n")
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python make_lfs.py <source_dir> <output_bin> <total_size_bytes>")
        sys.exit(1)
    make_lfs(sys.argv[1], sys.argv[2], int(sys.argv[3]))
