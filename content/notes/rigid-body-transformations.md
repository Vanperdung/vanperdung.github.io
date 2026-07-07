+++
title       = 'Bài học chi tiết: Phép biến đổi vật rắn'
date        = '2026-07-08T00:00:00+07:00'
draft       = false
description = 'Bài học về rigid body, pose, ma trận quay và ma trận biến đổi thuần nhất.'
tags        = ['Robotics', 'Rigid Body', 'Transformations']
math        = true
+++

# Bài học chi tiết: Phép biến đổi vật rắn (Rigid-Body Transformations)

> **Phạm vi học:** Tài liệu này tổng hợp và mở rộng nội dung từ slide 1 đến slide 21 của bài *MEAM 620: Rigid Body Transformations*. Các thuật ngữ chuyên ngành được viết bằng tiếng Việt và kèm tiếng Anh trong ngoặc ở lần đầu xuất hiện.
>
> **Quy ước quan trọng:** Trong tài liệu này, ký hiệu \({}^{A}\) ở bên trái một vector hoặc ma trận cho biết đại lượng được **biểu diễn trong frame A**. Chỉ số dưới thường chỉ frame hoặc đối tượng được mô tả.

---

## Mục tiêu sau khi học

Sau khi hoàn thành phần này, bạn cần có thể làm được bốn việc. Thứ nhất, mô tả một vật rắn bằng vị trí và hướng của một frame gắn với vật. Thứ hai, đọc đúng ý nghĩa của ký hiệu frame trong các biểu thức như \({}^{A}\mathbf{R}_{B}\) và \({}^{A}\mathbf{o}_{B}\). Thứ ba, sử dụng ma trận quay (rotation matrix) để đổi tọa độ, mô tả orientation hoặc quay trực tiếp một vector. Cuối cùng, ghép quay và tịnh tiến vào ma trận biến đổi thuần nhất (homogeneous transformation matrix) để mô tả pose đầy đủ và ghép chuỗi biến đổi qua nhiều frame.

Một nguyên tắc xuyên suốt là: **đừng nhìn công thức chỉ như một phép nhân ma trận. Hãy luôn xác định đại lượng đang được biểu diễn trong frame nào, phép quay xảy ra quanh trục nào, và vector đang là điểm hay vector hướng.** Nếu ba câu hỏi này được trả lời rõ, phần lớn lỗi trong rigid-body transformations sẽ biến mất.

---

# Phần 1. Trực giác về vật rắn, pose và rigid-body transformation

## 1.1. Vật rắn là gì?

Một **vật rắn** (rigid body) là một vật mà ta giả sử không biến dạng trong quá trình chuyển động. Giả sử trên vật có hai điểm bất kỳ P và Q. Khi vật chuyển động, khoảng cách giữa chúng phải luôn giữ nguyên:

\[
\|P-Q\| = \|P'-Q'\|.
\]

Nói cách khác, vật có thể bay đi, xoay đi, nghiêng đi hoặc lật đi, nhưng không được kéo dài, thu ngắn hoặc bẻ cong. Trong bài toán robotics, một drone, một camera gắn trên drone, một link của robot arm hoặc một end-effector thường được mô hình hóa như rigid body. Đây là một lý tưởng hóa rất hữu ích, vì nó giúp ta tập trung vào chuyển động hình học thay vì phải mô hình hóa biến dạng đàn hồi của vật.

Một rigid body trong không gian ba chiều có sáu bậc tự do (degrees of freedom). Ba bậc đầu tiên đến từ việc nó có thể tịnh tiến theo ba hướng; ba bậc còn lại đến từ việc nó có thể thay đổi orientation. Vì vậy, để biết hoàn toàn trạng thái hình học của vật, ta không thể chỉ cho một tọa độ vị trí duy nhất.

## 1.2. Position, orientation và pose

**Vị trí** (position) trả lời câu hỏi: một điểm chuẩn trên vật đang ở đâu? Thông thường, điểm chuẩn này được chọn là gốc của body frame hoặc tâm khối lượng. Nếu gốc body frame ở tọa độ (2,1,3) trong world frame, thì ta biết vị trí của vật theo quy ước đó.

**Hướng** (orientation) trả lời câu hỏi: hệ trục gắn với vật đang quay như thế nào so với một hệ trục tham chiếu? Chỉ một điểm không thể cho ta information về orientation, vì một điểm không có hướng. Muốn biết drone đang hướng về đâu, ta phải quan sát các trục gắn với drone: ví dụ trục hướng ra mũi, trục hướng sang phải và trục vuông góc với mặt phẳng thân drone.

Khi ghép hai thông tin lại, ta có **pose**:

\[
\boxed{
\text{pose} = \text{position} + \text{orientation}.
}
\]

Pose là khái niệm cơ bản nhất trong phần này. Hai drone có thể ở cùng vị trí nhưng khác pose nếu chúng hướng khác nhau. Ngược lại, chúng có thể cùng orientation nhưng khác pose nếu ở hai vị trí khác nhau.

![Slide 3 – Ví dụ drone vừa tịnh tiến vừa đổi hướng](/images/rigid_body_slide_03.png)

*Slide 3. Cùng một drone xuất hiện ở nhiều thời điểm. Mũi tên xanh gợi ý phần tịnh tiến, còn các góc nghiêng khác nhau thể hiện phần quay.*

![Slide 4 – Cùng rigid body ở hai pose khác nhau](/images/rigid_body_slide_04.png)

*Slide 4. Hình dạng drone được giữ nguyên, nhưng vị trí và orientation thay đổi. Đây là rigid-body motion, không phải biến dạng.*

## 1.3. Phép biến đổi vật rắn gồm hai thành phần

Một **phép biến đổi vật rắn** (rigid-body transformation) đưa rigid body từ pose đầu sang pose cuối. Về bản chất, nó có hai phần: một rotation matrix và một translation vector.

\[
\boxed{\mathbf{p}_{\mathrm{new}}=\mathbf{R}\mathbf{p}+\mathbf{t}}
\]

Trong công thức này, \(\mathbf{R}\) giữ khoảng cách và góc giữa các điểm, còn \(\mathbf{t}\) dịch toàn bộ vật. Dấu \(+\) không có nghĩa rotation và translation là hai số cùng loại. Nó có nghĩa: sau khi điểm được quay, ta cộng thêm translation vector.

**Phép quay** (rotation) đổi hướng các trục của body frame. Nó làm thay đổi cách vật nhìn về các hướng trong không gian, nhưng không thay đổi khoảng cách giữa các điểm trên vật. **Phép tịnh tiến** (translation) dịch toàn bộ vật sang một vị trí khác mà không tự nó làm thay đổi orientation.

