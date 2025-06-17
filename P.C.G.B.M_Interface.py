import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

class PCGBMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PCGBM - Game Recommender")
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_window()

        ttk.Label(self.root, text="Login as", font=("Arial", 14)).pack(pady=10)
        ttk.Button(self.root, text="User", command=self.create_user_interface).pack(pady=5)
        ttk.Button(self.root, text="Admin", command=self.admin_login).pack(pady=5)

    def create_user_interface(self):
        self.clear_window()

        ttk.Label(self.root, text="Select your PC Specifications", font=("Arial", 14)).pack(pady=10)

        self.graphics_var = tk.StringVar()
        self.processor_var = tk.StringVar()
        self.memory_var = tk.StringVar()

        graphics_options = ["Geforce GTX 1050 Ti", "Geforce GTX 1060", "Geforce GTX 1070 Ti"]
        processor_options = ["i3", "i5", "i7"]
        memory_options = ["4GB", "8GB", "16GB"]

        self.create_dropdown("Graphics Card:", graphics_options, self.graphics_var)
        self.create_dropdown("Processor:", processor_options, self.processor_var)
        self.create_dropdown("Memory (RAM):", memory_options, self.memory_var)

        ttk.Button(self.root, text="Find Compatible Games", command=self.query_games).pack(pady=10)
        ttk.Button(self.root, text="Back to Login", command=self.create_login_screen).pack()

    def create_dropdown(self, label, options, variable):
        ttk.Label(self.root, text=label).pack()
        dropdown = ttk.Combobox(self.root, textvariable=variable, values=options)
        dropdown.pack(pady=5)

    def query_games(self):
        g = self.graphics_var.get()
        p = self.processor_var.get()
        r = self.memory_var.get()

        if not (g and p and r):
            messagebox.showerror("Error", "Please select all specs.")
            return

        try:
            conn = mysql.connector.connect(host="localhost", user="root", passwd='abc@123', database="pcgbm")
            cursor = conn.cursor()
            query = f"SELECT G_name, storage_GB_, price_$_, ReviewScore_outof100, PCprice_Rs FROM pcgbm WHERE processor='{p}' AND graphics='{g}' AND memory='{r}'"
            cursor.execute(query)
            results = cursor.fetchall()

            if not results:
                messagebox.showinfo("No Results", "No games match your configuration.")
                return

            df = pd.DataFrame(results, columns=["Game Name", "Storage(GB)", "Price($)", "Review Score", "PC Price (Rs)"])
            self.display_results(df)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

    def display_results(self, df):
        self.clear_window()

        ttk.Label(self.root, text="Compatible Games", font=("Arial", 14)).pack(pady=10)

        tree = ttk.Treeview(self.root, columns=list(df.columns), show='headings')
        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        for _, row in df.iterrows():
            tree.insert('', tk.END, values=list(row))

        tree.pack(pady=10)

        ttk.Button(self.root, text="Show Graphs", command=self.show_graph_menu).pack(pady=5)
        ttk.Button(self.root, text="Back", command=self.create_user_interface).pack()

    def show_graph_menu(self):
        self.clear_window()
        ttk.Label(self.root, text="Choose Graph Type", font=("Arial", 14)).pack(pady=10)
        ttk.Button(self.root, text="Pie Chart", command=self.show_pie_chart).pack(pady=5)
        ttk.Button(self.root, text="Bar Chart", command=self.show_bar_chart).pack(pady=5)
        ttk.Button(self.root, text="Line Graph", command=self.show_line_chart).pack(pady=5)
        ttk.Button(self.root, text="Scatter Plot", command=self.show_scatter_plot).pack(pady=5)
        ttk.Button(self.root, text="Back", command=self.create_user_interface).pack(pady=10)

    def show_pie_chart(self):
        labels = ['Geforce GTX 1050 Ti', 'Geforce GTX 1060', 'Geforce GTX 1070 Ti']
        sizes = [23, 27, 21]
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
        plt.title("Games in PCGBM for various Graphics card")
        plt.axis('equal')
        plt.show()

    def show_bar_chart(self):
        labels = ['i3', 'i5', 'i7']
        values = [25, 22, 24]
        plt.bar(labels, values, color='skyblue')
        plt.title("Games for various Processors")
        plt.ylabel("Number of Games")
        plt.show()

    def show_line_chart(self):
        labels = ['4GB', '8GB', '16GB']
        values = [24, 19, 28]
        plt.plot(labels, values, marker='o')
        plt.title("Games in PCGBM for various RAM")
        plt.xlabel("RAM")
        plt.ylabel("Number of Games")
        plt.grid(True)
        plt.show()

    def show_scatter_plot(self):
        labels = ['40 to 60', '61 to 80', '81 to 100']
        values = [3, 19, 48]
        plt.scatter(labels, values, color='green')
        plt.title("Games in PCGBM for various Review Scores")
        plt.xlabel("Review Score Range")
        plt.ylabel("Number of Games")
        plt.grid(True)
        plt.show()

    def admin_login(self):
        self.clear_window()
        ttk.Label(self.root, text="Admin Login", font=("Arial", 14)).pack(pady=10)

        ttk.Label(self.root, text="Login ID:").pack()
        self.admin_user = tk.Entry(self.root)
        self.admin_user.pack(pady=5)

        ttk.Label(self.root, text="Password:").pack()
        self.admin_pass = tk.Entry(self.root, show="*")
        self.admin_pass.pack(pady=5)

        ttk.Button(self.root, text="Login", command=self.verify_admin).pack(pady=10)
        ttk.Button(self.root, text="Back to Login", command=self.create_login_screen).pack()

    def verify_admin(self):
        if self.admin_user.get() == "pcgbm" and self.admin_pass.get() == "****":
            self.admin_dashboard()
        else:
            messagebox.showerror("Access Denied", "Invalid credentials.")

    def admin_dashboard(self):
        self.clear_window()
        ttk.Label(self.root, text="Admin Dashboard", font=("Arial", 14)).pack(pady=10)
        ttk.Button(self.root, text="Add Game Record", command=self.add_game_record).pack(pady=5)
        ttk.Button(self.root, text="View / Edit / Delete Records", command=self.view_edit_delete_records).pack(pady=5)
        ttk.Button(self.root, text="Back to Login", command=self.create_login_screen).pack(pady=10)

    def add_game_record(self):
        self.clear_window()
        ttk.Label(self.root, text="Add Game Record", font=("Arial", 14)).pack(pady=10)

        self.entries = {}
        fields = ["Game Name", "Processor", "Memory", "Graphics", "Storage(GB)", "Price($)", "Platform", "Review Score", "PC Price"]
        for field in fields:
            ttk.Label(self.root, text=field + ":").pack()
            entry = ttk.Entry(self.root)
            entry.pack(pady=2)
            self.entries[field] = entry

        ttk.Button(self.root, text="Submit", command=self.insert_game_record).pack(pady=10)
        ttk.Button(self.root, text="Back", command=self.admin_dashboard).pack()

    def insert_game_record(self):
        try:
            conn = mysql.connector.connect(host="localhost", user="root", passwd='abc@123', database="pcgbm")
            cursor = conn.cursor()
            values = [self.entries[f].get() for f in self.entries]
            query = f"""
                INSERT INTO pcgbm (G_name, processor, memory, graphics, storage_GB_, price_$_, platform, ReviewScore_outof100, PCprice_Rs)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(query, values)
            conn.commit()
            messagebox.showinfo("Success", "Game record added.")
            self.admin_dashboard()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", str(err))

    def view_edit_delete_records(self):
        self.clear_window()
        ttk.Label(self.root, text="Game Records", font=("Arial", 14)).pack(pady=10)

        self.record_tree = ttk.Treeview(self.root, columns=("G_name", "processor", "memory", "graphics"), show='headings')
        for col in self.record_tree["columns"]:
            self.record_tree.heading(col, text=col)
        self.record_tree.pack(pady=10)

        ttk.Button(self.root, text="Refresh", command=self.load_records).pack(pady=5)
        ttk.Button(self.root, text="Edit Selected", command=self.edit_selected_record).pack(pady=5)
        ttk.Button(self.root, text="Delete Selected", command=self.delete_selected_record).pack(pady=5)
        ttk.Button(self.root, text="Back", command=self.admin_dashboard).pack(pady=10)

        self.load_records()

    def load_records(self):
        for row in self.record_tree.get_children():
            self.record_tree.delete(row)
        try:
            conn = mysql.connector.connect(host="localhost", user="root", passwd='abc@123', database="pcgbm")
            cursor = conn.cursor()
            cursor.execute("SELECT G_name, processor, memory, graphics FROM pcgbm")
            for row in cursor.fetchall():
                self.record_tree.insert('', tk.END, values=row)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", str(err))

    def edit_selected_record(self):
        selected = self.record_tree.selection()
        if not selected:
            messagebox.showwarning("Select Record", "Please select a record to edit.")
            return
        values = self.record_tree.item(selected[0], 'values')
        self.edit_game_record(values)

    def edit_game_record(self, record):
        self.clear_window()
        ttk.Label(self.root, text="Edit Game Record", font=("Arial", 14)).pack(pady=10)
        self.entries = {}
        fields = ["G_name", "processor", "memory", "graphics"]
        for i, field in enumerate(fields):
            ttk.Label(self.root, text=field + ":").pack()
            entry = ttk.Entry(self.root)
            entry.insert(0, record[i])
            entry.pack(pady=2)
            self.entries[field] = entry
        ttk.Button(self.root, text="Save Changes", command=self.update_game_record).pack(pady=10)
        ttk.Button(self.root, text="Back", command=self.view_edit_delete_records).pack()

    def update_game_record(self):
        try:
            values = [self.entries[f].get() for f in ["processor", "memory", "graphics", "G_name"]]
            conn = mysql.connector.connect(host="localhost", user="root", passwd='abc@123', database="pcgbm")
            cursor = conn.cursor()
            cursor.execute("UPDATE pcgbm SET processor=%s, memory=%s, graphics=%s WHERE G_name=%s", values)
            conn.commit()
            messagebox.showinfo("Success", "Record updated.")
            self.view_edit_delete_records()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", str(err))

    def delete_selected_record(self):
        selected = self.record_tree.selection()
        if not selected:
            messagebox.showwarning("Select Record", "Please select a record to delete.")
            return
        values = self.record_tree.item(selected[0], 'values')
        confirm = messagebox.askyesno("Confirm Delete", f"Delete record for {values[0]}?")
        if confirm:
            try:
                conn = mysql.connector.connect(host="localhost", user="root", passwd='abc@123', database="pcgbm")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM pcgbm WHERE G_name=%s", (values[0],))
                conn.commit()
                self.load_records()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", str(err))

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = PCGBMApp(root)
    root.mainloop()
