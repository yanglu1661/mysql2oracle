#!/usr/bin/python3
import threading
import subprocess
import os
import sys
import logging
import configparser

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

# 从配置文件中获取 DataX 相关目录
job_dir = config.get("datax", "datax_jobs_dir").strip()
log_dir = config.get("datax", "datax_logs_dir").strip()
datax_home = config.get("datax", "datax_home").strip()
main_log_file = os.path.join(log_dir, "datax_multithread_run.log")

# 自定义线程类，继承 threading.Thread
class DataXJobThread(threading.Thread):
    def __init__(self, file_list, lock, log_dir, main_logger):
        threading.Thread.__init__(self)
        self.file_list = file_list  # 文件列表
        self.lock = lock  # 线程锁
        self.log_dir = log_dir  # 日志文件目录
        self.main_logger = main_logger  # 主日志记录器

    def run(self):
        while True:
            with self.lock:
                if not self.file_list:
                    break  # 如果文件列表为空，退出循环
                file_path = self.file_list.pop(0)  # 取出一个文件
            self.process_file(file_path)  # 处理文件

    def process_file(self, file_path):
        try:
            self.main_logger.info(f"Processing file: {file_path}")
            # 生成日志文件路径
            log_file = os.path.join(self.log_dir, os.path.basename(file_path) + ".log")
            # 使用 subprocess 调用 datax.py 处理文件，并将日志输出到文件
            with open(log_file, "w") as log_f:
                result = subprocess.run(
                    ["python3", os.path.join(datax_home, "bin/datax.py"), file_path],
                    stdout=log_f,
                    stderr=subprocess.STDOUT,  # 将标准错误重定向到标准输出
                    text=True
                )
            # 记录处理结果
            self.main_logger.info(f"Finished processing {file_path}. Log saved to {log_file}")
            if result.returncode != 0:
                self.main_logger.error(f"Error in {file_path}. Check log file: {log_file}")
        except Exception as e:
            self.main_logger.error(f"Failed to process {file_path}: {e}")

# 主函数
def main(job_dir, num_threads, log_dir, main_log_file):
    # 配置主日志记录器
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(main_log_file),  # 输出到主日志文件
            logging.StreamHandler()  # 输出到控制台
        ]
    )
    main_logger = logging.getLogger("main_logger")

    # 获取所有 job 文件
    file_list = [os.path.join(job_dir, f) for f in os.listdir(job_dir) if f.endswith(".json")]
    if not file_list:
        main_logger.info("No job files found in the directory.")
        return

    # 创建日志目录（如果不存在）
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 创建线程锁
    lock = threading.Lock()

    # 创建并启动线程
    threads = []
    for _ in range(num_threads):
        thread = DataXJobThread(file_list, lock, log_dir, main_logger)
        thread.start()
        threads.append(thread)

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    main_logger.info("All files processed.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./datax_multithread_run.py <num_threads>")
        sys.exit(1)

    num_threads = int(sys.argv[1])  # 线程数

    if not os.path.isdir(job_dir):
        print(f"Directory {job_dir} does not exist.")
        sys.exit(1)

    main(job_dir, num_threads, log_dir, main_log_file)


