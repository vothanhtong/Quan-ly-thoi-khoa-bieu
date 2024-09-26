du_lieu_ngoai = []

def hien_thi_menu():
    print("1.Thêm sự kiện mới")
    print("2.Xem lịch trình")
    print("3.Chỉnh sửa sự kiện")
    print("4.Thoát")

def them_su_kien_vao_thoi_khoa_bieu():
    while True:
        su_kien = {}
        su_kien['Tháng'] = input("Nhập tháng: ")
        su_kien['Tuần'] = input("Nhập tuần: ")
        su_kien['Ngày'] = input("Nhập ngày: ")
        su_kien['Thời gian bắt đầu'] = input("Nhập thời gian bắt đầu: ")
        su_kien['Thời gian kết thúc'] = input("Nhập thời gian kết thúc: ")
        su_kien['Tên sự kiện'] = input("Nhập tên sự kiện: ")
        su_kien['Chi tiết sự kiện'] = input("Nhập chi tiết sự kiện: ")
        su_kien['Quan trọng'] = input("Sự kiện có quan trọng không? (Có/Không): ")

        # Kiểm tra sự kiện trùng lặp
        kiem_tra = None
        for event in du_lieu_ngoai:
            if (event['Tháng'] == su_kien['Tháng'] and 
                event['Tuần'] == su_kien['Tuần'] and 
                event['Ngày'] == su_kien['Ngày'] and 
                event['Tên sự kiện'] == su_kien['Tên sự kiện']):
                kiem_tra = event
                break
        
        if kiem_tra:
            print(f"Sự kiện '{su_kien['Tên sự kiện']}' đã tồn tại vào ngày này.")
            lua_chon = input("Bạn muốn hợp nhất sự kiện không? (Có/Không): ").strip().lower()
            if lua_chon == 'có':
                kiem_tra['Chi tiết sự kiện'] += " | " + su_kien['Chi tiết sự kiện']
                kiem_tra['Thời gian bắt đầu'] = min(kiem_tra['Thời gian bắt đầu'], su_kien['Thời gian bắt đầu'])
                kiem_tra['Thời gian kết thúc'] = max(kiem_tra['Thời gian kết thúc'], su_kien['Thời gian kết thúc'])
                kiem_tra['Quan trọng'] = 'Có' if 'Có' in (kiem_tra['Quan trọng'], su_kien['Quan trọng']) else 'Không'
                print("Sự kiện đã được hợp nhất.")
            else:
                print("Sự kiện không được thêm.")
        else:
            du_lieu_ngoai.append(su_kien)
            print(f"\nSự kiện '{su_kien['Tên sự kiện']}' đã được thêm vào lịch trình.\n")
        
        tiep_tuc = input("Bạn có muốn thêm sự kiện khác không? (nhập 'end' để thoát): ") . strip() . lower()
        if tiep_tuc == 'end':
            break

def xem_lich_trinh():
    if not du_lieu_ngoai:
        print("Không có sự kiện nào được lên lịch.")
    else:
        for i, su_kien in enumerate(du_lieu_ngoai, start=1):
            print(f"--- Sự kiện {i} ---")
            print(f"Tháng: {su_kien['Tháng']}")
            print(f"Tuần: {su_kien['Tuần']}")
            print(f"Ngày: {su_kien['Ngày']}")
            print(f"Thời gian bắt đầu: {su_kien['Thời gian bắt đầu']}")
            print(f"Thời gian kết thúc: {su_kien['Thời gian kết thúc']}")
            print(f"Tên sự kiện: {su_kien['Tên sự kiện']}")
            print(f"Chi tiết sự kiện: {su_kien['Chi tiết sự kiện']}")
            print(f"Quan trọng: {su_kien['Quan trọng']}")
            print()

def sua_su_kien():
    if not du_lieu_ngoai:
        print("Không có sự kiện nào để sửa.")
        return

    thang = input("Nhập tháng của sự kiện cần sửa: ")
    tuan = input("Nhập tuần của sự kiện cần sửa: ")
    ngay = input("Nhập ngày của sự kiện cần sửa: ")
    
    found_events = [event for event in du_lieu_ngoai if event['Tháng'] == thang and event['Tuần'] == tuan and event['Ngày'] == ngay]
    
    if not found_events:
        print("Không tìm thấy sự kiện nào vào ngày này.")
        return

    print(" \nCác sự kiện trong ngày đã chọn: ")
    for i, event in enumerate(found_events, start=1):
        print(f"{i}. {event['Tên sự kiện']}")

    try:
        index = int(input("Chọn số của sự kiện bạn muốn chỉnh sửa: ")) - 1
        event = found_events[index]
    except (ValueError,IndexError):
        print("Lựa chọn không hợp lệ.")
        return

    print("\nChọn tùy chọn:")
    print("1. Thêm công việc.")
    print("2. Chỉnh sửa công việc.")
    print("3. Xóa công việc.")
    lua_chon = input("Chọn tùy chọn (1/2/3): ")
    if lua_chon == '1':
        event['Chi tiết sự kiện'] += " | " + input("Nhập chi tiết công việc mới: ")
        print("Công việc đã được thêm.")
    
    elif lua_chon == '2':
        event['Thời gian bắt đầu'] = input("Nhập thời gian bắt đầu mới: ")
        event['Thời gian kết thúc'] = input("Nhập thời gian kết thúc mới: ")
        event['Chi tiết sự kiện'] = input("Nhập chi tiết sự kiện mới: ")
        event['Quan trọng'] = input("Sự kiện này có quan trọng không? (Có/Không): ")
        print("Sự kiện đã được chỉnh sửa.")
    
    elif lua_chon == '3':
        du_lieu_ngoai.remove(event)
        print("Sự kiện đã bị xóa.")
    else:
        print("Tùy chọn không hợp lệ.")

while True:
    hien_thi_menu()
    lua_chon = input("Chọn một tùy chọn (1/2/3/4): ")
    if lua_chon == '1':
        them_su_kien_vao_thoi_khoa_bieu()
    elif lua_chon == '2':
        xem_lich_trinh()
    elif lua_chon == '3':
        sua_su_kien()
    elif lua_chon == '4':
        break
    else:
        print("Lựa chọn không hợp lệ, vui lòng chọn lại.")
