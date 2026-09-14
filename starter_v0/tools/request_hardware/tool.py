import json
import uuid
import datetime

def request_hardware(employee_id: str, hardware_type: str, justification: str = "") -> str:
    """Bonus tool: Yêu cầu thiết bị phần cứng mới."""
    if not employee_id:
        return json.dumps({
            "error": "Thiếu mã nhân viên (employee_id). Yêu cầu người dùng cung cấp."
        }, ensure_ascii=False)
        
    if not hardware_type:
         return json.dumps({
            "error": "Thiếu loại thiết bị (hardware_type). Vui lòng cung cấp."
        }, ensure_ascii=False)

    request_id = f"HW-{str(uuid.uuid4())[:8].upper()}"
    status = "pending_approval"
    
    return json.dumps({
        "status": status,
        "request_id": request_id,
        "employee_id": employee_id,
        "hardware_type": hardware_type,
        "message": f"Yêu cầu cấp phát {hardware_type} cho nhân viên {employee_id} đã được ghi nhận. Trạng thái: {status}.",
        "timestamp": datetime.datetime.now().isoformat()
    }, ensure_ascii=False)
