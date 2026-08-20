# CONTEXT — Glossary

Từ vựng chuẩn của project. Đây **chỉ** là glossary — không chứa chi tiết triển khai,
không phải spec, không phải scratch pad.

## Thuật ngữ

**Kỳ quay** (Draw) — Một lượt quay số đã hoàn tất. Danh tính là cặp `(game, draw_id)`.
`draw_id` luôn là chuỗi 5 chữ số zero-pad (`01386`), không bao giờ là số nguyên trần.

**Bộ số chính** (Main) — 6 số được quay ra. Luôn sắp xếp tăng dần.

**Số phụ** (Bonus) — Số thứ 7, **chỉ** Power 6/55 có. Không thuộc bộ số chính và không
bao giờ trùng với số chính. Chỉ dùng để xác định Jackpot 2.

**Bao 12** (Wheel-12) — Cách chơi chọn 12 số rồi đánh toàn bộ `C(12,6) = 924` tổ hợp.
Một kỳ bao 12 cho một game = 9.240.000đ.

**Lời tiên tri** (Prophecy) — 12 số mà oracle cam kết cho một kỳ **chưa quay**, được ghi
lại **trước** thời điểm quay. Sinh deterministic từ seed. Append-only, không sửa được.

**Tầng Thật** (Honest layer) — Thống kê trung thực: tần suất, khoảng cách, chi-square.
Kết luận thường là "không có gì cả", và nó được in ra đúng như vậy.

**Tầng Tà Đạo** (Cursed layer) — Oracle sinh 12 số từ tín hiệu vũ trụ. Giá trị dự báo
bằng không. Đây là phát biểu về sự thật, không phải sự khiêm tốn.

**Tín hiệu vũ trụ** (Cosmic signal) — Một đại lượng có thật (giá BTC, nhiệt độ Hà Nội,
ngày âm lịch, con giáp) được oracle dùng làm cớ. `None` nghĩa là tín hiệu im lặng —
không lấy được — và oracle vẫn phải chạy bình thường.

**Nghiệp báo** (Karma) — Quy tắc tà đạo: số vừa làm số phụ kỳ trước bị giảm trọng số.

**Bảng Phong Thần** (Scoreboard) — Đối chiếu lời tiên tri với kết quả thật: tỉ lệ trúng
so với mức ngẫu nhiên, tiền đốt, tiền thắng, ROI.

**Đốt giấy** (Paper burn) — Tiền **giả định** đã tiêu. Toàn bộ project là paper-trading;
không có dòng nào liên quan tới tiền thật.

**ROI bỏ jackpot** (Jackpot-free ROI) — ROI tính khi loại các giải jackpot. Chỉ số hạng
nhất, không phải phụ lục: một kỳ trúng jackpot trong ~1350 kỳ đủ để đẩy ROI từ −86% lên
dương, trong khi tỉ lệ trúng vẫn đúng bằng mức ngẫu nhiên.

**Backtest** — Chạy lại oracle trên lịch sử. **Phản thực** (counterfactual): không phải
tiên tri đã cam kết, và không bao giờ được ghi vào `predictions.jsonl`.

**Game đánh được bao 12** (wheel-playable) — Game có cơ cấu giải và giá vé để định giá bao
12, tức là Vietlott. Chỉ những game này mới có tiên tri, bao 12 và Bảng Phong Thần.

**Game chỉ thống kê** (stats-only) — Powerball và Mega Millions. Mang vào **chỉ** để Tầng
Thật chỉ ra rằng xổ số Mỹ cũng ngẫu nhiên y như Vietlott. Không tiên tri, không bao 12.

**Pool phụ riêng** (separate bonus pool) — Số phụ được quay từ dải số riêng, nên **được
phép trùng** số chính. Powerball (đỏ 1–26) và Mega Millions (vàng 1–25) là vậy: có 99 và 68
kỳ thật trùng như thế. Khác hẳn số phụ Power 6/55, quay cùng dải và không được trùng.

**XSMB** — Xổ số kiến thiết Miền Bắc. **Không** dùng kiểu `Kỳ quay` vì nó phá mọi bất biến
của `Draw`: 27 giải mỗi ngày, không gian 00–99 (**có số 0**), và **cho phép trùng lặp**
trong cùng một kỳ. Có kiểu `XsmbDraw` riêng. Không bao giờ sinh tiên tri.

**Upstream lag đã vá** (patched lag) — Kỳ mà mirror bỏ sót, được lấy bù từ `vietlott.vn`.
Trang chính thức **chỉ** cho kỳ mới nhất, nên chỉ vá được đúng ca lag phổ biến nhất.

