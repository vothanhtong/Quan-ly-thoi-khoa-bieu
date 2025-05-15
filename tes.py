/*
Dự án: Ứng dụng quản lý lịch trình trên web (chạy localhost)
Ngôn ngữ chính: Python (Flask)
Giao diện: HTML và CSS
Cơ sở dữ liệu đơn giản: file JSON để lưu trữ sự kiện

Cấu trúc thư mục:

schedule_app/
├── app.py                  # Server Flask
├── data/
│   └── events.json         # "Database" lưu trữ sự kiện dưới dạng JSON
├── templates/
│   ├── index.html          # Trang chính hiển thị menu và liên kết
│   ├── add_event.html      # Form thêm sự kiện
│   ├── view_schedule.html  # Hiển thị lịch trình
│   └── edit_event.html     # Form chỉnh sửa sự kiện

└── static/
    └── style.css           # CSS chung

1. Sử dụng Flask để tạo server đơn giản chạy trên localhost: http://127.0.0.1:5000
2. Các route tương ứng:
   - `/`             : Trang menu chính
   - `/add`         : Form thêm sự kiện + xử lý POST
   - `/view`        : Hiển thị tất cả sự kiện
   - `/edit/<int:id>`: Form sửa hoặc xóa sự kiện theo id
   - `/static/style.css`: CSS style

3. Cách hoạt động của "database" JSON:
   - Mỗi sự kiện là một object trong mảng events.json:
     {
       "id": 1,
       "month": "5",
       "week": "2",
       "day": "15",
       "start": "10:00",
       "end": "11:00",
       "title": "Họp nhóm",
       "details": "Thảo luận dự án",
       "important": "Có"
     }
   - Khi thêm, đọc file, thêm object mới (tự tăng id), ghi lại file.
   - Khi sửa hoặc xóa, đọc file, thay đổi mảng, ghi lại file.

Các bạn chỉ cần cài Flask (`pip install flask`) và chạy `python app.py` để bắt đầu.

---
# app.py
```python
from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
data_file = os.path.join(os.path.dirname(__file__), 'data', 'events.json')

# Đọc dữ liệu JSON
def read_events():
    if not os.path.exists(data_file):
        return []
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)

# Ghi dữ liệu JSON
def write_events(events):
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(events, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_event():
    events = read_events()
    if request.method == 'POST':
        new_id = max([e['id'] for e in events], default=0) + 1
        event = {
            'id': new_id,
            'month': request.form['month'],
            'week': request.form['week'],
            'day': request.form['day'],
            'start': request.form['start'],
            'end': request.form['end'],
            'title': request.form['title'],
            'details': request.form['details'],
            'important': request.form.get('important', 'Không')
        }
        events.append(event)
        write_events(events)
        return redirect(url_for('view_schedule'))
    return render_template('add_event.html')

@app.route('/view')
def view_schedule():
    events = read_events()
    return render_template('view_schedule.html', events=events)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_event(id):
    events = read_events()
    event = next((e for e in events if e['id'] == id), None)
    if not event:
        return 'Không tìm thấy sự kiện', 404
    if request.method == 'POST':
        if 'delete' in request.form:
            events = [e for e in events if e['id'] != id]
        else:
            event.update({
                'month': request.form['month'],
                'week': request.form['week'],
                'day': request.form['day'],
                'start': request.form['start'],
                'end': request.form['end'],
                'title': request.form['title'],
                'details': request.form['details'],
                'important': request.form.get('important', 'Không')
            })
        write_events(events)
        return redirect(url_for('view_schedule'))
    return render_template('edit_event.html', event=event)

if __name__ == '__main__':
    app.run(debug=True)
```

# templates/index.html
```html
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="/static/style.css">
  <title>Quản lý lịch trình</title>
</head>
<body>
  <div class="menu">
    <h1>Quản lý lịch trình</h1>
    <ul>
      <li><a href="/add">Thêm sự kiện mới</a></li>
      <li><a href="/view">Xem lịch trình</a></li>
    </ul>
  </div>
</body>
</html>
```

# static/style.css
```css
body { font-family: Arial, sans-serif; background: #f4f4f4; margin: 0; padding: 0; }
.menu { text-align: center; padding: 50px; }
a { text-decoration: none; color: #333; font-size: 1.2em; }
