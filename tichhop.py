import hashlib as hs
import math
import random
import sympy
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
from tkinter import filedialog

##### KHAI BAO THUAT TOAN DSA
# Khai bao bien toan cuc
global l, q, x, y, p, g, r, s

# Thuat toan ham bam: SHA-1
def bamDuLieu(data):
    # Ham bam mat ma
    text = hs.sha1(data.encode()).hexdigest()
    # Chuyen ham bam sang dang byte
    hexa_to_bytes = bytes.fromhex(text)
    # Ham doi hexa sang integer
    hexa_to_int = int.from_bytes(hexa_to_bytes, byteorder='big')
    return hexa_to_int

# Thuat toan binh phuong va nhan:

def binhPhuongvaNhan(x, n, p):
    result = 1  # Khoi tao p =1
    binary_n = bin(n)[2:]  # Lay gia tri nhi phan cua n bo tien to 0b
    for bit in binary_n:
        result = result = (result * result) % p
        result = result % p

        if bit == '1':  # Neu bit = 1 thi nhan voi x
            result = result * x
        result = result % p
    return result


# Thuat toan o-clit mo rong:
def oClitMoRong(r0, r1):
    a, b = r0, r1
    sa, ta = 1, 0
    sb, tb = 0, 1
    while (b > 1):
        q = a // b
        r = a % b
        sr = sa - q * sb
        tr = ta - q * tb
        a = b
        sa, ta = sb, tb
        b = r
        sb, tb = sr, tr
        while(tr < 0):
            tr += r0
    return tr


# Kiem tra so nguyen to: Dang bi khong su dung ham kiem tra SNT
def kiemTraSNT(x):
    for i in range(2, int(math.sqrt(x)), 1):
        if x % i == 0:
            return False
        else:
            return True


# Khoi tao cac tham so
def khoiTaoThamSo():
    global l, q, x, y, p, g
    # dang bi khong su dung l
    l = random.randint(512, 1024)
    while (l % 64 != 0):
        l = random.randint(512, 1024)

    p = sympy.randprime(3, 50)  #
    q = sympy.randprime(3, p-1)  #
    while (p - 1) % q != 0:
        q = sympy.randprime(3, p-1)  #

    g = sympy.randprime(3, p - 1)
    while (binhPhuongvaNhan(g, q, p) != 1):
        g = sympy.randprime(3, p - 1)  #
    x = random.randint(1, q - 1)  # Khoa rieng tu
    y = binhPhuongvaNhan(g, x, p)  # Khoa cong khai
    y = int(y)  #
    print("Cac gia tri ngau nhien: p={0}, q={1}, g={2}".format(p, q, g))
    print("Khoa bi mat x la: ", x)
    print("khoa cong khai y la: ", y)


# Chu ky dien tu:
def chuKyDienTu():
    global l, q, x, y, p, g, r, s
    thongdiep = content_entry.get()  #
    mabam = hs.sha1(thongdiep.encode()).hexdigest()  #
    soLieuBam = bamDuLieu(thongdiep)

    messagebox.showinfo("Ky chu ky", "Noi dung: {0} duoc ky thanh: {1}".format(thongdiep, mabam))
    # Random khoa k
    k = random.randint(2, q - 1)
    print("Khoa random k la: ", k)
    r = binhPhuongvaNhan(g, k, p) % q
    while (r == 0):
        k = random.randint(2, q - 1)  # Random khoa k
        r = binhPhuongvaNhan(g, k, p) % q

    s = (oClitMoRong(q, k) * (soLieuBam + x * r) % q) % q
    while (s == 0 or s ==1):
        k = random.randint(2, q - 1)  # Random khoa k
        r = binhPhuongvaNhan(g, k, p) % q
        while (r == 0):
            k = random.randint(2, q - 1)  # Random khoa k
            r = binhPhuongvaNhan(g, k, p) % q
        s = (oClitMoRong(q, k) * (soLieuBam + x * r) % q) % q

    print('Gia tri cap gia tri (r, s): ({0}, {1})'.format(int(r), int(s)))