Ví dụ, một drone bay tiến về trước thường không chỉ translation. Để tạo gia tốc ngang, drone thường pitch; do đó, orientation cũng đổi. Đây là lý do rigid-body transformation là ngôn ngữ tự nhiên để mô tả các hệ robot bay, robot tay máy, camera và cảm biến.

### Tóm tắt phần 1

Rigid body là vật giữ nguyên hình dạng. Pose gồm position và orientation. Một rigid-body transformation mô tả thay đổi pose bằng cách kết hợp rotation và translation.

---

# Phần 2. Hệ quy chiếu (Reference Frame) và tọa độ vector

## 2.1. Vì sao phải có reference frame?

Một câu như “điểm này ở tọa độ (1,2,0)” vẫn chưa đầy đủ nếu ta không nói tọa độ đó được đo theo hệ trục nào. Trong robotics, mọi position, velocity, force, acceleration, orientation hoặc angular velocity đều phải đi kèm một frame để xác định ý nghĩa.

Một **hệ quy chiếu** (reference frame) trong không gian 3D gồm:

- một gốc tọa độ;
- ba trục định hướng;
- một quy ước chiều dương của từng trục.

Ta dùng frame A làm ví dụ. Ba vector cơ sở của nó được ký hiệu là:

\[
\mathbf{a}_1,\qquad \mathbf{a}_2,\qquad \mathbf{a}_3.
\]

Tương tự, frame B có các vector cơ sở:

\[
\mathbf{b}_1,\qquad \mathbf{b}_2,\qquad \mathbf{b}_3.
\]

Trong hình học robotics cơ bản, các frame này là **trực chuẩn** (orthonormal). Điều đó có hai tầng ý nghĩa. “Trực” (orthogonal) nghĩa là các trục vuông góc từng đôi một. “Chuẩn” (normal) nghĩa là mỗi trục có độ dài bằng một.

\[
\|\mathbf{a}_i\|=1,
\qquad
\mathbf{a}_i^T\mathbf{a}_j=0\quad (i\ne j).
\]

Các điều kiện tương tự cũng áp dụng cho \(\mathbf{b}_1,\mathbf{b}_2,\mathbf{b}_3\).

![Slide 5 – Hệ quy chiếu A và B](/images/rigid_body_slide_05.png)

*Slide 5. Frame A có các basis vectors màu đỏ; frame B có các basis vectors màu xanh. Vector \(\mathbf{v}\) là một đối tượng hình học trong không gian, còn các tọa độ của nó phụ thuộc frame được chọn.*

## 2.2. Vector vật lý và vector tọa độ là hai thứ khác nhau

Đây là một trong những phân biệt quan trọng nhất của toàn bài. Một **vector vật lý** là mũi tên có hướng và độ dài tồn tại trong không gian. Ví dụ, vận tốc thật của drone, lực đẩy thật của rotor hoặc vector nối từ một điểm đến điểm khác đều là các đối tượng hình học.

Để làm việc với vector bằng số, ta biểu diễn nó theo basis vectors của một frame. Trong frame A, ta viết:

\[
\mathbf v = v_1\mathbf a_1 + v_2\mathbf a_2 + v_3\mathbf a_3.
\]

Ba số \(v_1,v_2,v_3\) cho biết thành phần của vector theo từng trục \(\mathbf{a}_1,\mathbf{a}_2,\mathbf{a}_3\). Viết dạng cột:

\[
{}^{A}\mathbf v=
\begin{bmatrix}
v_1\\v_2\\v_3
\end{bmatrix}.
\]

Dấu \({}^{A}\) không phải là lũy thừa. Nó nhắc rằng ba số trong vector cột được đo theo frame A. Nếu đổi sang frame B, cùng vector vật lý có thể có bộ số khác:

\[
{}^{A}\mathbf v \ne {}^{B}\mathbf v.
\]

Điều này không có nghĩa hai vector vật lý khác nhau. Nó chỉ nói rằng ta đang dùng hai bộ “thước đo theo hướng” khác nhau để mô tả cùng mũi tên.

## 2.3. Một ví dụ trực giác

Giả sử một drone đang bay về hướng Bắc. Trong world frame, hãy giả sử trục \(x_W\) hướng Bắc. Khi đó vận tốc drone có thể gần như là:

\[
{}^{W}\mathbf v=
\begin{bmatrix}
5\\0\\0
\end{bmatrix}\text{ m/s}.
\]

Bây giờ drone yaw \(90^\circ\), khiến mũi drone hướng Đông. Cùng vận tốc vật lý nói trên, nếu được biểu diễn trong body frame, có thể có dạng:

\[
{}^{B}\mathbf v=
\begin{bmatrix}
0\\-5\\0
\end{bmatrix}\text{ m/s},
\]

hoặc một dấu khác tùy quy ước trục body. Điều thay đổi không phải vận tốc thật trong không gian; điều thay đổi là “hướng nào được gọi là x, y, z” trong frame đang dùng.

## 2.4. Tính thuận tay phải (right-handedness)

Các hệ trục trong robotics thường là hệ thuận tay phải (right-handed frame). Điều đó có thể được kiểm tra bằng tích có hướng:

\[
\mathbf a_1\times \mathbf a_2=\mathbf a_3.
\]

Điều kiện này quan trọng vì một hệ trục “bị lật gương” vẫn có thể có ba trục vuông góc và độ dài đơn vị, nhưng không thể được tạo ra chỉ bằng một rotation vật lý. Về sau, điều kiện \(\det(\mathbf{R})=+1\) sẽ đảm bảo orientation matrix biểu diễn một phép quay chứ không phải reflection.

### Tóm tắt phần 2

Reference frame cung cấp gốc và ba trục để biểu diễn đại lượng hình học bằng số. Vector vật lý không phụ thuộc frame, nhưng tọa độ của nó phụ thuộc frame. Ký hiệu frame phải được giữ rõ trong mọi phép tính.

---

# Phần 3. Pose của rigid body và ý nghĩa của ký hiệu frame

## 3.1. Một frame gắn với vật thể

Để mô tả một rigid body, ta gắn một frame B cứng vào nó. Vì frame này gắn cứng với vật, nếu vật quay thì các trục của B cũng quay; nếu vật tịnh tiến thì gốc B cũng tịnh tiến. Một frame tham chiếu A — thường là world frame — được dùng để quan sát frame B.

