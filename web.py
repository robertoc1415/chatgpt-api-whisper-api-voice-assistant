import gradio as gr
import openai
import config
openai.api_key=config.OPENAI_API_KEY
messages=[]
messages=[
            {"role": "system", "content": "You are a helpful assistant."}
        ]
def transcribe(audio):
    global messages
    audio_file= open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    messages.append({"role": "user", "content": transcript["text"]})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    system_message= response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": system_message})
    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"
    return chat_transcript
ui = gr.Interface(fn=transcribe, inputs=gr.Audio(source="microphone", type="filepath"), outputs="text").launch()
ui.launch()   
