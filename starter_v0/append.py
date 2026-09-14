import json

with open("artifacts/tools.yaml", "a", encoding="utf-8") as f:
    f.write('''
  - name: request_hardware
    description: "Yêu cầu cấp phát thiết bị phần cứng mới. Bắt buộc phải có mã nhân viên (employee_id) và loại thiết bị (hardware_type)."
    parameters:
      type: object
      properties:
        employee_id: {type: string, description: "Mã nhân viên"}
        hardware_type: {type: string, description: "Loại thiết bị yêu cầu (VD: monitor, mouse, keyboard)"}
        justification: {type: string, default: "", description: "Lý do yêu cầu"}
      required: [employee_id, hardware_type]
''')
print("Done appending to tools.yaml")
