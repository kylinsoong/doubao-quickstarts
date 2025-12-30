// 绩效评估应用的核心JavaScript代码

// 全局变量
let employees = [];
const API_BASE_URL = '/api/employees';

// DOM元素
const tableBody = document.getElementById('tableBody');
const addEmployeeBtn = document.getElementById('addEmployeeBtn');
const exportBtn = document.getElementById('exportBtn');
const searchInput = document.getElementById('searchInput');
const departmentFilter = document.getElementById('departmentFilter');
const performanceFilter = document.getElementById('performanceFilter');
const employeeModal = document.getElementById('employeeModal');
const closeBtn = document.querySelector('.close');
const employeeForm = document.getElementById('employeeForm');
const modalTitle = document.getElementById('modalTitle');
const cancelBtn = document.getElementById('cancelBtn');

// 页面加载完成后初始化
window.addEventListener('DOMContentLoaded', () => {
    initApp();
});

// 初始化应用
async function initApp() {
    // 从API加载数据
    await loadEmployees();
    
    // 渲染表格
    renderTable();
    
    // 绑定事件
    bindEvents();
}

// 绑定事件
function bindEvents() {
    // 按钮事件
    addEmployeeBtn.addEventListener('click', openAddModal);
    exportBtn.addEventListener('click', exportData);
    
    // 搜索和过滤事件
    searchInput.addEventListener('input', handleSearch);
    departmentFilter.addEventListener('change', handleFilter);
    performanceFilter.addEventListener('change', handleFilter);
    
    // 模态框事件
    closeBtn.addEventListener('click', closeModal);
    cancelBtn.addEventListener('click', closeModal);
    window.addEventListener('click', (e) => {
        if (e.target === employeeModal) {
            closeModal();
        }
    });
    
    // 表单事件
    employeeForm.addEventListener('submit', handleFormSubmit);
}

// 加载员工数据
async function loadEmployees() {
    try {
        const response = await fetch(API_BASE_URL);
        if (response.ok) {
            employees = await response.json();
        } else {
            console.error('Failed to load employees:', response.status);
            // 如果API调用失败，使用模拟数据
            employees = getMockData();
        }
    } catch (error) {
        console.error('Error loading employees:', error);
        // 如果发生网络错误，使用模拟数据
        employees = getMockData();
    }
}

// 保存员工数据到数据库的功能已移至后端API

// 获取模拟数据
function getMockData() {
    return [
        {
            id: 1,
            name: '张三',
            department: '技术部',
            position: '高级工程师',
            yearsOfService: 5,
            performanceScore: 92,
            performanceLevel: '优秀',
            evaluationDate: '2024-06-15'
        },
        {
            id: 2,
            name: '李四',
            department: '市场部',
            position: '市场经理',
            yearsOfService: 3,
            performanceScore: 85,
            performanceLevel: '良好',
            evaluationDate: '2024-06-15'
        },
        {
            id: 3,
            name: '王五',
            department: '销售部',
            position: '销售代表',
            yearsOfService: 2,
            performanceScore: 78,
            performanceLevel: '合格',
            evaluationDate: '2024-06-15'
        },
        {
            id: 4,
            name: '赵六',
            department: '人力资源部',
            position: 'HR专员',
            yearsOfService: 4,
            performanceScore: 90,
            performanceLevel: '优秀',
            evaluationDate: '2024-06-15'
        },
        {
            id: 5,
            name: '钱七',
            department: '财务部',
            position: '会计',
            yearsOfService: 3,
            performanceScore: 75,
            performanceLevel: '合格',
            evaluationDate: '2024-06-15'
        },
        {
            id: 6,
            name: '孙八',
            department: '技术部',
            position: '工程师',
            yearsOfService: 2,
            performanceScore: 68,
            performanceLevel: '待改进',
            evaluationDate: '2024-06-15'
        },
        {
            id: 7,
            name: '周九',
            department: '技术部',
            position: '测试工程师',
            yearsOfService: 3,
            performanceScore: 88,
            performanceLevel: '良好',
            evaluationDate: '2024-06-15'
        },
        {
            id: 8,
            name: '吴十',
            department: '市场部',
            position: '市场专员',
            yearsOfService: 1,
            performanceScore: 82,
            performanceLevel: '良好',
            evaluationDate: '2024-06-15'
        }
    ];
}

// 渲染表格
function renderTable(filteredEmployees = null) {
    const dataToRender = filteredEmployees || employees;
    
    tableBody.innerHTML = '';
    
    dataToRender.forEach(employee => {
        const row = createTableRow(employee);
        tableBody.appendChild(row);
    });
}

// 创建表格行
function createTableRow(employee) {
    const row = document.createElement('tr');
    
    row.innerHTML = `
        <td>${employee.id}</td>
        <td>${employee.name}</td>
        <td>${employee.department}</td>
        <td>${employee.position}</td>
        <td>${employee.yearsOfService}</td>
        <td>${employee.performanceScore}</td>
        <td><span class="performance-level ${getLevelClass(employee.performanceLevel)}">${employee.performanceLevel}</span></td>
        <td>${employee.evaluationDate}</td>
        <td>
            <button class="btn btn-edit" onclick="openEditModal(${employee.id})">编辑</button>
            <button class="btn btn-delete" onclick="deleteEmployee(${employee.id})">删除</button>
        </td>
    `;
    
    return row;
}

// 获取绩效等级对应的CSS类名
function getLevelClass(level) {
    switch (level) {
        case '优秀':
            return 'excellent';
        case '良好':
            return 'good';
        case '合格':
            return 'qualified';
        case '待改进':
            return 'needs-improvement';
        default:
            return '';
    }
}

