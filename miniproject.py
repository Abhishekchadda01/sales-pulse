import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ==========================================================
# 1. CORE DATA ANALYTICS ENGINE (Unit-1 & Unit-2)
# ==========================================================
class SalesAnalyzer:
    """Handles sales data modeling, cleaning, and mathematical computations using NumPy and Pandas."""

    def __init__(self):
        self.df = self._generate_sample_sales_data()

    def _generate_sample_sales_data(self) -> pd.DataFrame:
        """Generates realistic sales transactions for demonstration."""
        np.random.seed(42)
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        categories = ["Electronics", "Clothing", "Home & Kitchen", "Books", "Sports"]
        regions = ["North", "South", "East", "West"]

        n_records = 60
        data = {
            "Transaction_ID": [f"TRX-{1000 + i}" for i in range(n_records)],
            "Month": np.random.choice(months, size=n_records),
            "Category": np.random.choice(categories, size=n_records),
            "Region": np.random.choice(regions, size=n_records),
            "Quantity": np.random.randint(1, 15, size=n_records),
            "Unit_Price": np.random.choice([150, 450, 800, 1200, 2500, 5000], size=n_records),
        }
        df = pd.DataFrame(data)
        # Revenue = Quantity * Unit_Price (using NumPy vectorization)
        df["Total_Revenue"] = np.multiply(df["Quantity"].to_numpy(), df["Unit_Price"].to_numpy())
        return df

    def get_summary_metrics(self) -> dict:
        """Calculates key statistical indicators."""
        if self.df.empty:
            return {
                "total_revenue": 0,
                "avg_transaction": 0.0,
                "max_sale": 0,
                "total_items": 0,
                "total_orders": 0
            }
        rev = self.df["Total_Revenue"].to_numpy()
        return {
            "total_revenue": int(np.sum(rev)),
            "avg_transaction": float(np.mean(rev)),
            "max_sale": int(np.max(rev)),
            "total_items": int(np.sum(self.df["Quantity"].to_numpy())),
            "total_orders": len(self.df)
        }

    def add_sale_record(self, month: str, category: str, region: str, qty: int, price: float):
        """Appends a new transaction into the dataset."""
        new_id = f"TRX-{1000 + len(self.df)}"
        total = qty * price
        new_row = pd.DataFrame([{
            "Transaction_ID": new_id,
            "Month": month,
            "Category": category,
            "Region": region,
            "Quantity": qty,
            "Unit_Price": price,
            "Total_Revenue": total
        }])
        self.df = pd.concat([self.df, new_row], ignore_index=True)


