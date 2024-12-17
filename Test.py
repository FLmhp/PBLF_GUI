import tkinter as tk
from tkinter import ttk
from tkinter import messagebox  # 引入messagebox模块
import csv  # 引入csv模块
from CookManagement import cook_dishes  # 导入cook_dishes函数

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

        # 确保登录窗口获得焦点
        login_window.focus_force()

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
        self.function_window = tk.Toplevel(self)
        self.function_window.title("功能选择")

        # 窗口居中设置
        window_width = 400
        window_height = 300
        screen_width = self.function_window.winfo_screenwidth()
        screen_height = self.function_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.function_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 创建一个框架以居中按钮
        button_frame = tk.Frame(self.function_window)
        button_frame.pack(expand=True)

        # 创建功能按钮
        edit_menu_button = ttk.Button(button_frame, text="编辑菜单", command=self.edit_menu)
        edit_menu_button.pack(pady=10)

        # 新增编辑管理员信息按钮
        edit_admin_info_button = ttk.Button(button_frame, text="编辑管理员信息", command=self.edit_admin_info)
        edit_admin_info_button.pack(pady=10)

        income_expense_button = ttk.Button(button_frame, text="收支明细", command=self.show_income_expense)
        income_expense_button.pack(pady=10)

        set_chef_number_button = ttk.Button(button_frame, text="设置厨师数", command=self.set_chef_number)
        set_chef_number_button.pack(pady=10)


    def edit_admin_info(self):
        # 关闭功能选择窗口
        self.function_window.destroy()

        # 创建编辑管理员信息窗口
        edit_admin_window = tk.Toplevel(self)
        edit_admin_window.title("编辑管理员信息")

        edit_admin_window.focus_force()

        # 窗口居中设置
        window_width = 400
        window_height = 300
        screen_width = edit_admin_window.winfo_screenwidth()
        screen_height = edit_admin_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        edit_admin_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 创建Treeview表格
        columns = ("用户名", "密码")
        tree = ttk.Treeview(edit_admin_window, columns=columns, show='headings')
        tree.pack(expand=True, fill='both', side=tk.TOP)

        # 设置列标题并自定义样式
        style = ttk.Style()
        style.configure("Custom.Treeview", background="#faff72", foreground="black")
        style.map("Custom.Treeview", background=[('selected', '#ff8936')])  # 选中时的背景色

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")  # 设置列的对齐方式为居中

        tree.configure(style="Custom.Treeview")  # 应用样式

        # 加载管理员信息
        def load_data():
            try:
                with open('admininfo.csv', newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        tree.insert('', 'end', values=row)
            except FileNotFoundError:
                messagebox.showwarning("警告", "admininfo.csv 文件未找到")

        load_data()

        # 新增空白行的函数
        def add_blank_row():
            tree.insert('', 'end', values=("", ""))  # 插入一行空白行

        # 删除选中行的函数
        def delete_selected_row():
            selected_item = tree.selection()  # 获取选中行
            if selected_item:
                for item in selected_item:
                    tree.delete(item)  # 删除选中的行

        # 更新管理员信息的函数
        def save_edit(item, col_index, new_value):
            tree.item(item, values=[*tree.item(item, 'values')[:col_index], new_value, *tree.item(item, 'values')[col_index + 1:]])

            # 更新admininfo.csv文件
            try:
                with open('admininfo.csv', 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    for child in tree.get_children():
                        writer.writerow(tree.item(child, 'values'))
            except Exception as e:
                messagebox.showwarning("警告", f"保存信息时出错: {e}")

        # 双击事件编辑单元格
        def edit_cell(event):
            item = tree.focus()
            column = tree.identify_column(event.x)
            col_index = int(column.replace('#', '')) - 1
            old_value = tree.item(item, 'values')[col_index]
            entry = ttk.Entry(edit_admin_window)
            entry.insert(0, old_value)
            entry.bind('<Return>', lambda e: [save_edit(item, col_index, entry.get()), entry.destroy()])  # 确保回车键调用save_edit函数
            entry.bind('<Escape>', lambda e: entry.destroy())
            entry.place(x=event.x, y=event.y)
            entry.focus_set()

        tree.bind('<Double-1>', edit_cell)

        # 创建按钮框架
        button_frame = ttk.Frame(edit_admin_window)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        # 创建新增按钮
        add_button = ttk.Button(button_frame, text="新增", command=add_blank_row)
        add_button.pack(side=tk.LEFT, padx=5)

        # 创建删除按钮
        delete_button = ttk.Button(button_frame, text="删除", command=delete_selected_row)
        delete_button.pack(side=tk.LEFT, padx=5)

        # 创建退出按钮
        exit_button = ttk.Button(button_frame, text="退出", command=lambda: [edit_admin_window.destroy(), self.show_function_selection()])
        exit_button.pack(side=tk.LEFT, padx=5)



    def edit_menu(self):
        # 关闭功能选择窗口
        self.function_window.destroy()

        # 创建编辑窗口
        edit_window = tk.Toplevel(self)
        edit_window.title("编辑菜单")

        edit_window.focus_force()
        
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
        columns = ("菜名", "售价/元", "成本/元", "制作时长/min")
        tree = ttk.Treeview(edit_window, columns=columns, show='headings', style="Custom.Treeview")
        tree.pack(expand=True, fill='both', side=tk.TOP)
        
        # 设置列标题和宽度
        tree.heading("菜名", text="菜名")
        tree.heading("售价/元", text="售价/元")
        tree.heading("成本/元", text="成本/元")
        tree.heading("制作时长/min", text="制作时长/min")
        
        # 设置列宽和对齐方式
        for col in columns:
            tree.column(col, anchor="center")  # 设置列的对齐方式为居中
        tree.column("菜名", width=150)
        tree.column("售价/元", width=100)
        tree.column("成本/元", width=100)
        tree.column("制作时长/min", width=100)
    
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

        #绑定Insert键到新增按钮
        edit_window.bind('<Insert>', lambda event: add_button.invoke())
        
        # 绑定Delete键到删除按钮
        edit_window.bind('<Delete>', lambda event: delete_button.invoke())

        # 绑定Esc键到退出按钮
        # edit_window.bind('<Escape>', lambda event: exit_button.invoke())
        
        def show_search_result():
            dish_name = search_entry.get()
            items = tree.get_children()  # 获取所有行
            found = False  # 用于标记是否找到菜名
            for item in items:
                values = tree.item(item, 'values')
                # 检查搜索的菜名是否在当前行的菜名中
                if (dish_name in values[0]) and (dish_name!= ""):  # values[0] 是菜名
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

        # 绑定回车键到确认按钮
        # edit_window.bind('<Return>', lambda event: confirm_button.invoke())
    
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
        self.show_function_selection()  # 重新显示功能选择窗口


    def show_income_expense(self):
        # 显示收支明细的逻辑实现
        print("显示收支明细")

    def set_chef_number(self):
        # 关闭功能选择窗口
        self.function_window.destroy()
    
        # 创建设置厨师数量的窗口
        chef_number_window = tk.Toplevel(self)
        chef_number_window.title("设置厨师数量")
    
        chef_number_window.focus_force()
    
        # 窗口居中设置
        window_width = 400
        window_height = 300
        screen_width = chef_number_window.winfo_screenwidth()
        screen_height = chef_number_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        chef_number_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
        # 创建Treeview表格
        columns = ("级别", "数量")
        tree = ttk.Treeview(chef_number_window, columns=columns, show='headings')
        tree.pack(expand=True, fill='both')
    
        # 设置列标题并居中对齐
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")
    
        # 加载厨师数量数据
        def load_data():
            try:
                with open('Cooks.csv', newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    next(reader)  # 跳过表头
                    for row in reader:
                        tree.insert('', 'end', values=row)
            except FileNotFoundError:
                messagebox.showwarning("警告", "Cooks.csv 文件未找到")
    
        load_data()
    
        # 更新厨师数量
        def save_edit(item, col_index, new_value):
            tree.item(item, values=[*tree.item(item, 'values')[:col_index], new_value, *tree.item(item, 'values')[col_index + 1:]])
    
            # 更新Cooks.csv文件
            try:
                with open('Cooks.csv', 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(columns)  # 写入表头
                    for child in tree.get_children():
                        writer.writerow(tree.item(child, 'values'))
            except Exception as e:
                messagebox.showwarning("警告", f"保存信息时出错: {e}")
    
        # 双击事件编辑单元格
        def edit_cell(event):
            item = tree.focus()
            column = tree.identify_column(event.x)
            col_index = int(column.replace('#', '')) - 1
            old_value = tree.item(item, 'values')[col_index]
            entry = ttk.Entry(chef_number_window)
            entry.insert(0, old_value)
            entry.bind('<Return>', lambda e: [save_edit(item, col_index, entry.get()), entry.destroy()])
            entry.bind('<Escape>', lambda e: entry.destroy())
            entry.place(x=event.x, y=event.y)
            entry.focus_set()
    
        tree.bind('<Double-1>', edit_cell)
    
        # 创建退出按钮
        exit_button = ttk.Button(chef_number_window, text="退出", command=chef_number_window.destroy)
        exit_button.pack(pady=10)



    def order_mode(self):
        # 进入用户点餐模式的逻辑实现
        order_window = tk.Toplevel(self)
        order_window.title("用户点餐")

        # 窗口居中设置
        window_width = 900  # 增加宽度
        window_height = 400
        screen_width = order_window.winfo_screenwidth()
        screen_height = order_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        order_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 创建样式并设置Treeview的背景颜色
        style = ttk.Style()
        style.configure("Custom.Treeview", background="#faff72", foreground="black")
        style.map("Custom.Treeview", background=[('selected', '#ff8936')])  # 选中时的背景色

        # 创建Treeview表格
        columns = ("菜名", "售价/元", "制作时长/min", "数量", "总价/元")
        tree = ttk.Treeview(order_window, columns=columns, show='headings', style="Custom.Treeview")
        tree.pack(expand=True, fill='both')

        # 设置列标题和宽度
        tree.heading("菜名", text="菜名")
        tree.heading("售价/元", text="售价/元")
        tree.heading("制作时长/min", text="制作时长/min")
        tree.heading("数量", text="数量")
        tree.heading("总价/元", text="总价/元")

        tree.column("菜名", width=200, anchor="center")  # 菜名列宽度设置
        tree.column("售价/元", width=100, anchor="center")  # 售价列宽度设置
        tree.column("制作时长/min", width=120, anchor="center")  # 制作时长列宽度设置
        tree.column("数量", width=100, anchor="center")  # 数量列宽度设置
        tree.column("总价/元", width=120, anchor="center")  # 总价列宽度设置

        # 加载数据
        def load_data():
            try:
                with open('Dishes.csv', newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        # 初始化数量为0，移除成本
                        tree.insert('', 'end', values=row[:2] + [row[3], 0, 0])  # 将数量初始化为0，单价乘数量为0，忽略成本

            except FileNotFoundError:
                messagebox.showwarning("警告", "Dishes.csv 文件未找到")

        load_data()

        # 创建一个总价行（初始化为0）
        total_price = 0
        total_row = tree.insert('', 'end', values=["", "", "", "", total_price])

        # 更新总价的方法
        def update_total_price():
            nonlocal total_price  # 声明总价为非局部变量
            total_price = 0  # 重置总价
            for item in tree.get_children():
                if item != total_row:  # 忽略总价行
                    values = tree.item(item, 'values')
                    quantity = eval(values[3])  # 获取数量
                    price = eval(values[1])  # 获取售价
                    if isinstance(quantity, int) and isinstance(price, (int, float)):
                        total = quantity * price
                        total_price += total
                        # 更新总价列
                        tree.item(item, values=list(values[:3]) + [quantity, total])  # 更新数量和总价

            # 更新总价行
            tree.item(total_row, values=["", "", "", "", total_price])  # 更新总价行

        # 创建确认和退出按钮框架
        button_frame = ttk.Frame(order_window)
        button_frame.pack(pady=10)

        confirm_button = ttk.Button(button_frame, text="确认", command=lambda: self.select_dining_mode(order_window, total_price)) 
        confirm_button.pack(side=tk.LEFT, padx=(0, 10))

        exit_button = ttk.Button(button_frame, text="退出", command=order_window.destroy)
        exit_button.pack(side=tk.LEFT)

        # 绑定鼠标滚轮事件以增加或减少数量
        def scroll_quantity(event):
            item = tree.focus()
            if item:
                values = tree.item(item, 'values')
                current_quantity = int(values[3])  # 获取当前数量
                if event.delta > 0:  # 向上滚动，增加数量
                    new_quantity = current_quantity + 1
                else:  # 向下滚动，减少数量
                    new_quantity = current_quantity - 1
                    if new_quantity < 0:  # 限制数量不能小于0
                        new_quantity = 0
                # 更新数量和总价
                tree.item(item, values=list(values[:3]) + [new_quantity, new_quantity * eval(values[1])])  
                update_total_price()  # 更新总价

        tree.bind('<MouseWheel>', scroll_quantity)  # 绑定鼠标滚轮事件

    def select_dining_mode(self, order_window, total_price):
        # 创建选择用餐方式的窗口
        dining_mode_window = tk.Toplevel(self)
        dining_mode_window.title("选择用餐方式")

        window_width = 300
        window_height = 200
        screen_width = dining_mode_window.winfo_screenwidth()
        screen_height = dining_mode_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        dining_mode_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 创建按钮选择堂食或外送
        dine_in_button = ttk.Button(dining_mode_window, text="堂食", command=lambda: self.finalize_order("堂食", total_price, order_window, dining_mode_window))
        dine_in_button.pack(pady=10)

        takeout_button = ttk.Button(dining_mode_window, text="外送", command=lambda: self.finalize_order("外送", total_price, order_window, dining_mode_window))
        takeout_button.pack(pady=10)

    def finalize_order(self, dining_mode, total_price, order_window, dining_mode_window):
        # 获取每道菜的制作时长，构建cook_times列表
        cook_times = []
        total_row_index = len(order_window.children['!treeview'].get_children()) - 1  # 总价行的索引

        # 遍历所有的子项
        for index, item in enumerate(order_window.children['!treeview'].get_children()):  
            # 确保忽略最后一行（总价行）
            if index == total_row_index:
                continue

            values = order_window.children['!treeview'].item(item, 'values')
            quantity = values[3]
            cooking_time = values[2]  # 获取制作时长
            cook_times.extend([int(cooking_time)] * int(quantity))  # 计算每道菜的总制作时长并加入列表

        total_cook_time = cook_dishes(cook_times)  # 调用cook_dishes计算总制作时长
        messagebox.showinfo("订单确认", f"您选择的用餐方式是: {dining_mode}\n总价为: {total_price}元\n总的制作时间为: {total_cook_time}分钟")
        dining_mode_window.destroy()
        order_window.destroy()




if __name__ == "__main__":
    app = RestaurantManagementSystem()
    app.mainloop()
