from runtime import Args
from typings.file_upload.file_upload import Input, Output

"""
Each file needs to export a function named `handler`. This function is the entrance to the Tool.

Parameters:
args: parameters of the entry function.
args.input - input parameters, you can get test input value by args.input.xxx.
args.logger - logger instance used to print logs, injected by runtime.

Remember to fill in input/output in Metadata, it helps LLM to recognize and use tool.

Return:
The return data of the function, which should match the declared output parameters.
"""
def handler(args: Args[Input])->Output:

    urls = args.input.urls

    message = []
    pdf = {
        "type": "pdf",
        "value": ["document1.pdf", "report2.pdf", "invoice3.pdf"]
    }
    message.append(pdf)
    doc = {
       "type": "doc",
       "value": ["file1.docx", "notes2.docx", "summary3.docx"]
    }
    message.append(doc)
    excel = {
        "type": "excel",
        "value": ["data1.xlsx", "budget2.xlsx", "schedule3.xlsx"]
    }
    message.append(excel)
    jpg = {
        "type": "jpg",
        "value": ["image1.jpg", "photo2.jpg", "banner3.jpg"]
    }
    message.append(jpg)
    return {"message": message}