Khi đó, pose của B trong A gồm hai thành phần: vị trí của gốc B và orientation của frame B. Ta viết:

\[
\boxed{{}^{A}\mathcal{P}_B=\left({}^{A}\mathbf{o}_B,\;{}^{A}\mathbf{R}_B\right)}
\]

Trong đó, \({}^{A}\mathcal{P}_B\) nghĩa là pose của frame B so với frame A. \({}^{A}\mathbf{o}_B\) là position của gốc B trong A; còn \({}^{A}\mathbf{R}_B\) là orientation của các trục B khi nhìn bằng A.

![Slide 6 – Rigid Body Pose](/images/rigid_body_slide_06.png)

*Slide 6. Gốc của frame B nằm lệch khỏi gốc A một vector \(\mathbf{o}\). Ba trục xanh \(\mathbf{b}_1,\mathbf{b}_2,\mathbf{b}_3\) cho biết body frame đang định hướng như thế nào trong reference frame.*

## 3.2. Vị trí gốc B trong frame A

Vector từ gốc A đến gốc B được viết:

\[
{}^{A}\mathbf o_B=
\begin{bmatrix}
o_1\\o_2\\o_3
\end{bmatrix}.
\]

Cách đọc chi tiết là:

- chỉ số dưới B: vector đang chỉ đến gốc frame B;
- chỉ số trên A: các thành phần của vector được viết theo trục frame A.

Ví dụ:

\[
{}^{A}\mathbf o_B=
\begin{bmatrix}
2\\1\\3
\end{bmatrix}
\]

nghĩa là: từ gốc A, đi 2 đơn vị theo \(+\mathbf{a}_1\), 1 đơn vị theo \(+\mathbf{a}_2\) và 3 đơn vị theo \(+\mathbf{a}_3\) thì đến gốc B.

## 3.3. Orientation của B trong A

Các trục của B có thể được viết theo basis vectors của A. Ví dụ:

\[
\mathbf b_1
=R_{11}\mathbf a_1+R_{21}\mathbf a_2+R_{31}\mathbf a_3.
\]

Các hệ số \(R_{11},R_{21},R_{31}\) là tọa độ của trục \(\mathbf{b}_1\) khi nhìn trong frame A. Tương tự:

\[
\mathbf b_2
=R_{12}\mathbf a_1+R_{22}\mathbf a_2+R_{32}\mathbf a_3,
\]

\[
\mathbf b_3
=R_{13}\mathbf a_1+R_{23}\mathbf a_2+R_{33}\mathbf a_3.
\]

Ba cột tọa độ này sẽ được ghép thành ma trận quay. Điểm quan trọng là: orientation không phải chỉ là “ba góc” một cách mặc định. Trong phần này, orientation được biểu diễn một cách hình học hơn: **ba trục body được viết trong world frame**.

### Tóm tắt phần 3

Pose của body frame B trong reference frame A được mô tả bởi position của gốc B và orientation của ba trục B. Ký hiệu trên/dưới giúp theo dõi cả frame biểu diễn lẫn frame được mô tả.

---

# Phần 4. Ma trận quay (Rotation Matrix)

## 4.1. Cấu trúc của ma trận quay

Ta định nghĩa:

\[
\boxed{
{}^{A}\mathbf R_B=
\begin{bmatrix}
{}^{A}\mathbf b_1 & {}^{A}\mathbf b_2 & {}^{A}\mathbf b_3
\end{bmatrix}.
}
\]

Đây là công thức cần nhớ theo nghĩa hình học. Ba cột của \({}^{A}\mathbf{R}_B\) chính là ba trục của frame B, nhưng mỗi trục đã được viết bằng tọa độ trong A.

Khai triển:

\[
{}^{A}\mathbf R_B=
\begin{bmatrix}
R_{11} & R_{12} & R_{13}\\
R_{21} & R_{22} & R_{23}\\
R_{31} & R_{32} & R_{33}
\end{bmatrix}.
\]

Cột thứ nhất là \({}^{A}\mathbf{b}_1\), cột thứ hai là \({}^{A}\mathbf{b}_2\), và cột thứ ba là \({}^{A}\mathbf{b}_3\). Không nên đọc các hàng theo cùng cách đó; trong convention đang dùng, **cột** mới là các axes của frame nguồn B.

![Slide 7 – Rotation Matrix](/images/rigid_body_slide_07.png)

*Slide 7. Hình và công thức cùng minh họa rằng ma trận \({}^{A}\mathbf{R}_B\) chứa các basis vectors của frame B được biểu diễn trong frame A.*

## 4.2. Đổi tọa độ giữa hai frame

Giả sử \(\mathbf{p}\) là một điểm hay vector vật lý. Nếu tọa độ của nó trong B là:

\[
{}^{B}\mathbf p=
\begin{bmatrix}
p^B_1\\p^B_2\\p^B_3
\end{bmatrix},
\]

thì phát biểu hình học tương ứng là:

\[
\mathbf p=p^B_1\mathbf b_1+p^B_2\mathbf b_2+p^B_3\mathbf b_3.
\]

Khi biểu diễn các trục \(\mathbf{b}_i\) theo frame A, ta thu được:

\[
{}^{A}\mathbf p=
{}^{A}\mathbf R_B\;{}^{B}\mathbf p.
\]

Đây là **biến đổi tọa độ** (coordinate transformation). Điểm hoặc vector vật lý không bị quay trong thế giới thật; ta chỉ đổi tọa độ từ basis B sang basis A.

Một mẹo kiểm tra rất hiệu quả là “khử chỉ số ở giữa”:

\[
{}^{A}\mathbf R_B\;{}^{B}\mathbf p
\quad\Rightarrow\quad
{}^{A}\mathbf p.
\]

Bạn có thể hình dung \({}^{A}\mathbf{R}_B\) như một toán tử “nhận tọa độ trong B và xuất tọa độ trong A”.

## 4.3. Ý nghĩa của từng phần tử \(R_{ij}\)

Một phần tử của ma trận quay có thể được viết dưới dạng tích vô hướng:

\[
R_{ij}=\mathbf a_i^T\mathbf b_j.
\]

Điều này có nghĩa R_{ij} là projection của trục thứ j của B lên trục thứ i của A. Vì cả hai đều là unit vectors:

\[
R_{ij}=\cos\angle(\mathbf a_i,\mathbf b_j).
\]

Ví dụ, \(R_{21}\) cho biết trục \(\mathbf{b}_1\) có thành phần bao nhiêu theo hướng \(\mathbf{a}_2\). Nếu \(R_{21}=1\), hai trục trùng chiều; nếu \(R_{21}=0\), chúng vuông góc; nếu \(R_{21}=-1\), chúng ngược chiều.

