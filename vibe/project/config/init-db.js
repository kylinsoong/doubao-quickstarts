// 数据库初始化脚本
const pool = require('./db');

async function initDatabase() {
    try {
        // 创建employees表
        await pool.query(`
            CREATE TABLE IF NOT EXISTS employees (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                department VARCHAR(255) NOT NULL,
                position VARCHAR(255) NOT NULL,
                yearsOfService INT NOT NULL,
                performanceScore DECIMAL(5, 1) NOT NULL,
                performanceLevel VARCHAR(20) NOT NULL,
                evaluationDate DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        `);
        
        console.log('Database initialized successfully');
        
        // 关闭连接池
        await pool.end();
    } catch (error) {
        console.error('Error initializing database:', error);
        process.exit(1);
    }
}

// 执行初始化
initDatabase();