// 打开添加员工模态框
function openAddModal() {
    modalTitle.textContent = '添加员工';
    employeeForm.reset();
    document.getElementById('employeeId').value = '';
    employeeModal.style.display = 'block';
}

// 打开编辑员工模态框
function openEditModal(id) {
    const employee = employees.find(emp => emp.id === id);
    if (!employee) return;
    
    modalTitle.textContent = '编辑员工';
    document.getElementById('employeeId').value = employee.id;
    document.getElementById('name').value = employee.name;
    document.getElementById('department').value = employee.department;
    document.getElementById('position').value = employee.position;
    document.getElementById('yearsOfService').value = employee.yearsOfService;
    document.getElementById('performanceScore').value = employee.performanceScore;
    document.getElementById('evaluationDate').value = employee.evaluationDate;
    
    employeeModal.style.display = 'block';
}

// 关闭模态框
function closeModal() {
    employeeModal.style.display = 'none';
    employeeForm.reset();
}

// 处理表单提交
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const id = parseInt(document.getElementById('employeeId').value);
    const name = document.getElementById('name').value;
    const department = document.getElementById('department').value;
    const position = document.getElementById('position').value;
    const yearsOfService = parseInt(document.getElementById('yearsOfService').value);
    const performanceScore = parseFloat(document.getElementById('performanceScore').value);
    const evaluationDate = document.getElementById('evaluationDate').value;
    
    // 计算绩效等级
    const performanceLevel = calculatePerformanceLevel(performanceScore);
    
    const employeeData = {
        name,
        department,
        position,
        yearsOfService,
        performanceScore,
        performanceLevel,
        evaluationDate
    };
    
    try {
        if (id) {
            // 更新现有员工
            await updateEmployee(id, employeeData);
        } else {
            // 添加新员工
            await addEmployee(employeeData);
        }
        
        closeModal();
        await loadEmployees(); // 重新加载数据
        renderTable();
    } catch (error) {
        console.error('Error saving employee:', error);
        alert('保存员工数据失败，请稍后重试。');
    }
}

// 添加员工
async function addEmployee(employeeData) {
    try {
        const response = await fetch(API_BASE_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(employeeData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to add employee');
        }
        
        const newEmployee = await response.json();
        employees.push(newEmployee);
    } catch (error) {
        console.error('Error adding employee:', error);
        throw error;
    }
}

// 更新员工
async function updateEmployee(id, employeeData) {
    try {
        const response = await fetch(`${API_BASE_URL}/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(employeeData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to update employee');
        }
        
        const updatedEmployee = await response.json();
        const index = employees.findIndex(emp => emp.id === id);
        if (index !== -1) {
            employees[index] = updatedEmployee;
        }
    } catch (error) {
        console.error('Error updating employee:', error);
        throw error;
    }
}

// 删除员工
async function deleteEmployee(id) {
    if (confirm('确定要删除这个员工的绩效记录吗？')) {
        try {
            const response = await fetch(`${API_BASE_URL}/${id}`, {
                method: 'DELETE'
            });
            
            if (!response.ok) {
                throw new Error('Failed to delete employee');
            }
            
            // 从本地数组中移除
            employees = employees.filter(emp => emp.id !== id);
            renderTable();
        } catch (error) {
            console.error('Error deleting employee:', error);
            alert('删除员工数据失败，请稍后重试。');
        }
    }
}

// 计算绩效等级
function calculatePerformanceLevel(score) {
    if (score >= 90) {
        return '优秀';
    } else if (score >= 80) {
        return '良好';
    } else if (score >= 70) {
        return '合格';
    } else {
        return '待改进';
    }
}

// 处理搜索
function handleSearch() {
    const searchTerm = searchInput.value.toLowerCase();
    const filtered = filterEmployees(searchTerm);
    renderTable(filtered);
}

// 处理过滤
function handleFilter() {
    const searchTerm = searchInput.value.toLowerCase();
    const filtered = filterEmployees(searchTerm);
    renderTable(filtered);
}

// 过滤员工数据
function filterEmployees(searchTerm = '') {
    return employees.filter(employee => {
        // 搜索过滤
        const matchesSearch = !searchTerm || 
            employee.name.toLowerCase().includes(searchTerm) || 
            employee.department.toLowerCase().includes(searchTerm);
        
        // 部门过滤
        const matchesDepartment = !departmentFilter.value || 
            employee.department === departmentFilter.value;
        
        // 绩效等级过滤
        const matchesPerformance = !performanceFilter.value || 
            employee.performanceLevel === performanceFilter.value;
        
        return matchesSearch && matchesDepartment && matchesPerformance;
    });
}

// 导出数据
function exportData() {
    if (employees.length === 0) {
        alert('没有数据可以导出！');
        return;
    }
    
    // 转换为CSV格式
    const csvContent = convertToCSV(employees);
    
    // 创建下载链接
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    
    if (link.download !== undefined) {
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', `绩效评估数据_${new Date().toISOString().slice(0, 10)}.csv`);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

// 转换为CSV格式
function convertToCSV(data) {
    const headers = ['员工ID', '姓名', '部门', '职位', '工作年限', '绩效评分', '绩效等级', '评估日期'];
    const csv = [headers.join(',')];
    
    data.forEach(employee => {
        const row = [
            employee.id,
            `"${employee.name}"`,
            `"${employee.department}"`,
            `"${employee.position}"`,
            employee.yearsOfService,
            employee.performanceScore,
            `"${employee.performanceLevel}"`,
            employee.evaluationDate
        ];
        csv.push(row.join(','));
    });
    
    return csv.join('\n');
}

// 确保函数在全局作用域可用
window.openEditModal = openEditModal;
window.deleteEmployee = deleteEmployee;