
def load_file_content(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

content = load_file_content("prompt.caption.syn.check.ini")

print(type(content))