# Xac minh chu ky dien tu:
def kiemTraChuKy():
    global q, y, p, g, r, s
    # Bam lai o dau nguoi nhan:
    noidung = content_text.get("1.0", "end-1c")
    mabam2 = hs.sha1(noidung.encode()).hexdigest()  #
    # print("Thong diep: {0} duoc bam lai tao thanh: {1}".format(noidung, mabam2))
    gtrBamLai = bamDuLieu(noidung)
    if r > 0 and r < q and s > 0 and s < q:
        w = oClitMoRong(q, s)
        u1 = (gtrBamLai * w) % q
        u1 = int(u1)
        u2 = (r * w) % q
        u2 = int(u2)
        v = ((binhPhuongvaNhan(g, u1, p) * binhPhuongvaNhan(y, u2, p)) % p) % q
        print('Gia tri r= {},v= {}'.format(int(r), int(v)))
        if v == r:
            return True
        else:
            return False
    else:
        return False


'''
if __name__ == "__main__":
    khoiTaoThamSo()
    chuKyDienTu()
    if kiemTraChuKy()==True:
        print('Chu ky da duoc xac thuc')
    else:
        print('Chu ky khong hop le')
'''

##### GIAO DIEN GUI THUC THI CHUONG TRINH
window = tk.Tk()
window.title("Chữ ký điện tử DSS sử dụng thuật toán DSA")
window.geometry("1000x500+230+100")
window.iconbitmap("C:Users\Admin\Downloads\icons8-calculator-50.ico")

main_frame = tk.Frame(window)
main_frame.pack(fill=tk.BOTH, expand=True)

##### CAC HAM THUC THI CHUONG TRINH
global check_press_button
check_press_button = False


def generate_number():
    khoiTaoThamSo()
    messagebox.showinfo('Success', 'Genarate number successfully !!!')
    p_entry.insert(0, p)
    q_entry.insert(0, q)
    g_entry.insert(0, g)
    x_entry.insert(0, x)
    y_entry.insert(0, y)
    global check_press_button
    check_press_button = True


global content


def open_file():
    global content
    file_path = filedialog.askopenfilename(
        title='Choose file',
        filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')]
    )
    with open(file_path, 'r') as f:
        messagebox.showinfo("Notification", "Open file successfully !")
        content = f.readlines()
        content_entry.delete(0, 'end')
        content_entry.insert(0, content)


def sign_signature():
    global check_press_button
    if check_press_button == True:
        chuKyDienTu()
    else:
        messagebox.showerror("Something was wrong", "Have you pressed genarate_number button yet ?")


def send_content():
    global content, q, y, p
    content = content_entry.get()
    content_text.insert('1.0', content)
    p_entry_right.insert(0, p)
    q_entry_right.insert(0, q)
    y_entry_right.insert(0, y)
    messagebox.showinfo("Notification", "Send succesfully")


def vertify():
    if kiemTraChuKy() == True:
        messagebox.showinfo("Notification", "Vertify Signature Successfully")
    else:
        messagebox.showerror("Notification", "Probably, your recieved content was changed")


def saveIntoFile():
    global content
    content_str = str(content)
    content_str = content_str.strip("['']")
    check = False
    file_path = filedialog.askopenfilename(
        title='Choose file',
        filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')]
    )
    with open(file_path, 'w') as f:
        f.write(content_str)
        check = True
    if check == True:
        messagebox.showinfo("Notification", "Saved file Successfully")
    else:
        messagebox.showerror("Something was wrong !")


bg_left = 'lightblue'
left_frame = tk.Frame(main_frame, bg=bg_left, width=400, height=400)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

bg_right = 'lightgreen'
right_frame = tk.Frame(main_frame, bg=bg_right, width=400, height=400)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

bigger_font = tkfont.Font(size=16)