## 4.4. Tính trực giao và nghịch đảo

Do các cột của \(\mathbf{R}\) là các trục trực chuẩn, chúng thỏa:

\[
\mathbf b_i^T\mathbf b_i=1,
\qquad
\mathbf b_i^T\mathbf b_j=0\quad(i\ne j).
\]

Viết dưới dạng ma trận, điều này trở thành:

\[
\boxed{
\mathbf R^T\mathbf R=
\mathbf R\mathbf R^T=
\mathbf I.
}
\]

Một ma trận thỏa điều kiện trên được gọi là **ma trận trực giao** (orthogonal matrix). Hệ quả tính toán rất quan trọng là:

\[
\boxed{
\mathbf R^{-1}=\mathbf R^T.
}
\]

Vì vậy, nếu \({}^{A}\mathbf{R}_B\) đổi tọa độ từ B sang A, thì đổi ngược lại chỉ cần chuyển vị:

\[
{}^{B}\mathbf R_A=
\left({}^{A}\mathbf R_B\right)^T.
\]

## 4.5. Vì sao orientation chỉ có ba bậc tự do?

Ma trận \(3\times3\) có chín phần tử, nhưng orientation 3D chỉ có ba degrees of freedom. Lý do là các phần tử của rotation matrix không độc lập. Điều kiện ba cột có độ dài bằng một cho ba ràng buộc. Điều kiện ba cặp cột vuông góc cho thêm ba ràng buộc. Tổng cộng có sáu ràng buộc:

\[
9-6=3.
\]

Vì vậy, ma trận quay là một representation dư thừa nhưng rất thuận tiện để nhân và ghép biến đổi.

## 4.6. Điều kiện determinant bằng +1

Ma trận trực giao nói chung có determinant +1 hoặc -1. Để là rotation matrix hợp lệ, nó phải thỏa thêm:

\[
\boxed{\det(\mathbf R)=+1.}
\]

Nếu determinant bằng -1, phép biến đổi có chứa reflection — tương tự việc soi gương — và có thể đổi hệ thuận tay phải thành hệ thuận tay trái. Một rigid body rotation vật lý thuần túy không làm điều đó.

Tập các rotation matrices 3D được ký hiệu là:

\[
SO(3)=\{\mathbf R\in\mathbb R^{3\times3}:\mathbf R^T\mathbf R=\mathbf I,\det(\mathbf R)=+1\}.
\]

### Tóm tắt phần 4

Ma trận \({}^{A}\mathbf{R}_B\) có các cột là axes của B trong A và đổi tọa độ theo \({}^{A}\mathbf{p}={}^A\mathbf{R}_B{}^B\mathbf{p}\). Rotation matrix phải trực giao, có nghịch đảo bằng chuyển vị và determinant bằng +1.

---

# Phần 5. Các phép quay cơ bản quanh trục x, y, z

Các phép quay quanh ba trục cơ sở là những “khối xây dựng” (building blocks) cho orientation 3D. Trước khi ghép nhiều phép quay, bạn cần hiểu thật chắc từng phép quay đơn.

## 5.1. Quay quanh trục x

Quay một frame quanh trục x một góc \(\phi\) được biểu diễn bởi:

\[
\mathbf R_x(\phi)=
\begin{bmatrix}
1 & 0 & 0\\
0 & \cos\phi & -\sin\phi\\
0 & \sin\phi & \cos\phi
\end{bmatrix}.
\]

Trực giác: trục x là trục quay, nên nó không thay đổi. Hai trục còn lại quay trong mặt phẳng yz. Vì cột đầu là:

\[
\begin{bmatrix}1\\0\\0\end{bmatrix},
\]

nên \(x_B\) vẫn trùng \(x_A\). Các cột còn lại cho biết \(y_B\) và \(z_B\) nghiêng như thế nào trong A.

![Slide 9 – Quay quanh trục x](/images/rigid_body_slide_09.png)

*Slide 9. Trục x giữ nguyên; các trục y và z xoay trong mặt phẳng vuông góc với x.*

Một kiểm tra dấu nhanh là đặt \(\phi=90^\circ\):

\[
\mathbf R_x(90^\circ)=
\begin{bmatrix}
1&0&0\\
0&0&-1\\
0&1&0
\end{bmatrix}.
\]

Khi đó y được đưa về +z, còn z được đưa về -y theo quy tắc bàn tay phải (right-hand rule).

## 5.2. Quay quanh trục y

Quay một góc \(\theta\) quanh trục y:

\[
\mathbf R_y(\theta)=
\begin{bmatrix}
\cos\theta&0&\sin\theta\\
0&1&0\\
-\sin\theta&0&\cos\theta
\end{bmatrix}.
\]

Ở đây trục y giữ nguyên, còn x và z quay trong mặt phẳng xz. Khi \(\theta=90^\circ\):

\[
\mathbf R_y(90^\circ)=
\begin{bmatrix}
0&0&1\\
0&1&0\\
-1&0&0
\end{bmatrix}.
\]

Do đó x được đưa về -z, còn z được đưa về +x.

![Slide 10 – Quay quanh trục y](/images/rigid_body_slide_10.png)

*Slide 10. Trục y là trục quay, còn x và z quay trong mặt phẳng xz.*

## 5.3. Quay quanh trục z

Quay một góc \(\psi\) quanh trục z:

\[
\mathbf R_z(\psi)=
\begin{bmatrix}
\cos\psi&-\sin\psi&0\\
\sin\psi&\cos\psi&0\\
0&0&1
\end{bmatrix}.
\]

Trục z không đổi. Trục x và y quay trong mặt phẳng xy. Với \(\psi=90^\circ\):

\[
\mathbf R_z(90^\circ)=
\begin{bmatrix}
0&-1&0\\
1&0&0\\
0&0&1
\end{bmatrix}.
\]

Kết quả là x được đưa về +y, y được đưa về -x.

![Slide 11 – Quay quanh trục z](/images/rigid_body_slide_11.png)

*Slide 11. Trục z giữ nguyên, còn x và y quay trong mặt phẳng xy.*

## 5.4. Liên hệ với roll, pitch và yaw

Trong nhiều quy ước drone phổ biến, rotation quanh trục body-x được gọi là **roll**, quanh body-y là **pitch**, và quanh body-z là **yaw**. Tuy nhiên, bạn phải luôn kiểm tra quy ước cụ thể của hệ đang dùng, vì một số hệ chọn trục z hướng lên, một số khác chọn hướng xuống; một số chọn x hướng trước, một số lại chọn hướng khác.

