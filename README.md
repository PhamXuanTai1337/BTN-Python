# Hướng dẫn sử dụng máy tính PyQt6

File chương trình: `may_tinh_vibe_code.py`. Ứng dụng tính biểu thức với bốn phép cộng, trừ, nhân, chia và dấu ngoặc.

## Cài đặt và mở ứng dụng trên Windows

1. Đặt file Python vào một thư mục rồi mở thư mục đó trong File Explorer.
2. Bấm vào **thanh địa chỉ** ở phía trên, gõ `cmd` và nhấn Enter. Cửa sổ CMD sẽ mở ngay trong thư mục chứa file.
3. Trong cửa sổ CMD, chạy lần lượt:

```cmd
py -m pip install PyQt6
py "may_tinh_vibe_code.py"
```

Nếu CMD không nhận lệnh `py`, thay `py` bằng `python`. Nếu bạn đã đổi tên file, hãy dùng đúng tên mới trong lệnh chạy; ví dụ: `py may_tinh_vibe_code.py`.

## Cách sử dụng

- Nhập biểu thức trực tiếp vào ô phía trên **hoặc** bấm các phím số và phép tính trên giao diện.
- Bấm `=` hoặc nhấn **Enter** khi con trỏ đang ở ô nhập để xem kết quả.
- Dùng `+`, `−`, `×`, `÷` để cộng, trừ, nhân, chia. Dùng `(` và `)` để nhóm phép tính.
- Bấm `C` để xóa toàn bộ biểu thức và kết quả; bấm `DEL` để xóa ký tự ngay trước con trỏ.
- Có thể nhập số thập phân bằng dấu chấm hoặc dấu phẩy, ví dụ `1,5+2`.

Ví dụ để thử:

| Nhập | Kết quả |
| --- | ---: |
| `12+3` | `15` |
| `12/3` | `4` |
| `(2+3)*4` | `20` |
| `0.1+0.2` | `0.3` |

Nếu nhập sai như `1+` hoặc `abc`, ứng dụng sẽ báo biểu thức không hợp lệ. Phép tính `1/0` sẽ báo không thể chia cho 0. Kết quả vượt giới hạn tính toán cũng được báo lỗi.
