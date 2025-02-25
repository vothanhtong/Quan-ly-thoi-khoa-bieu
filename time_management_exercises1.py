import json
from datetime import datetime

# Danh sách lưu trữ tài khoản và sự kiện
tai_khoan_nguoi_dung = {}
lich_trinh_su_kien = []

# Tệp lưu trữ dữ liệu
FILE_TAI_KHOAN = "tai_khoan.json"
FILE_LICH_TRINH = "lich_trinh.json"

# Tải dữ liệu từ tệp JSON (nếu có)
def tai_du_lieu():
    global tai_khoan_nguoi_dung, lich_trinh_su_kien
    try:
        with open(FILE_TAI_KHOAN, 'r', encoding='utf-8') as f:
            tai_khoan_nguoi_dung = json.load(f)
        with open(FILE_LICH_TRINH, 'r', encoding='utf-8') as f:
            lich_trinh_su_kien = json.load(f)
    except FileNotFoundError:
        print("Không tìm thấy dữ liệu cũ, khởi tạo mới.")

# Lưu dữ liệu vào tệp JSON
def luu_du_lieu():
    with open(FILE_TAI_KHOAN, 'w', encoding='utf-8') as f:
        json.dump(tai_khoan_nguoi_dung, f, ensure_ascii=False, indent=4)
    with open(FILE_LICH_TRINH, 'w', encoding='utf-8') as f:
        json.dump(lich_trinh_su_kien, f, ensure_ascii=False, indent=4)

# Hiển thị menu
def hien_thi_menu(chuc_nang):
    menus = {
        "main": "\n--- MENU CHÍNH ---\n1. Đăng Nhập\n2. Tạo Tài Khoản\n3. Thoát",
        "sau_dang_nhap": "\n--- MENU SỰ KIỆN ---\n1. Thêm Sự Kiện\n2. Xem Lịch Trình\n3. Chỉnh Sửa Sự Kiện\n4. Tìm Kiếm Sự Kiện\n5. Sắp Xếp Lịch Trình\n6. Đăng Xuất"
    }
    print(menus[chuc_nang])

# Tạo tài khoản mới
def tao_tai_khoan():
    print("\n--- TẠO TÀI KHOẢN ---")
    while True:
        ten = input("Tên đăng nhập: ").strip()
        if ten in tai_khoan_nguoi_dung:
            print("Tên đăng nhập đã tồn tại.")
            continue
        mat_khau = input("Mật khẩu: ").strip()
        if mat_khau == input("Xác nhận mật khẩu: ").strip():
            tai_khoan_nguoi_dung[ten] = mat_khau
            luu_du_lieu()
            print("Tài khoản đã được tạo thành công!")
            return
        print("Mật khẩu không khớp, thử lại.")

# Đăng nhập
def dang_nhap():
    print("\n--- ĐĂNG NHẬP ---")
    ten = input("Tên đăng nhập: ").strip()
    mat_khau = input("Mật khẩu: ").strip()
    if tai_khoan_nguoi_dung.get(ten) == mat_khau:
        print(f"Chào mừng {ten} đã đăng nhập!")
        return ten
    print("Sai tên đăng nhập hoặc mật khẩu.")
    return None

# Thêm sự kiện mới
def them_su_kien():
    print("\n--- THÊM SỰ KIỆN ---")
    su_kien = {
        'Tháng': input("Nhập tháng (1-12): ").strip(),
        'Ngày': input("Nhập ngày (1-31): ").strip(),
        'Thời gian bắt đầu': input("Nhập thời gian bắt đầu (HH:MM): ").strip(),
        'Thời gian kết thúc': input("Nhập thời gian kết thúc (HH:MM): ").strip(),
        'Tên sự kiện': input("Nhập tên sự kiện: ").strip(),
        'Chi tiết': input("Nhập chi tiết sự kiện: ").strip(),
        'Quan trọng': input("Sự kiện quan trọng? (Có/Không): ").strip().capitalize()
    }

    # Kiểm tra định dạng ngày và thời gian
    try:
        datetime.strptime(f"{su_kien['Tháng']}/{su_kien['Ngày']}/2025", "%m/%d/%Y")
        datetime.strptime(su_kien['Thời gian bắt đầu'], "%H:%M")
        datetime.strptime(su_kien['Thời gian kết thúc'], "%H:%M")
    except ValueError:
        print("Ngày hoặc thời gian không hợp lệ!")
        return

    # Kiểm tra trùng lặp
    su_kien_trung = next((e for e in lich_trinh_su_kien if e['Ngày'] == su_kien['Ngày'] and e['Tháng'] == su_kien['Tháng'] and e['Tên sự kiện'] == su_kien['Tên sự kiện']), None)
    if su_kien_trung:
        hop_nhat = input("Sự kiện trùng lặp! Hợp nhất không? (Có/Không): ").strip().capitalize()
        if hop_nhat == "Có":
            su_kien_trung['Chi tiết'] += " | " + su_kien['Chi tiết']
            su_kien_trung['Thời gian bắt đầu'] = min(su_kien_trung['Thời gian bắt đầu'], su_kien['Thời gian bắt đầu'])
            su_kien_trung['Thời gian kết thúc'] = max(su_kien_trung['Thời gian kết thúc'], su_kien['Thời gian kết thúc'])
            su_kien_trung['Quan trọng'] = "Có" if "Có" in (su_kien_trung['Quan trọng'], su_kien['Quan trọng']) else "Không"
            print("Sự kiện đã được hợp nhất.")
        else:
            print("Sự kiện không được thêm.")
    else:
        lich_trinh_su_kien.append(su_kien)
        print("Sự kiện đã được thêm thành công!")
    luu_du_lieu()

