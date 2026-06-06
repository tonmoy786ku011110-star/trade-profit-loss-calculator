import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os
from datetime import datetime

class TradeCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Trade Profit/Loss Calculator - ট্রেড লাভ/ক্ষতি ক্যালকুলেটর")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1e1e2e")
        
        # Data storage
        self.trades = []
        self.csv_file = "trades.csv"
        self.load_trades()
        
        # Create UI
        self.create_widgets()
        self.update_display()
    
    def create_widgets(self):
        # Title
        title = tk.Label(self.root, text="📊 Trade Profit/Loss Calculator", 
                        font=("Arial", 20, "bold"), fg="#00d4ff", bg="#1e1e2e")
        title.pack(pady=10)
        
        # Input Frame
        input_frame = ttk.LabelFrame(self.root, text="Trade Information / ট্রেড তথ্য", padding=10)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        # Entry Price
        ttk.Label(input_frame, text="Entry Price / প্রবেশ মূল্য:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_price = ttk.Entry(input_frame, width=15)
        self.entry_price.grid(row=0, column=1, padx=5, pady=5)
        
        # Exit Price
        ttk.Label(input_frame, text="Exit Price / বেরিয়ে যাওয়ার মূল্য:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.exit_price = ttk.Entry(input_frame, width=15)
        self.exit_price.grid(row=0, column=3, padx=5, pady=5)
        
        # Quantity
        ttk.Label(input_frame, text="Quantity / পরিমাণ:").grid(row=0, column=4, sticky="w", padx=5, pady=5)
        self.quantity = ttk.Entry(input_frame, width=15)
        self.quantity.grid(row=0, column=5, padx=5, pady=5)
        
        # Add Trade Button
        add_btn = ttk.Button(input_frame, text="Add Trade / ট্রেড যোগ করুন", command=self.add_trade)
        add_btn.grid(row=0, column=6, padx=10, pady=5)
        
        # Statistics Frame
        stats_frame = ttk.LabelFrame(self.root, text="Statistics / পরিসংখ্যান", padding=10)
        stats_frame.pack(fill="x", padx=10, pady=10)
        
        # Total Profit/Loss
        ttk.Label(stats_frame, text="Total Profit/Loss / মোট লাভ/ক্ষতি:").grid(row=0, column=0, sticky="w", padx=5)
        self.total_label = ttk.Label(stats_frame, text="0.00", font=("Arial", 12, "bold"), foreground="green")
        self.total_label.grid(row=0, column=1, sticky="w", padx=5)
        
        # Winning Trades
        ttk.Label(stats_frame, text="Winning Trades / সফল ট্রেড:").grid(row=0, column=2, sticky="w", padx=5)
        self.winning_label = ttk.Label(stats_frame, text="0", font=("Arial", 12))
        self.winning_label.grid(row=0, column=3, sticky="w", padx=5)
        
        # Losing Trades
        ttk.Label(stats_frame, text="Losing Trades / ব্যর্থ ট্রেড:").grid(row=0, column=4, sticky="w", padx=5)
        self.losing_label = ttk.Label(stats_frame, text="0", font=("Arial", 12))
        self.losing_label.grid(row=0, column=5, sticky="w", padx=5)
        
        # Win Rate
        ttk.Label(stats_frame, text="Win Rate / জয়ের হার:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.win_rate_label = ttk.Label(stats_frame, text="0%", font=("Arial", 12))
        self.win_rate_label.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        # Total Trades
        ttk.Label(stats_frame, text="Total Trades / মোট ট্রেড:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.total_trades_label = ttk.Label(stats_frame, text="0", font=("Arial", 12))
        self.total_trades_label.grid(row=1, column=3, sticky="w", padx=5, pady=5)
        
        # Average Profit
        ttk.Label(stats_frame, text="Average Profit/Loss / গড় লাভ/ক্ষতি:").grid(row=1, column=4, sticky="w", padx=5, pady=5)
        self.avg_label = ttk.Label(stats_frame, text="0.00", font=("Arial", 12))
        self.avg_label.grid(row=1, column=5, sticky="w", padx=5, pady=5)
        
        # Trade History Frame
        history_frame = ttk.LabelFrame(self.root, text="Trade History / ট্রেড ইতিহাস", padding=10)
        history_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Treeview for trades
        columns = ("#", "Entry Price", "Exit Price", "Quantity", "Profit/Loss", "Status", "Time")
        self.tree = ttk.Treeview(history_frame, columns=columns, height=12, show="headings")
        
        # Define column headings and widths
        column_widths = {"#": 30, "Entry Price": 80, "Exit Price": 80, 
                        "Quantity": 70, "Profit/Loss": 100, "Status": 60, "Time": 120}
        for col in columns:
            self.tree.column(col, width=column_widths[col])
            self.tree.heading(col, text=col)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)
        
        # Button Frame
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        # Save Button
        save_btn = ttk.Button(btn_frame, text="💾 Save to CSV / CSV তে সংরক্ষণ করুন", command=self.save_to_csv)
        save_btn.pack(side="left", padx=5)
        
        # Clear All Button
        clear_btn = ttk.Button(btn_frame, text="🗑️ Clear All / সব মুছে দিন", command=self.clear_all)
        clear_btn.pack(side="left", padx=5)
        
        # Delete Selected Button
        delete_btn = ttk.Button(btn_frame, text="❌ Delete Selected / নির্বাচিত মুছে দিন", command=self.delete_selected)
        delete_btn.pack(side="left", padx=5)
        
        # Refresh Button
        refresh_btn = ttk.Button(btn_frame, text="🔄 Refresh / রিফ্রেশ করুন", command=self.update_display)
        refresh_btn.pack(side="left", padx=5)
    
    def add_trade(self):
        try:
            entry = float(self.entry_price.get())
            exit_p = float(self.exit_price.get())
            qty = float(self.quantity.get())
            
            if entry <= 0 or exit_p <= 0 or qty <= 0:
                messagebox.showerror("Error / ত্রুটি", "All values must be positive / সমস্ত মূল্য ইতিবাচক হতে হবে")
                return
            
            profit_loss = (exit_p - entry) * qty
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            trade = {
                "entry": entry,
                "exit": exit_p,
                "quantity": qty,
                "profit_loss": profit_loss,
                "timestamp": timestamp
            }
            
            self.trades.append(trade)
            self.save_trades()
            self.update_display()
            
            # Clear inputs
            self.entry_price.delete(0, tk.END)
            self.exit_price.delete(0, tk.END)
            self.quantity.delete(0, tk.END)
            
            messagebox.showinfo("Success / সফল", f"Trade added! Profit/Loss: {profit_loss:.2f}")
        
        except ValueError:
            messagebox.showerror("Error / ত্রুটি", "Please enter valid numbers / দয়া করে সঠিক সংখ্যা প্রবেশ করুন")
    
    def update_display(self):
        # Clear treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add trades to treeview
        for i, trade in enumerate(self.trades, 1):
            pl = trade['profit_loss']
            status = "✅ Win" if pl > 0 else "❌ Loss" if pl < 0 else "⚪ Break"
            color = "green" if pl > 0 else "red" if pl < 0 else "gray"
            
            self.tree.insert("", "end", values=(
                i,
                f"{trade['entry']:.2f}",
                f"{trade['exit']:.2f}",
                f"{trade['quantity']:.2f}",
                f"{pl:.2f}",
                status,
                trade['timestamp']
            ), tags=(color,))
        
        # Configure tag colors
        self.tree.tag_configure("green", foreground="green")
        self.tree.tag_configure("red", foreground="red")
        self.tree.tag_configure("gray", foreground="gray")
        
        # Update statistics
        self.update_statistics()
    
    def update_statistics(self):
        if not self.trades:
            self.total_label.config(text="0.00", foreground="gray")
            self.winning_label.config(text="0")
            self.losing_label.config(text="0")
            self.win_rate_label.config(text="0%")
            self.total_trades_label.config(text="0")
            self.avg_label.config(text="0.00")
            return
        
        total = sum(t['profit_loss'] for t in self.trades)
        winning = sum(1 for t in self.trades if t['profit_loss'] > 0)
        losing = sum(1 for t in self.trades if t['profit_loss'] < 0)
        win_rate = (winning / len(self.trades) * 100) if self.trades else 0
        avg = total / len(self.trades) if self.trades else 0
        
        # Update labels
        total_color = "green" if total > 0 else "red" if total < 0 else "gray"
        self.total_label.config(text=f"{total:.2f}", foreground=total_color)
        self.winning_label.config(text=str(winning))
        self.losing_label.config(text=str(losing))
        self.win_rate_label.config(text=f"{win_rate:.1f}%")
        self.total_trades_label.config(text=str(len(self.trades)))
        self.avg_label.config(text=f"{avg:.2f}")
    
    def save_to_csv(self):
        if not self.trades:
            messagebox.showwarning("Warning / সতর্কতা", "No trades to save / সংরক্ষণের জন্য কোন ট্রেড নেই")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["#", "Entry Price", "Exit Price", "Quantity", "Profit/Loss", "Status", "Timestamp"])
                
                for i, trade in enumerate(self.trades, 1):
                    pl = trade['profit_loss']
                    status = "Win" if pl > 0 else "Loss" if pl < 0 else "Break"
                    writer.writerow([
                        i,
                        f"{trade['entry']:.2f}",
                        f"{trade['exit']:.2f}",
                        f"{trade['quantity']:.2f}",
                        f"{pl:.2f}",
                        status,
                        trade['timestamp']
                    ])
            
            messagebox.showinfo("Success / সফল", f"Trades saved to {file_path}")
        
        except Exception as e:
            messagebox.showerror("Error / ত্রুটি", f"Could not save file: {str(e)}")
    
    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning / সতর্কতা", "Please select a trade to delete / মুছতে একটি ট্রেড নির্বাচন করুন")
            return
        
        if messagebox.askyesno("Confirm / নিশ্চিত করুন", "Delete this trade? / এই ট্রেডটি মুছে দিতে চান?"):
            for item in selected:
                index = int(self.tree.item(item, 'values')[0]) - 1
                if 0 <= index < len(self.trades):
                    del self.trades[index]
            
            self.save_trades()
            self.update_display()
    
    def clear_all(self):
        if not self.trades:
            messagebox.showinfo("Info / তথ্য", "No trades to clear / মুছতে কোন ট্রেড নেই")
            return
        
        if messagebox.askyesno("Confirm / নিশ্চিত করুন", "Delete all trades? / সমস্ত ট্রেড মুছে দিতে চান?"):
            self.trades = []
            self.save_trades()
            self.update_display()
    
    def save_trades(self):
        try:
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['entry', 'exit', 'quantity', 'profit_loss', 'timestamp'])
                writer.writeheader()
                writer.writerows(self.trades)
        except Exception as e:
            print(f"Error saving trades: {e}")
    
    def load_trades(self):
        if not os.path.exists(self.csv_file):
            return
        
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    trade = {
                        'entry': float(row['entry']),
                        'exit': float(row['exit']),
                        'quantity': float(row['quantity']),
                        'profit_loss': float(row['profit_loss']),
                        'timestamp': row['timestamp']
                    }
                    self.trades.append(trade)
        except Exception as e:
            print(f"Error loading trades: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TradeCalculator(root)
    root.mainloop()
