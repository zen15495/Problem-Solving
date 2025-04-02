import csv

class Seat:
    def __init__(self, seat_number):
        self.seat_number = seat_number
        self.is_booked = False
        self.student_id = None
        self.student_name = None

    def book(self, student_id, student_name):
        if not self.is_booked:
            self.is_booked = True
            self.student_id = student_id
            self.student_name = student_name
            return True
        return False

    def cancel(self):
        if self.is_booked:
            self.is_booked = False
            self.student_id = None
            self.student_name = None
            return True
        return False

    def to_dict(self):
        return {
            "seat_number": self.seat_number,
            "is_booked": self.is_booked,
            "student_id": self.student_id or "",
            "student_name": self.student_name or ""
        }

class Booking:
    def __init__(self, total_seats=25, filename="seats.csv"):
        self.seats = [Seat(i + 1) for i in range(total_seats)]
        self.filename = filename
        self.load_data()

    def display_seats(self):
        print("\nผังที่นั่งสอบ:")
        print("+" + "-" * 25 + "+")
        for seat in self.seats:
            status = "X" if seat.is_booked else "O"
            print(status, end=" ")
        print("\n+" + "-" * 25 + "+")
        
    def booked_seat(self, seat_number, student_id, student_name):
        if 1 <= seat_number <= len(self.seats):
            if self.seats[seat_number - 1].book(student_id, student_name):
                self.save_data()
                return "จองที่นั่งสำเร็จ!"
            else:
                return "ที่นั่งนี้ถูกจองไปแล้ว!"
        return "หมายเลขที่นั่งไม่ถูกต้อง!"

    def cancel_booking(self, seat_number):
        if 1 <= seat_number <= len(self.seats):
            if self.seats[seat_number - 1].cancel():
                self.save_data()
                return "ยกเลิกการจองสำเร็จ!"
            else:
                return "ที่นั่งนี้ยังไม่ได้ถูกจอง!"
        return "หมายเลขที่นั่งไม่ถูกต้อง!"

    def get_available_seats(self):
        return [seat.seat_number for seat in self.seats if not seat.is_booked]

    def get_booked_seats(self):
        return [(seat.seat_number, seat.student_name) for seat in self.seats if seat.is_booked]

    def save_data(self):
        with open(self.filename, "w", newline="", encoding="utf-8") as file:  # แก้ไข encoding เป็น utf-8
            writer = csv.DictWriter(file, fieldnames=["seat_number", "is_booked", "student_id", "student_name"])
            writer.writeheader()
            for seat in self.seats:
                writer.writerow(seat.to_dict())

    def load_data(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:  # แก้ไข encoding เป็น utf-8
                reader = csv.DictReader(file)
                for row in reader:
                    seat = self.seats[int(row["seat_number"]) - 1]
                    seat.is_booked = row["is_booked"] == "True"
                    seat.student_id = row["student_id"] or None
                    seat.student_name = row["student_name"] or None
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    booking_system = Booking()
    while True:
        print("\nเมนู:")
        print("1. แสดงที่นั่งทั้งหมด")
        print("2. แสดงที่นั่งว่าง")
        print("3. แสดงที่นั่งที่ถูกจอง")
        print("4. จองที่นั่ง")
        print("5. ยกเลิกการจอง")
        print("6. ออกจากโปรแกรม")
        choice = input("เลือกเมนู: ")

        if choice == "1":
            booking_system.display_seats()
        elif choice == "2":
            print("ที่นั่งว่าง:", booking_system.get_available_seats())
        elif choice == "3":
            print("ที่นั่งที่ถูกจอง:", booking_system.get_booked_seats())
        elif choice == "4":
            seat_number = int(input("กรอกหมายเลขที่นั่ง: "))
            student_id = input("กรอกรหัสนักศึกษา: ")
            student_name = input("กรอกชื่อนักศึกษา: ")
            print(booking_system.booked_seat(seat_number, student_id, student_name))
        elif choice == "5":
            seat_number = int(input("กรอกหมายเลขที่นั่งที่ต้องการยกเลิก: "))
            print(booking_system.cancel_booking(seat_number))
        elif choice == "6":
            print("ออกจากโปรแกรม...")
            break
        else:
            print("ตัวเลือกไม่ถูกต้อง! กรุณาลองใหม่อีกครั้ง")