# Xem lịch trình
def xem_lich_trinh():
    print("\n--- LỊCH TRÌNH ---")
    if not lich_trinh_su_kien:
        print("Không có sự kiện nào.")
        return
    for i, su_kien in enumerate(lich_trinh_su_kien, 1):
        print(f"\nSự kiện {i}:")
        for k, v in su_kien.items():
            print(f"  {k}: {v}")

# Chỉnh sửa hoặc xóa sự kiện
def chinh_sua_su_kien():
    print("\n--- CHỈNH SỬA SỰ KIỆN ---")
    if not lich_trinh_su_kien:
        print("Không có sự kiện nào để chỉnh sửa.")
        return
    thang = input("Nhập tháng: ").strip()
    ngay = input("Nhập ngày: ").strip()
    su_kien_theo_ngay = [e for e in lich_trinh_su_kien if e['Tháng'] == thang and e['Ngày'] == ngay]
    
    if not su_kien_theo_ngay:
        print("Không tìm thấy sự kiện nào.")
        return
    
    for i, e in enumerate(su_kien_theo_ngay, 1):
        print(f"{i}. {e['Tên sự kiện']} ({e['Thời gian bắt đầu']} - {e['Thời gian kết thúc']})")
    try:
        chon = int(input("Chọn số sự kiện để chỉnh sửa: ")) - 1
        su_kien = su_kien_theo_ngay[chon]
    except (ValueError, IndexError):
        print("Lựa chọn không hợp lệ.")
        return
    
    print("1. Cập nhật\n2. Xóa")
    lua_chon = input("Chọn: ").strip()
    if lua_chon == "1":
        su_kien.update({k: input(f"Nhập {k} mới (Enter để giữ nguyên '{su_kien[k]}'): ").strip() or su_kien[k] for k in su_kien})
        print("Sự kiện đã được cập nhật.")
    elif lua_chon == "2":
        lich_trinh_su_kien.remove(su_kien)
        print("Sự kiện đã bị xóa.")
    else:
        print("Lựa chọn không hợp lệ.")
    luu_du_lieu()

# Tìm kiếm sự kiện
def tim_kiem_su_kien():
    print("\n--- TÌM KIẾM SỰ KIỆN ---")
    tu_khoa = input("Nhập từ khóa (tên hoặc chi tiết): ").strip().lower()
    ket_qua = [e for e in lich_trinh_su_kien if tu_khoa in e['Tên sự kiện'].lower() or tu_khoa in e['Chi tiết'].lower()]
    if not ket_qua:
        print("Không tìm thấy sự kiện nào.")
        return
    for i, e in enumerate(ket_qua, 1):
        print(f"\nKết quả {i}: {e}")

# Sắp xếp lịch trình
def sap_xep_lich_trinh():
    print("\n--- SẮP XẾP LỊCH TRÌNH ---")
    print("1. Theo ngày\n2. Theo mức độ quan trọng")
    lua_chon = input("Chọn: ").strip()
    if lua_chon == "1":
        lich_trinh_su_kien.sort(key=lambda x: (x['Tháng'], x['Ngày'], x['Thời gian bắt đầu']))
    elif lua_chon == "2":
        lich_trinh_su_kien.sort(key=lambda x: (x['Quan trọng'] != "Có", x['Tháng'], x['Ngày']))
    else:
        print("Lựa chọn không hợp lệ.")
        return
    print("Lịch trình đã được sắp xếp.")
    luu_du_lieu()

# Menu sau đăng nhập
def menu_sau_dang_nhap():
    while True:
        hien_thi_menu("sau_dang_nhap")
        lua_chon = input("Chọn: ").strip()
        if lua_chon == "1":
            them_su_kien()
        elif lua_chon == "2":
            xem_lich_trinh()
        elif lua_chon == "3":
            chinh_sua_su_kien()
        elif lua_chon == "4":
            tim_kiem_su_kien()
        elif lua_chon == "5":
            sap_xep_lich_trinh()
        elif lua_chon == "6":
            print("Đã đăng xuất.")
            break
        else:
            print("Lựa chọn không hợp lệ.")

# Chương trình chính
def chuong_trinh():
    tai_du_lieu()
    while True:
        hien_thi_menu("main")
        lua_chon = input("Chọn: ").strip()
        if lua_chon == "1":
            nguoi_dung = dang_nhap()
            if nguoi_dung:
                menu_sau_dang_nhap()
        elif lua_chon == "2":
            tao_tai_khoan()
        elif lua_chon == "3":
            print("Thoát chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ.")

if __name__ == "__main__":
    chuong_trinh()