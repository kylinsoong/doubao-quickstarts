from tldextract import extract

def extract_second_level_domain(url):
    parsed = extract(url)
    return f"{parsed.domain}.{parsed.suffix}" if parsed.domain and parsed.suffix else None

# 示例URL（输入中的长URL）
urls = [
    "https://m.xiaohe.cn/medical/qa/70000001724645?enter_position=qa_xiaohe_searchcard&host_aid=13&search_id=021748831637886fdbddc03000f020a1740e53bea0000def5fbfd&search_result_id=&token_type=toutiao_web",
    "https://feedcoop.douyin.com/d7412725594255475251/?biz_log=B29K1xjjUs2ekKakxH7TMbX3uF4A2rWijeWFLZdiJc4rXPFSbXMZ9Ht2iHnPTu4XSoDLryhQCucJDxpBCxH7VouGVCB8hzU2Mj4HH4rbYjd6avK8rxgjLakPbFiuKSqffcXFrZpPS1KCVzLBqJWvkRTLbGXhX7VsuygL6zFiZVz6gev4YShEBCuEzSSnG9p&group_id=7412725594255475251&label=torchlight&platform_source=1&utm_source=content_plugin_gztvx3gc_default_content",
    "https://open.toutiao.com/a7347960671482577444/?biz_log=B29K1xjjUs2ekKakxH7TMbX3uF4A2rWijeWFLZdiJc4rXPFSbXMZ9Ht2iHnPTu4XSoDLryhQCucJDxpBCxH7VonsaoewpgEZB361B462bXobDmMbZYTJKkPgeduHn2N5QF5QQcEtFfXmMQPMCBA9iziKvXf9b9hpCzyoPKPFmf2GKaz2Bg7S767sz2wMhh4&group_id=7347960671482577444&label=torchlight&utm_source=content_plugin_gztvx3gc_default_content"
]

# 提取二级域名
for url in urls:
    second_level_domain = extract_second_level_domain(url)
    print(f"URL: {url}\n二级域名: {second_level_domain}\n")
