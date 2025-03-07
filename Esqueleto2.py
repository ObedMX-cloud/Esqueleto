import tkinter as tk
from tkinter import font, messagebox, ttk, simpledialog
import sqlite3
import threading

# Clase para gestionar tareas
class GestorTareas:
    def __init__(self, db_path="tareas.db"):
        self.db_path = db_path
        self._crear_tabla()

    def _crear_tabla(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS tareas (id INTEGER PRIMARY KEY, titulo TEXT, estado TEXT)")
        conn.commit()
        conn.close()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def agregar_tarea(self, titulo):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tareas (titulo, estado) VALUES (?, ?)", (titulo, "Pendiente"))
        conn.commit()
        conn.close()

    def eliminar_tarea(self, id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tareas WHERE id = ?", (id,))
        conn.commit()
        conn.close()

    def completar_tarea(self, id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tareas SET estado = 'Completada' WHERE id = ?", (id,))
        conn.commit()
        conn.close()

    def editar_tarea(self, id, nuevo_titulo):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tareas SET titulo = ? WHERE id = ?", (nuevo_titulo, id))
        conn.commit()
        conn.close()

    def obtener_tareas(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tareas")
        tareas = cursor.fetchall()
        conn.close()
        return tareas

# Clase para gestionar deudas
class GestorDeudas:
    def __init__(self, db_path="deudas.db"):
        self.db_path = db_path
        self._crear_tabla()

    def _crear_tabla(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS deudas (id INTEGER PRIMARY KEY, acreedor TEXT, monto REAL, vencimiento TEXT, interes REAL)")
        conn.commit()
        conn.close()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def agregar_deuda(self, acreedor, monto, vencimiento, interes):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO deudas (acreedor, monto, vencimiento, interes) VALUES (?, ?, ?, ?)",
                       (acreedor, monto, vencimiento, interes))
        conn.commit()
        conn.close()

    def eliminar_deuda(self, id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM deudas WHERE id = ?", (id,))
        conn.commit()
        conn.close()

    def modificar_deuda(self, id, nueva_deuda):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE deudas SET acreedor = ?, monto = ?, vencimiento = ?, interes = ? WHERE id = ?",
                       (nueva_deuda["acreedor"], nueva_deuda["monto"], nueva_deuda["vencimiento"], nueva_deuda["interes"], id))
        conn.commit()
        conn.close()

    def obtener_deudas(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM deudas")
        deudas = cursor.fetchall()
        conn.close()
        return deudas

# Clase principal de la aplicación
class FormularioMaestroDesign(tk.Tk):
    def __init__(self):
        super().__init__()
        self.gestor_tareas = GestorTareas()
        self.gestor_deudas = GestorDeudas()
        self.config_window()
        self.paneles()
        self.controles_barra_superior()
        self.controles_menu_lateral()
        self.mostrar_dashboard()  # Mostrar el dashboard por defecto

    def config_window(self):
        self.title("Gestión de Tareas y Deudas")
        w, h = 1024, 600
        self.geometry(f"{w}x{h}")
        self.resizable(False, False)

    def paneles(self):
        self.barra_superior = tk.Frame(self, bg="#2A2A2A", height=50)
        self.barra_superior.pack(side=tk.TOP, fill='both')

        self.menu_lateral = tk.Frame(self, bg="#1E1E1E", width=150)
        self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False)

        self.cuerpo_principal = tk.Frame(self, bg="#FFFFFF")
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)

    def controles_barra_superior(self):
        font_awesome = font.Font(family='FontAwesome', size=12)
        self.labelTitulo = tk.Label(self.barra_superior, text="Gestión de Tareas y Deudas")
        self.labelTitulo.config(fg="#fff", font=("Roboto", 15), bg="#2A2A2A", pady=10, width=16)
        self.labelTitulo.pack(side=tk.LEFT)

        self.buttonMenuLateral = tk.Button(self.barra_superior, text="\uf0c9", font=font_awesome,
                                           command=self.toggle_panel, bd=0, bg="#2A2A2A", fg="white")
        self.buttonMenuLateral.pack(side=tk.LEFT)

    def controles_menu_lateral(self):
        ancho_menu = 20
        alto_menu = 2
        font_awesome = font.Font(family='FontAwesome', size=15)

        buttons_info = [
            ("Tareas", "\uf109", self.mostrar_dashboard),
            ("Deudas", "\uf155", self.mostrar_deudas)
        ]

        for text, icon, command in buttons_info:
            button = tk.Button(self.menu_lateral, command=command)
            self.configurar_boton_menu(button, text, icon, font_awesome, ancho_menu, alto_menu)

    def configurar_boton_menu(self, button, text, icon, font_awesome, ancho_menu, alto_menu):
        button.config(text=f"  {icon}    {text}", anchor="w", font=font_awesome,
                      bd=0, bg="#1E1E1E", fg="white", width=ancho_menu, height=alto_menu)
        button.pack(side=tk.TOP)
        self.bind_hover_events(button)

    def bind_hover_events(self, button):
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))

    def on_enter(self, event, button):
        button.config(bg="#3A3A3A", fg='white')

    def on_leave(self, event, button):
        button.config(bg="#1E1E1E", fg='white')

    def toggle_panel(self):
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill='y')

    def mostrar_dashboard(self):
        self.limpiar_cuerpo()
        self.crear_interfaz_tareas()

    def mostrar_deudas(self):
        self.limpiar_cuerpo()
        self.crear_interfaz_deudas()

    def limpiar_cuerpo(self):
        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()

    def crear_interfaz_tareas(self):
        frame = tk.Frame(self.cuerpo_principal, bg="#FFFFFF")
        frame.pack(pady=10)

        entrada = ttk.Entry(frame, width=40, font=("Arial", 12))
        entrada.grid(row=0, column=0, padx=5, pady=5)

        btn_agregar = ttk.Button(frame, text="Agregar", command=lambda: self.agregar_tarea(entrada))
        btn_agregar.grid(row=0, column=1, padx=5)

        frame_lista = tk.Frame(self.cuerpo_principal, bg="#FFFFFF")
        frame_lista.pack()

        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.lista_tareas = tk.Listbox(frame_lista, width=50, height=15, font=("Arial", 12), yscrollcommand=scrollbar.set)
        self.lista_tareas.pack(padx=10, pady=5)
        scrollbar.config(command=self.lista_tareas.yview)

        self.lista_tareas.bind("<Double-Button-1>", self.completar_tarea)

        btn_completar = ttk.Button(self.cuerpo_principal, text="Marcar como Completada", command=self.completar_tarea)
        btn_completar.pack(pady=5)

        btn_editar = ttk.Button(self.cuerpo_principal, text="Editar Tarea", command=self.editar_tarea)
        btn_editar.pack(pady=5)

        btn_eliminar = ttk.Button(self.cuerpo_principal, text="Eliminar Tarea", command=self.eliminar_tarea)
        btn_eliminar.pack(pady=5)

        self.actualizar_lista()

    def agregar_tarea(self, entrada):
        titulo = entrada.get().strip()
        if titulo:
            try:
                threading.Thread(target=self._agregar_tarea_background, args=(titulo,)).start()
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al agregar la tarea: {e}")
        else:
            messagebox.showwarning("Aviso", "Debes ingresar una tarea.")

    def _agregar_tarea_background(self, titulo):
        self.gestor_tareas.agregar_tarea(titulo)
        self.actualizar_lista()

    def eliminar_tarea(self):
        try:
            index = self.lista_tareas.curselection()[0]
            tarea_id = self.gestor_tareas.obtener_tareas()[index][0]
            respuesta = messagebox.askyesno("Confirmación", "¿Seguro que quieres eliminar esta tarea?")
            if respuesta:
                self.gestor_tareas.eliminar_tarea(tarea_id)
                self.actualizar_lista()
        except IndexError:
            messagebox.showwarning("Aviso", "Selecciona una tarea para eliminar.")

    def completar_tarea(self, event=None):
        try:
            index = self.lista_tareas.curselection()[0]
            tarea_id = self.gestor_tareas.obtener_tareas()[index][0]
            self.gestor_tareas.completar_tarea(tarea_id)
            self.actualizar_lista()
        except IndexError:
            messagebox.showwarning("Aviso", "Selecciona una tarea para marcar como completada.")

    def editar_tarea(self):
        try:
            index = self.lista_tareas.curselection()[0]
            tarea_id = self.gestor_tareas.obtener_tareas()[index][0]
            nuevo_titulo = simpledialog.askstring("Editar tarea", "Modifica la tarea:")
            if nuevo_titulo:
                self.gestor_tareas.editar_tarea(tarea_id, nuevo_titulo)
                self.actualizar_lista()
        except IndexError:
            messagebox.showwarning("Aviso", "Selecciona una tarea para editar.")

    def actualizar_lista(self):
        self.lista_tareas.delete(0, tk.END)
        for tarea in self.gestor_tareas.obtener_tareas():
            estado_texto = "✅" if tarea[2] == "Completada" else "❌"
            self.lista_tareas.insert(tk.END, f"{estado_texto} {tarea[1]}")

    def crear_interfaz_deudas(self):
        frame_top = tk.Frame(self.cuerpo_principal, bg="#D3D3D3", height=50)
        frame_top.pack(fill="x")

        tk.Label(frame_top, text="Gestión de Deudas", font=("Arial", 18, "bold"), bg="#AEC6CF", fg="white").pack(pady=10)

        frame_form = tk.Frame(self.cuerpo_principal, bg="#AEC6CF", padx=20, pady=20)
        frame_form.pack(fill="x", padx=20, pady=10)

        self.crear_formulario(frame_form)

        frame_table = tk.Frame(self.cuerpo_principal, bg="#AEC6CF")
        frame_table.pack(expand=True, fill="both", padx=20, pady=10)

        self.crear_tabla(frame_table)

    def crear_formulario(self, frame):
        labels = ["Acreedor:", "Monto:", "Fecha Vencimiento:", "Interés (%)"]
        self.entries = {}

        for idx, label in enumerate(labels):
            tk.Label(frame, text=label, font=("Arial", 12), bg="#AEC6CF").grid(row=idx, column=0, sticky="w", pady=5)
            entry = ttk.Entry(frame, font=("Arial", 12))
            entry.grid(row=idx, column=1, padx=10, pady=5)
            self.entries[label] = entry

        ttk.Button(frame, text="Agregar Deuda", command=self.guardar_adeudo).grid(row=len(labels), columnspan=2, pady=10)

    def crear_tabla(self, frame):
        columnas = ("Acreedor", "Monto", "Vencimiento", "Interés")
        self.tree = ttk.Treeview(frame, columns=columnas, show="headings")

        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(expand=True, fill="both")

        btn_frame = tk.Frame(frame, bg="#ffffff")
        btn_frame.pack(fill="x")

        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar_adeudo).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Modificar", command=self.modificar_adeudo).pack(side="left", padx=5)

        self.actualizar_tabla()

    def guardar_adeudo(self):
        acreedor = self.entries["Acreedor:"].get()
        monto = self.entries["Monto:"].get()
        vencimiento = self.entries["Fecha Vencimiento:"].get()
        interes = self.entries["Interés (%)"].get()

        if not acreedor or not monto.replace('.', '', 1).isdigit():
            messagebox.showwarning("Error", "Ingrese un acreedor y un monto válido.")
            return

        try:
            self.gestor_deudas.agregar_deuda(acreedor, float(monto), vencimiento, interes)
            self.actualizar_tabla()
            messagebox.showinfo("Éxito", "Deuda agregada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al agregar la deuda: {e}")

    def actualizar_tabla(self):
        self.tree.delete(*self.tree.get_children())
        for deuda in self.gestor_deudas.obtener_deudas():
            self.tree.insert("", "end", values=(deuda[1], deuda[2], deuda[3], deuda[4]))

    def eliminar_adeudo(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Error", "Seleccione una deuda para eliminar.")
            return

        deuda_id = self.tree.item(selected_item, "values")[0]
        self.gestor_deudas.eliminar_deuda(deuda_id)
        self.actualizar_tabla()
        messagebox.showinfo("Éxito", "Deuda eliminada correctamente.")

    def modificar_adeudo(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Error", "Seleccione una deuda para modificar.")
            return

        deuda_id = self.tree.item(selected_item, "values")[0]
        nueva_deuda = {
            "acreedor": self.entries["Acreedor:"].get(),
            "monto": float(self.entries["Monto:"].get()),
            "vencimiento": self.entries["Fecha Vencimiento:"].get(),
            "interes": float(self.entries["Interés (%)"].get())
        }
        self.gestor_deudas.modificar_deuda(deuda_id, nueva_deuda)
        self.actualizar_tabla()
        messagebox.showinfo("Éxito", "Deuda modificada correctamente.")

if __name__ == "__main__":
    app = FormularioMaestroDesign()
    app.mainloop()