Công thức ma trận không tự thay đổi, nhưng việc gán “roll/pitch/yaw” vào chuyển động vật lý phụ thuộc convention frame.

### Tóm tắt phần 5

Quay quanh trục nào thì trục đó giữ nguyên; hai trục còn lại quay trong mặt phẳng vuông góc với nó. Ba ma trận \(\mathbf{R}_x,\mathbf{R}_y,\mathbf{R}_z\) là các building blocks cho mọi rotation 3D.

---

# Phần 6. Phép quay hợp thành (Composite Rotations)

Một rigid body thường không chỉ quay quanh một trục. Khi phải ghép nhiều phép quay, hai câu hỏi quyết định thứ tự nhân là: **phép quay tiếp theo được thực hiện quanh trục của frame hiện tại hay quanh trục cố định của world frame?**

## 6.1. Quay quanh frame hiện tại (current-frame / intrinsic rotation)

Giả sử ta bắt đầu ở frame 0, quay để được frame 1, rồi lại quay quanh một trục thuộc chính frame 1 để được frame 2. Khi đó:

\[
{}^{0}\mathbf R_2=
{}^{0}\mathbf R_1\;{}^{1}\mathbf R_2.
\]

Ma trận quay mới nằm bên phải. Vì vậy ta nói: **quay quanh current frame thì post-multiply**.

\[
\boxed{
\text{Current frame}
\quad\Rightarrow\quad
\text{nhân ma trận mới ở bên phải.}
}
\]

![Slide 12 – Composite rotations trong current frame](/images/rigid_body_slide_12.png)

*Slide 12. Phép quay thứ hai được thực hiện quanh một trục thuộc frame trung gian đã quay. Vì vậy quan hệ được ghép theo chuỗi frame: \({}^0\mathbf{R}_2={}^0\mathbf{R}_1{}^1\mathbf{R}_2\).*

Một cách đọc hình học là: frame 1 đã quay theo vật. Bây giờ “xoay quanh trục y của vật” nghĩa là xoay quanh trục \(y_1\), không phải trục \(y_0\) của world.

## 6.2. Quay quanh frame cố định (fixed-frame / extrinsic rotation)

Bây giờ xét tình huống khác. Ta đã có orientation \({}^{A}\mathbf{R}_B\), rồi muốn quay toàn bộ frame B quanh một trục cố định của frame A. Gọi phép quay thêm này là \({}^{A}\mathbf{R}_{\Delta}\). Khi đó:

\[
{}^{A}\mathbf{R}_{B,\mathrm{new}} = {}^{A}\mathbf{R}_{\Delta}{}^{A}\mathbf{R}_B
\]

Ma trận mới nằm bên trái. Vì vậy ta nói: **quay quanh fixed frame thì pre-multiply**. Cách viết có chỉ số frame giúp ta thấy rõ phép quay thêm được biểu diễn trong frame A.

\[
\boxed{
\text{Fixed frame}
\quad\Rightarrow\quad
\text{nhân ma trận mới ở bên trái.}
}
\]

![Slide 13 – Composite rotations trong fixed frame](/images/rigid_body_slide_13.png)

*Slide 13. Phép quay thứ hai vẫn dùng một trục của frame cố định. Dù vật đã quay, world axes không quay theo vật.*

## 6.3. Vì sao current frame và fixed frame có thể cho cùng orientation cuối?

Một chuỗi intrinsic rotations quanh current axes có thể được mô tả bằng một chuỗi extrinsic rotations quanh fixed axes, nhưng **thứ tự axes phải đảo lại**. Đây không phải vì matrix multiplication giao hoán. Trái lại, rotation matrices nói chung không giao hoán:

\[
\mathbf R_x(\phi)\mathbf R_y(\theta)
\ne
\mathbf R_y(\theta)\mathbf R_x(\phi).
\]

Điều đúng là: nếu bạn đổi cách mô tả từ “quay quanh axes gắn với vật” sang “quay quanh axes cố định trong thế giới”, thì phải đổi thứ tự mô tả để giữ nguyên geometry cuối cùng.

![Slide 14 – Tổng kết current và fixed frame](/images/rigid_body_slide_14.png)

*Slide 14. Slide nhấn mạnh hai quy tắc: post-multiply cho current frame và pre-multiply cho fixed frame. Kết quả có thể tương đương nếu convention được theo dõi đúng.*

## 6.4. Cách làm bài an toàn

Khi gặp bài composite rotations, hãy viết lần lượt bốn dòng nháp:

1. Frame nào là reference/world frame?
2. Sau mỗi bước, trục quay thuộc frame nào?
3. Ma trận đang mô tả orientation của frame hay đang quay active vector?
4. Các frame indices có khớp ở giữa khi nhân không?

Ví dụ, nếu bạn có \({}^A\mathbf{R}_B\) rồi thêm một phép quay từ B sang C được mô tả trong body frame hiện tại, công thức là:

\[
{}^A\mathbf R_C={}^A\mathbf R_B\;{}^B\mathbf R_C.
\]

Chỉ số B ở giữa khớp nhau. Chính quy tắc này thường đáng tin hơn việc cố gắng nhớ một chuỗi trục bằng trực giác không đầy đủ.

### Tóm tắt phần 6

Current-frame rotations dùng axes đã quay theo vật, nên post-multiply. Fixed-frame rotations dùng axes không đổi của reference frame, nên pre-multiply. Rotation matrices không giao hoán; muốn đổi giữa intrinsic và extrinsic descriptions phải đảo thứ tự convention một cách nhất quán.

---

# Phần 7. Quay vector trực tiếp và ba cách hiểu của ma trận quay

## 7.1. Active vector rotation

Cho đến đây, chúng ta thường dùng \({}^A\mathbf{R}_B\) để đổi biểu diễn tọa độ của cùng một vector giữa hai frame. Nhưng ma trận quay cũng có thể được dùng để quay chính vector trong một frame cố định. Ta viết:

\[
\mathbf{v}_{\mathrm{new}}=\mathbf{R}\mathbf{v}.
\]

Ở đây, frame giữ nguyên nhưng vector vật lý bị quay. Cách nhìn này gọi là **active vector rotation**.

![Slide 16 – Quay trực tiếp vector](/images/rigid_body_slide_16.png)

*Slide 16. Vector \(\mathbf{v}=[0,1,1]^T\) được quay \(90^\circ\) quanh trục x để tạo vector mới \(\mathbf{v}_{\mathrm{new}}\).*

