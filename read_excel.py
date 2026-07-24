# ---------------- READ EXCEL ----------------
# Config tkinter
root = tk.Tk()
root.withdraw() 
root.attributes('-topmost', True)

# Merge "Open file" Window
ruta_archivo = filedialog.askopenfilename(
    title="Selecciona el archivo Excel a cargar",
    filetypes=[("Archivos de Excel", "*.xlsx *.xls"), ("Todos los archivos", "*.*")]
)
if ruta_archivo:
    df = pd.read_excel(ruta_archivo)
    print(f"✅ Archivo cargado con éxito desde:\n{ruta_archivo}\n")
product_codes = df.iloc[:115, 0].dropna().astype(str)
