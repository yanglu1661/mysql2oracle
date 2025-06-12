#!/usr/bin/python3
import os
import argparse
import configparser
import oracledb

# 解析命令行参数
parser = argparse.ArgumentParser(description="导入 Oracle DDL 文件")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--ddl', action='store_true', help='仅导入非 foreign_keys 的 DDL 文件')
group.add_argument('--foreign-keys', action='store_true', help='仅导入 foreign_keys 的 DDL 文件')
args = parser.parse_args()

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

oracle_conf = config['oracledb']
username = oracle_conf.get('username').strip()
password = oracle_conf.get('password').strip()
host = oracle_conf.get('host').strip()
port = oracle_conf.get('port').strip()
service_name = oracle_conf.get('service_name').strip()

# 构建 Oracle 连接
try:
    conn = oracledb.connect(user=username, password=password, dsn=f"{host}:{port}/{service_name}")
    print("✅ 成功连接到 Oracle 数据库")
except oracledb.Error as e:
    print("❌ Oracle 数据库连接失败:", e)
    exit(1)

cursor = conn.cursor()

ddl_dir = 'oracle_schema_ddl'

# 遍历目录，按参数筛选文件
for filename in sorted(os.listdir(ddl_dir)):
    if not filename.endswith('.oracle.sql'):
        continue

    is_fk = 'foreign_keys' in filename

    # 根据参数决定是否处理该文件
    if args.ddl and is_fk:
        continue
    if args.foreign_keys and not is_fk:
        continue

    file_path = os.path.join(ddl_dir, filename)
    print(f"📄 正在导入：{filename}")

    with open(file_path, 'r') as f:
        sql_content = f.read()

    # 按分号拆分 SQL 语句，逐条执行
    statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
    for idx, stmt in enumerate(statements, 1):
        try:
            cursor.execute(stmt)
        except oracledb.DatabaseError as e:
            print(f"❌ 第 {idx} 条 SQL 执行失败 in {filename}:")
            print("   SQL 片段：", stmt[:120].replace('\n', ' '))
            print("   错误信息：", e)


# 提交并关闭连接
conn.commit()
cursor.close()
conn.close()
print("✅ 所有选定的 DDL 导入完成")

