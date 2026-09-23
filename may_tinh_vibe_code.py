"""Máy tính nhập biểu thức, bản xây dựng với sự hỗ trợ của AI."""

import ast
from decimal import Decimal, DivisionByZero, InvalidOperation, Overflow, localcontext
import math
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


def tinh_bieu_thuc(bieu_thuc):
    bieu_thuc = bieu_thuc.strip().replace(",", ".").replace("×", "*").replace("÷", "/")
    if not bieu_thuc:
        raise ValueError("Hãy nhập phép tính.")
    if len(bieu_thuc) > 200:
        raise ValueError("Biểu thức quá dài (tối đa 200 ký tự).")

    try:
        cay = ast.parse(bieu_thuc, mode="eval")
    except (SyntaxError, ValueError, RecursionError) as loi:
        raise ValueError("Biểu thức không hợp lệ.") from loi

    def tinh_nut(nut):
        if isinstance(nut, ast.Constant) and type(nut.value) in (int, float):
            if isinstance(nut.value, float) and not math.isfinite(nut.value):
                raise ValueError("Số nhập vượt giới hạn tính toán.")
            chu_so = ast.get_source_segment(bieu_thuc, nut)
            try:
                so = Decimal(chu_so if chu_so is not None else str(nut.value))
            except InvalidOperation as loi:
                raise ValueError("Số nhập không hợp lệ.") from loi
            if not so.is_finite():
                raise ValueError("Số nhập không hợp lệ.")
            return so

        if isinstance(nut, ast.UnaryOp):
            so = tinh_nut(nut.operand)
            if isinstance(nut.op, ast.UAdd):
                return so
            if isinstance(nut.op, ast.USub):
                return -so

        if isinstance(nut, ast.BinOp):
            trai = tinh_nut(nut.left)
            phai = tinh_nut(nut.right)
            if isinstance(nut.op, ast.Add):
                return trai + phai
            if isinstance(nut.op, ast.Sub):
                return trai - phai
            if isinstance(nut.op, ast.Mult):
                return trai * phai
            if isinstance(nut.op, ast.Div):
                if phai == 0:
                    raise ZeroDivisionError("Không thể chia cho 0.")
                return trai / phai

        raise ValueError("Chỉ hỗ trợ số, ngoặc và bốn phép tính + - * /.")

    try:
        with localcontext() as boi_canh:
            boi_canh.prec = 28
            boi_canh.Emax = 308
            boi_canh.Emin = -308
            ket_qua = tinh_nut(cay.body)
            if not ket_qua.is_finite():
                raise ArithmeticError("Kết quả vượt giới hạn tính toán.")
            if ket_qua.is_zero():
                return "0"
            ket_qua = ket_qua.normalize()
            if -6 <= ket_qua.adjusted() < 16:
                return format(ket_qua, "f")
            return str(ket_qua)
    except DivisionByZero as loi:
        raise ZeroDivisionError("Không thể chia cho 0.") from loi
    except (Overflow, InvalidOperation) as loi:
        raise ArithmeticError("Kết quả vượt giới hạn tính toán.") from loi


class MayTinhVibe(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Máy tính cá nhân - bản vibe code")
        self.setMinimumSize(350, 470)

        tieu_de = QLabel("MÁY TÍNH CÁ NHÂN")
        tieu_de.setObjectName("tieuDe")

        self.bieu_thuc = QLineEdit()
        self.bieu_thuc.setObjectName("bieuThuc")
        self.bieu_thuc.setPlaceholderText("Nhập phép tính hoặc nhấn các nút")
        self.bieu_thuc.setMaxLength(200)
        self.bieu_thuc.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.bieu_thuc.returnPressed.connect(self.tinh)

        self.ket_qua = QLabel("Kết quả sẽ hiện ở đây")
        self.ket_qua.setObjectName("ketQua")
        self.ket_qua.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.ket_qua.setWordWrap(True)

        luoi = QGridLayout()
        luoi.setSpacing(9)
        cac_hang = [
            ["C", "DEL", "(", ")"],
            ["7", "8", "9", "÷"],
            ["4", "5", "6", "×"],
            ["1", "2", "3", "−"],
            ["0", ".", "=", "+"],
        ]
        for hang, cac_nut in enumerate(cac_hang):
            for cot, ky_tu in enumerate(cac_nut):
                nut = QPushButton(ky_tu)
                nut.setMinimumHeight(58)
                if ky_tu == "=":
                    nut.setObjectName("bang")
                    nut.clicked.connect(self.tinh)
                elif ky_tu == "C":
                    nut.clicked.connect(self.xoa)
                elif ky_tu == "DEL":
                    nut.clicked.connect(self.xoa_mot_ky_tu)
                else:
                    nut.clicked.connect(lambda checked=False, ky_tu=ky_tu: self.them(ky_tu))
                luoi.addWidget(nut, hang, cot)

        bo_cuc = QVBoxLayout(self)
        bo_cuc.setContentsMargins(20, 20, 20, 20)
        bo_cuc.setSpacing(16)
        bo_cuc.addWidget(tieu_de)
        bo_cuc.addWidget(self.bieu_thuc)
        bo_cuc.addWidget(self.ket_qua)
        bo_cuc.addLayout(luoi)

        self.setStyleSheet("""
            QWidget { background: #111827; color: #f9fafb; font-size: 17px; }
            QLabel#tieuDe { color: #a5b4fc; font-size: 19px; font-weight: bold; }
            QLineEdit#bieuThuc {
                background: #1f2937; border: 1px solid #4b5563;
                border-radius: 10px; padding: 12px; font-size: 22px;
            }
            QLabel#ketQua { min-height: 40px; font-size: 20px; }
            QPushButton { background: #374151; border: 0; border-radius: 10px; }
            QPushButton:hover { background: #4b5563; }
            QPushButton:pressed { background: #6b7280; }
            QPushButton#bang { background: #6366f1; font-weight: bold; }
            QPushButton#bang:hover { background: #4f46e5; }
        """)

    def them(self, ky_tu):
        if ky_tu == "−":
            ky_tu = "-"
        self.bieu_thuc.insert(ky_tu)
        self.bieu_thuc.setFocus()

    def xoa(self):
        self.bieu_thuc.clear()
        self.ket_qua.setText("Kết quả sẽ hiện ở đây")
        self.bieu_thuc.setFocus()

    def xoa_mot_ky_tu(self):
        self.bieu_thuc.backspace()
        self.bieu_thuc.setFocus()

    def tinh(self):
        try:
            ket_qua = tinh_bieu_thuc(self.bieu_thuc.text())
        except (ValueError, ZeroDivisionError, ArithmeticError) as loi:
            self.ket_qua.setStyleSheet("color: #fca5a5;")
            self.ket_qua.setText(str(loi))
        else:
            self.ket_qua.setStyleSheet("color: #86efac;")
            self.ket_qua.setText(f"= {ket_qua}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    cua_so = MayTinhVibe()
    cua_so.show()
    sys.exit(app.exec())
