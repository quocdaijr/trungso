# Nguồn tài nguyên · Asset credits

Mọi file trong thư mục này **tự host**. Trang không gọi một request nào ra ngoài để lấy
ảnh hay emoji.

---

## `dong-ho-dai-cat.webp`

- **Tên gốc:** *Đại Cát* (大吉 — "đại cát", vận may lớn), tranh khắc gỗ Đông Hồ
- **Nguồn:** [Wikimedia Commons — `Dong Ho painting - Dai cat.jpg`](https://commons.wikimedia.org/wiki/File:Dong_Ho_painting_-_Dai_cat.jpg)
- **Giấy phép:** **Public domain**
- **Ngày tải:** 2026-08-19
- **Đã xử lý:** `cwebp -q 72 -resize 240 0` — từ 500×684 JPG (127 KB) xuống 240px WebP (21 KB).
  Hiển thị ≤160px nên 240px cho 1,5× mật độ; tranh màu phẳng nên không cần hơn.

## `emoji/*.svg` — 13 file

- **Nguồn:** [jdecked/twemoji](https://github.com/jdecked/twemoji) (fork còn được maintain của
  `twitter/twemoji`), thư mục `assets/svg/`
- **Giấy phép:** **đồ hoạ CC-BY 4.0** · code MIT — xem
  [`LICENSE-GRAPHICS`](https://github.com/jdecked/twemoji/blob/master/LICENSE-GRAPHICS)
- **Bản quyền:** © Twitter / X
- **Ngày tải:** 2026-08-19
- **Attribution:** README của Twemoji nói rõ *"we will accept a mention in a project README or
  an 'About' section or footer on a website"*. Ghi công ở footer colophon của trang, ở
  `README.md`, và ở đây.
- **Không sửa đổi** — dùng nguyên bản.

Codepoint đã tải: `1f52e 🔮` `26a0 ⚠` `1f512 🔒` `1f480 💀` `1f340 🍀` `262f ☯` `1f4c9 📉`
`1f4ca 📊` `1f321 🌡` `1f558 🕘` `1f1fb-1f1f3 🇻🇳` `1fa84 🪄` `1f3b2 🎲`

## Hình thầy bói — `site/thay.js`

- **Nguồn:** vẽ tay trong repo này, không dựa trên nhân vật nào có sẵn
- **Giấy phép:** MIT, cùng phần còn lại của repo
- Là **inline SVG** chứ không phải file ảnh, để `currentColor` kế thừa và hình tự đổi màu theo
  cả bốn bộ da

---

## Đã cân nhắc và loại

| Nguồn | Vì sao loại |
|---|---|
| **OpenMoji** | CC-BY-**SA** 4.0 — copyleft. Sửa là phải mở lại theo CC-BY-SA, xung đột repo MIT |
| **Template meme nổi tiếng** (Drake, Distracted Boyfriend…) | Là ảnh stock / phim / người thật, có bản quyền |
| **Nhân vật kiểu Flork** | [The Flork Company](https://www.florkofcows.com/licensing-attribution/) giữ bản quyền + thương hiệu, và **không cấp phép cho AI** |
| **Ảnh phim** (VD *King of the Hill*) | 20th Television / Disney |
| **Meme lấy từ mạng xã hội** | "Thấy trên Facebook" không phải giấy phép |

Lý do bao trùm: repo này là **MIT**, nghĩa là nó cấp quyền phát hành lại cho mọi người clone.
Không thể cấp quyền cho thứ mình không sở hữu.
