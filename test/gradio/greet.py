import gradio as gr

def greet(input):
    return "Hello " + input + "!"

demo = gr.Interface(
    fn=greet,
    inputs="text",
    outputs="text"
)

demo.launch()

