# 🔮 trungso

*Thầy phán số cho con. Rồi toán học phán thầy.*

[![Oracle](https://github.com/quocdaijr/trungso/actions/workflows/oracle.yml/badge.svg)](https://github.com/quocdaijr/trungso/actions/workflows/oracle.yml)
[![CI](https://github.com/quocdaijr/trungso/actions/workflows/ci.yml/badge.svg)](https://github.com/quocdaijr/trungso/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)](pyproject.toml)
[![Ruff](https://img.shields.io/badge/lint-ruff-261230.svg)](https://docs.astral.sh/ruff/)
[![tests](https://img.shields.io/badge/tests-459%20passing-brightgreen.svg)](tests/)
[![draws analysed](https://img.shields.io/badge/draws%20analysed-12%2C578-informational.svg)](#kết-quả-tầng-thật-trên-dữ-liệu-thật)
[![chi-square](https://img.shields.io/badge/chi²%20p--value-0.53%20→%20random-informational.svg)](#kết-quả-tầng-thật-trên-dữ-liệu-thật)
[![prediction accuracy](https://img.shields.io/badge/prediction%20accuracy-0%25-critical.svg)](DISCLAIMER.md)
[![expected ROI](https://img.shields.io/badge/expected%20ROI-−86%25-critical.svg)](DISCLAIMER.md)
[![status](https://img.shields.io/badge/status-satire-ff69b4.svg)](DISCLAIMER.md)

**🇬🇧 English → [README.en.md](README.en.md)**

---

> ## ⚠️ ĐỌC CÂU NÀY TRƯỚC
>
> ### Trang này không dự đoán được xổ số. Không phần mềm nào làm được.
>
> Đây là một **thí nghiệm đốt token AI**. Mọi con số ở đây là ngẫu nhiên, và trang tự công
> khai chứng minh điều đó bằng chi-square trên 12.578 kỳ quay.
>
> - **Không bán gì** — không thu tiền, không tài khoản, không quảng cáo
> - **Không liên quan Vietlott** — không liên kết, không tài trợ, không uỷ quyền
> - **Dữ liệu từ mirror bên thứ ba**, có thể sai hoặc thiếu — cần chính xác thì tra [vietlott.vn](https://vietlott.vn)
> - **18+**
> - **Tự chịu rủi ro** — phần mềm cung cấp NGUYÊN TRẠNG, mọi tổn thất là của riêng bạn
>
> 📄 Đầy đủ: [**DISCLAIMER.md**](DISCLAIMER.md)

---

## Vì sao repo này tồn tại

Nói thật: **để số token AI đã đốt không đi đâu mất.**

Đây là sản phẩm phụ của một cuộc thí nghiệm code bằng AI. Thay vì để hàng triệu token trôi
vào hư không, chúng biến thành một thứ chạy được, có test, và tự giễu chính nó.

Giá trị thật duy nhất của repo nằm ở **Tầng Thật** — phần thống kê chứng minh xổ số là ngẫu
nhiên, trên dữ liệu thật của 5 xổ số và 2 quốc gia. Phần còn lại là một ông thầy bói vỉa hè
bằng code.

Con vào đây tìm số để đánh thì thầy nói luôn: số ở đây ngẫu nhiên **đúng bằng** số con tự
bốc. Khác biệt duy nhất là trang này **thừa nhận điều đó**.

## Hai tầng

**Tầng Thật** — thống kê tử tế: tần suất, khoảng cách (gap), kiểm định chi-square so với
phân phối đều. Kết quả dự kiến: `p >> 0.05`, tức là *chả có gì cả*. Và nó in ra đúng như thế.

**Tầng Tà Đạo** — oracle sinh 12 số từ "tín hiệu vũ trụ": thần số học ngày quay, giá BTC,
nhiệt độ Hà Nội, ngày âm lịch, con giáp, và nghiệp báo của số phụ kỳ trước. Zero giá trị
dự báo. 100% giá trị giải trí.

## Thứ làm project này trung thực

Mỗi lời tiên tri sinh **deterministic** từ `sha256(version|game|draw_id|date|signals)` và
được ghi vào `data/predictions.jsonl` **trước** khi kỳ đó quay. Chạy lại ra đúng số cũ.
Không thể sửa hồi tố. Nhờ vậy Bảng Phong Thần mới có ý nghĩa.

## Dùng

```bash
uv sync

uv run trungso ingest --check-gaps      # tải kết quả; tự vá từ vietlott.vn khi mirror lag
uv run trungso stats                    # Tầng Thật: chi-square + phán quyết (mọi nguồn)
uv run trungso oracle                   # Tầng Tà Đạo: 12 số + lời sấm
uv run trungso score                    # dựng lại Bảng Phong Thần
uv run trungso backtest --game mega645  # tiên tri lại toàn bộ lịch sử → ROI
uv run trungso today                    # dashboard kỳ quay tới
uv run trungso site                     # sinh site/data.json cho trang tĩnh
uv run trungso notify --kind prophecy   # đẩy 12 số lên Telegram
```

Xem trang tĩnh:

```bash
uv run trungso site && python3 -m http.server -d site 8000
```

Telegram cần `TELEGRAM_BOT_TOKEN` và `TELEGRAM_CHAT_ID` (GitHub Secrets khi chạy CI).
Thiếu biến thì `notify` báo lỗi rõ ràng, còn pipeline dữ liệu **không bao giờ** bị ảnh hưởng.

## Bốn bộ da

Trang có bốn bộ da đổi được ngay trên nav, lưu ở `localStorage`:

| | giấy | chữ hiển thị | tinh thần |
|---|---|---|---|
| **Vé Số** (mặc định) | giấy ngả vàng | Bungee | vé số vỉa hè, mực riso đỏ |
| **Thần Tài** | đỏ sẫm | Playfair Display | bàn thờ, chữ nhũ vàng |
| **Vỉa Hè** | gần đen | Anton | brutalist, phosphor xanh |
| **Y2K** | tím | Bungee Shade | diễn đàn lô đề đầu 2000 |

Một cấu trúc, bốn bộ da. Mọi màu và font đều qua token trong `site/tokens.css` — không có
giá trị thô nào trong trang. Mọi bề mặt chữ đạt **AA 4.5:1 ở cả bốn bộ da** (thấp nhất 4.56),
đo bằng canvas chứ không ước lượng.

Font display đều đã kiểm có **glyph tiếng Việt** — nhiều font đẹp thì không, và dùng nhầm là
vỡ sạch dấu.

## Cá nhân hoá — và vì sao không có đăng ký

Trang có **Oracle Tử Vi**: nhập ngày sinh (tuỳ chọn thêm tên và giới tính), nhận 12 số riêng
tính từ can chi, nạp âm ngũ hành, cung hoàng đạo, thần số học, sao chiếu mệnh, tam hợp và
tứ hành xung — kèm bảng so kè giữa **số tử vi của bạn**, **oracle nhà cái** và **mức ngẫu
nhiên thuần**.

> **🔒 Không có đăng ký, không có tài khoản, không có server.** Ngày sinh, tên và giới tính
> chỉ nằm trong `localStorage` của trình duyệt. Không request nào mang chúng đi đâu. Nút
> "Xoá dữ liệu" xoá sạch.

Đây là quyết định kiến trúc, không phải sự lười: repo này **commit dữ liệu vào git public**
làm audit trail, nên dữ liệu cá nhân tuyệt đối không được chạm vào đường dữ liệu — git
history thì không xoá được. Mà toàn bộ phần vui đều suy ra được từ mỗi ngày sinh, nên chẳng
cần thu thập gì cả.

Trình duyệt **không** cài lại thuật toán âm lịch: Python sinh sẵn bảng tra (ngày Tết, can
chi, nạp âm mỗi năm 1929–2035) nhúng vào `site/data.json`. Có test đối chiếu chéo chạy
`site/personal.js` thật qua Node để đảm bảo JS và Python không bao giờ lệch nhau.

## Nguồn dữ liệu

| Nguồn | Dùng làm gì | Quy mô |
|---|---|---|
| [`thanhnhu/vietlott`](https://github.com/thanhnhu/vietlott) (MIT) | Nguồn chính — Power 6/55 & Mega 6/45 | 1386 + 1353 kỳ, từ 2017 |
| `vietlott.vn` | Dự phòng khi mirror lag (chỉ lấy được kỳ mới nhất) | — |
| `vietlott.vn` (cùng trang đó) | Giá trị nồi + các hạng giải theo từng kỳ | 2 game |
| [`khiemdoan/vietnam-lottery-xsmb-analysis`](https://github.com/khiemdoan/vietnam-lottery-xsmb-analysis) (MIT) | XSMB — Tầng Thật + tín hiệu vũ trụ | 7526 kỳ, từ 2005 |
| [`jbaranski/jeffs-lottery-utils`](https://github.com/jbaranski/jeffs-lottery-utils) (MIT) | Powerball & Mega Millions — chỉ để thống kê | 1395 + 918 kỳ |
| CoinGecko / Open-Meteo | Tín hiệu vũ trụ (BTC, thời tiết) | — |

`data.ny.gov` (nguồn "chính thống" hay được nhắc tới) **không dùng được**: cả domain trả
403 từ mạng này, kể cả trang HTML thường, có hay không có header browser.

Game Mỹ **chỉ để thống kê** — không tiên tri, không bao 12, không Bảng Phong Thần. Bao 12
là sản phẩm của Vietlott; mục đích duy nhất của data Mỹ là cho Tầng Thật chỉ ra rằng xổ số
Mỹ cũng ngẫu nhiên y như vậy.

### Con số nồi là gì, và không là gì

Trang kết quả ghi giá trị Jackpot **tại kỳ đã quay** — và đó là con số duy nhất một request
HTTP thuần lấy được: vietlott.vn phát ước tính cho kỳ **sắp tới** qua JavaScript, còn các
trang chủ/`choi-ngay` trả về một vỏ 18 KB không có dữ liệu nào.

Nên khi không ai trúng, trang ghi **"ít nhất X"**, vì nồi kỳ sau là X cộng thêm tiền vé bán
ra. Nó không bao giờ ghi "giải đang X". Nó cũng luôn nói rõ tiền đó của **kỳ nào**: nếu lượt
đọc giải thất bại, con số còn lưu thuộc về một kỳ cũ hơn — và một con số cũ mang nhãn hiện
tại đúng là thứ repo này dựng ra để không in.

Phép tính của Bảng Phong Thần **không đổi**. Các hạng cố định đúng là cố định — trang live
xác nhận 40.000.000 / 500.000 / 50.000 cho Power, khớp `games.py` — và nồi thì vốn đã bị loại
khỏi `roi_excluding_jackpot` chính vì nó biến động. Giờ có test bắt bảng tĩnh phải khớp bảng
live, nên upstream đổi giá là nó văng lỗi chứ không im.

### Sáu số hay mười hai? Cả hai — và giờ trang nói rõ số nào là số nào

Vé Vietlott thường — "Cách chơi: **Cơ bản**" trong app — là **6 số, 10.000đ**. Bao 12 là
lựa chọn thật, không phải em nghĩ ra: trang giới thiệu sản phẩm của Vietlott liệt kê **11 mức
bao** (5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 18) và ghi giá một bộ số là 10.000đ, nên
`C(12,6) = 924` tổ hợp = 9.240.000đ là đúng. Các trang tổng hợp bên ngoài hay ghi sai — có bài
liệt kê 7 mức rồi lại nói "11 loại" ngay trong cùng bài — nên chỉ trang gốc được tin.

Trước đây trang chỉ đưa 12 số, tức là ai mua vé Cơ bản phải **tự đoán đánh 6 số nào**. Giờ có
cả hai, và có luôn **ranh giới**: một kỳ điển hình chỉ boost 1–3 số trong 12, phần còn lại
đứng đúng cùng một mức — nên chỉ đúng bấy nhiêu số là có lý do, số còn lại lấy từ thế hoà, và
trang nói thẳng ra.

Hoà thì phá bằng seed của lời tiên tri, **không** theo số tăng dần. Đo ra chứ không chọn cho
đẹp: xếp hoà tăng dần làm 6 số cơ bản có trung bình **20,79** so với **28,52** của bộ 12 —
lệch **7,7** về số nhỏ, sinh ra hoàn toàn bởi cách phá hoà. Ship một quy luật giả thì phá sạch
lý do tồn tại của repo này.

### Hôm nay trúng thì thực nhận bao nhiêu?

Con số ước tính nồi **kỳ tới** không có ở bất kỳ trang nào một request thuần lấy được.
Nhưng câu này thì có — và nó chính là câu mà con số jackpot làm người ta muốn hỏi, nên
trang trả lời bằng số học chứ không bằng một con số nó không có.

Mega 6/45, bao 12 tốn 9.240.000đ:

| trúng | 1 trên | thực nhận | lãi/lỗ |
|---|---|---|---|
| 3 | 7 | 2.520.000đ | −6.720.000đ |
| 4 | 31 | 15.120.000đ | **+5.880.000đ** |
| 5 | 312 | 112.000.000đ | **+102.760.000đ** |
| 6 | 8.815 | 24.946.610.500đ | **+24.937.370.500đ** |

Bảng buộc phải có **cả hai nửa**. Riêng cột tiền đọc ra thành lời khuyên nên chơi — trúng 4
số đã có lãi thật. Riêng cột xác suất đọc ra thành "giải bèo", mà giải không hề bèo. Chỉ khi
đứng cạnh nhau chúng mới nói đúng: tiền là thật, và xác suất là thứ lấy lại. Trúng 4 trở lên
xảy ra khoảng **1 trên 28 kỳ** — đó là chỗ −71,57% đi ra.

## Kết quả Tầng Thật trên dữ liệu thật

Kiểm định chi-square, H₀ = "mọi số đồng xác suất":

| Nguồn | Kỳ | Lượt số | χ² | df | p-value | Bác bỏ H₀? |
|---|---:|---:|---:|---:|---:|---|
| Power 6/55 | 1.386 | 8.316 | 52,45 | 54 | **0,5343** | không |
| Mega 6/45 | 1.353 | 8.118 | 32,57 | 44 | **0,8982** | không |
| Powerball (US) | 1.395 | 6.975 | 78,86 | 68 | **0,1731** | không |
| Mega Millions (US) | 918 | 4.590 | 60,17 | 69 | **0,7671** | không |
| XSMB Miền Bắc | 7.526 | **203.202** | 104,26 | 99 | **0,3391** | không |

Năm xổ số độc lập, hai quốc gia, **231.201 lượt số**, 21 năm dữ liệu — và **không một
nguồn nào** bác bỏ được giả thuyết ngẫu nhiên. Con số nào trông "nóng" cũng chỉ là nhiễu.

## Lịch quay

- **Power 6/55** — 18h thứ 3, thứ 5, thứ 7
- **Mega 6/45** — 18h thứ 4, thứ 6, chủ nhật
- **XSMB** — 18h15 hàng ngày

## Tài nguyên hình ảnh

Toàn bộ **tự host trong repo** — trang không gọi một request nào ra ngoài để lấy ảnh hay emoji.
Chi tiết từng file, kèm ngày tải và cả danh sách nguồn *đã cân nhắc rồi loại*, ở
[`site/img/CREDITS.md`](site/img/CREDITS.md).

| Thứ | Nguồn | Giấy phép |
|---|---|---|
| Tranh khắc gỗ Đông Hồ *Đại Cát* | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Dong_Ho_painting_-_Dai_cat.jpg) | Public domain |
| 13 emoji | [jdecked/twemoji](https://github.com/jdecked/twemoji) — © Twitter/X | đồ hoạ **CC-BY 4.0**, code MIT |
| Hình thầy bói (7 dáng) | vẽ tay trong repo này, `site/thay.js` | MIT, cùng repo |

Repo này là MIT, tức là ai clone cũng được cấp lại quyền phát hành. Nên nó **không thể** chứa
thứ nó không sở hữu: meme nhân vật có bản quyền, ảnh chụp phim, hay ảnh lấy từ mạng xã hội đều
bị loại — không phải vì khó tìm, mà vì không có giấy phép. Cũng đã loại **OpenMoji**: nó là
CC-BY-**SA**, copyleft, xung đột với MIT.

## Giấy phép & miễn trừ trách nhiệm

[MIT](LICENSE) — phần mềm cung cấp **NGUYÊN TRẠNG**, không bảo đảm dưới bất kỳ hình thức nào.
Giấy phép MIT áp cho **code**; tài nguyên bên thứ ba giữ giấy phép riêng, xem bảng trên.

Bản miễn trừ đầy đủ (song ngữ): [**DISCLAIMER.md**](DISCLAIMER.md)

Con dùng cái này để đánh xổ số rồi thua thì đó là quyết định của con, không phải của thầy,
và càng không phải của repo.

### Nếu cờ bạc đang là vấn đề

*Phần này thầy không nói. Đây là chuyện thật.*

Việt Nam **không có** đường dây nóng riêng cho nghiện cờ bạc. Nguồn miễn phí có thật gần nhất
là [Đường dây nóng Ngày Mai](https://duongdaynongngaymai.vn/hotline/) — **096.306.1414**,
13:00–20:30 T4–CN. Đó là hỗ trợ **khủng hoảng tâm lý**, không phải chuyên về cờ bạc, nhưng họ
lắng nghe và không phán xét.
