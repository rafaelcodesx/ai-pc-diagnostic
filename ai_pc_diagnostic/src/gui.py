import customtkinter as ctk
from logic import SistemaExperto  # Importamos el cerebro

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AppDoctor(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.cerebro = SistemaExperto()
   
        # ... (Copia aquí el resto de tus widgets de la versión anterior) ...
        # Solo asegúrate de conectar el botón a self.buscar_solucion
        self.lbl_titulo = ctk.CTkLabel(self, text="🤖 DIAGNÓSTICO PC", font=("Roboto", 24, "bold"))
        self.lbl_titulo.pack(pady=20)

        # Campo de Texto
        self.entry_sintoma = ctk.CTkEntry(self, placeholder_text="Escribe el síntoma (ej: ruido fuerte)", width=300)
        self.entry_sintoma.pack(pady=10)
        
        # Botón (Al hacer clic llama a self.buscar_solucion)
        self.btn_buscar = ctk.CTkButton(self, text="Analizar Problema", command=self.buscar_solucion)
        self.btn_buscar.pack(pady=10)

        # Caja de Resultado (Frame)
        self.frame_res = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_res.pack(pady=20, fill="both", expand=True)

        self.lbl_res_titulo = ctk.CTkLabel(self.frame_res, text="", font=("Arial", 20, "bold"))
        self.lbl_res_titulo.pack()

        self.txt_resultado = ctk.CTkTextbox(
            self.frame_res, 
            width=400, 
            height=200, 
            font=("Consolas", 14), # Fuente tipo código/técnica
            text_color="#E0E0E0",
            wrap="word" # Ajusta el texto para que no se salga de lado
        )
        self.txt_resultado.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Mensaje inicial
        self.txt_resultado.insert("0.0", "Esperando consulta...\nEl diagnóstico aparecerá aquí.")
        self.txt_resultado.configure(state="disabled") # Bloqueamos para que el usuario no escriba
        
        self.btn_lista_problemas = ctk.CTkButton(self, text="Ver Síntomas Conocidos", command=self.mostrar_lista_problemas)
        self.btn_lista_problemas.pack(pady=10)
    
    def mostrar_lista_problemas(self):
        problemas = self.cerebro.conocimientos
        lista_problemas = "\n".join([f"• {p.replace('_', ' ').capitalize()}" for p in problemas])
        
        self.lbl_res_titulo.configure(text="SÍNTOMAS CONOCIDOS", text_color="#00FFFF") # Cian
        self.lbl_res_texto.configure(text=lista_problemas)
    
    def buscar_solucion(self):
        texto = self.entry_sintoma.get()
        titulo, detalle = self.cerebro.consultar(texto)
        
        # 1. Configurar Título (Esto sigue igual, es una Label)
        if titulo:
            self.lbl_res_titulo.configure(text=titulo, text_color="#00FF00")
        else:
            self.lbl_res_titulo.configure(text="No encontrado", text_color="orange")
            detalle = "No tengo información local y no hay conexión a IA disponible."

        # 2. Escribir en el TextBox (Lo nuevo)
        self.txt_resultado.configure(state="normal") # Desbloquear para escribir
        self.txt_resultado.delete("0.0", "end")      # Borrar todo lo anterior
        self.txt_resultado.insert("0.0", detalle)    # Escribir lo nuevo
        self.txt_resultado.configure(state="disabled") # Volver a bloquear (Solo lectura)
if __name__ == "__main__":
    app = AppDoctor()
    app.mainloop()
