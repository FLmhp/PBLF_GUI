import tkinter as tk
from tkinter import ttk
from tkinter import messagebox  # 引入messagebox模块

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
                            print("登录成功")  # 登录成功后的操作
                            login_window.destroy()  # 关闭登录窗口
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

    def order_mode(self):
        # 进入用户点餐模式的逻辑实现
        print("进入用户点餐模式")

if __name__ == "__main__":
    app = RestaurantManagementSystem()
    app.mainloop()
