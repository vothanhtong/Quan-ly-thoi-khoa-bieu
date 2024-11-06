# Danh sách toàn cục để lưu dữ liệu sự kiện
lich_trinh_su_kien = []

# Hiển thị các tùy chọn trong menu
def hien_thi_menu():
    print("\n--- MENU ---")
    print("1. Thêm Sự Kiện Mới")
    print("2. Xem Lịch Trình")
    print("3. Chỉnh Sửa Sự Kiện")
    print("4. Thoát")

# Hàm thêm sự kiện mới, với tính năng kiểm tra trùng lặp và hợp nhất nếu cần
def them_su_kien():
    while True:
        su_kien = {
            'Tháng': input("Nhập tháng: "),
            'Tuần': input("Nhập tuần: "),
            'Ngày': input("Nhập ngày: "),
            'Thời gian bắt đầu': input("Nhập thời gian bắt đầu: "),
            'Thời gian kết thúc': input("Nhập thời gian kết thúc: "),
            'Tên sự kiện': input("Nhập tên sự kiện: "),
            'Chi tiết sự kiện': input("Nhập chi tiết sự kiện: "),
            'Quan trọng': input("Sự kiện này có quan trọng không? (Có/Không): ")
        }

        # Kiểm tra sự kiện trùng lặp dựa trên ngày và tên sự kiện
        su_kien_trung_lap = next((e for e in lich_trinh_su_kien if
                                  e['Tháng'] == su_kien['Tháng'] and
                                  e['Tuần'] == su_kien['Tuần'] and
                                  e['Ngày'] == su_kien['Ngày'] and
                                  e['Tên sự kiện'] == su_kien['Tên sự kiện']), None)

        if su_kien_trung_lap:
            print(f"Sự kiện '{su_kien['Tên sự kiện']}' đã tồn tại vào ngày này.")
            lua_chon_hop_nhat = input("Bạn có muốn hợp nhất sự kiện không? (Có/Không): ").strip().lower()
            if lua_chon_hop_nhat == 'có':
                # Hợp nhất thông tin chi tiết nếu người dùng đồng ý
                su_kien_trung_lap['Chi tiết sự kiện'] += " | " + su_kien['Chi tiết sự kiện']
                su_kien_trung_lap['Thời gian bắt đầu'] = min(su_kien_trung_lap['Thời gian bắt đầu'], su_kien['Thời gian bắt đầu'])
                su_kien_trung_lap['Thời gian kết thúc'] = max(su_kien_trung_lap['Thời gian kết thúc'], su_kien['Thời gian kết thúc'])
                su_kien_trung_lap['Quan trọng'] = 'Có' if 'Có' in (su_kien_trung_lap['Quan trọng'], su_kien['Quan trọng']) else 'Không'
                print("Sự kiện đã được hợp nhất.")
            else:
                print("Sự kiện không được thêm.")
        else:
            # Thêm sự kiện mới vào lịch trình nếu không có trùng lặp
            lich_trinh_su_kien.append(su_kien)
            print(f"Sự kiện '{su_kien['Tên sự kiện']}' đã được thêm vào lịch trình.\n")

        # Thoát vòng lặp nếu người dùng không muốn thêm sự kiện khác
        if input("Thêm sự kiện khác? Nhập 'end' để dừng: ").strip().lower() == 'end':
            break

# Hàm để hiển thị tất cả các sự kiện trong lịch trình
def xem_lich_trinh():
    if not lich_trinh_su_kien:
        print("Không có sự kiện nào được lên lịch.")
    else:
        for i, su_kien in enumerate(lich_trinh_su_kien, start=1):
            print(f"\n--- Sự kiện {i} ---")
            for key, value in su_kien.items():
                print(f"{key}: {value}")