## 7.2. Tính chi tiết ví dụ ở slide 16

Vector ban đầu là:

\[
\mathbf v=
\begin{bmatrix}
0\\1\\1
\end{bmatrix}.
\]

Ta quay quanh trục x một góc:

\[
\theta=\frac{\pi}{2}.
\]

Khi đó:

\[
\mathbf R_x\left(\frac{\pi}{2}\right)=
\begin{bmatrix}
1&0&0\\
0&0&-1\\
0&1&0
\end{bmatrix}.
\]

Nhân ma trận:

\[
\begin{aligned}
\mathbf{v}_{\mathrm{new}}
&=
\begin{bmatrix}
1&0&0\\
0&0&-1\\
0&1&0
\end{bmatrix}
\begin{bmatrix}
0\\1\\1
\end{bmatrix} \\
&=
\begin{bmatrix}
0\\-1\\1
\end{bmatrix}
\end{aligned}
\]

Ta có thể kiểm tra trực giác. Thành phần theo x không đổi vì quay quanh trục x. Thành phần \(+y\) quay về \(+z\); thành phần \(+z\) quay về \(-y\). Cộng hai đóng góp này, ta có đúng vector \([0,-1,1]^T\).

Độ dài cũng được bảo toàn:

\[
\|\mathbf v\|=\sqrt{2},
\qquad
\|\mathbf{v}_{\mathrm{new}}\|=\sqrt{2}.
\]

## 7.3. Ba cách hiểu cần phân biệt

Một rotation matrix có thể xuất hiện trong ba vai trò khác nhau.

**Thứ nhất, đổi tọa độ** (coordinate transformation): vector vật lý không thay đổi nhưng frame dùng để biểu diễn thay đổi.

\[
{}^A\mathbf p={}^A\mathbf R_B{}^B\mathbf p.
\]

**Thứ hai, mô tả orientation**: \({}^A\mathbf{R}_B\) ghi lại các axes của B trong A.

\[
{}^A\mathbf R_B=
\begin{bmatrix}
{}^A\mathbf b_1&{}^A\mathbf b_2&{}^A\mathbf b_3
\end{bmatrix}.
\]

**Thứ ba, quay active vector**: frame giữ nguyên còn vector thay đổi.

\[
\mathbf{v}_{\mathrm{new}}=\mathbf{R}\mathbf{v}.
\]

![Slide 17 – Ba vai trò của rotation matrices](/images/rigid_body_slide_17.png)

*Slide 17. Slide tóm tắt ba vai trò của rotation matrix và nhắc lại quan hệ giữa fixed-frame và current-frame composition.*

## 7.4. Nguồn gốc của nhiều lỗi dấu và transpose

Một lỗi rất phổ biến là lấy công thức đúng cho coordinate transformation rồi dùng nó như active rotation, hoặc ngược lại. Trong nhiều convention, hai cách nhìn liên hệ với nhau bằng inverse/transposition. Vì vậy, khi thấy dấu sine “có vẻ ngược”, đừng vội sửa dấu; hãy kiểm tra xem bạn đang:

- quay vector hay đổi basis;
- quay frame hay quay object;
- biểu diễn vector bằng cột hay hàng;
- dùng right-handed hay left-handed convention.

Chỉ sau khi trả lời các câu hỏi này mới nên kiểm tra công thức chi tiết.

### Tóm tắt phần 7

Ma trận quay có thể dùng để đổi tọa độ, mô tả orientation hoặc quay trực tiếp vector. Các biểu thức có thể giống nhau về hình thức nhưng khác ý nghĩa vật lý. Phải xác định rõ bài toán trước khi quyết định dùng \(\mathbf{R}\), \(\mathbf{R}^T\) hoặc thứ tự nhân nào.

---

# Phần 8. Ma trận biến đổi thuần nhất (Homogeneous Transformations)

## 8.1. Từ rotation-only đến pose đầy đủ

Ma trận quay chỉ giải quyết phần orientation. Nhưng để đổi tọa độ của một điểm gắn trên rigid body, ta cần tính cả translation của gốc body frame.

Giả sử điểm \(\mathbf{p}\) có tọa độ \({}^B\mathbf{p}\) trong body frame B. Muốn tìm tọa độ của nó trong reference frame A, ta phải làm hai bước:

1. quay offset của điểm từ axes B sang axes A;
2. cộng vị trí gốc của B trong A.

Công thức là:

\[
\boxed{
{}^A\mathbf p
={}^{A}\mathbf R_B\;{}^{B}\mathbf p
+{}^A\mathbf o_B.
}
\]

![Slide 18 – Homogeneous Transformations](/images/rigid_body_slide_18.png)

*Slide 18. Vector \({}^B\mathbf{p}\) đi từ gốc B đến điểm p. Sau khi quay sang A và cộng offset \({}^A\mathbf{o}_B\), ta nhận được \({}^A\mathbf{p}\).*

## 8.2. Cách đọc công thức một cách vật lý

Hãy xem \({}^B\mathbf{p}\) là “offset của điểm so với body frame”. Khi thân drone quay, offset này cũng phải quay theo body. Do đó, trước tiên ta nhân với \({}^A\mathbf{R}_B\).

Sau phép quay, kết quả cho biết offset của điểm đã hướng như thế nào trong world frame. Nhưng nó vẫn đang được đặt như thể gốc body frame nằm ở gốc world frame. Ta phải cộng \({}^A\mathbf{o}_B\) để đưa nó đến đúng vị trí thật của body frame.

Một ví dụ: camera nằm phía trước drone 0.2 m trong body frame. Nếu drone yaw, “phía trước drone” quay theo drone. Nếu drone bay đi, toàn bộ camera cũng dịch theo drone. Đây chính là công thức \(\mathbf{R}\mathbf{p}+\mathbf{o}\).

## 8.3. Vì sao cần homogeneous coordinates?

Biểu thức \(\mathbf{R}\mathbf{p}+\mathbf{t}\) chứa cả phép nhân ma trận và phép cộng vector. Ta muốn biểu diễn toàn bộ transformation bằng **một phép nhân ma trận** để dễ ghép chuỗi transforms. Ta làm điều đó bằng cách thêm một tọa độ thứ tư bằng 1 cho point:

\[
\mathbf P=
\begin{bmatrix}
\mathbf p\\1
\end{bmatrix}.
\]

Ma trận biến đổi thuần nhất có dạng:

\[
\boxed{
\mathbf H=
\begin{bmatrix}
\mathbf R&\mathbf t\\
\mathbf 0^T&1
\end{bmatrix}.
}
\]

Khi đó:

\[
\mathbf{P}_{\mathrm{new}}=\mathbf{H}\mathbf{P}
\]

Khai triển:

\[
\begin{aligned}
\mathbf{H}\mathbf{P}
&=
\begin{bmatrix}
\mathbf{R}&\mathbf{t}\\
\mathbf{0}^{T}&1
\end{bmatrix}
\begin{bmatrix}
\mathbf{p}\\
1
\end{bmatrix}\\
&=
\begin{bmatrix}
\mathbf{R}\mathbf{p}+\mathbf{t}\\
1
\end{bmatrix}
\end{aligned}
\]

Như vậy, phần tử 1 cuối vector homogeneous chính là “công tắc” khiến translation được cộng vào.

## 8.4. Point và direction vector trong homogeneous coordinates

Đây là một làm rõ quan trọng trong robotics. Một **point** dùng:

\[
\mathbf P=
\begin{bmatrix}\mathbf p\\1\end{bmatrix}.
\]

Một **direction vector**, velocity vector hoặc force vector không có vị trí gốc cố định, nên dùng:

\[
\mathbf V=
\begin{bmatrix}\mathbf v\\0\end{bmatrix}.
\]

Khi nhân transformation với vector hướng:

\[
\begin{aligned}
\mathbf{H}
\begin{bmatrix}
\mathbf{v}\\
0
\end{bmatrix}
&=
\begin{bmatrix}
\mathbf{R}&\mathbf{t}\\
\mathbf{0}^{T}&1
\end{bmatrix}
\begin{bmatrix}
\mathbf{v}\\
0
\end{bmatrix}\\
&=
\begin{bmatrix}
\mathbf{R}\mathbf{v}\\
0
\end{bmatrix}
\end{aligned}
\]

Translation biến mất, đúng với trực giác: chỉ vì ta dịch drone sang một chỗ khác không có nghĩa velocity vector hoặc thrust direction tự tăng thêm một offset vị trí.

![Slide 19 – Cấu trúc homogeneous transformation](/images/rigid_body_slide_19.png)

*Slide 19. Ma trận \(\mathbf{H}\) gồm khối rotation \(\mathbf{R}\) và translation vector \(\mathbf{t}\). Khi viết point dưới homogeneous form, rigid-body transformation trở thành một phép nhân ma trận 4×4.*

### Tóm tắt phần 8

Homogeneous transformation gói rotation và translation thành \(4\times4\) matrix. Với point, dùng homogeneous coordinate cuối bằng 1; với free/direction vector, dùng 0. Công thức trung tâm là \({}^A\mathbf{p}={}^A\mathbf{R}_B{}^B\mathbf{p}+{}^A\mathbf{o}_B\).

---

# Phần 9. Ghép ma trận biến đổi thuần nhất (Composite Transformations)

## 9.1. Tách transformation thành quay và tịnh tiến

Với:

\[
\mathbf{H}=
\begin{bmatrix}
\mathbf{R}&\mathbf{t}\\
\mathbf{0}^{T}&1
\end{bmatrix},
\]

ta có thể viết:

\[
\mathbf{H}=
\underbrace{
\begin{bmatrix}
\mathbf{I}&\mathbf{t}\\
\mathbf{0}^{T}&1
\end{bmatrix}}_{\mathbf{T}(\mathbf{t})}
\underbrace{
\begin{bmatrix}
\mathbf{R}&\mathbf{0}\\
\mathbf{0}^{T}&1
\end{bmatrix}}_{\widetilde{\mathbf R}}.
\]

Nếu tác động lên point column, ma trận ở bên phải tác động trước. Do đó, đọc từ phải sang trái: point được quay bởi \(\mathbf{R}\), sau đó được tịnh tiến bởi \(\mathbf{t}\) trong frame ban đầu.

Slide cũng đưa ra cách diễn giải tương đương theo frame construction: có thể nhìn việc đặt frame mới như tịnh tiến gốc đến vị trí mới rồi quay axes trong current frame. Hai cách đọc này chỉ an toàn khi bạn theo dõi rõ vector \(\mathbf{t}\) được biểu diễn ở frame nào.

![Slide 20 – Composite Transformations](/images/rigid_body_slide_20.png)

*Slide 20. Hình minh họa việc cùng homogeneous transformation có thể được nhìn qua thứ tự tác động lên point hoặc qua quá trình xây dựng frame mới. Không được hoán đổi ma trận tùy ý; phải gắn ý nghĩa frame cho từng factor.*

## 9.2. Ghép transformation qua frame trung gian

Giả sử ta có ba frame A,B,C. Nếu biết pose của B trong A và pose của C trong B, thì pose của C trong A là:

\[
{}^{A}\mathbf{H}_C = {}^{A}\mathbf{H}_B{}^{B}\mathbf{H}_C
\]

Ký hiệu B ở giữa khớp nhau, giống hệt quy tắc của rotation matrices. Đây là lý do homogeneous transformations đặc biệt phù hợp cho robot arm: ta có thể đi từ base đến link 1, từ link 1 đến link 2, rồi từ link 2 đến end-effector bằng cách nhân chuỗi matrices.

## 9.3. Khai triển block multiplication

Viết:

\[
{}^{A}\mathbf{H}_B=
\begin{bmatrix}{}^{A}\mathbf{R}_B&{}^{A}\mathbf{o}_B\\\mathbf{0}^{T}&1\end{bmatrix},
\qquad
{}^{B}\mathbf{H}_C=
\begin{bmatrix}{}^{B}\mathbf{R}_C&{}^{B}\mathbf{o}_C\\\mathbf{0}^{T}&1\end{bmatrix}
\]

Khi nhân, rotation phần cuối là:

\[
{}^{A}\mathbf{R}_C = {}^{A}\mathbf{R}_B{}^{B}\mathbf{R}_C
\]

Translation phần cuối là:

\[
{}^{A}\mathbf{o}_C = {}^{A}\mathbf{R}_B{}^{B}\mathbf{o}_C+{}^{A}\mathbf{o}_B
\]

Hạng tử đầu tiên rất có ý nghĩa. Vector từ B đến C ban đầu được viết theo axes B, nên trước khi cộng vào một vector đang ở A, nó phải được quay sang A. Sau đó mới cộng position của B trong A.

## 9.4. Current frame và fixed frame vẫn tuân theo quy tắc cũ

Các nguyên tắc ghép rotation matrices áp dụng nguyên vẹn cho homogeneous transformations.

