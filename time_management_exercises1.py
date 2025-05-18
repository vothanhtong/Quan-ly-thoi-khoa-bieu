import json
from datetime import datetime, timedelta
import uuid

class Event:
    def __init__(self, date_time_start: datetime, date_time_end: datetime, title: str,
                 details: str = "", important: bool = False, event_id: str = None):
        self.id = event_id or str(uuid.uuid4())
        self.start = date_time_start
        self.end = date_time_end
        self.title = title
        self.details = details
        self.important = important

    def to_dict(self):
        return {
            "id": self.id,
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
            "title": self.title,
            "details": self.details,
            "important": self.important
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            date_time_start=datetime.fromisoformat(data["start"]),
            date_time_end=datetime.fromisoformat(data["end"]),
            title=data["title"],
            details=data.get("details", ""),
            important=data.get("important", False),
            event_id=data.get("id")
        )

class CalendarManager:
    ACCOUNTS_FILE = "tai_khoan.json"
    EVENTS_FILE = "lich_trinh.json"

    def __init__(self):
        self.users = {}          # username -> password
        self.events = []         # list of Event
        self.current_user = None
        self.load_data()

    def load_data(self):
        try:
            with open(self.ACCOUNTS_FILE, 'r', encoding='utf-8') as f:
                self.users = json.load(f)
        except FileNotFoundError:
            print("No accounts file found. Starting fresh.")

        try:
            with open(self.EVENTS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.events = [Event.from_dict(e) for e in data]
        except FileNotFoundError:
            print("No events file found. Starting fresh.")

    def save_data(self):
        with open(self.ACCOUNTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, ensure_ascii=False, indent=4)
        with open(self.EVENTS_FILE, 'w', encoding='utf-8') as f:
            json.dump([e.to_dict() for e in self.events], f, ensure_ascii=False, indent=4)

    def register(self):
        username = input("Tên đăng nhập: ").strip()
        if username in self.users:
            print("Tên đăng nhập đã tồn tại.")
            return
        password = input("Mật khẩu: ").strip()
        confirm = input("Xác nhận mật khẩu: ").strip()
        if password != confirm:
            print("Mật khẩu không khớp.")
            return
        self.users[username] = password
        self.save_data()
        print("Đăng ký thành công!")

    def login(self):
        username = input("Tên đăng nhập: ").strip()
        password = input("Mật khẩu: ").strip()
        if self.users.get(username) == password:
            self.current_user = username
            print(f"Chào mừng {username}!")
        else:
            print("Sai tên hoặc mật khẩu.")

    def _parse_date_time(self, date_str, time_str):
        return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")

    def add_event(self):
        print("--- Thêm sự kiện ---")
        date = input("Ngày (YYYY-MM-DD): ").strip()
        start = input("Thời gian bắt đầu (HH:MM): ").strip()
        end = input("Thời gian kết thúc (HH:MM): ").strip()
        title = input("Tên sự kiện: ").strip()
        details = input("Chi tiết: ").strip()
        important = input("Quan trọng? (y/N): ").strip().lower() == 'y'

        try:
            dt_start = self._parse_date_time(date, start)
            dt_end = self._parse_date_time(date, end)
            if dt_start >= dt_end:
                raise ValueError("Thời gian bắt đầu phải trước thời gian kết thúc.")
        except ValueError as e:
            print(f"Lỗi định dạng: {e}")
            return

        # Check for duplicates
        for e in self.events:
            if e.start == dt_start and e.title == title and self.current_user == e.title:
                print("Sự kiện đã tồn tại.")
                return

        new_event = Event(dt_start, dt_end, title, details, important)
        self.events.append(new_event)
        self.save_data()
        print("Đã thêm sự kiện.")

    def list_events(self, sort_by='date'):
        print("--- Lịch trình ---")
        if not self.events:
            print("Chưa có sự kiện nào.")
            return
        if sort_by == 'date':
            sorted_events = sorted(self.events, key=lambda e: (e.start, not e.important))
        else:
            sorted_events = sorted(self.events, key=lambda e: (not e.important, e.start))
        for e in sorted_events:
            imp = '!' if e.important else ''
            print(f"[{e.id}] {e.start} - {e.end} {imp}\n    {e.title}: {e.details}")

    def find_events(self):
        kw = input("Tìm kiếm (từ khóa): ").strip().lower()
        results = [e for e in self.events if kw in e.title.lower() or kw in e.details.lower()]
        if not results:
            print("Không tìm thấy sự kiện.")
            return
        for e in results:
            print(f"[{e.id}] {e.start} - {e.end}\n    {e.title}: {e.details}")

    def edit_event(self):
        event_id = input("Nhập ID sự kiện cần sửa: ").strip()
        event = next((e for e in self.events if e.id == event_id), None)
        if not event:
            print("Không tìm thấy sự kiện.")
            return
        print("1. Cập nhật\n2. Xóa")
        choice = input("Chọn: ").strip()
        if choice == '1':
            new_title = input(f"Tên ({event.title}): ").strip() or event.title
            new_details = input(f"Chi tiết ({event.details}): ").strip() or event.details
            new_imp = input(f"Quan trọng ({'y' if event.important else 'n'}): ").strip().lower()
            event.title = new_title
            event.details = new_details
            if new_imp in ('y','n'):
                event.important = (new_imp == 'y')
            print("Đã cập nhật.")
        elif choice == '2':
            self.events.remove(event)
            print("Đã xóa sự kiện.")
        else:
            print("Lựa chọn không hợp lệ.")
        self.save_data()

    def upcoming(self, days=7):
        now = datetime.now()
        future = now + timedelta(days=days)
        upcoming = [e for e in self.events if now <= e.start <= future]
        print(f"--- Sự kiện trong {days} ngày tới ---")
        for e in sorted(upcoming, key=lambda e: e.start):
            print(f"{e.start.date()}: {e.title} at {e.start.time()}")

    def main_menu(self):
        while True:
            print("1. Đăng nhập\n2. Đăng ký\n3. Thoát")
            c = input("Chọn: ").strip()
            if c == '1':
                self.login()
                if self.current_user:
                    self.user_menu()
            elif c == '2':
                self.register()
            elif c == '3':
                break

    def user_menu(self):
        while True:
            print("1.Thêm\n2.Xem\n3.Tìm\n4.Sửa/Xóa\n5.Sắp xếp\n6.Sắp tới\n7.Đăng xuất")
            c = input("Chọn: ").strip()
            if c == '1': self.add_event()
            elif c == '2': self.list_events()
            elif c == '3': self.find_events()
            elif c == '4': self.edit_event()
            elif c == '5': self.list_events(sort_by='importance')
            elif c == '6': self.upcoming()
            elif c == '7':
                self.current_user = None
                break
            else:
                print("Không hợp lệ.")

if __name__ == '__main__':
    cm = CalendarManager()
    cm.main_menu()