from tkinter import Tk, Button, Entry, filedialog, Label, Text, Scrollbar, END
import subprocess
import re
import os
import threading


# Variáveis globais
filepath = ''
distname_entry = ''

def getfile():
    global filepath
    filepath = filedialog.askopenfilename()  # Abrir caixa de diálogo para seleção de arquivos
    file_text_entry.delete(0, 'end')
    file_text_entry.insert(0, filepath)
    
    # Extraindo um número do caminho do arquivo
    filename = os.path.basename(filepath)  # Usar os.path.basename para obter o nome do arquivo
    numbers = re.findall(r'\d+', filename)  # Encontrar todos os números
    
    if numbers:  # Verificar se algum número foi encontrado
        distname_entry.delete(0, 'end')
        distname_entry.insert(0, numbers[0])  # Inserir o primeiro número encontrado
    else:
        distname_entry.delete(0, 'end')
        distname_entry.insert(0, filename.split('.')[0])

def generate_frames():
    # Função para executar o comando ffmpeg em um thread separado
    def run_ffmpeg():
        # Obtendo valores dos campos de entrada e garantindo que sejam interpretados como inteiros
        fps = fps_entry.get()
        quality = quality_entry.get()
        input_file = file_text_entry.get()
        
        # Verificar se os campos não estão vazios e definir valores padrão se necessário
        if not fps:
            fps = '2'
        if not quality:
            quality = '2'
        
        # Criar diretório de saída se não existir
        output_dir = os.path.join(os.path.dirname(filepath), distname_entry.get())
        os.makedirs(output_dir, exist_ok=True)
        
        # Comando ffmpeg
        command = [
            'ffmpeg', '-i', input_file, '-r', fps, '-q:v', quality, 
            os.path.join(output_dir, 'frame_%04d.jpg')
        ]
        
        # Configurar startupinfo para ocultar a janela de comando em Windows
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE

        # Executar o comando ffmpeg
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, startupinfo=startupinfo)
        
        while True:
            output = process.stderr.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                # Atualiza a área de texto com a saída do ffmpeg
                console_output.insert(END, output)
                console_output.yview(END)  # Rola para o final da área de texto

        # Mensagem após a conclusão
        console_output.insert(END, "Frames gerados com sucesso.\n")

    # Criar e iniciar a thread para executar ffmpeg
    threading.Thread(target=run_ffmpeg).start()

# Criando a janela principal
window = Tk()
window.title('FrameCutter')
window.geometry('410x300')  # Diminuir o tamanho da janela

#icon here


# Linha 1
Label(window, text='Destination').grid(row=0, column=2, padx=10, pady=5, sticky='w')  
select_file_button = Button(window, text='Select File', font=(None, 9), width=8, command=getfile)
select_file_button.grid(row=1, column=0, padx=10, pady=10, sticky='w')  # Linha 1, Coluna 0

file_text_entry = Entry(window, width=20)
file_text_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')  #

distname_entry = Entry(window, width=20)
distname_entry.grid(row=1, column=2, padx=10, pady=10, sticky='w')  # 

# Linha 2
generate_button = Button(window, text='Generate', font=(None, 9), width=8, command=generate_frames)
generate_button.grid(row=3, column=0, padx=10, pady=10, sticky='w')  

Label(window, text='Fps (default 2)').grid(row=2, column=1, padx=10, pady=5, sticky='w')  #
fps_entry = Entry(window, width=20)
fps_entry.grid(row=3, column=1, padx=10, pady=10, sticky='w')  #
fps_entry.insert(0, '2')  # Valor padrão para fps

Label(window, text='Quality (1 best, 5 bad)').grid(row=2, column=2, padx=10, pady=5, sticky='w') 

quality_entry = Entry(window, width=20)
quality_entry.grid(row=3, column=2, padx=10, pady=10, sticky='w')  

quality_entry.insert(0, '2')

# Linha 3
scrollbar = Scrollbar(window)
scrollbar.grid(row=4, column=2, sticky='ns')  # Adiciona a barra de rolagem

console_output = Text(window, wrap='none', width=30, height=6, yscrollcommand=scrollbar.set)
console_output.grid(row=4, column=0, columnspan=2, padx=5, sticky='w')
scrollbar.config(command=console_output.yview)  # Conecta a barra de rolagem com a área de texto

# Centraliza a janela na tela
window.update_idletasks()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
window.geometry(f'{window_width}x{window_height}+{x}+{y}')

window.mainloop()
