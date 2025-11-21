import customtkinter as ctk
from tkinter import messagebox
import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

PRODUCTS_FILE = "products.txt"
ADMIN_PASSWORD = "1234"

class SupermarketApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("سوپرمارکت")
        self.geometry("600x600")
        self.products = self.load_products()
        self.cart = {}
        self.show_main_menu()

    def load_products(self):
        products = {}
        with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if "," in line:
                    name, price, qty = line.strip().split(",")
                    products[name] = [float(price), int(qty)]
        return products

    def save_products(self):
        with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
            for name, data in self.products.items():
                f.write(f"{name},{data[0]},{data[1]}\n")

    def show_main_menu(self):
        self.clear_window()
        ctk.CTkLabel(self, text="سوپرمارکت", font=("IRANSans", 28, "bold")).pack(pady=40)
        ctk.CTkButton(self, text="ورود مشتری", width=200, height=50, font=("IRANSans", 16, "bold"), command=self.show_customer_page, fg_color="green").pack(pady=20)
        ctk.CTkButton(self, text="ورود ادمین", width=200, height=50, font=("IRANSans", 16, "bold"), command=self.admin_login).pack(pady=10)

    def show_customer_page(self):
        self.clear_window()
        ctk.CTkLabel(self, text="محصولات", font=("IRANSans", 24, "bold")).pack(pady=20)
        frame = ctk.CTkScrollableFrame(self, width=450, height=350)
        frame.pack(pady=10)
        self.entries = {}
        for name, data in self.products.items():
            price, qty = data
            if qty > 0:
                row = ctk.CTkFrame(frame)
                row.pack(fill="x", pady=5, padx=10)
                ctk.CTkLabel(row, text=f"{name} - {price}$ (موجودی: {qty})", font=("IRANSans", 16)).pack(side="left", padx=10)
                entry = ctk.CTkEntry(row, width=60, placeholder_text="0")
                entry.pack(side="right", padx=10)
                self.entries[name] = entry
        ctk.CTkButton(self, text="فاکتور", font=("IRANSans", 16), command=self.show_invoice_page).pack(pady=20)
        ctk.CTkButton(self, text="بازگشت", font=("IRANSans", 16), command=self.show_main_menu).pack()

    def show_invoice_page(self):
        self.cart.clear()
        for name, entry in self.entries.items():
            try:
                qty = int(entry.get() or 0)
                if qty > 0:
                    if qty <= self.products[name][1]:
                        self.cart[name] = (qty, self.products[name][0])
                    else:
                        messagebox.showerror("خطا", f"موجودی '{name}' کافی نیست!")
                        return
            except ValueError:
                messagebox.showerror("خطا", f"تعداد '{name}' معتبر نیست!")
                return
        if not self.cart:
            messagebox.showwarning("خطا", "هیچ محصولی انتخاب نشده است.")
            return
        self.clear_window()
        ctk.CTkLabel(self, text="فاکتور خرید", font=("IRANSans", 24, "bold")).pack(pady=20)
        frame = ctk.CTkFrame(self)
        frame.pack(padx=20, pady=10, fill="both", expand=True)
        total = 0
        for name, (qty, price) in self.cart.items():
            line = f"{name} × {qty} = {qty * price:.2f} $"
            ctk.CTkLabel(frame, text=line, font=("IRANSans", 16)).pack(anchor="w", pady=3)
            total += qty * price
        ctk.CTkLabel(frame, text=f"\n جمع کل: {total:.2f}", font=("IRANSans", 18, "bold")).pack(pady=10)
        ctk.CTkButton(self, text="تأیید خرید", fg_color="#00cc66", font=("IRANSans", 16), command=self.confirm_purchase).pack(pady=10)
        ctk.CTkButton(self, text="بازگشت", fg_color="gray", font=("IRANSans", 16), command=self.show_customer_page).pack()

    def confirm_purchase(self):
        for name, (qty, _) in self.cart.items():
            self.products[name][1] -= qty
        self.save_products()

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("invoices.txt", "a", encoding="utf-8") as f:
            f.write(f"\n--- فاکتور جدید ({now}) ---\n")
            total = 0
            for name, (qty, price) in self.cart.items():
                line = f"{name} × {qty} = {qty * price:.2f} $"
                f.write(line + "\n")
                total += qty * price
            f.write(f"جمع کل: {total:.2f}\n")
            f.write("-------------------------\n")

        messagebox.showinfo("خرید انجام شد", "خرید شما با موفقیت ثبت شد!")
        self.show_main_menu()

    def admin_login(self):
        win = ctk.CTkToplevel(self)
        win.title("ورود ادمین")
        win.geometry("300x200")
        ctk.CTkLabel(win, text="رمز عبور", font=("IRANSans", 16)).pack(pady=10)
        password_entry = ctk.CTkEntry(win, show="*", width=180)
        password_entry.pack(pady=5)

        def check_password():
            if password_entry.get() == ADMIN_PASSWORD:
                win.destroy()
                self.show_admin_panel()
            else:
                messagebox.showerror("خطا", "رمز عبور اشتباه است!")
        ctk.CTkButton(win, text="ورود", font=("IRANSans", 16), command=check_password).pack(pady=15)

    def show_admin_panel(self):
        self.clear_window()
        ctk.CTkLabel(self, text="پنل ادمین", font=("IRANSans", 24, "bold")).pack(pady=20)
        frame = ctk.CTkScrollableFrame(self, width=450, height=350)
        frame.pack(pady=10)
        self.entries_admin = {}
        for name, data in self.products.items():
            price, qty = data
            row = ctk.CTkFrame(frame)
            row.pack(fill="x", pady=5, padx=10)
            name_entry = ctk.CTkEntry(row, width=150)
            name_entry.insert(0, name)
            name_entry.pack(side="left", padx=5)
            price_entry = ctk.CTkEntry(row, width=80)
            price_entry.insert(0, str(price))
            price_entry.pack(side="left", padx=5)
            qty_entry = ctk.CTkEntry(row, width=80)
            qty_entry.insert(0, str(qty))
            qty_entry.pack(side="left", padx=5)
            del_btn = ctk.CTkButton(row, text="حذف", width=50, fg_color="#aa3333", command=lambda n=name: self.delete_product(n))
            del_btn.pack(side="right", padx=5)
            self.entries_admin[name] = (name_entry, price_entry, qty_entry)
        ctk.CTkButton(self, text="افزودن محصول", font=("IRANSans", 16), command=self.add_product).pack(pady=10)
        ctk.CTkButton(self, text="ذخیره تغییرات", font=("IRANSans", 16), command=self.save_admin_changes).pack(pady=5)
        ctk.CTkButton(self, text="بازگشت", font=("IRANSans", 16), command=self.show_main_menu).pack(pady=10)
    def add_product(self):
        win = ctk.CTkToplevel(self)
        win.title("افزودن محصول جدید")
        win.geometry("300x300")

        ctk.CTkLabel(win, text="نام محصول", font=("IRANSans", 14)).pack(pady=10)
        name_entry = ctk.CTkEntry(win, width=200)
        name_entry.pack()

        ctk.CTkLabel(win, text="قیمت", font=("IRANSans", 14)).pack(pady=10)
        price_entry = ctk.CTkEntry(win, width=200)
        price_entry.pack()

        ctk.CTkLabel(win, text="تعداد", font=("IRANSans", 14)).pack(pady=10)
        qty_entry = ctk.CTkEntry(win, width=200)
        qty_entry.pack()

        def save_new():
            try:
                name = name_entry.get().strip()
                price = float(price_entry.get())
                qty = int(qty_entry.get())
                if name and price >= 0 and qty >= 0:
                    self.products[name] = [price, qty]
                    self.save_products()
                    messagebox.showinfo("موفق", f"محصول '{name}' با موفقیت اضافه شد.")
                    win.destroy()
                    self.show_admin_panel()
                else:
                    messagebox.showerror("خطا", "اطلاعات وارد شده معتبر نیستند.")
            except ValueError:
                messagebox.showerror("خطا", "قیمت و تعداد باید عدد باشند!")

        ctk.CTkButton(win, text="افزودن", font=("IRANSans", 16),
                      fg_color="#00cc66", command=save_new).pack(pady=20)

    def delete_product(self, name):
        if messagebox.askyesno("تأیید حذف", f"آیا '{name}' حذف شود؟"):
            self.products.pop(name, None)
            self.save_products()
            self.show_admin_panel()

    def save_admin_changes(self):
        new_products = {}
        for name, (n_entry, p_entry, q_entry) in self.entries_admin.items():
            new_name = n_entry.get().strip()
            try:
                new_price = float(p_entry.get())
                new_qty = int(q_entry.get())
                if new_name:
                    new_products[new_name] = [new_price, new_qty]
            except ValueError:
                messagebox.showerror("خطا", f"اطلاعات '{new_name}' معتبر نیست!")
                return
        self.products = new_products
        self.save_products()
        messagebox.showinfo("ذخیره شد", "تغییرات با موفقیت ذخیره شد")
        self.show_admin_panel()

    def clear_window(self):
        for w in self.winfo_children():
            w.destroy()
app = SupermarketApp()
app.mainloop()