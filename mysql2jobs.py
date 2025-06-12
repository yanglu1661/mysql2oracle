#!/usr/bin/python3
import pymysql
import json
import configparser
import os

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')  # 修改配置文件名

# 从配置文件中获取 MySQL 连接信息
mysql_config = {
    "dbname": config.get("mysql", "dbname").strip(),
    "user": config.get("mysql", "user").strip(),
    "password": config.get("mysql", "password").strip(),
    "host": config.get("mysql", "host").strip(),
    "port": config.get("mysql", "port").strip()
}

# 从配置文件中获取 Oracle 连接信息
oracle_config = {
    "username": config.get("oracledb", "username").strip(),
    "password": config.get("oracledb", "password").strip(),
    "host": config.get("oracledb", "host").strip(),
    "port": config.get("oracledb", "port").strip(),
    "service_name": config.get("oracledb", "service_name").strip()
}

# 构建 Oracle JDBC URL
oracle_config["jdbcUrl"] = f"jdbc:oracle:thin:@{oracle_config['host']}:{oracle_config['port']}/{oracle_config['service_name']}"

# 从配置文件中获取 DataX 相关目录
jobs_dir = config.get("datax", "datax_jobs_dir").strip()
logs_dir = config.get("datax", "datax_logs_dir").strip()
datax_home = config.get("datax", "datax_home").strip()

# 确保 jobs_dir 存在
if not os.path.exists(jobs_dir):
    os.makedirs(jobs_dir)

# 连接到 MySQL 数据库
conn = pymysql.connect(
    host=mysql_config["host"],
    user=mysql_config["user"],
    password=mysql_config["password"],
    database=mysql_config["dbname"],
    port=int(mysql_config["port"]),
    charset='utf8mb4'
)

# 获取所有表名（排除视图）
cursor = conn.cursor()
cursor.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = %s 
    AND table_type = 'BASE TABLE'
""", (mysql_config["dbname"],))
tables = cursor.fetchall()

# 获取每个表的列信息
def get_table_columns(table_name):
    cursor.execute(f"SHOW COLUMNS FROM `{table_name}`")
    columns = cursor.fetchall()
    return [column[0] for column in columns]

for table in tables:
    table_name = table[0]

    # 获取当前表的列信息
    columns = get_table_columns(table_name)

    # 为每个表生成一个 DataX 配置
    datax_config = {
        "job": {
            "content": [{
                "reader": {
                    "name": "mysqlreader",
                    "parameter": {
                        "username": mysql_config["user"],
                        "password": mysql_config["password"],
                        "column": columns,  # 动态获取列信息
                        "connection": [
                            {
                                "jdbcUrl": [f"jdbc:mysql://{mysql_config['host']}:{mysql_config['port']}/{mysql_config['dbname']}?useSSL=false"],
                                "table": [table_name]
                            }
                        ],
                    }
                },
                "writer": {
                    "name": "oraclewriter",
                    "parameter": {
                        "username": oracle_config["username"],
                        "password": oracle_config["password"],
                        "column": columns,  # 动态获取列信息
                        "connection": [
                            {
                                "jdbcUrl": oracle_config["jdbcUrl"],
                                "table": [f"{table_name}"]
                            }
                        ],
                    }
                }
            }],
            "setting": {
                "speed": {
                    "channel": 5  # 根据需要调整并发数
                }
            }
        }
    }

    # 输出配置到文件，文件名与表名相同
    with open(f'{jobs_dir}/{table_name}.json', 'w') as f:
        json.dump(datax_config, f, indent=4)

# 关闭数据库连接
cursor.close()
conn.close()
