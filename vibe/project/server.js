// 后端主应用文件
const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const pool = require('./config/db');

// 创建Express应用
const app = express();

// 配置中间件
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// 提供静态文件
app.use(express.static(__dirname));

// API路由

// 获取所有员工
app.get('/api/employees', async (req, res) => {
    try {
        const [rows] = await pool.query('SELECT * FROM employees');
        res.json(rows);
    } catch (error) {
        console.error('Error fetching employees:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// 获取单个员工
app.get('/api/employees/:id', async (req, res) => {
    try {
        const { id } = req.params;
        const [rows] = await pool.query('SELECT * FROM employees WHERE id = ?', [id]);
        if (rows.length === 0) {
            res.status(404).json({ error: 'Employee not found' });
        } else {
            res.json(rows[0]);
        }
    } catch (error) {
        console.error('Error fetching employee:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// 添加员工
app.post('/api/employees', async (req, res) => {
    try {
        const { name, department, position, yearsOfService, performanceScore, performanceLevel, evaluationDate } = req.body;
        const [result] = await pool.query(
            'INSERT INTO employees (name, department, position, yearsOfService, performanceScore, performanceLevel, evaluationDate) VALUES (?, ?, ?, ?, ?, ?, ?)',
            [name, department, position, yearsOfService, performanceScore, performanceLevel, evaluationDate]
        );
        res.json({ id: result.insertId, ...req.body });
    } catch (error) {
        console.error('Error adding employee:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// 更新员工
app.put('/api/employees/:id', async (req, res) => {
    try {
        const { id } = req.params;
        const { name, department, position, yearsOfService, performanceScore, performanceLevel, evaluationDate } = req.body;
        const [result] = await pool.query(
            'UPDATE employees SET name = ?, department = ?, position = ?, yearsOfService = ?, performanceScore = ?, performanceLevel = ?, evaluationDate = ? WHERE id = ?',
            [name, department, position, yearsOfService, performanceScore, performanceLevel, evaluationDate, id]
        );
        if (result.affectedRows === 0) {
            res.status(404).json({ error: 'Employee not found' });
        } else {
            res.json({ id, ...req.body });
        }
    } catch (error) {
        console.error('Error updating employee:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// 删除员工
app.delete('/api/employees/:id', async (req, res) => {
    try {
        const { id } = req.params;
        const [result] = await pool.query('DELETE FROM employees WHERE id = ?', [id]);
        if (result.affectedRows === 0) {
            res.status(404).json({ error: 'Employee not found' });
        } else {
            res.json({ message: 'Employee deleted successfully' });
        }
    } catch (error) {
        console.error('Error deleting employee:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// 启动服务器
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});