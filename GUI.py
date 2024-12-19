import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import time, csv

from CookManagement import cook_dishes
from Map import get_dist_dura


class RestaurantManagementSystem(tk.Tk):
    def __init__(self):
        super().__init__()

        self.address = "四川省成都市建设北路二段四号"  # 餐厅地址

        self.title("餐厅管理系统V2.0")  # 设置窗口标题
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

        income_expense_button = ttk.Button(button_frame, text="收入明细", command=self.show_profit)
        income_expense_button.pack(pady=10)

        set_chef_number_button = ttk.Button(button_frame, text="设置厨师数", command=self.set_chef_number)
        set_chef_number_button.pack(pady=10)

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

        # 保存数据到 Dishes.csv
        def save_data():
            try:
                with open('Dishes.csv', 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    for child in tree.get_children():
                        writer.writerow(tree.item(child, 'values'))  # 写入每一行的值
            except Exception as e:
                messagebox.showwarning("警告", f"保存信息时出错: {e}")
        
        # 删除选中行的函数
        def delete_selected_row():
            selected_item = tree.selection()  # 获取选中行
            if selected_item:
                for item in selected_item:
                    tree.delete(item)  # 删除选中的行
                save_data()  # 删除后保存数据
        
        # 新增空白行的函数
        def add_blank_row():
            tree.insert('', 'end', values=("", "", "", ""))  # 插入一行空白行
            save_data()  # 删除后保存数据
        
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
            found_items = []  # 用于存储找到的菜品信息
            for item in items:
                values = tree.item(item, 'values')
                # 检查搜索的菜名是否在当前行的菜名中
                if (dish_name in values[0]) and (dish_name != ""):  # values[0] 是菜名
                    found_items.append(values)
            
            # 确认是否找到匹配的菜品
            if found_items:
                # 将搜索结果写入SearchDishes.csv
                try:
                    with open('SearchDishes.csv', 'w', newline='', encoding='utf-8') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(["菜名", "售价/元", "成本/元", "制作时长/min"])  # 写入表头
                        writer.writerows(found_items)  # 写入找到的菜品信息
                except Exception as e:
                    messagebox.showwarning("警告", f"写入SearchDishes.csv时出错: {e}")
            
                # 创建新窗口以显示搜索结果
                result_window = tk.Toplevel(self)
                result_window.title("搜索结果")
            
                # 窗口居中设置
                window_width = 600
                window_height = 400
                screen_width = result_window.winfo_screenwidth()
                screen_height = result_window.winfo_screenheight()
                x = (screen_width - window_width) // 2
                y = (screen_height - window_height) // 2
                result_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
            
                # 创建Treeview表格显示搜索结果
                search_columns = ("菜名", "售价/元", "成本/元", "制作时长/min")
                result_tree = ttk.Treeview(result_window, columns=search_columns, show='headings')
                result_tree.pack(expand=True, fill='both', side=tk.TOP)
            
                # 设置列标题和宽度
                for col in search_columns:
                    result_tree.heading(col, text=col)
                    result_tree.column(col, anchor="center", width=150)  # 设置列的宽度和对齐方式
                    
                # 插入找到的菜品信息到表格中
                for row in found_items:
                    result_tree.insert('', 'end', values=row)
            
                # 创建新搜索框和确认按钮
                search_frame = ttk.Frame(result_window)
                search_frame.pack(side=tk.BOTTOM, fill='x', pady=10)
            
                ttk.Label(search_frame, text="请输入菜名搜索:").pack(side=tk.LEFT, padx=(0, 5))
                new_search_entry = ttk.Entry(search_frame)
                new_search_entry.insert(0, dish_name)  # 将之前的搜索菜名填入新的搜索框
                new_search_entry.pack(side=tk.LEFT, expand=True, fill='x', padx=(0, 5))
            
                def new_show_search_result():
                    new_dish_name = new_search_entry.get()
                    new_found_items = []  # 用于存储新搜索的匹配项
                    for item in items:
                        values = tree.item(item, 'values')
                        if (new_dish_name in values[0]) and (new_dish_name != ""):
                            new_found_items.append(values)
            
                    # 清理结果树
                    for i in result_tree.get_children():
                        result_tree.delete(i)
            
                    if new_found_items:
                        for row in new_found_items:
                            result_tree.insert('', 'end', values=row)
                    else:
                        messagebox.showinfo("搜索结果", "未找到匹配的菜品")
            
                confirm_button = ttk.Button(search_frame, text="确认", command=new_show_search_result)
                confirm_button.pack(side=tk.LEFT)
            
            else:
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
    def show_profit(self):
        daily_profit = {}  # 用于存储每日总利润

        try:
            with open('Bills.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()
                current_date = ""
                for line in lines:
                    line = line.strip()
                    if line.startswith("下单时间:"):
                        # 提取日期部分
                        current_date = line.split()[1].split(" ")[0]  # 获取日期
                        if current_date not in daily_profit:
                            daily_profit[current_date] = 0  # 初始化日期的总利润为0
                    elif line.startswith("总利润:"):
                        # 提取利润
                        profit = float(line[5:-1])  # 取出利润并转换为浮点数
                        if current_date:
                            daily_profit[current_date] += profit  # 累加到对应日期的利润

        except FileNotFoundError:
            messagebox.showwarning("警告", "Bills.txt 文件未找到")
            return

        # 将每日利润写入Profit.csv文件
        self.write_profit_to_csv(daily_profit)

        # 绘制利润分析图
        if daily_profit:
            dates = list(daily_profit.keys())
            profits = list(daily_profit.values())

            # 创建新的窗口
            profit_window = tk.Toplevel(self)
            profit_window.title("每日利润分析")

            # 设置窗口大小
            window_width = 900  # 设置宽度
            window_height = 500  # 设置高度
            profit_window.geometry(f"{window_width}x{window_height}")

            # 计算屏幕中心位置
            screen_width = profit_window.winfo_screenwidth()
            screen_height = profit_window.winfo_screenheight()
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            profit_window.geometry(f"{window_width}x{window_height}+{x}+{y}")  # 重新设置窗口位置

            # 创建Figure
            fig = plt.Figure(figsize=(10, 5))
            ax = fig.add_subplot(111)  # 创建一个子图
            ax.plot(dates, profits, marker='o', linestyle='-', color='b')
            ax.set_title("每日利润趋势图", fontproperties='SimHei')  # 使用SimHei字体显示中文
            ax.set_xlabel("日期", fontproperties='SimHei')  # 使用SimHei字体显示中文
            ax.set_ylabel("总利润 (元)", fontproperties='SimHei')  # 使用SimHei字体显示中文

            # 自动格式化x轴日期
            ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: dates[int(x)] if int(x) < len(dates) else ''))
            ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))  # 限制x轴刻度为整数
            ax.grid()

            # 在窗口中展示图形
            canvas = FigureCanvasTkAgg(fig, profit_window)
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            canvas.draw()  # 绘制图形

    def write_profit_to_csv(self, daily_profit):
        try:
            with open('Profit.csv', 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["日期", "总利润"])  # 写入表头
                for date, profit in daily_profit.items():
                    writer.writerow([date, profit])  # 写入每一行数据
        except Exception as e:
            messagebox.showwarning("警告", f"写入Profit.csv时出错: {e}")
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
        exit_button = ttk.Button(chef_number_window, text="退出", command=lambda: self.exit_edit(chef_number_window))
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
        total_cook_time = 0
        total_row = tree.insert('', 'end', values=["", "", total_cook_time, "", total_price])

        # 更新总价和总时长的方法
        def update_total_price():
            nonlocal total_price  # 声明总价为非局部变量
            total_price = 0  # 重置总价
            cook_times = []  # 重置总时长

            for item in tree.get_children():
                if item != total_row:  # 忽略总价行
                    values = tree.item(item, 'values')
                    quantity = eval(values[3])  # 获取数量
                    price = eval(values[1])  # 获取售价
                    time = eval(values[2])  # 获取制作时长
                    if isinstance(quantity, int) and isinstance(price, (int, float)):
                        total = quantity * price
                        total_price += total
                        cook_times.extend([time] * quantity)  # 累加总时长
                        # 更新总价列
                        tree.item(item, values=list(values[:3]) + [quantity, total])  # 更新数量和总价

            total_cook_time = cook_dishes(cook_times)  # 调用cook_dishes计算总制作时长
            # 更新总价行
            tree.item(total_row, values=["", "", total_cook_time, "", total_price])  # 更新总价行

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
    
        # 创建一个框架以居中按钮
        button_frame = ttk.Frame(dining_mode_window)
        button_frame.pack(expand=True)  # 使用expand=True以使框架扩大并居中
    
        # 创建按钮选择堂食或外送
        dine_in_button = ttk.Button(button_frame, text="堂食", command=lambda: self.finalize_order("堂食", total_price, order_window, dining_mode_window))
        dine_in_button.pack(pady=10)
    
        takeout_button = ttk.Button(button_frame, text="外送", command=lambda: self.ask_for_address(total_price, order_window, dining_mode_window))
        takeout_button.pack(pady=10)

    def ask_for_address(self, total_price, order_window, dining_mode_window):
        # 创建输入地址的对话框
        address_window = tk.Toplevel(dining_mode_window)
        address_window.title("输入送餐地址")
        address_window.focus_force() # 强制聚焦到地址输入框

        window_width = 300
        window_height = 150
        screen_width = address_window.winfo_screenwidth()
        screen_height = address_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        address_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        ttk.Label(address_window, text="请输入送餐地址:").pack(pady=10)
        address_entry = ttk.Entry(address_window, width=40)
        address_entry.pack(pady=5)

        def confirm_address():
            address = address_entry.get()  # 获取用户输入的地址
            if address:
                self.finalize_order("外送", total_price, order_window, dining_mode_window, address)
                address_window.destroy()  # 关闭地址输入窗口
            else:
                messagebox.showwarning("警告", "地址不能为空！")  # 提示用户输入地址
                address_entry.delete(0, tk.END)  # 清空输入框
                address_entry.focus_set()  # 重新聚焦到输入框

        confirm_button = ttk.Button(address_window, text="确认", command=confirm_address)
        confirm_button.pack(pady=10)

        address_entry.bind('<Return>', lambda e: confirm_address())  # 绑定回车键

    def finalize_order(self, dining_mode, total_price, order_window, dining_mode_window, address=None):
        # 获取每道菜的制作时长，构建cook_times列表
        cook_times = []
        total_row_index = len(order_window.children['!treeview'].get_children()) - 1  # 总价行的索引

        # 遍历所有的子项
        order_details = []  # 用于存储订单信息
        total_cost = 0  # 总成本
        total_profit = 0  # 总利润

        for index, item in enumerate(order_window.children['!treeview'].get_children()):
            if index == total_row_index:  # 忽略最后一行（总价行）
                continue
            
            values = order_window.children['!treeview'].item(item, 'values')
            dish_name = values[0]  # 菜名
            price = float(values[1])  # 售价（以浮点数表示）
            quantity = int(values[3])  # 数量
            cooking_time = int(values[2])  # 获取制作时长

            cost = self.get_cost(dish_name)  # 获取菜品成本
            total_cost += cost * quantity  # 计算总成本
            total_profit += (price - cost) * quantity  # 计算总利润

            order_details.append(f"菜名: {dish_name}, 售价: {price}元, 数量: {quantity}")

            cook_times.extend([cooking_time] * quantity)  # 计算每道菜的总制作时长并加入列表

        total_cook_time = cook_dishes(cook_times)  # 计算总制作时长
        total_cook_time_dhm = self.convert_to_dhm(total_cook_time)  # 转换为天时分格式

        # 生成订单编号和下单时间
        order_id = f"订单编号: {self.generate_order_id()}"
        order_time = f"下单时间: {self.get_current_time()}"

        # 预计完成时间
        estimated_finish_time = datetime.now() + timedelta(minutes=total_cook_time)  # 计算预计完成时间
        estimated_finish_time_str = estimated_finish_time.strftime("%Y-%m-%d %H:%M:%S")  # 格式化为字符串

        # 将订单信息写入Bill.txt文件
        with open('Bills.txt', 'a', encoding='utf-8') as file:
            file.write(f"{order_id}\n")
            file.write(f"{order_time}\n")
            file.write("\n".join(order_details) + "\n")
            file.write(f"总价: {total_price}元\n")
            file.write(f"总成本: {total_cost}元\n")
            file.write(f"总利润: {total_profit}元\n")  # 写入总利润
            file.write("=" * 40 + "\n")  # 分隔符

        if dining_mode == "外送" and address:
            diliver_time = get_dist_dura(self.address, address)[1] / 60  # 计算配送时间
            diliver_time_str = self.convert_to_dhm(diliver_time)  # 转换为时分秒格式
            estimated_delivery_time = estimated_finish_time + timedelta(minutes=diliver_time)  # 计算预计送达时间
            estimated_delivery_time_str = estimated_delivery_time.strftime("%Y-%m-%d %H:%M:%S")  # 格式化为字符串

            messagebox.showinfo("订单确认", 
                f"您选择的用餐方式是: {dining_mode}\n总价: {total_price}元\n"
                f"预计完成时间: {estimated_finish_time_str}\n送餐地址: {address}\n"
                f"预计送达时间: {estimated_delivery_time_str}")
        else:
            messagebox.showinfo("订单确认", 
                f"您选择的用餐方式是: {dining_mode}\n总价: {total_price}元\n"
                f"预计完成时间: {estimated_finish_time_str}")

        dining_mode_window.destroy()
        order_window.destroy()

    def get_cost(self, dish_name):
        # 从Dishes.csv文件中根据菜名获取对应成本
        try:
            with open('Dishes.csv', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[0] == dish_name:  # 假设菜名在第一列，成本在第三列
                        return float(row[2])  # 返回成本，转换为浮点数
        except FileNotFoundError:
            messagebox.showwarning("警告", "Dishes.csv 文件未找到")
        return 0  # 如果未找到成本，返回0

    def generate_order_id(self):
        # 生成简单的订单编号逻辑，使用时间戳
        return str(int(time.time()))  # 使用当前时间作为简单的订单编号

    def get_current_time(self):
        # 获取当前时间
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def convert_to_dhm(self, minutes):
        # 计算总天数
        days = int(minutes // 1440)
        # 计算小时数
        hours = int((minutes % 1440) // 60)
        # 计算剩余分钟数
        remaining_minutes = int(minutes % 60)

        # 构建输出字符串
        parts = []
        if days > 0:
            parts.append(f"{days}天")
        if hours > 0:
            parts.append(f"{hours}小时")
        if remaining_minutes > 0:
            parts.append(f"{remaining_minutes}分钟")

        return ' '.join(parts) if parts else "0分钟"  # 如果所有部分为0时显示"0分钟"

if __name__ == "__main__":
    app = RestaurantManagementSystem()
    app.mainloop()