# ==========================================================
# 2. TKINTER GUI DASHBOARD (Unit-3)
# ==========================================================
class SalesDashboardApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Interactive Sales Analytics & Visualization Dashboard")
        self.root.geometry("1180x750")
        self.root.minsize(1000, 650)

        self.analyzer = SalesAnalyzer()

        # Dynamic StringVars for real-time KPI card updates
        self.kpi_vars = {
            "total_revenue": tk.StringVar(),
            "avg_transaction": tk.StringVar(),
            "max_sale": tk.StringVar(),
            "total_items": tk.StringVar(),
            "total_orders": tk.StringVar()
        }

        self._configure_styles()
        self._build_header()
        self._build_kpi_cards()
        self._build_notebook_tabs()

        # Initial data load
        self.update_kpi_cards()
        self.render_all_charts()

    def _configure_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", font=("Segoe UI", 9), rowheight=24)
        self.style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        self.style.configure("TLabel", font=("Segoe UI", 10))
        self.style.configure("TButton", font=("Segoe UI", 10))

    def _build_header(self):
        banner = tk.Frame(self.root, bg="#0F172A", height=55)
        banner.pack(fill=tk.X, side=tk.TOP)
        title = tk.Label(
            banner,
            text="SALES PERFORMANCE & ANALYTICS SYSTEM",
            font=("Segoe UI", 14, "bold"),
            fg="#F8FAFC",
            bg="#0F172A"
        )
        title.pack(side=tk.LEFT, padx=20, pady=12)

    def _build_kpi_cards(self):
        kpi_frame = tk.Frame(self.root, bg="#F1F5F9", height=80)
        kpi_frame.pack(fill=tk.X, padx=15, pady=10)

        cards = [
            ("Total Gross Revenue", self.kpi_vars["total_revenue"], "#2563EB"),
            ("Avg Sale Value", self.kpi_vars["avg_transaction"], "#0D9488"),
            ("Highest Transaction", self.kpi_vars["max_sale"], "#7C3AED"),
            ("Total Units Sold", self.kpi_vars["total_items"], "#EA580C"),
            ("Total Orders", self.kpi_vars["total_orders"], "#475569"),
        ]

        for title, var, color in cards:
            card = tk.Frame(kpi_frame, bg="white", relief="ridge", bd=1, padx=12, pady=8)
            card.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)

            tk.Label(card, text=title, font=("Segoe UI", 8, "bold"), fg="#64748B", bg="white").pack(anchor="w")
            tk.Label(card, textvariable=var, font=("Segoe UI", 13, "bold"), fg=color, bg="white").pack(anchor="w", pady=(3, 0))

    def update_kpi_cards(self):
        """Recalculates all KPI metrics and updates UI cards in real-time."""
        metrics = self.analyzer.get_summary_metrics()
        self.kpi_vars["total_revenue"].set(f"Rs. {metrics['total_revenue']:,}")
        self.kpi_vars["avg_transaction"].set(f"Rs. {metrics['avg_transaction']:,.1f}")
        self.kpi_vars["max_sale"].set(f"Rs. {metrics['max_sale']:,}")
        self.kpi_vars["total_items"].set(f"{metrics['total_items']:,} pcs")
        self.kpi_vars["total_orders"].set(str(metrics["total_orders"]))

    def _build_notebook_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        # Tab 1: Charts & Analytics
        self.charts_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.charts_tab, text="  Visual Charts  ")
        self._setup_charts_view()

        # Tab 2: Raw Records & Form
        self.records_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.records_tab, text="  Transaction Records  ")
        self._setup_records_view()

    # ------------------ CHARTS TAB ------------------
    def _setup_charts_view(self):
        top_bar = ttk.Frame(self.charts_tab, padding=8)
        top_bar.pack(fill=tk.X)

        ttk.Button(top_bar, text="Manual Refresh Charts", command=self.render_all_charts).pack(side=tk.LEFT)
        ttk.Label(top_bar, text="Plots automatically update when you add a new transaction.", font=("Segoe UI", 9, "italic")).pack(side=tk.LEFT, padx=15)

        self.canvas_container = ttk.Frame(self.charts_tab)
        self.canvas_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def render_all_charts(self):
        """Cleans and re-renders all 3 plots using latest data."""
        for widget in self.canvas_container.winfo_children():
            widget.destroy()

        df = self.analyzer.df
        if df.empty:
            return

        fig, axes = plt.subplots(1, 3, figsize=(14, 4.3), dpi=95)
        fig.patch.set_facecolor("#FAFAFA")

        # 1. Monthly Revenue (Line + Area chart)
        month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        monthly_rev = df.groupby("Month")["Total_Revenue"].sum().reindex(month_order).fillna(0)

        axes[0].plot(monthly_rev.index, monthly_rev.values, marker="o", color="#2563EB", linewidth=2)
        axes[0].fill_between(monthly_rev.index, monthly_rev.values, color="#93C5FD", alpha=0.35)
        axes[0].set_title("Sales Trend Over Time", fontsize=10, fontweight="bold")
        axes[0].set_ylabel("Revenue (Rs.)", fontsize=8)
        axes[0].tick_params(axis="x", rotation=45, labelsize=8)
        axes[0].grid(True, linestyle="--", alpha=0.5)

        # 2. Performance Across Categories (Bar Plot)
        cat_rev = df.groupby("Category")["Total_Revenue"].sum().sort_values(ascending=False)
        colors = ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"]
        axes[1].bar(cat_rev.index, cat_rev.values, color=colors[:len(cat_rev)], edgecolor="#334155")
        axes[1].set_title("Revenue by Product Category", fontsize=10, fontweight="bold")
        axes[1].tick_params(axis="x", rotation=35, labelsize=8)
        axes[1].grid(axis="y", linestyle="--", alpha=0.5)

        # 3. Distribution by Customer Region (Pie Chart)
        region_rev = df.groupby("Region")["Total_Revenue"].sum()
        pie_colors = ["#60A5FA", "#34D399", "#FBBF24", "#F87171"]
        axes[2].pie(
            region_rev.values,
            labels=region_rev.index,
            autopct="%1.1f%%",
            startangle=130,
            colors=pie_colors,
            wedgeprops={"edgecolor": "white", "linewidth": 1.2}
        )
        axes[2].set_title("Sales Share by Region", fontsize=10, fontweight="bold")

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # ------------------ RECORDS TAB ------------------
    def _setup_records_view(self):
        form_frame = ttk.LabelFrame(self.records_tab, text=" Insert New Transaction ", padding=12)
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        cats = ["Electronics", "Clothing", "Home & Kitchen", "Books", "Sports"]
        regs = ["North", "South", "East", "West"]

        ttk.Label(form_frame, text="Month:").grid(row=0, column=0, sticky=tk.W, pady=6)
        self.entry_month = ttk.Combobox(form_frame, values=months, state="readonly", width=18)
        self.entry_month.current(0)
        self.entry_month.grid(row=0, column=1, pady=6)

        ttk.Label(form_frame, text="Category:").grid(row=1, column=0, sticky=tk.W, pady=6)
        self.entry_cat = ttk.Combobox(form_frame, values=cats, state="readonly", width=18)
        self.entry_cat.current(0)
        self.entry_cat.grid(row=1, column=1, pady=6)

        ttk.Label(form_frame, text="Region:").grid(row=2, column=0, sticky=tk.W, pady=6)
        self.entry_reg = ttk.Combobox(form_frame, values=regs, state="readonly", width=18)
        self.entry_reg.current(0)
        self.entry_reg.grid(row=2, column=1, pady=6)

        ttk.Label(form_frame, text="Quantity:").grid(row=3, column=0, sticky=tk.W, pady=6)
        self.entry_qty = ttk.Entry(form_frame, width=20)
        self.entry_qty.grid(row=3, column=1, pady=6)

        ttk.Label(form_frame, text="Unit Price (Rs.):").grid(row=4, column=0, sticky=tk.W, pady=6)
        self.entry_price = ttk.Entry(form_frame, width=20)
        self.entry_price.grid(row=4, column=1, pady=6)

        btn_add = ttk.Button(form_frame, text="Add Transaction", command=self.handle_add_entry)
        btn_add.grid(row=5, column=0, columnspan=2, pady=(15, 0), sticky=tk.EW)

        table_frame = ttk.Frame(self.records_tab, padding=10)
        table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        cols = ("Transaction_ID", "Month", "Category", "Region", "Quantity", "Unit_Price", "Total_Revenue")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")
        for col in cols:
            self.tree.heading(col, text=col.replace("_", " "))
            self.tree.column(col, anchor=tk.CENTER, width=105)

        tree_scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self._populate_table()

    def _populate_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for _, row in self.analyzer.df.iterrows():
            self.tree.insert("", tk.END, values=list(row))

    def handle_add_entry(self):
        m = self.entry_month.get()
        c = self.entry_cat.get()
        r = self.entry_reg.get()
        qty_str = self.entry_qty.get().strip()
        price_str = self.entry_price.get().strip()

        try:
            qty = int(qty_str)
            price = float(price_str)
            if qty <= 0 or price <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Quantity and Price must be positive numbers.")
            return

        # 1. Add record into DataFrame
        self.analyzer.add_sale_record(m, c, r, qty, price)

        # 2. Real-time updates across the dashboard
        self._populate_table()     # Update Table
        self.update_kpi_cards()    # Auto-update Top Revenue, Items & Total Order cards
        self.render_all_charts()   # Auto-update Line, Bar, and Pie charts

        # 3. Clear inputs & select newly added row
        self.entry_qty.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
        
        children = self.tree.get_children()
        if children:
            self.tree.selection_set(children[-1])
            self.tree.see(children[-1])

        messagebox.showinfo("Success", "Transaction added! All totals & charts have been refreshed.")


# ==========================================================
# 3. APPLICATION ENTRY POINT
# ==========================================================
if __name__ == "__main__":
    app_window = tk.Tk()
    app = SalesDashboardApp(app_window)
    app_window.mainloop()