import gradio as gr
from PIL import Image

def invert_image(input_img):
    img = Image.fromarray(input_img.astype('uint8'))
    inverted_img = Image.eval(img, lambda x: 255 - x)
    return inverted_img

demo = gr.Interface(
    fn=invert_image,
    inputs=gr.Image(),
    outputs=gr.Image()
)

demo.launch()
