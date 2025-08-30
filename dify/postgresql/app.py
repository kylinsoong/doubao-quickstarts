import psycopg2
import os
from psycopg2 import OperationalError, Error

def create_connection(db_name, db_user, db_password, db_host, db_port):
    """创建与PostgreSQL数据库的连接"""
    connection = None
    try:
        print("\n[INFO] 正在测试数据库连接...")
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("[SUCCESS] 数据库连接成功")
    except OperationalError as e:
        print(f"[ERROR] 数据库连接失败: {e}")
    return connection

def execute_query(connection, query, operation_name):
    """执行SQL查询（CREATE, INSERT, UPDATE, DELETE）"""
    cursor = connection.cursor()
    try:
        print(f"\n[INFO] 正在执行: {operation_name}")
        cursor.execute(query)
        connection.commit()
        print(f"[SUCCESS] {operation_name} 执行成功")
    except Error as e:
        print(f"[ERROR] {operation_name} 执行失败: {e}")

def execute_query_with_data(connection, query, data, operation_name):
    """执行带参数的SQL查询"""
    cursor = connection.cursor()
    try:
        print(f"\n[INFO] 正在执行: {operation_name}")
        cursor.execute(query, data)
        connection.commit()
        print(f"[SUCCESS] {operation_name} 执行成功")
    except Error as e:
        print(f"[ERROR] {operation_name} 执行失败: {e}")

def execute_read_query(connection, query, operation_name, data=None):
    """执行查询并返回结果（SELECT）"""
    cursor = connection.cursor()
    result = None
    try:
        print(f"\n[INFO] 正在执行: {operation_name}")
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        print(f"[SUCCESS] {operation_name} 执行成功")
        return result
    except Error as e:
        print(f"[ERROR] {operation_name} 执行失败: {e}")
        return None

def main():
    print("="*50)
    print("=== 开始PostgreSQL初始化测试 ===")
    print("="*50)

    # 从环境变量加载数据库连接参数
    try:
        print("\n[INFO] 正在加载数据库配置...")
        db_config = {
            "db_name": os.environ["DB_DATABASE"],
            "db_user": os.environ["DB_USERNAME"],
            "db_password": os.environ["DB_PASSWORD"],
            "db_host": os.environ["DB_HOST"],
            "db_port": os.environ.get("DB_PORT", "5432")
        }
        print("[SUCCESS] 数据库配置加载完成")
        print(f"[INFO] 连接信息: {db_config['db_host']}:{db_config['db_port']} 数据库: {db_config['db_name']}")
    except KeyError as e:
        print(f"[ERROR] 缺少必要的环境变量: {e}")
        print("[INFO]  required environment variables: DB_DATABASE, DB_USERNAME, DB_PASSWORD, DB_HOST (DB_PORT optional)")
        print("\n=== 初始化测试失败 ===")
        return

    # 1. 测试数据库连接
    connection = create_connection(**db_config)
    if not connection:
        print("\n[FATAL] 无法建立数据库连接，测试终止")
        print("\n=== 初始化测试失败 ===")
        return

    try:
        # 2. 测试创建表
        create_table_query = """
        CREATE TABLE IF NOT EXISTS test_table (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            age INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        execute_query(connection, create_table_query, "创建测试表")

        # 3. 测试插入数据
        insert_query = """
        INSERT INTO test_table (name, email, age)
        VALUES (%s, %s, %s);
        """
        test_data = ("Test User", "test@example.com", 30)
        execute_query_with_data(connection, insert_query, test_data, "插入测试数据")

        # 4. 测试查询数据
        select_query = "SELECT * FROM test_table;"
        records = execute_read_query(connection, select_query, "查询测试数据")
        if records:
            print("[INFO] 查询结果:")
            for record in records:
                print(f"[INFO] 记录: {record}")

        # 5. 测试更新数据
        update_query = """
        UPDATE test_table
        SET age = %s
        WHERE email = %s;
        """
        update_data = (31, "test@example.com")
        execute_query_with_data(connection, update_query, update_data, "更新测试数据")

        # 验证更新结果
        updated_records = execute_read_query(
            connection, 
            "SELECT * FROM test_table WHERE email = %s;", 
            "验证数据更新",
            ("test@example.com",)
        )
        if updated_records:
            print("[INFO] 更新后的数据:")
            print(f"[INFO] {updated_records[0]}")

        # 6. 测试删除数据
        delete_query = "DELETE FROM test_table WHERE email = %s;"
        execute_query_with_data(connection, delete_query, ("test@example.com",), "删除测试数据")

        # 验证删除结果
        remaining_records = execute_read_query(connection, select_query, "验证数据删除")
        print(f"[INFO] 删除后剩余记录数: {len(remaining_records) if remaining_records else 0}")

        # 7. 清理测试表
        drop_table_query = "DROP TABLE IF EXISTS test_table;"
        execute_query(connection, drop_table_query, "清理测试表")

    finally:
        # 关闭数据库连接
        if connection:
            connection.close()
            print("\n[INFO] 数据库连接已关闭")

    print("\n" + "="*50)
    print("=== PostgreSQL初始化测试完成 ===")
    print("="*50)

if __name__ == "__main__":
    main()
    