Nếu transform mới được định nghĩa trong current frame:

\[
{}^{A}\mathbf{H}_C = {}^{A}\mathbf{H}_B{}^{B}\mathbf{H}_C
\]

Ta post-multiply vì transform mới nằm trong frame hiện tại. Nếu một transform mới được định nghĩa theo fixed/world frame, ta pre-multiply:

\[
{}^{A}\mathbf{H}_{B,\mathrm{new}} = {}^{A}\mathbf{H}_{\Delta}{}^{A}\mathbf{H}_B
\]

![Slide 21 – Quy tắc composite transformations](/images/rigid_body_slide_21.png)

*Slide 21. Homogeneous transformations dùng cùng quy tắc current-frame/post-multiply và fixed-frame/pre-multiply như rotation matrices.*

## 9.5. Ví dụ số nhỏ

Cho point:

\[
\mathbf p=
\begin{bmatrix}1\\0\\0\end{bmatrix}.
\]

Quay \(90^\circ\) quanh z rồi dịch 2 đơn vị theo x của original frame. Chọn:

\[
\mathbf R=
\begin{bmatrix}
0&-1&0\\
1&0&0\\
0&0&1
\end{bmatrix},
\qquad
\mathbf t=
\begin{bmatrix}2\\0\\0\end{bmatrix}.
\]

Kết quả:

\[
\begin{aligned}
\mathbf{p}_{\mathrm{new}}
&=\mathbf{R}\mathbf{p}+\mathbf{t}\\
&=\begin{bmatrix}0\\1\\0\end{bmatrix}
+\begin{bmatrix}2\\0\\0\end{bmatrix}\\
&=\begin{bmatrix}2\\1\\0\end{bmatrix}
\end{aligned}
\]

Điểm ban đầu được quay từ \(+x\) sang \(+y\), sau đó toàn bộ kết quả được dịch sang \(+x\) hai đơn vị.

### Tóm tắt phần 9

Homogeneous transformations ghép theo frame indices: \({}^A\mathbf{H}_C={}^A\mathbf{H}_B{}^B\mathbf{H}_C\). Rotation và translation đều được cập nhật khi nhân block matrices. Quy tắc post-multiply/current frame và pre-multiply/fixed frame vẫn giữ nguyên.

---

# Phần 10. Bảng ghi nhớ nhanh và các lỗi thường gặp

## 10.1. Bảng công thức cốt lõi

| Ý nghĩa | Công thức |
|---|---|
| Vector theo basis A | \(\mathbf v=v_1\mathbf a_1+v_2\mathbf a_2+v_3\mathbf a_3\) |
| Pose của B trong A | \({}^A\mathcal{P}_B=\left({}^A\mathbf{o}_B,{}^A\mathbf{R}_B\right)\) |
| Cột của rotation matrix | \({}^A\mathbf R_B=[{}^A\mathbf b_1\;{}^A\mathbf b_2\;{}^A\mathbf b_3]\) |
| Đổi tọa độ vector/offset | \({}^A\mathbf p={}^A\mathbf R_B{}^B\mathbf p\) |
| Inverse rotation | \({}^B\mathbf R_A=({}^A\mathbf R_B)^T\) |
| Rigid-body point transform | \({}^A\mathbf p={}^A\mathbf R_B{}^B\mathbf p+{}^A\mathbf o_B\) |
| Homogeneous transform | \({}^A\mathbf H_B=\begin{bmatrix}{}^A\mathbf R_B&{}^A\mathbf o_B\\0^T&1\end{bmatrix}\) |
| Compose frames | \({}^A\mathbf H_C={}^A\mathbf H_B{}^B\mathbf H_C\) |
| Current frame | post-multiply |
| Fixed frame | pre-multiply |

## 10.2. Các lỗi thường gặp

**Lỗi 1: quên frame của vector.** Viết \(\mathbf{p}\) mà không nói nó ở frame nào rất dễ gây sai khi cộng hoặc nhân. Hãy ưu tiên viết \({}^A\mathbf{p}\) hoặc \({}^B\mathbf{p}\) trong bước suy luận.

**Lỗi 2: cộng hai vector đang được biểu diễn ở hai frame khác nhau.** Không thể cộng trực tiếp \({}^A\mathbf{o}_B\) và \({}^B\mathbf{o}_C\). Trước tiên, phải đổi một trong hai về cùng frame.

**Lỗi 3: nhầm cột và hàng của rotation matrix.** Trong convention của bài này, columns của \({}^A\mathbf{R}_B\) là basis vectors của B viết trong A.

**Lỗi 4: dùng \(\mathbf{R}^T\) khi chưa biết mình đang đổi frame hay quay vector.** Hãy diễn giải bài toán bằng lời trước, rồi mới chọn công thức.

**Lỗi 5: đảo thứ tự nhân ma trận do đọc thời gian từ trái sang phải.** Với vector cột, factor bên phải tác động trước. Khi ghép frames, để các indices dẫn đường: \({}^A\mathbf{R}_B{}^B\mathbf{R}_C={}^A\mathbf{R}_C\).

**Lỗi 6: coi homogeneous vector của point và direction vector là như nhau.** Point có phần tử cuối 1, direction vector có phần tử cuối 0.

### Tóm tắt phần 10

Chìa khóa để dùng transformations đúng là giữ nhất quán các frame indices, phân biệt point với direction vector, và xác định rõ current/fixed frame trước khi nhân ma trận.

---

# Kết luận

Rigid-body transformations là ngôn ngữ chung để mô tả position và orientation trong robotics. Bắt đầu từ reference frames, ta biểu diễn orientation bằng rotation matrices; sau đó dùng homogeneous transformations để gộp rotation với translation. Mọi biến đổi phức tạp cuối cùng đều được tạo thành từ các khối đơn giản này, miễn là ta theo dõi cẩn thận frame của từng đại lượng và thứ tự nhân.

Khi gặp một công thức mới, hãy quay lại ba câu hỏi nền tảng:

1. Đại lượng này được biểu diễn trong frame nào?
2. Phép biến đổi đang mô tả quan hệ frame, đổi tọa độ hay quay vector?
3. Phép quay/biến đổi mới được định nghĩa trong current frame hay fixed frame?

Nếu trả lời được ba câu đó, bạn sẽ có nền tảng chắc chắn để học tiếp động học robot, camera geometry, state estimation và điều khiển drone.

---

## Nguồn slide

MEAM 620, *Rigid Body Transformations*, các slide 1–21 của tệp `01_2018_transformations.pdf`.