# Hàm chỉnh sửa hoặc xóa sự kiện dựa trên ngày cụ thể
def sua_su_kien():
    if not lich_trinh_su_kien:
        print("Không có sự kiện nào để chỉnh sửa.")
        return

    thang, tuan, ngay = input("Nhập tháng: "), input("Nhập tuần: "), input("Nhập ngày: ")

    # Tìm các sự kiện vào ngày đã chọn
    su_kien_theo_ngay = [e for e in lich_trinh_su_kien if e['Tháng'] == thang and e['Tuần'] == tuan and e['Ngày'] == ngay]
    
    if not su_kien_theo_ngay:
        print("Không tìm thấy sự kiện nào vào ngày này.")
        return

    # Hiển thị các sự kiện để người dùng chọn
    print("\nCác sự kiện vào ngày đã chọn:")
    for idx, su_kien in enumerate(su_kien_theo_ngay, start=1):
        print(f"{idx}. {su_kien['Tên sự kiện']}")

    # Kiểm tra lựa chọn của người dùng
    try:
        chi_so_chon = int(input("Chọn số của sự kiện bạn muốn chỉnh sửa: ")) - 1
        su_kien_chon = su_kien_theo_ngay[chi_so_chon]
    except (ValueError, IndexError):
        print("Lựa chọn không hợp lệ.")
        return

    # Menu cho các tùy chọn chỉnh sửa
    print("\n1. Thêm chi tiết\n2. Chỉnh sửa chi tiết\n3. Xóa sự kiện")
    lua_chon = input("Chọn tùy chọn (1/2/3): ").strip()

    if lua_chon == '1':
        su_kien_chon['Chi tiết sự kiện'] += " | " + input("Nhập chi tiết bổ sung: ")
        print("Đã thêm chi tiết.")
    
    elif lua_chon == '2':
        su_kien_chon.update({
            'Thời gian bắt đầu': input("Nhập thời gian bắt đầu mới: "),
            'Thời gian kết thúc': input("Nhập thời gian kết thúc mới: "),
            'Chi tiết sự kiện': input("Nhập chi tiết mới: "),
            'Quan trọng': input("Sự kiện này có quan trọng không? (Có/Không): ")
        })
        print("Sự kiện đã được cập nhật.")

    elif lua_chon == '3':
        lich_trinh_su_kien.remove(su_kien_chon)
        print("Sự kiện đã bị xóa.")
    else:
        print("Tùy chọn không hợp lệ.")

# Vòng lặp chính để tương tác với menu
while True:
    hien_thi_menu()
    lua_chon_nguoi_dung = input("Chọn một tùy chọn (1/2/3/4): ").strip()
    if lua_chon_nguoi_dung == '1':
        them_su_kien()
    elif lua_chon_nguoi_dung == '2':
        xem_lich_trinh()
    elif lua_chon_nguoi_dung == '3':
        sua_su_kien()
    elif lua_chon_nguoi_dung == '4':
        print("Thoát chương trình.")
        break
    else:
        print("Lựa chọn không hợp lệ, vui lòng chọn lại.")



# Các nâng cấp và cải tiến
# Hàm Được Tổ Chức Lại: Mỗi hàm bây giờ chỉ tập trung vào một nhiệm vụ cụ thể, giúp mã nguồn dễ đọc và dễ bảo trì hơn.
# Cải Tiến Kiểm Tra Trùng Lặp: Khi thêm sự kiện, chương trình kiểm tra trùng lặp và cung cấp tùy chọn hợp nhất nếu cần.
# Tương Tác Người Dùng Tốt Hơn: Mỗi tùy chọn trong menu có hướng dẫn rõ ràng, và các lỗi được xử lý để tránh chương trình bị dừng đột ngột.
# Cấu Trúc Dữ Liệu Tối Giản: Các sự kiện được lưu trữ trong dạng từ điển, và việc truy xuất dữ liệu trở nên ngắn gọn và hiệu quả hơn.
# Xử Lý Lỗi: try-except trong hàm sua_su_kien giúp ngăn chặn các lỗi nhập không hợp lệ của người dùng.
# Cơ Chế Vòng Lặp và Thoát: Vòng lặp được tối ưu để thoát chương trình hoặc thoát các vòng lặp cụ thể khi cần thiết.