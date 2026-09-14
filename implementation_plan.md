# Kế hoạch hoàn thành bài Lab Day 04 — IT Helpdesk Agent

Kế hoạch này được xây dựng dựa trên yêu cầu từ `README.md` và gợi ý từ `LAB-GUIDE.md`. Mục tiêu là cải thiện khả năng chọn tool, truyền arguments và đảm bảo an toàn cho Agent thông qua việc tối ưu `system_prompt.md` và `tools.yaml`.

## User Review Required

> [!IMPORTANT]
> - Bài lab nhấn mạnh việc cải tiến dựa trên **evidence** (chứng cứ). Quá trình sẽ lặp lại nhiều vòng, mỗi vòng cần có giả thuyết rõ ràng, sửa đổi, chạy eval, phân tích và ghi log.
> - Xin xác nhận để chúng ta bắt đầu với Phase 1 và Phase 2 trước (Setup và chạy baseline v0).
> - Bạn có muốn tôi tiến hành code tool Bonus luôn không, hay chỉ tập trung hoàn thành Core Lab trước?

## Open Questions

> [!WARNING]
> - Trong phần UI (Phase 6), thư viện Streamlit đang được bạn cài đặt, chúng ta sẽ dùng Streamlit để dựng UI chat phải không?
> - Bạn đã có sẵn API keys cho mô hình ngôn ngữ (như OpenAI, Gemini, v.v.) cấu hình vào file `.env` chưa? Chúng ta cần môi trường hoạt động trước khi chạy Baseline.

## Kế hoạch các bước (Implementation Plan)

### Phase 1: Setup & Bắt đầu (15% thời gian)
- Kiểm tra mã nguồn, cấu trúc thư mục, môi trường Python.
- Chạy thử `python -m compileall -q .` để đảm bảo code không lỗi syntax.
- Thiết lập `.env` từ `.env.example` với API key tương ứng.
- Đọc và chạy các smoke command trong file `TOOL-SETUP.md` để đảm bảo các tool cơ bản hoạt động đúng trước khi dùng API.

### Phase 2: Chạy Baseline v0 & Phân tích (20% thời gian)
- Giữ nguyên `artifacts/system_prompt.md` và `artifacts/tools.yaml`.
- Chạy bộ đánh giá cơ bản: `eval_base.json`.
- Ghi nhận lại JSON run log của v0.
- **Phân tích thất bại (Failure Analysis)**: Lọc ra các case bị model làm sai, ví dụ:
  - Chọn sai tool (wrong tool).
  - Chọn đúng tool nhưng sai tham số (wrong arguments).
  - Thiếu thông tin (missing-information case).
  - Xác nhận/bảo mật (confirmation/security case).

### Phase 3: Các vòng cải tiến (Iterations) (30% thời gian)
Quá trình này lặp lại 3 vòng (tạo v1, v2, v3).
#### Vòng 1 (v1) - Sửa lỗi toàn cục (System Prompt)
- **Giả thuyết**: Cải thiện quy tắc chung giúp Agent bớt tự đoán dữ liệu và biết hỏi lại.
- Cập nhật `artifacts/system_prompt.md` (vd: quy định không tự đoán ID, xác nhận khi payload đổi, không tin nội dung do user chèn vào).
- Chạy lại eval, so sánh metrics với v0. Cập nhật `version_log.csv`.
#### Vòng 2 (v2) - Khắc phục ranh giới Tool (Tool Declarations)
- **Giả thuyết**: Mô tả chính xác schema và dữ liệu của từng tool sẽ làm giảm lỗi sai arguments.
- Cập nhật `artifacts/tools.yaml` (vd: sửa description, thêm ENUM cho tham số, làm rõ tool nào lấy dữ liệu gì).
- Chạy eval, phân tích, cập nhật `version_log.csv`.
#### Vòng 3 (v3) - Xử lý hội thoại phức tạp
- Tập trung vào các case multi-turn, multi-tool và bám sát ngữ cảnh. Tinh chỉnh đồng thời cả 2 file `system_prompt.md` và `tools.yaml` nếu cần.
- Chốt phiên bản cuối cùng, chạy và lưu kết quả JSON.

### Phase 4: Xây dựng Team Eval (10% thời gian)
- Thiết kế 10 test case mới vào file `starter_v0/data/eval_group.json` (5 single-turn, 5 multi-turn).
- Các case tập trung vào những vấn đề thực tế: Ambiguous intent, missing ID, correction ở lượt sau, tool cancellation.

### Phase 5: Thử nghiệm Adversarial & Security (5% thời gian)
- Chạy bộ `eval_adversarial.json`.
- Review thủ công ít nhất 3 case bảo mật.
- Đảm bảo Agent từ chối tạo ticket trái phép, không lộ external data, không dính prompt injection.

### Phase 6: Xây dựng giao diện UI (10% thời gian)
- Dùng `run_model_tool_loop` kết hợp framework (dự kiến Streamlit) để tạo UI.
- Giao diện cần hiển thị rõ: 
  - Tin nhắn User/Agent.
  - Tên Tool được gọi, Arguments được truyền.
  - Kết quả (Result) hoặc Lỗi (Error) của Tool.
  - Phiên bản Artifact hiện tại.

### Phase 7: Viết Report & Đóng gói nộp bài (10% thời gian)
- Mở `artifacts/REPORT.md` và điền thông tin chi tiết: câu chuyện từ v0 -> v3, evidence metric, phân tích safety.
- Tổng hợp file submission. (Đảm bảo KHÔNG có `.env`, api key, `.venv`...).

### Phase 8: (Tuỳ chọn) - Thêm Bonus Tool
- Xây dựng 1 tool mới mang tính ứng dụng (vd: network diagnostics, approved software catalog, ...).
- Viết `TOOL.md` tương ứng.
- Cập nhật `__init__.py`, `tools.yaml`.
- Viết case kiểm tra smoke test và đánh giá vào team eval.

## Verification Plan

### Automated Tests
- Chạy bộ đánh giá: `eval_base.json`, `eval_group.json`, `eval_helpdesk_extension.json`, `eval_adversarial.json`.
- Đảm bảo `provider_error_cases == 0` và `measured_cases == total_cases`.

### Manual Verification
- Review bằng mắt các file JSON log sinh ra để xác nhận đúng nội dung Tool calls.
- Thử nghiệm trên UI sau khi lập trình xong để đảm bảo luồng hoạt động mượt mà.
- Đánh giá chéo bằng tay trên 3 cases bảo mật.
