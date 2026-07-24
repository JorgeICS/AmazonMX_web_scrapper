# ---------------- SAVE ----------------
df_out = pd.DataFrame(results)
# Config tkinter
root = tk.Tk()
root.withdraw()
root.attributes('-topmost', True)
# Open "Save as" Window
file_path = filedialog.asksaveasfilename(
    defaultextension='.xlsx',
    filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
    title="Select file path to save"
)
if file_path:
    df_out.to_excel(file_path, index=False)
    print(f" File succesfully saved: {file_path}")
else:
    print(" Save Canceled")
