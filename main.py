import subprocess
import tkinter as tk
from tkinter import messagebox
import webbrowser

password = None
root = None
top_password = None
label_mysql_status = None
label_apache_status = None

def process_command(command):
    try:
        global password
        if not password:
            return;

        process = subprocess.Popen(['wsl', '--user', 'root', 'sudo'] + command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
        output, errors = process.communicate(input=password+'\n')
        
        if errors:
            print(f"Erro: {errors}")
        
        return output;
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def on_submit_password():
    global root
    global password
    global entry_password

    password = entry_password.get()

    if not is_valid_password():
        messagebox.showerror("Erro", "Senha inválida")
        return

    root.deiconify()
    top_password.withdraw()
    start_application()

def is_valid_password():
    global password
    try:
        process = subprocess.Popen(['wsl', '--user', 'root', 'sudo', 'true'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8',)
        process.communicate(input=password+'\n')
        return process.returncode == 0
    except Exception as e:
        print(f"Ocorreu um erro ao verificar a senha: {e}")
        return False

def start_get_password():
    global root
    global top_password
    global entry_password
    top_password = tk.Tk()
    top_password.title("Autenticação")
    top_password.geometry("300x100")
    top_password.resizable(False, False)
    top_password.configure(bg="#EFEFEF")
    root = top_password

    label_password = tk.Label(top_password, text="Digite a senha do WSL:", font=("Arial", 12), bg="#EFEFEF")
    label_password.pack()

    entry_password = tk.Entry(top_password, show="*", font=("Arial", 12))
    entry_password.pack()

    btn_submit = tk.Button(top_password, text="Enviar", command=on_submit_password, bg="#2196F3", fg="white")
    btn_submit.pack()

def start_application():
    global password
    global root
    global label_mysql_status
    global label_apache_status
    if not password:
        start_get_password()
        return

    if not root:
        root = tk.Tk()

    root = tk.Tk()
    root.title("ServiceHUB - WSL")
    root.resizable(False, False)
    root.configure(bg="#EFEFEF", padx=10, pady=10, borderwidth=0, highlightthickness=0, relief='ridge', highlightbackground="#EFEFEF", highlightcolor="#EFEFEF", bd=0, cursor="arrow", takefocus=False)

    frame_apache = tk.Frame(root, padx=10, pady=10, bg="#EFEFEF")
    frame_apache.pack(side=tk.LEFT, padx=10, pady=10)

    frame_mysql = tk.Frame(root, padx=10, pady=10, bg="#EFEFEF")
    frame_mysql.pack(side=tk.LEFT, padx=10, pady=10)

    frame_install = tk.Frame(root, padx=10, pady=10, bg="#EFEFEF")
    frame_install.pack()

    lbl_apache = tk.Label(frame_apache, text="Apache", font=("Arial", 14), bg="#EFEFEF", fg="black", padx=10, pady=10, width=10, height=2, borderwidth=0)
    lbl_apache.pack()

    lbl_mysql = tk.Label(frame_mysql, text="MySQL", font=("Arial", 14), bg="#EFEFEF", fg="black", padx=10, pady=10, width=10, height=2, borderwidth=0)
    lbl_mysql.pack()

    btn_start_apache = tk.Button(frame_apache, text="Iniciar", command=start_apache, bg="#4CAF50", fg="white", padx=10, pady=10, width=10, height=2, font=("Arial", 12), borderwidth=0)
    btn_start_apache.pack(pady=5)

    btn_stop_apache = tk.Button(frame_apache, text="Parar", command=stop_apache, bg="#F44336", fg="white", padx=10, pady=10, width=10, height=2, font=("Arial", 12), borderwidth=0)
    btn_stop_apache.pack(pady=5)

    btn_start_mysql = tk.Button(frame_mysql, text="Iniciar", command=start_mysql, bg="#4CAF50", fg="white", padx=10, pady=10, width=10, height=2, font=("Arial", 12), borderwidth=0)
    btn_start_mysql.pack(pady=5)

    btn_stop_mysql = tk.Button(frame_mysql, text="Parar", command=stop_mysql, bg="#F44336", fg="white", padx=10, pady=10, width=10, height=2, font=("Arial", 12), borderwidth=0)
    btn_stop_mysql.pack(pady=5)

    btn_install = tk.Button(frame_install, text="Instalar", command=install_dependencies, bg="#2196F3", fg="white", padx=10, pady=10, width=10, height=2, font=("Arial", 12), borderwidth=0)
    btn_install.pack()

    btn_open_phpmyadmin = tk.Button(frame_install, text="PhpMyAdmin", command=open_phpmyadmin, bg="#FF9800", fg="white", padx=10, pady=10, width=10, height=2, font=("Arial", 12), borderwidth=0)
    btn_open_phpmyadmin.pack()

    label_apache_status = tk.Label(frame_apache, text="Apache Status", font=("Arial", 12), bg="#EFEFEF", fg="black", padx=10, pady=10, width=10, height=2, borderwidth=0)
    label_apache_status.pack()

    label_mysql_status = tk.Label(frame_mysql, text="MySQL Status", font=("Arial", 12), bg="#EFEFEF", fg="black", padx=10, pady=10, width=10, height=2, borderwidth=0)
    label_mysql_status.pack()

    update_status_labels()

def get_apache_status():
    status = process_command(['service', 'apache2', 'status'])
    if status is None:
        return;

    if "active (running)" in status:
        return "Apache: Ativo"
    else:
        return "Apache: Inativo"

def get_mysql_status():
    status = process_command(['service', 'mysql', 'status'])
    if status is None:
        return;

    if "active (running)" in status:
        return "MySQL: Ativo"
    else:
        return "MySQL: Inativo"

def update_status_labels():
    global root
    global label_mysql_status
    global label_apache_status
    
    apache_status = get_apache_status()
    mysql_status = get_mysql_status()
    
    if not label_apache_status:
        label_apache_status = tk.Label(root, text="", font=("Arial", 12), bg="#EFEFEF")
        label_apache_status.pack()

    if not label_mysql_status:
        label_mysql_status = tk.Label(root, text="", font=("Arial", 12), bg="#EFEFEF")
        label_mysql_status.pack()

    label_apache_status.config(text=apache_status)
    label_mysql_status.config(text=mysql_status)
    
    root.after(10000, update_status_labels)

def install_dependencies():
    try:
        process_command(['apt', 'update'])
        process_command(['apt', 'install', '-y', 'apache2', 'mysql-server', 'php', 'phpmyadmin'])
        process_command(['phpenmod', 'mbstring'])
        process_command(['ln', '-s', '/usr/share/phpmyadmin', '/var/www/html/phpmyadmin'])
        process_command(['ln', '-s', '/etc/phpmyadmin/apache.conf', '/etc/apache2/conf-available/phpmyadmin.conf'])
        process_command(['a2enconf', 'phpmyadmin'])
        process_command(["sudo", "mysql", "-u", "root", "-e", "ALTER", "USER", "'root'@'localhost'", "IDENTIFIED", "WITH", "mysql_native_password", "BY", "'teste';"])
        process_command(['service', 'mysql', 'restart'])
        process_command(['service', 'apache2', 'restart'])
        messagebox.showinfo("Instalação Concluída", "Apache, MySQL e phpMyAdmin foram instalados.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro durante a instalação: {e}")

def open_phpmyadmin():
    webbrowser.open('http://localhost/phpmyadmin')

def start_apache():
    process_command(['service', 'apache2', 'start'])
    update_status_labels()

def stop_apache():
    process_command(['service', 'apache2', 'stop'])
    update_status_labels()

def start_mysql():
    process_command(['service', 'mysql', 'start'])
    update_status_labels()

def stop_mysql():
    process_command(['service', 'mysql', 'stop'])
    update_status_labels()

if __name__ == "__main__":
    start_application()
    update_status_labels()
    root.mainloop()
