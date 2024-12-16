import tkinter as tk
from tkinter import ttk
from tkinter import messagebox  # 引入messagebox模块
import csv  # 引入csv模块

class RestaurantManagementSystem(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("餐厅管理系统V1.0")  # 设置窗口标题
        self.geometry("400x300")  # 设置窗口大小
        self.configure(bg="#fff143")  # 更改主窗口颜色

        # 窗口居中设置
        window_width = 400
        window_height = 300
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")  # 重新设置窗口大小和位置

        # 创建样式并设置主框架的背景颜色
        style = ttk.Style()
        style.configure("MainFrame.TFrame", background="#f2be45")

        # 创建一个主框架
        main_frame = ttk.Frame(self, style="MainFrame.TFrame")
        main_frame.pack(expand=True)

        # 创建数字显示标签，放置在最上方
        self.number_label = ttk.Label(main_frame, font=("Arial", 16), background="#f2be45")
        self.number_label.grid(row=0, column=0, columnspan=2, pady=10)

        # 创建文本框显示“巨献”
        self.title_label = ttk.Label(main_frame, text="巨献", font=("Arial", 24), background="#f2be45")
        self.title_label.grid(row=1, column=0, columnspan=2, pady=10)

        # 创建按钮
        self.management_button = ttk.Button(main_frame, text="管理模式", command=self.management_mode)
        self.order_button = ttk.Button(main_frame, text="用户点餐模式", command=self.order_mode)

        # 修改按钮背景颜色
        self.management_button.configure(style="TButton")
        self.order_button.configure(style="TButton")

        # 将按钮放置在左右
        self.management_button.grid(row=2, column=0, padx=(50, 10), pady=20, sticky='ew')
        self.order_button.grid(row=2, column=1, padx=(10, 50), pady=20, sticky='ew')

        # 初始化字符并开始显示
        self.characters = ['马瀚鹏', '李韦成', '宋宇阳', '裴科斌']  # 要显示的字符
        self.current_index = 0  # 当前显示字符的索引
        self.update_character()

    def update_character(self):
        # 显示字符，并自动滚动
        self.number_label.config(text=self.characters[self.current_index])
        self.current_index += 1
        if self.current_index >= len(self.characters):
            self.current_index = 0
        self.after(1000, self.update_character)  # 每隔1000毫秒（1秒）更新一次

    def management_mode(self):
        # 进入管理模式的逻辑实现
        login_window = tk.Toplevel(self)  # 创建一个新的窗口
        login_window.title("管理员登录")

        # 窗口居中设置
        window_width = 300
        window_height = 200
        screen_width = login_window.winfo_screenwidth()
        screen_height = login_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        login_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 创建标签和输入框
        ttk.Label(login_window, text="用户名:").pack(pady=5)
        username_entry = ttk.Entry(login_window)
        username_entry.pack(pady=5)

        ttk.Label(login_window, text="密码:").pack(pady=5)
        password_entry = ttk.Entry(login_window, show="*")
        password_entry.pack(pady=5)

        attempts = 0  # 尝试次数计数

        def verify_credentials():
            nonlocal attempts  # 使用外部变量
            username = username_entry.get()
            password = password_entry.get()

            # 读取admininfo.csv文件
            try:
                with open('admininfo.csv', 'r') as file:
                    lines = file.readlines()
                    for line in lines:
                        admin_username, admin_password = line.strip().split(',')
                        if username == admin_username and password == admin_password:
                            # 登录成功后的操作
                            messagebox.showinfo("登录成功", "您已经成功登录")  # 弹出提示窗口
                            login_window.destroy()  # 关闭登录窗口

                            self.show_function_selection()  # 弹出功能选择窗口
                            return

                    attempts += 1
                    if attempts >= 3:
                        messagebox.showwarning("警告", "密码错误次数过多，自动退出")  # 错误次数达到上限
                        login_window.destroy()  # 关闭窗口
                    else:
                        messagebox.showwarning("登录失败", f"用户名或密码错误，您还有 {3 - attempts} 次机会")  # 弹出警告窗口
                        username_entry.delete(0, tk.END)  # 清空用户名输入框
                        password_entry.delete(0, tk.END)  # 清空密码输入框
                        messagebox.showinfo("提示", "请重新输入用户名和密码")  # 弹出提示窗口
                        login_window.lift()  # 将窗口提到前面
                        username_entry.focus()  # 聚焦到用户名输入框

            except FileNotFoundError:
                print("admininfo.csv文件未找到")  # 处理文件未找到的情况
                login_window.destroy()

        # 创建确认和退出按钮并左右放置
        button_frame = ttk.Frame(login_window)
        button_frame.pack(pady=10)

        confirm_button = ttk.Button(button_frame, text="确认", command=verify_credentials)
        confirm_button.pack(side=tk.LEFT, padx=(0, 10))  # 左侧对齐，右侧留空

        exit_button = ttk.Button(button_frame, text="退出", command=login_window.destroy)
        exit_button.pack(side=tk.LEFT)  # 左侧对齐

        # 绑定回车键和Esc键
        login_window.bind('<Return>', lambda event: verify_credentials())
        login_window.bind('<Escape>', lambda event: login_window.destroy())


    def show_function_selection(self):
        # 功能选择窗口
        function_window = tk.Toplevel(self)
        function_window.title("功能选择")

        # 窗口居中设置
        window_width = 400
        window_height = 300
        screen_width = function_window.winfo_screenwidth()
        screen_height = function_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        function_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 创建一个框架以居中按钮
        button_frame = tk.Frame(function_window)
        button_frame.pack(expand=True)

        # 创建功能按钮
        edit_menu_button = ttk.Button(button_frame, text="编辑菜单", command=self.edit_menu)
        edit_menu_button.pack(pady=10)

        income_expense_button = ttk.Button(button_frame, text="收支明细", command=self.show_income_expense)
        income_expense_button.pack(pady=10)

        set_chef_number_button = ttk.Button(button_frame, text="设置厨师数", command=self.set_chef_number)
        set_chef_number_button.pack(pady=10)

        reset_password_button = ttk.Button(button_frame, text="重置管理员密码", command=self.reset_admin_password)
        reset_password_button.pack(pady=10)

    def edit_menu(self):
        # 创建编辑窗口
        edit_window = tk.Toplevel(self)
        edit_window.title("编辑菜单")
        
        # 窗口居中设置
        window_width = 600
        window_height = 400
        screen_width = edit_window.winfo_screenwidth()
        screen_height = edit_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        edit_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 创建样式并设置Treeview的背景颜色
        style = ttk.Style()
        style.configure("Custom.Treeview", background="#faff72", foreground="black")
        style.map("Custom.Treeview", background=[('selected', '#ff8936')])  # 选中时的背景色
        
        # 创建Treeview表格
        columns = ("菜名", "售价", "成本", "制作时长")
        tree = ttk.Treeview(edit_window, columns=columns, show='headings', style="Custom.Treeview")
        tree.pack(expand=True, fill='both', side=tk.TOP)
        
        # 设置列标题和宽度
        tree.heading("菜名", text="菜名")
        tree.heading("售价", text="售价")
        tree.heading("成本", text="成本")
        tree.heading("制作时长", text="制作时长")
        
        # 设置列宽和对齐方式
        for col in columns:
            tree.column(col, anchor="center")  # 设置列的对齐方式为居中
        tree.column("菜名", width=150)
        tree.column("售价", width=100)
        tree.column("成本", width=100)
        tree.column("制作时长", width=100)
    
        # 加载数据
        def load_data():
            try:
                with open('Dishes.csv', newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        tree.insert('', 'end', values=row)
            except FileNotFoundError:
                messagebox.showwarning("警告", "Dishes.csv 文件未找到")
    
        load_data()
        
        # 删除选中行的函数
        def delete_selected_row():
            selected_item = tree.selection()  # 获取选中行
            if selected_item:
                for item in selected_item:
                    tree.delete(item)  # 删除选中的行
        
        # 新增空白行的函数
        def add_blank_row():
            tree.insert('', 'end', values=("", "", "", ""))  # 插入一行空白行
        
        # 创建按钮框架，设置在Treeview的下方并上下居中
        button_frame = ttk.Frame(edit_window)
        button_frame.pack(side=tk.TOP, pady=10)
        
        # 创建新增按钮
        add_button = ttk.Button(button_frame, text="新增", command=add_blank_row)
        add_button.pack(side=tk.LEFT, padx=5)  # 左侧对齐，右侧留空
        
        # 创建删除按钮
        delete_button = ttk.Button(button_frame, text="删除", command=delete_selected_row)
        delete_button.pack(side=tk.LEFT, padx=5)  # 左侧对齐，右侧留空
        
        # 创建退出按钮
        exit_button = ttk.Button(button_frame, text="退出编辑", command=lambda: self.exit_edit(edit_window))
        exit_button.pack(side=tk.LEFT, padx=5)  # 左侧对齐，右侧留空
    
        # 搜索框和确认按钮
        search_frame = ttk.Frame(edit_window)
        search_frame.pack(side=tk.BOTTOM, fill='x', pady=10)
        
        ttk.Label(search_frame, text="请输入菜名搜索:").pack(side=tk.LEFT, padx=(0, 5))
        search_entry = ttk.Entry(search_frame)
        search_entry.pack(side=tk.LEFT, expand=True, fill='x', padx=(0, 5))
        
        def show_search_result():
            dish_name = search_entry.get()
            items = tree.get_children()  # 获取所有行
            found = False  # 用于标记是否找到菜名
            for item in items:
                values = tree.item(item, 'values')
                # 检查搜索的菜名是否在当前行的菜名中
                if dish_name in values[0]:  # values[0] 是菜名
                    messagebox.showinfo("搜索结果", f"找到菜名: {values[0]}, 售价: {values[1]}, 成本: {values[2]}, 制作时长: {values[3]}")
                    found = True
                    break
                
            if not found:
                messagebox.showinfo("搜索结果", "未找到匹配的菜品")
            
            search_entry.delete(0, tk.END)  # 清空文本框
            edit_window.lift()  # 保持编辑窗口在最上面
            self.focus_set()  # 聚焦回功能选择窗口
            edit_window.focus_force()  # 强制编辑窗口获得焦点
            
        confirm_button = ttk.Button(search_frame, text="确认", command=show_search_result)
        confirm_button.pack(side=tk.LEFT)
    
        # 绑定双击事件编辑单元格
        def edit_cell(event):
            item = tree.focus()
            column = tree.identify_column(event.x)
            col_index = int(column.replace('#', '')) - 1
            old_value = tree.item(item, 'values')[col_index]
            entry = ttk.Entry(edit_window)
            entry.insert(0, old_value)
            entry.bind('<Return>', lambda e: save_edit(item, col_index, entry.get()))
            entry.bind('<Escape>', lambda e: entry.destroy())
            entry.place(x=event.x, y=event.y)
            entry.focus_set()
        
            def save_edit(item, col_index, new_value):
                tree.item(item, values=[*tree.item(item, 'values')[:col_index], new_value, *tree.item(item, 'values')[col_index + 1:]])
                with open('Dishes.csv', 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    for child in tree.get_children():
                        writer.writerow(tree.item(child, 'values'))
                entry.destroy()
    
        tree.bind('<Double-1>', edit_cell)
    

    def exit_edit(self, edit_window):
        edit_window.destroy()  # 关闭编辑窗口
        self.focus_set()  # 将焦点转移到功能选择窗口



    def show_income_expense(self):
        # 显示收支明细的逻辑实现
        print("显示收支明细")

    def set_chef_number(self):
        # 设置厨师数的逻辑实现
        print("设置厨师数")

    def reset_admin_password(self):
        # 重置管理员密码的逻辑实现
        print("重置管理员密码")


    def order_mode(self):
        # 进入用户点餐模式的逻辑实现
        print("进入用户点餐模式")

if __name__ == "__main__":
    app = RestaurantManagementSystem()
    app.mainloop()
