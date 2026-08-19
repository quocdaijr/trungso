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
| [`khiemdoan/vietnam-lottery-xsmb-analysis`](https://github.com/khiemdoan/vietnam-lottery-xsmb-analysis) (MIT) | XSMB — Tầng Thật + tín hiệu vũ trụ | 7526 kỳ, từ 2005 |
| [`jbaranski/jeffs-lottery-utils`](https://github.com/jbaranski/jeffs-lottery-utils) (MIT) | Powerball & Mega Millions — chỉ để thống kê | 1395 + 918 kỳ |
| CoinGecko / Open-Meteo | Tín hiệu vũ trụ (BTC, thời tiết) | — |

`data.ny.gov` (nguồn "chính thống" hay được nhắc tới) **không dùng được**: cả domain trả
403 từ mạng này, kể cả trang HTML thường, có hay không có header browser.

Game Mỹ **chỉ để thống kê** — không tiên tri, không bao 12, không Bảng Phong Thần. Bao 12
là sản phẩm của Vietlott; mục đích duy nhất của data Mỹ là cho Tầng Thật chỉ ra rằng xổ số
Mỹ cũng ngẫu nhiên y như vậy.

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

## Giấy phép & miễn trừ trách nhiệm

[MIT](LICENSE) — phần mềm cung cấp **NGUYÊN TRẠNG**, không bảo đảm dưới bất kỳ hình thức nào.

Bản miễn trừ đầy đủ (song ngữ): [**DISCLAIMER.md**](DISCLAIMER.md)

Con dùng cái này để đánh xổ số rồi thua thì đó là quyết định của con, không phải của thầy,
và càng không phải của repo.

### Nếu cờ bạc đang là vấn đề

*Phần này thầy không nói. Đây là chuyện thật.*

Việt Nam **không có** đường dây nóng riêng cho nghiện cờ bạc. Nguồn miễn phí có thật gần nhất
là [Đường dây nóng Ngày Mai](https://duongdaynongngaymai.vn/hotline/) — **096.306.1414**,
13:00–20:30 T4–CN. Đó là hỗ trợ **khủng hoảng tâm lý**, không phải chuyên về cờ bạc, nhưng họ
lắng nghe và không phán xét.
