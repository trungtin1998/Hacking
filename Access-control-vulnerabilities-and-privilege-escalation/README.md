# Testing for Privilege Escalation

## I. Vertical privilege escalation
Nếu một user có thể truy cập các chức năng mà lẽ ra họ không được phép truy cập, đó được gọi là **vertical privilege escalation**. Chẳng hạn, nếu một standard user có thể truy cập
vào trang admin nơi có thể thực hiện thao tác xóa một tài khoản khác, thì đó được gọi là **vertical privilege escalation**.

### 1. Các chức năng không được bảo vệ
#### a. Giới thiệu
Đây là một dạng tấn công vô cùng đơn giản dựa trên việc ứng dụng không hề bảo vệ nào đối với các chức năng nhạy cảm. Do đó với bất kì user nào cũng có thể truy cập và sử dụng tính năng đó mà không cần quyền admin, chỉ cần có link tới trang đó. Các tính năng quan trọng có thể bị lộ bằng 2 cách khai thác sau:
	* Khai thác file robots.txt
	* Brute force danh sách các endpoint để tìm ra các tính năng ẩn.
#### b. Demo
* Lab: https://portswigger.net/web-security/access-control/lab-unprotected-admin-functionality
* Đề: Trang admin panel không được bảo vệ. Giải lab bằng cách truy cập vào trang này và xóa user `carlos`.
* Cách 1: Khai thác thông tin file robots.txt
	* Truy cập vào trang robots.txt: Phần nội dung chứa liên kết tới trang admin panel
![exploit robots.txt](./Images/1.png)
	* Truy cập trang admin panel và xóa user `carlos`
![remove user](./Images/2.png)
* Cách 2: Brute force danh sách các endpoint 
	* Sử dụng tool dirsearch với URL là trang home của target. Tìm ra được trang admin panel
![brute force using dirsearch](./Images/3.png)

