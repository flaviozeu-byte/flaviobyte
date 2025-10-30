import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
import wavio
import threading
import time
import os

gravando = False
gravacao_thread = None

def gravar_audio():
    global gravando
    gravando = True

    fs = 44100  # taxa de amostragem
    duracao = 0
    frames = []

    messagebox.showinfo("Gravação", "Gravação iniciada. Clique em 'Parar Gravação' para finalizar.")

    while gravando:
        data = sd.rec(int(fs * 1), samplerate=fs, channels=2, dtype='int16')
        sd.wait()
        frames.append(data)
        duracao += 1

    arquivo_saida = f"gravacao_{int(time.time())}.wav"
    audio_final = b''.join([f.tobytes() for f in frames])
    wavio.write(arquivo_saida, sd.numpy.frombuffer(audio_final, dtype='int16').reshape(-1, 2), fs, sampwidth=2)

    messagebox.showinfo("Finalizado", f"Gravação salva como:\n{arquivo_saida}")

def iniciar_gravacao():
    global gravacao_thread
    if gravacao_thread and gravacao_thread.is_alive():
        messagebox.showwarning("Aviso", "Já está gravando!")
        return

    gravacao_thread = threading.Thread(target=gravar_audio, daemon=True)
    gravacao_thread.start()

def parar_gravacao():
    global gravando
    gravando = False

# Interface gráfica
janela = tk.Tk()
janela.title("🎧 Tiny Recorder")
janela.geometry("350x200")

tk.Label(janela, text="🎙️ Tiny Recorder", font=("Arial", 14)).pack(pady=20)
tk.Button(janela, text="Iniciar Gravação", command=iniciar_gravacao, width=25, height=2).pack(pady=5)
tk.Button(janela, text="Parar Gravação", command=parar_gravacao, width=25, height=2).pack(pady=5)
tk.Label(janela, text="O áudio será salvo no mesmo local do programa.", font=("Arial", 9)).pack(pady=10)

janela.mainloop()
