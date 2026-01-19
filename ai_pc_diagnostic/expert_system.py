import customtkinter as ctk

class Problema:
    def __init__(self, nombre, gravedad):
        self.nombre = nombre
        self.gravedad = gravedad

    def mostrar_solucion(self):
        pass  

class ProblemaSoftware(Problema):
    def mostrar_solucion(self):
        pass

class ProblemaHardware(Problema):
    def mostrar_solucion(self):
        pass

class SistemaExperto:
    def __init__(self):

        self.__base_conocimiento = {
            "pantalla_azul": ProblemaSoftware("Error de Windows (BSOD)", "Alta"),
            "ruido_fuerte": ProblemaHardware("Ventilador Sucio", "Media"),
            "internet_lento": ProblemaSoftware("Drivers desactualizados", "Baja"),
            "olor_quemado": ProblemaHardware("Fuente de poder dañada", "CRÍTICA"),
            "pc_no_prende": ProblemaHardware("Problema de Placa Madre", "CRÍTICA"),
            "teclado_no_funciona": ProblemaHardware("Conexión floja o dañada", "Media"),
            "programas_se_cierran": ProblemaSoftware("Infección de Malware", "Alta"),
            "virus_detectado": ProblemaSoftware("Infección de Virus", "CRÍTICA"),
        }


    @property
    def conocimientos(self):
        return list(self.__base_conocimiento.keys())
    
    def consultar(self, sintoma):
        key = sintoma.lower().replace(" ", "_")
        if key in self.__base_conocimiento:
            prob = self.__base_conocimiento[key]
            return prob.nombre, prob.mostrar_solucion()
        else:
            return None, None
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class AppDoctor(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.cerebro = SistemaExperto() 


        self.title("Tecno-Doctor IA")
        self.geometry("500x400")

    
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

        self.lbl_res_texto = ctk.CTkLabel(self.frame_res, text="Esperando consulta...", font=("Arial", 14), wraplength=400)
        self.lbl_res_texto.pack(pady=10)
        
        self.btn_lista_problemas = ctk.CTkButton(self, text="Ver Síntomas Conocidos", command=self.mostrar_lista_problemas)
        self.btn_lista_problemas.pack(pady=10)
    def buscar_solucion(self):
        # 1. Obtenemos lo que escribió el usuario
        texto_usuario = self.entry_sintoma.get()
        
        # 2. Le preguntamos al cerebro
        nombre, solucion = self.cerebro.consultar(texto_usuario)

        # 3. Actualizamos la pantalla según la respuesta
        if nombre:
            self.lbl_res_titulo.configure(text=f"DETECTADO: {nombre}", text_color="#00FF00") # Verde
            self.lbl_res_texto.configure(text=solucion)
        else:
            self.lbl_res_titulo.configure(text="NO ENCONTRADO", text_color="orange")
            self.lbl_res_texto.configure(text="No conozco ese síntoma.\nPrueba con: 'pantalla azul', 'olor quemado'...")
    def mostrar_lista_problemas(self):
        problemas = self.cerebro.conocimientos
        lista_problemas = "\n".join([f"• {p.replace('_', ' ').capitalize()}" for p in problemas])
        
        self.lbl_res_titulo.configure(text="SÍNTOMAS CONOCIDOS", text_color="#00FFFF") # Cian
        self.lbl_res_texto.configure(text=lista_problemas)

if __name__ == "__main__":
    app = AppDoctor()
    app.mainloop()
   
