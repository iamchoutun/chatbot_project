import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
import requests

# -----------------------------------------------
# Backend configuration (Render deployment)
# -----------------------------------------------
BACKEND_URL = os.getenv("BACKEND_HOST", "https://your-render-app.onrender.com")
BACKEND_RELOAD_URL = f"{BACKEND_URL}/reload-faq"
BACKEND_SAVE_URL = f"{BACKEND_URL}/update-faq"
BACKEND_FETCH_URL = f"{BACKEND_URL}/faq-data"

# -----------------------------------------------
# Local CSV fallback (if backend unavailable)
# -----------------------------------------------
CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "faq.csv")


class FAQEditor:
    """GUI editor for managing FAQ for chatbot in real-time."""

    def __init__(self, root: tk.Tk):
        """Initialize the FAQ editor GUI."""
        self.root = root
        self.root.title("FAQ Editor (Real-time)")
        self.root.geometry("700x450")

        # Treeview for displaying FAQ entries
        self.tree = ttk.Treeview(root, columns=("Question", "Answer"), show="headings", height=15)
        self.tree.heading("Question", text="Question")
        self.tree.heading("Answer", text="Answer")
        self.tree.column("Question", width=250)
        self.tree.column("Answer", width=420)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # Buttons frame
        frame = tk.Frame(root)
        frame.pack(fill=tk.X, padx=8, pady=4)

        tk.Button(frame, text="Add", command=self.add_entry, width=10).pack(side=tk.LEFT, padx=4)
        tk.Button(frame, text="Edit", command=self.edit_entry, width=10).pack(side=tk.LEFT, padx=4)
        tk.Button(frame, text="Delete", command=self.delete_entry, width=10).pack(side=tk.LEFT, padx=4)
        tk.Button(frame, text="Save", command=self.save_to_csv_and_backend, width=20).pack(side=tk.LEFT, padx=4)
        tk.Button(frame, text="Reload Chatbot", command=self.reload_chatbot, width=15).pack(side=tk.RIGHT, padx=4)
        tk.Button(frame, text="Fetch from Backend", command=self.fetch_faq, width=15).pack(side=tk.RIGHT, padx=4)

        # Load FAQ initially
        self.fetch_faq()

    # -------------------- DATA HANDLING --------------------
    def fetch_faq(self):
        """Fetch FAQ from backend or fallback to local CSV."""
        try:
            res = requests.get(BACKEND_FETCH_URL, timeout=5)
            if res.status_code == 200:
                data = res.json()
                self.df = pd.DataFrame(data)
            else:
                messagebox.showwarning("Warning", f"Failed to fetch from backend: {res.status_code}")
                self.load_data()
        except Exception:
            self.load_data()
            messagebox.showinfo("Info", "Loaded data from local CSV instead.")
        self.refresh_table()

    def reload_chatbot(self):
        """Send request to backend to reload chatbot FAQ."""
        try:
            res = requests.post(BACKEND_RELOAD_URL, timeout=5)
            if res.status_code == 200:
                messagebox.showinfo("Success", "Backend chatbot reloaded successfully!")
            else:
                messagebox.showerror("Error", f"Backend error: {res.status_code}\n{res.text}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Cannot connect to backend: {e}")

    def save_to_backend(self, df: pd.DataFrame):
        """Send FAQ data to backend."""
        try:
            data = df.to_dict(orient="records")
            res = requests.post(BACKEND_SAVE_URL, json=data, timeout=5)
            if res.status_code == 200:
                messagebox.showinfo("Success", "FAQ sent to backend successfully!")
                self.reload_chatbot()
            else:
                messagebox.showerror("Error", f"Failed to send to backend: {res.status_code}\n{res.text}")
        except Exception as e:
            messagebox.showerror("Error", f"Cannot connect to backend: {e}")

    def load_data(self):
        """Load FAQ from local CSV."""
        if os.path.exists(CSV_PATH):
            self.df = pd.read_csv(CSV_PATH, dtype=str).fillna("")
        else:
            self.df = pd.DataFrame(columns=["question", "answer"])

    def refresh_table(self):
        """Refresh Treeview table with current DataFrame."""
        for r in self.tree.get_children():
            self.tree.delete(r)
        for _, row in self.df.iterrows():
            self.tree.insert("", tk.END, values=(row["question"], row["answer"]))

    # -------------------- GUI OPERATIONS --------------------
    def add_entry(self):
        """Add a new FAQ entry."""
        self.open_editor("Add Question", "", "")

    def edit_entry(self):
        """Edit the selected FAQ entry."""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Please select a row first")
            return
        values = self.tree.item(sel[0], "values")
        self.open_editor("Edit Question", values[0], values[1], sel[0])

    def delete_entry(self):
        """Delete the selected FAQ entry."""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Please select a row first")
            return
        for s in sel:
            self.tree.delete(s)

    def open_editor(self, title: str, question: str, answer: str, item=None):
        """Open a popup editor for adding/editing FAQ entries."""
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("500x200")

        tk.Label(win, text="Question:").grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))
        q_entry = tk.Entry(win, width=60)
        q_entry.grid(row=0, column=1, padx=10, pady=(10, 5))
        q_entry.insert(0, question)

        tk.Label(win, text="Answer:").grid(row=1, column=0, sticky="w", padx=10, pady=(5, 10))
        a_entry = tk.Entry(win, width=60)
        a_entry.grid(row=1, column=1, padx=10, pady=(5, 10))
        a_entry.insert(0, answer)

        def save_close():
            q_text = q_entry.get().strip()
            a_text = a_entry.get().strip()
            if not q_text or not a_text:
                messagebox.showwarning("Warning", "Please fill in both Question and Answer")
                return
            if item:
                self.tree.item(item, values=(q_text, a_text))
            else:
                self.tree.insert("", tk.END, values=(q_text, a_text))
            win.destroy()

        tk.Button(win, text="Save", command=save_close).grid(row=2, column=0, columnspan=2, pady=12)

    def save_to_csv_and_backend(self):
        """Save FAQ to local CSV and send to backend."""
        data = []
        for row in self.tree.get_children():
            values = self.tree.item(row, "values")
            data.append({"question": values[0], "answer": values[1]})
        df = pd.DataFrame(data)

        # Save CSV local
        df.to_csv(CSV_PATH, index=False, encoding="utf-8-sig")
        messagebox.showinfo("Success", "Saved to local CSV successfully")

        # Save to backend
        self.save_to_backend(df)


if __name__ == "__main__":
    root = tk.Tk()
    app = FAQEditor(root)
    root.mainloop()
