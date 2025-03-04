from stock_open_api.api.sse import sh_stock

if __name__ == '__main__':
    print(sh_stock.get_company_info('600016'))