**Upstream lag** — Trạng thái mirror không có gap `draw_id` nào nhưng vẫn thiếu kỳ so với
thực tế. Khác với **gap**, và cần cơ chế phát hiện riêng.

**Lá số** (Fortune) — Tập hợp suy ra được **chỉ từ ngày sinh**: can chi, con giáp, nạp âm,
mệnh ngũ hành, cung hoàng đạo, số chủ đạo, số tên, sao chiếu mệnh, tam hợp, tứ hành xung.
Là **dữ liệu dẫn xuất** — không chứa tên, không chứa ngày sinh.

**Oracle Tử Vi** (personal oracle) — Oracle riêng theo lá số, chạy **hoàn toàn trong trình
duyệt**. Khác với **oracle nhà cái** (Tầng Tà Đạo) vốn chạy trong CI và có Bảng Phong Thần
công khai.

**Chỉ-tại-máy** (local-only) — Nguyên tắc bất di bất dịch: ngày sinh, tên và giới tính nằm
trong `localStorage`, không có tài khoản, không có server, không request nào mang chúng đi.
Repo này commit dữ liệu vào git public, nên PII **không được phép** chạm vào đường dữ liệu.

**Bảng tra âm lịch** (lunar lookup table) — Bảng do Python sinh (ngày Tết + can chi + nạp âm
mỗi năm) nhúng trong `site/data.json`. Trình duyệt **không** cài lại thuật toán âm lịch; nó
tra bảng. Nhờ vậy hai bên không thể lệch nhau, và có test đối chiếu chéo qua Node.

**Thầy / con** — Ngôi xưng hô của **mọi văn bản hướng tới người đọc**: lời sấm, README,
tagline, và câu kết mục giấy phép. Thầy bói vỉa hè, không phải trợ lý. Thầy **không bao giờ**
nói "chắc chắn trúng" — đó là câu của trang lừa đảo, và là ranh giới cứng.

Thầy **im lặng** ở ba chỗ: khối miễn trừ trách nhiệm, mọi số liệu thống kê, và mục hỗ trợ tâm
lý. Độ vênh giữa bốn chặng gào thét và ba chỗ im lặng chính là cú hài — và cũng là thứ giữ cho
project trung thực. Xoá độ vênh đó là mất cả hai.

Cách gọi người đọc, theo vùng:

| Vùng | Gọi là | Ví dụ |
|---|---|---|
| Phần diễn — lời sấm, tagline, "vì sao repo tồn tại", câu kết mục giấy phép | **con** | *"Con cứ ghi đi, đúng sai tính sau."* |
| Ba vùng thầy im lặng — miễn trừ trách nhiệm, số liệu thống kê, hỗ trợ tâm lý | **bạn** (trung tính) | *"Mọi tổn thất tài chính là của riêng bạn."* |
| Khối cam kết riêng tư | **bạn** — đây là lời hứa người đọc tin vào, không phải chỗ diễn | *"chỉ nằm trong trình duyệt của bạn"* |

**"anh" / "chị"** thì không bao giờ — đó là giọng chat giữa người viết và chủ repo, đã từng
lọt vào README một lần và phải sửa. Nó không phải giọng của project.

**Bộ da** (skin) — Một trong bốn bảng token: `veso` · `thantai` · `viahe` · `y2k`. Đổi lúc
chạy, lưu `localStorage`. Cấu trúc trang không đổi theo bộ da; chỉ token đổi.

**Chặng** (stage) — Một trong năm bước có thứ tự của trang: KHAI → TƯỚNG → PHÁN → SỔ NỢ →
SỰ THẬT. Số chặng là **cấu trúc**, không phải trang trí.

**Cạn phước** — Tiếng lóng 2026, nghĩa là hết may. Con dấu bật ở Sổ Nợ khi ROI-bỏ-jackpot
xuống dưới −0,8. Là chỗ **duy nhất** giọng thầy được chạm vào khu số liệu.

**Bộ weight tà đạo** — Các hằng `BOOST_*` là **tuỳ ý có chủ đích**. Mọi bộ weight đều cho
cùng một EV, nên đây là lựa chọn thẩm mỹ chứ không phải tối ưu. Nói ngược lại là phá chính
tính trung thực mà project dựng lên.

**Luật trùng số gốc** (digit-root rule) — Boost số có **cùng số gốc** với mục tiêu, **không
phải** chia hết. Chia hết với số gốc 1 sẽ trúng toàn bộ dải số — một luật kích hoạt với mọi
số thì không còn là luật.

