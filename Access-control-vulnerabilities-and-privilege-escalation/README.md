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
* *Đề: Bài lab này có trang admin panel tại endpoint /admin. Nó chỉ có thể truy cập bởi user có trường `roleid` là 2. Giải bài lab này bằng cách truy cập admin panel và xóa tài khoản `carlos`. Bạn có thể đăng nhập vào tài khoản của một standard user với credential như sau: `wiener:peter`*.
* Đầu tiên ta sẽ đi tìm trang có thể cho phép ta modify thông tin user hoặc các vị trí cho phép ta gửi các POST Request. Ta xác định được vị trí đó là trang My Account, cho phép ta update email. Thử update email để xem cấu trúc của gói tin POST Request gửi lên Server để Update Profile user `wiener`:
![original POST Request](./Images/10.png)
![original Response](./Images/11.png)
* Ta phát hiện trong gói tin trả về có trường roleid. Do đó ta có thể lợi dụng để modify User Profile của user `wiener` khiến cho user này có vai trò admin.
![modified POST Request](./Images/12.png)
* Sau hành động này, user `wiener` đã trở thành user có quyền admin. Truy cập vào trang admin panel và xóa user `carlos`.
![admin panel of wiener by using modifying User Profile](./Images/13.png)

## 3. Broken access control resulting from platform misconfiguration
* Một vài ứng dụng thực thi việc kiểm soát truy cập vào nền tảng bởi việc hạn chế truy cập vào các URL và phương thức HTTP cụ thể dựa trên vai trò của user. 
* Nhiều framework hỗ trợ một vài header non-standard mà có thể được sử dụng để ghi đè vào URL tại các gói tin Request gốc, chẳng hạn `X-Original-URL` và `X-Rewrite-URL`. Nếu website kiểm soát nghiêm ngặt tại front-end để hạn chế sự truy cập dựa trên các URL, nhưng ứng dụng lại cho phép ghi đè thông qua header của gói tin request, nó có thể gây ra lỗi bypass việc kiểm soát truy cập. 
* *Ví dụ 1: URL-based access control can be circumvented*
* Lab: https://portswigger.net/web-security/access-control/lab-url-based-access-control-can-be-circumvented
* *Đề: Website này không xác thực admin panel tại trang /admin, nhưng hệ thống front-end được cấu hình để chặn các truy cập từ bên ngoài đến đường dẫn. Tuy nhiên, ứng dụng back-end được xây dựng sẵn trong framework để hỗ trợ `X-Original-URL` header. Để giải bài lab này, truy cập vào admin panel và xóa user `carlos`*
* Truy cập bằng standard user vào endpoint /admin, ta thấy truy cập bị từ chối.
![access denied](./Images/14.png)
* Sử dụng header `X-Original-URL` gửi kèm trong gói tin GET Request gửi lên server để ghi đè vào, ta có thể truy cập trang admin panel:
![modify Request](./Images/15.png)
![accessable admin panel](./Images/16.png)
* Xóa user `carlos` bằng cách gửi một POST Request lên server:
![remove user](./Images/17.png)
![solved lab](./Images/18.png)

## II. Horizontal privilege escalation
Horizontal privilege escalation phát sinh khi một user có thể truy cập vào các nguồn tài nguyên cùng loại nhưng thuộc về một user khác. Ví dụ như một nhân viên chỉ nên có thể truy cập vào công việc và bảng lương của họ, nhưng họ có thể truy cập vào các record của người khác, đó là hành động Horizontal privilege escalation.
### *Ví dụ 1: User ID controlled by request parameter*
* Lab: https://portswigger.net/web-security/access-control/lab-user-id-controlled-by-request-parameter
* *Đề: Bài lab này làm về lỗ hổng horizontal privilege escalation trên trang My Account. Submit API key của user `carlos` để hoàn thành bài lab này. Tài khoản của bạn là `wiener:peter`*
* Một ví dụ đơn giản về việc thay đổi User ID để truy cập vào tài nguyên của người khác. Chuyển trường `id` từ `wiener` sang `carlos` để có thể xem được `API key` của user `carlos`
![ID weiner](./Images/19.png)
![ID carlos](./Images/20.png)

* Trong một số ứng dụng, giá trị của các parameter có thể không thể đoán được. Ví dụ thay vì sử dụng số theo thứ tự tăng dần hoặc tên của user, ứng dụng có thể sử dụng globally unique identifiers (GUID) để định danh người dùng. Do đó Attacker rất khó đoán được định danh của người dùng khác. Tuy nhiên có thể GUID thuộc về người dùng khác có thể bị lộ ở một nơi nào đó trong ứng dụng, có thể giúp cho việc tấn công Horizontal privilege escalation có thể xảy ra.
### *Ví dụ 2: User ID controlled by request parameter, with unpredictable user IDs*
* Lab: https://portswigger.net/web-security/access-control/lab-user-id-controlled-by-request-parameter-with-unpredictable-user-ids
* *Đề: Bài lab này có lỗ hổng horizontal privilege escalation tại trang My Account, nhưng được định danh người dùng bởi GUID. Để giải bài lab này, tìm ra GUID cho user `carlos`, sau đó submit API Key của user này như kết quả. Tài khoản của bạn là ` wiener:peter`*
* Tại bài post số 3 - Procrastination, bài được viết bởi tác giả `carlos`. Ta có thể xem `userid` của user này bằng cách xem source code hoặc click vào tên tác giả.
![click username](./Images/21.png)
![GUID của carlos](./Images/22.png)
* Sau khi có `userid` của `carlos`, ta có vào trang My Account để tiến hành các tấn công Horizontal privilege escalation:
![GUID của wiener](./Images/23.png)
![GUID của carlos](./Images/24.png)