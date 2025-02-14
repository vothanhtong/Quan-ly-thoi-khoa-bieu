import hashlib
import json
import os

# File paths
USER_DATA_FILE = "users.json"
EVENT_DATA_FILE = "events.json"

def ma_hoa_mat_khau(mat_khau):
    return hashlib.sha256(mat_khau.encode()).hexdigest()

# Load data from files
def load_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            users = json.load(f)
    else:
        users = {}
    
    if os.path.exists(EVENT_DATA_FILE):
        with open(EVENT_DATA_FILE, "r") as f:
            events = json.load(f)
    else:
        events = {}
    return users, events

# Save data to files
def save_data(users, events):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)
    with open(EVENT_DATA_FILE, "w") as f:
        json.dump(events, f, indent=4)

def tao_tai_khoan(users, events):
    print("\n--- TẠO TÀI KHOẢN ---")
    while True:
        ten = input("Tên đăng nhập: ").strip()
        if ten in users:
            print("Tên đăng nhập đã tồn tại.")
            continue
        mk = input("Mật khẩu: ").strip()
        if mk == input("Xác nhận mật khẩu: ").strip():
            users[ten] = ma_hoa_mat_khau(mk)
            events[ten] = []
            save_data(users, events)
            print("Tài khoản đã tạo!")
            return
        print("Mật khẩu không khớp.")

def dang_nhap(users):
    print("\n--- ĐĂNG NHẬP ---")
    ten = input("Tên đăng nhập: ").strip()
    mk = ma_hoa_mat_khau(input("Mật khẩu: ").strip())
    if users.get(ten) == mk:
        print(f"Chào mừng {ten}!")
        return ten
    print("Sai tên đăng nhập hoặc mật khẩu.")
    return None

def them_su_kien(user, events):
    print("\n--- THÊM SỰ KIỆN ---")
    su_kien = {
        "Tháng": input("Tháng: ").strip(),
        "Tuần": input("Tuần: ").strip(),
        "Ngày": input("Ngày: ").strip(),
        "Thời gian": input("Thời gian: ").strip(),
        "Tên": input("Tên sự kiện: ").strip(),
        "Chi tiết": input("Chi tiết: ").strip(),
        "Quan trọng": input("Quan trọng (Có/Không): ").strip()
    }
    events[user].append(su_kien)
    save_data(users, events)
    print("Sự kiện đã được thêm.")

def xem_lich_trinh(user, events):
    print("\n--- LỊCH TRÌNH ---")
    if not events[user]:
        print("Không có sự kiện nào.")
        return
    for i, e in enumerate(events[user], 1):
        print(f"{i}. {e}")

def sua_su_kien(user, events):
    xem_lich_trinh(user, events)
    try:
        index = int(input("Chọn số sự kiện cần chỉnh sửa: ")) - 1
        if 0 <= index < len(events[user]):
            events[user][index]["Chi tiết"] = input("Nhập chi tiết mới: ").strip()
            save_data(users, events)
            print("Sự kiện đã được cập nhật.")
        else:
            print("Số không hợp lệ.")
    except ValueError:
        print("Lựa chọn không hợp lệ.")

def xoa_su_kien(user, events):
    xem_lich_trinh(user, events)
    try:
        index = int(input("Chọn số sự kiện cần xóa: ")) - 1
        if 0 <= index < len(events[user]):
            del events[user][index]
            save_data(users, events)
            print("Sự kiện đã bị xóa.")
        else:
            print("Số không hợp lệ.")
    except ValueError:
        print("Lựa chọn không hợp lệ.")

def menu_sau_dang_nhap(user, events):
    while True:
        lua_chon = input("\n1. Thêm Sự Kiện\n2. Xem Lịch Trình\n3. Sửa Sự Kiện\n4. Xóa Sự Kiện\n5. Đăng Xuất\nChọn: ").strip()
        if lua_chon == '1':
            them_su_kien(user, events)
        elif lua_chon == '2':
            xem_lich_trinh(user, events)
        elif lua_chon == '3':
            sua_su_kien(user, events)
        elif lua_chon == '4':
            xoa_su_kien(user, events)
        elif lua_chon == '5':
            print("Đã đăng xuất.")
            break
        else:
            print("Không hợp lệ.")

def chuong_trinh():
    global users, events
    users, events = load_data()
    while True:
        chon = input("\n1. Đăng Nhập\n2. Tạo Tài Khoản\n3. Thoát\nChọn: ").strip()
        if chon == '1':
            user = dang_nhap(users)
            if user:
                menu_sau_dang_nhap(user, events)
        elif chon == '2':
            tao_tai_khoan(users, events)
        elif chon == '3':
            print("Thoát chương trình.")
            break
        else:
            print("Không hợp lệ.")

# Chạy chương trình
chuong_trinh()
