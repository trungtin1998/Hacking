# Testing for Privilege Escalation

## I. Vertical privilege escalation
Nếu một user có thể truy cập các chức năng mà lẽ ra họ không được phép truy cập, đó được gọi là **vertical privilege escalation**. Chẳng hạn, nếu một standard user có thể truy cập
vào trang admin nơi có thể thực hiện thao tác xóa một tài khoản khác, thì đó được gọi là **vertical privilege escalation**.

### 1. Các chức năng không được bảo vệ
#### a. Giới thiệu
Đây là một dạng tấn công vô cùng đơn giản dựa trên việc ứng dụng không hề có phương pháp bảo vệ nào đối với các chức năng nhạy cảm. Do đó với bất kì user nào cũng có thể truy cập và sử dụng tính năng đó mà không cần quyền admin, chỉ cần có link tới trang đó. Các tính năng quan trọng có thể bị lộ bằng các cách khai thác sau:</br>
* Khai thác file robots.txt
* Brute force danh sách các endpoint để tìm ra các tính năng ẩn.
* Để lộ URL đến các chức năng nhạy cảm trong source code
#### b. Demo
##### *Ví dụ 1: Unprotected admin functionality*
* Lab: https://portswigger.net/web-security/access-control/lab-unprotected-admin-functionality
* *Đề: Trang admin panel không được bảo vệ. Giải lab bằng cách truy cập vào trang này và xóa user `carlos`.*
* Cách 1: Khai thác thông tin file robots.txt
	* Truy cập vào trang robots.txt: Phần nội dung chứa liên kết tới trang admin panel
![exploit robots.txt](./Images/1.png)
	* Truy cập trang admin panel và xóa user `carlos`
![remove user](./Images/2.png)
* Cách 2: Brute force danh sách các endpoint 
	* Sử dụng tool dirsearch với URL là trang home của target. Tìm ra được trang admin panel
![brute force using dirsearch](./Images/3.png)
##### *Ví dụ 2: Unprotected admin functionality with unpredictable URL*
* Lab: https://portswigger.net/web-security/access-control/lab-unprotected-admin-functionality-with-unpredictable-url
* *Đề: Bài lab này không có bất kì phương pháp bảo vệ nào đối với trang admin panel. Trang admin panel rất khó đoán, tuy nhiên thì trang này lại bị để lộ tại một nơi nào đó trong ứng dụng. Giải bài lab này bằng cách truy cập admin panel và xóa user `carlos`*
* Xem source code, ta thấy một thông tin đáng chú ý: Có một script đang xét user có phải là admin hay không để tạo một reference vào trang admin panel:
![unpredictable admin panel](./Images/4.png)
* Truy cập vào trang đó và xóa user `carlos`
![remove user](./Images/5.png)

### 2. Parameter-based access control methods
Một vài ứng dụng xác định quyền hạn/ vai trò của user khi đăng nhập và sau đó lưu trữ thông tin tại nơi mà user có khả năng chỉnh sửa như các trường ẩn, cookie, hoặc là đặt ngay query string parameter. Các bước tiếp theo ứng dụng sẽ quyết định về quyền hạn truy cập dựa trên các giá trị được user submit. Về cơ bản phương pháp này không an toàn bởi vì user có thể dễ dàng thay đổi giá trị và đạt được sự truy cập vào các tính năng mà user này không có quyền sử dụng, chẳng hạn như các chức năng quản trị.
#### *Ví dụ 1: User role controlled by request parameter*
* Lab: https://portswigger.net/web-security/access-control/lab-user-role-controlled-by-request-parameter
* *Đề: Trang admin panel sẽ được đặt tại endpoint /admin, nơi mà xác định có phải là admin hay không thông qua việc sử dụng cookie. Giải bài lab này bằng cách truy cập vào admin panel và sử dụng chúng để xóa tài khoản `carlos`. Credential tài khoản của bạn là `wiener:peter`*. 
* Theo gợi ý, ta sẽ sử dụng credential để đăng nhập vào tài khoản của user `wiener`:
![Login to wiener](./Images/6.png)
* Xem cookie, ta thấy có thể chỉnh sửa cookie để chuyển sang quyền admin. Modify value của trường admin từ `false` thành `true`
![Modify cookie](./Images/7.png)
* Refresh lại trang sau khi modify cookie, ta thấy có reference tới trang admin panel
![Reference tới trang admin panel](./Images/8.png)
* Delete user `carlos` tại trang admin panel
![Remove user](./Images/9.png)
#### *Ví dụ 2: User role can be modified in user profile*
* Lab: https://portswigger.net/web-security/access-control/lab-user-role-can-be-modified-in-user-profile
* *Đề: Bài lab này có trang admin panel tại endpoint /admin. Nó chỉ có thể truy cập bởi trường roleid của user là 2. Giải bài lab này bằng cách truy cập admin panel và xóa tài khoản `carlos`. Bạn có thể đăng nhập vào tài khoản của một standard user với credential như sau: `wiener:peter`*.
* Đầu tiên ta sẽ đi tìm trang có thể cho phép ta modify thông tin user hoặc các vị trí cho phép ta gửi các POST Request. Ta xác định được vị trí đó là trang My Account, cho phép ta update email. Thử update email để xem cấu trúc của gói tin POST Request gửi lên Server để Update Profile user `wiener`:
![original POST Request](./Images/10.png)
![original Response](./Images/11.png)
* Ta phát hiện trong gói tin trả về có trường roleid. Do đó ta có thể lợi dụng để POST Request modify User Profile của wiener khiến cho user này trở thành vai trò admin.
![modified POST Request](./Images/12.png)
* Sau hành động này, user `wiener` đã trở thành user có quyền admin. Truy cập vào trang admin panel và xóa user `carlos`.
![admin panel of wiener by using modifying User Profile](./Images/13.png)
