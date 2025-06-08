import pandas as pd
from datetime import datetime
import random
import string

def generate_product_code(existing_codes=None):
    """生成8位唯一产品代码"""
    if existing_codes is None:
        existing_codes = set()
    
    while True:
        code = ''.join(random.choices(string.digits, k=8))
        if code not in existing_codes:
            existing_codes.add(code)
            return code

def add_product_codes(products):
    """为产品列表添加唯一产品代码"""
    existing_codes = set()
    for product in products:
        product['代码'] = generate_product_code(existing_codes)
    return products

def export_to_excel(products, filename=None):
    """将理财产品数据导出到Excel文件"""
    if not filename:
        filename = f"理财产品_{datetime.now().strftime('%Y%m%d')}.xlsx"
    
    try:
        # 确保产品有代码
        products_with_code = add_product_codes(products.copy())
        
        # 转换数据为DataFrame
        df = pd.DataFrame(products_with_code)
        
        # 重命名列名，增加可读性
        df.columns = ['产品代码', '产品名称', '风险类型', '历史年化收益', '产品描述']
        
        # 调整列顺序
        df = df[['产品代码', '产品名称', '风险类型', '历史年化收益', '产品描述']]
        
        # 创建Excel写入器，使用xlsxwriter引擎
        with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
            # 写入数据
            df.to_excel(writer, sheet_name='理财产品列表', index=False)
            
            # 获取工作簿和工作表对象以进行格式设置
            workbook = writer.book
            worksheet = writer.sheets['理财产品列表']
            
            # 设置列宽
            for i, col in enumerate(df.columns):
                column_width = max(len(str(x)) for x in df[col])
                column_width = max(column_width, len(col)) + 2
                worksheet.set_column(i, i, column_width)
            
            # 添加标题行格式
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#D7E4BC',
                'border': 1
            })
            
            # 应用标题行格式
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
                
            # 添加数据行格式
            data_format = workbook.add_format({
                'border': 1,
                'text_wrap': True
            })
            
            # 应用数据行格式
            for row_num in range(1, len(df) + 1):
                for col_num in range(len(df.columns)):
                    worksheet.write(row_num, col_num, df.iloc[row_num-1, col_num], data_format)
            
            # 添加冻结窗格
            worksheet.freeze_panes(1, 0)
            
            # 添加筛选器
            worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)
            
            # 添加收益列的条件格式（绿色表示高收益）
            worksheet.conditional_format(
                f'D2:D{len(df)+1}',
                {
                    'type': 'cell',
                    'criteria': '>=',
                    'value': '0.15',
                    'format': workbook.add_format({'bg_color': '#C6EFCE'})
                }
            )
            
            # 添加产品代码列的条件格式（浅蓝色背景）
            worksheet.conditional_format(
                f'A2:A{len(df)+1}',
                {
                    'type': 'no_errors',
                    'format': workbook.add_format({'bg_color': '#E5F6FF'})
                }
            )
            
            # 添加进度提示
            print(f"已成功导出 {len(df)} 条理财产品数据到 {filename}")
            
    except Exception as e:
        print(f"导出Excel时出错: {e}")
        return False
    return True

# 示例数据
products = [
    {"名称":"成长精选股票型基金","类型":"高风险","历史收益":"年化18.2%","描述":"聚焦科技与消费领域成长股，适合长期投资"},
    {"名称":"价值蓝筹混合型基金","类型":"中高风险","历史收益":"年化12.5%","描述":"投资大型蓝筹股，兼顾价值与成长"},
    {"名称":"新能源主题股票基金","类型":"高风险","历史收益":"年化21.8%","描述":"专注新能源产业链，契合政策导向"},
    {"名称":"消费升级股票型产品","类型":"中高风险","历史收益":"年化15.3%","描述":"布局消费升级趋势，抗周期能力较强"},
    {"名称":"量化对冲混合型基金","类型":"中风险","历史收益":"年化8.7%","描述":"运用量化策略，对冲市场波动风险"},
    {"名称":"港股通精选股票基金","类型":"高风险","历史收益":"年化16.4%","描述":"投资香港市场优质标的，分散A股风险"},
    {"名称":"医药健康行业基金","类型":"中高风险","历史收益":"年化14.9%","描述":"布局医药创新与健康消费领域"},
    {"名称":"红利低波股票组合","类型":"中风险","历史收益":"年化9.8%","描述":"选取高股息、低波动股票，追求稳定收益"},
    {"名称":"科技创新ETF联接基金","类型":"高风险","历史收益":"年化19.3%","描述":"跟踪科技指数，分享科技创新红利"},
    {"名称":"均衡配置混合型产品","类型":"中风险","历史收益":"年化11.2%","描述":"股债平衡配置，追求稳健增值"}
]

# 导出数据
if __name__ == "__main__":
    export_to_excel(products)    