**Hình thầy** — Ông thầy bói vẽ bằng nét que, bảy dáng, sống trong repo này. Dáng được
chọn theo **số trúng thật** của kỳ chấm được cao nhất, nên nó là một cách đọc số liệu chứ
không phải đồ trang trí. Vẽ lệch có chủ ý: nét hoàn hảo là dấu hiệu máy làm.

**Bản in Đại Cát** — Tranh khắc gỗ Đông Hồ, public domain, đặt cạnh ROI âm. *Đại Cát* nghĩa
là **vận may lớn**; đó là toàn bộ câu đùa. Hiện đúng **một chỗ** trên trang, và chỉ khi kỳ tốt
nhất đạt từ 5 số trở lên.

**Tự host** — Mọi ảnh và emoji nằm trong repo. Trang không gọi request ra ngoài để lấy tài
nguyên hình ảnh. Ngoại lệ duy nhất có từ trước là Google Fonts.

**Cấp lại quyền** (sublicense) — Repo MIT cấp cho người clone quyền phát hành lại. Nên repo
không được chứa thứ nó không sở hữu. Đây là lý do loại meme nhân vật có bản quyền, ảnh phim,
và ảnh lấy từ mạng xã hội — thiếu giấy phép, không phải thiếu chỗ tìm.

**Nồi** (jackpot) — Giá trị Jackpot **tại kỳ đã quay**, đọc từ trang kết quả vietlott.vn.
Không phải ước tính cho kỳ sắp tới: vietlott chỉ phát con số ước tính qua JavaScript, HTML
thuần không có. Vì vậy trang **không bao giờ** gọi nó là "giải đang", chỉ gọi là nồi của
kỳ nào.

**Cộng dồn** (rolled over) — Hạng cao nhất của kỳ đó không ai trúng, nên nồi chuyển sang kỳ
sau. Đây là lý do câu duy nhất đúng là **"ít nhất X"**: kỳ sau sẽ là X cộng thêm tiền vé
bán ra. Trúng rồi thì nồi về mức sàn, và trang phải nói ra chuyện đó chứ không im.

**Khớp kỳ mới nhất** (`matches_latest_draw`) — Cờ so `draw_id` của số liệu giải với kỳ mới
nhất đã lưu. Nếu lượt đọc giải thất bại, con số còn lại thuộc về một kỳ cũ hơn; giấu nó thì
mất thông tin, mà trưng nó như số hiện tại thì là nói dối. Cờ này để trang nói rõ tiền đó
của kỳ nào.

**Mức sàn** (`jackpot_floor`) — Giá trị nồi reset về sau khi có người trúng. Cũng là ngưỡng
để bắt lỗi bóc dữ liệu: một "jackpot" thấp hơn mức sàn không phải jackpot nhỏ, nó là regex
bắt sai dòng — parser phải văng lỗi thay vì công bố.

## Từ tránh dùng

- **"số nóng" / "số lạnh" / "cầu" / "soi cầu"** — chỉ dùng khi đang trích dẫn để bóc phốt,
  không bao giờ dùng như khái niệm của project.
- **"power645"** — tên file của upstream đặt sai. Game đó tên là **Mega 6/45** (`mega645`).
  Tên sai chỉ được phép tồn tại ở đúng một chỗ: `GameSpec.mirror_filename`.
- **"dự đoán"** hiểu theo nghĩa thật — oracle **không** dự đoán. Nó *tiên tri*, và đó là
  từ được chọn có chủ ý.
- **"data.ny.gov"** như một nguồn khả dụng — cả domain trả 403 từ mạng này. Nguồn Mỹ đang
  dùng là `jbaranski/jeffs-lottery-utils`.
- **"cloudscraper"** như thứ bắt buộc để crawl `vietlott.vn` — đã kiểm chứng là **không
  cần**: `requests` kèm User-Agent browser trả về 200.
- **"đăng ký" / "tài khoản" / "thu thập dữ liệu người dùng"** — không tồn tại trong project
  này và sẽ không tồn tại. Cá nhân hoá đạt được **không cần** lưu gì của ai.
- **"chắc chắn trúng" / "số chuẩn" / "cam kết"** — thầy bựa tới đâu cũng dừng trước câu này.
- **"giải đang X tỷ"** — trang không biết con số đó. Nó biết nồi của kỳ đã quay,
  nên chỉ được nói **"ít nhất X"** khi cộng dồn, và phải kèm số kỳ.
- **"em"** khi oracle nói — oracle xưng **thầy**, gọi **con**. Không phải trợ lý.
- **"thấy trên Facebook"** như một nguồn tài nguyên — mạng xã hội không phải giấy
  phép. Ảnh không có nguồn và licence xác minh được thì không vào repo.
