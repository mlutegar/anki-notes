import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import re
import os


class AnkiConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Lista para Anki")
        self.root.geometry("800x600")

        # Frame principal
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Título
        title_label = tk.Label(main_frame, text="Conversor de Lista para Anki",
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 10))

        # Instrução
        instruction_label = tk.Label(main_frame,
                                     text="Cole sua lista abaixo e clique em 'Converter para Anki':",
                                     font=("Arial", 10))
        instruction_label.pack(anchor="w", pady=(0, 5))

        # Área de texto de entrada
        self.input_text = scrolledtext.ScrolledText(main_frame, height=15, width=90)
        self.input_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Frame para botões
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))

        # Botão converter
        convert_button = tk.Button(button_frame, text="Converter para Anki",
                                   command=self.convert_to_anki, bg="#4CAF50",
                                   fg="white", font=("Arial", 10, "bold"))
        convert_button.pack(side=tk.LEFT, padx=(0, 10))

        # Botão limpar
        clear_button = tk.Button(button_frame, text="Limpar",
                                 command=self.clear_input, bg="#f44336",
                                 fg="white", font=("Arial", 10))
        clear_button.pack(side=tk.LEFT, padx=(0, 10))

        # Botão carregar arquivo
        load_button = tk.Button(button_frame, text="Carregar Arquivo",
                                command=self.load_file, bg="#2196F3",
                                fg="white", font=("Arial", 10))
        load_button.pack(side=tk.LEFT)

        # Área de resultado
        result_label = tk.Label(main_frame, text="Resultado (formato Anki):",
                                font=("Arial", 10, "bold"))
        result_label.pack(anchor="w", pady=(10, 5))

        self.result_text = scrolledtext.ScrolledText(main_frame, height=10, width=90)
        self.result_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Botão salvar
        save_button = tk.Button(main_frame, text="Salvar como TXT",
                                command=self.save_file, bg="#FF9800",
                                fg="white", font=("Arial", 10, "bold"))
        save_button.pack(pady=(0, 10))

        # Exemplo na área de entrada
        example_text = """1- Red Dead Redemption

Redenção Sangrenta, Redenção Morta Vermelha

2- Gunslinger

Pistoleiro

3- Horse Bonding

Vínculo com o Cavalo

4- he's got himself caught into a scrape again

"Ele se meteu em uma enrascada de novo."

5- Continuing to bond with your horse increases its trust in you

"Continuar a fortalecer o vínculo com seu cavalo aumenta a confiança dele em você"""

        self.input_text.insert(tk.END, example_text)

    def convert_to_anki(self):
        input_content = self.input_text.get("1.0", tk.END).strip()

        if not input_content:
            messagebox.showwarning("Aviso", "Por favor, insira o conteúdo para converter.")
            return

        # Dividir o conteúdo por números seguidos de hífen
        # Usa regex para encontrar padrões como "1-", "32-", etc.
        entries = re.split(r'(?=\d+\s*-)', input_content)
        anki_cards = []

        for entry in entries:
            entry = entry.strip()
            if not entry:
                continue

            # Separar por linhas
            lines = [line.strip() for line in entry.split('\n') if line.strip()]

            if len(lines) >= 2:
                # Primeira linha: pergunta (remover numeração)
                question = re.sub(r'^\d+\s*-\s*', '', lines[0]).strip()

                # Segunda linha: resposta
                answer = lines[1].strip()

                # Remover aspas se existirem
                answer = answer.strip('"')

                # Remover formatação markdown
                answer = re.sub(r'\*\*(.*?)\*\*', r'\1', answer)

                # Verificar se temos pergunta e resposta válidas
                if question and answer:
                    # Criar card no formato Anki (pergunta TAB resposta)
                    anki_card = f"{question}\t{answer}"
                    anki_cards.append(anki_card)

        # Exibir resultado
        result = '\n'.join(anki_cards)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, result)

        if anki_cards:
            messagebox.showinfo("Sucesso", f"Convertido {len(anki_cards)} card(s) para o formato Anki!")
        else:
            messagebox.showwarning("Aviso", "Nenhum card foi encontrado no formato esperado.")

    def clear_input(self):
        self.input_text.delete("1.0", tk.END)
        self.result_text.delete("1.0", tk.END)

    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Selecionar arquivo",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.input_text.delete("1.0", tk.END)
                    self.input_text.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar arquivo: {str(e)}")

    def save_file(self):
        result_content = self.result_text.get("1.0", tk.END).strip()

        if not result_content:
            messagebox.showwarning("Aviso", "Não há conteúdo para salvar. Converta primeiro.")
            return

        file_path = filedialog.asksaveasfilename(
            title="Salvar arquivo",
            defaultextension=".txt",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(result_content)
                messagebox.showinfo("Sucesso", f"Arquivo salvo em: {file_path}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar arquivo: {str(e)}")


def main():
    root = tk.Tk()
    app = AnkiConverter(root)
    root.mainloop()


if __name__ == "__main__":
    main()