# LAM VIEC VOI LAYOUT BEN TRAI
p_label = tk.Label(left_frame, text='P', bg=bg_left)
p_entry = tk.Entry(left_frame, width=20, font=bigger_font)
q_label = tk.Label(left_frame, text='Q', bg=bg_left)
q_entry = tk.Entry(left_frame, width=20, font=bigger_font)
g_label = tk.Label(left_frame, text='G', bg=bg_left)
g_entry = tk.Entry(left_frame, width=20, font=bigger_font)
x_label = tk.Label(left_frame, text='X: private key', bg=bg_left, fg='red')
x_entry = tk.Entry(left_frame, width=20, font=bigger_font)
y_label = tk.Label(left_frame, text='Y: public key', bg=bg_left)
y_entry = tk.Entry(left_frame, width=20, font=bigger_font)
content_entry = tk.Entry(left_frame, font=bigger_font, bd=5)

btn_open_file = tk.Button(left_frame, text="Open file", width=20, bg=bg_right, command=open_file)
btn_gen_number = tk.Button(left_frame, text="Generate number", bg=bg_right, bd=5, command=generate_number)
btn_sig = tk.Button(left_frame, text="Sign signature", bg=bg_right, bd=5, command=sign_signature)
btn_send = tk.Button(left_frame, text="Send content", bg=bg_right, bd=5, command=send_content)

p_label.grid(row=0, column=0, padx=5, pady=10)
q_label.grid(row=1, column=0, padx=5, pady=10)
g_label.grid(row=2, column=0, padx=5, pady=10)
x_label.grid(row=3, column=0, padx=5, pady=10)
y_label.grid(row=4, column=0, padx=5, pady=10)

p_entry.grid(row=0, column=1, padx=5, pady=5)
q_entry.grid(row=1, column=1, padx=5, pady=5)
g_entry.grid(row=2, column=1, padx=5, pady=5)
y_entry.grid(row=3, column=1, padx=5, pady=5)
x_entry.grid(row=4, column=1, padx=5, pady=5)
content_entry.grid(row=6, column=0, columnspan=3, pady=20, sticky='nswe')

btn_open_file.grid(row=5, pady=20, columnspan=3, column=0)
btn_gen_number.grid(row=7, column=0, padx=5, pady=10)
btn_sig.grid(row=7, column=1, pady=10)
btn_send.grid(row=7, column=2, pady=10)

# LAM VIEC VOI LAYOUT BEN PHAI
content_text = tk.Text(right_frame, height=10, width=40, font=bigger_font)
content_text.grid(padx=25, pady=20, row=0, columnspan=2, sticky='nswe')

p_label_right = tk.Label(right_frame, text='P', bg=bg_right)
q_label_right = tk.Label(right_frame, text='Q', bg=bg_right)
y_label_right = tk.Label(right_frame, text='Y: public key', bg=bg_right, fg='red')

p_entry_right = tk.Entry(right_frame, font=bigger_font)
q_entry_right = tk.Entry(right_frame, font=bigger_font)
y_entry_right = tk.Entry(right_frame, font=bigger_font)

btn_vertifi = tk.Button(right_frame, text="Verify Recived Content", bd=5, bg=bg_left, command=vertify)
btn_saveFile = tk.Button(right_frame, text="Save Into File", bd=5, bg=bg_left, command=saveIntoFile)

p_label_right.grid(pady=10, column=0, row=1)
q_label_right.grid(pady=10, column=0, row=2)
y_label_right.grid(pady=10, column=0, row=3)

p_entry_right.grid(padx=5, pady=5, column=1, row=1)
q_entry_right.grid(padx=5, pady=5, column=1, row=2)
y_entry_right.grid(padx=5, pady=5, column=1, row=3)

btn_vertifi.grid(column=0, row=4, padx=5, pady=10)
btn_saveFile.grid(column=1, row=4, padx=5, pady=10)

window.mainloop()
