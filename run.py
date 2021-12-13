import gradio
from pipeline import pipeline

if __name__ == "__main__":
    interface = gradio.Interface(
        fn=pipeline,
        title="Zero-shot Math Problem Solving",
        inputs=[
            gradio.inputs.Textbox(lines=1, placeholder="xx-xxxxxxxxxxxxxxxxx", default="", label="apikey"),
            gradio.inputs.Textbox(lines=1, placeholder="Two trains leave San Rafael at the same time. They begin traveling westward, both traveling for 80 miles. The next day, they travel northwards, covering 150 miles. What's the distance covered by each train in the two days?", default="", label="problem"),
            gradio.inputs.Radio(["Codex", "GPT-3"], default="Codex", label="model"),
            gradio.inputs.Slider(minimum=0, maximum=1, step=0.01, default=0.5, label="temperature"),
            gradio.inputs.Slider(minimum=0, maximum=512, step=1, default=256, label="max-tokens")
        ],
        outputs=[
            gradio.outputs.Textbox(type="str", label="Generated Output"),
            gradio.outputs.Textbox(type="str", label="Execution Output"),
        ]
    )
    interface.launch()