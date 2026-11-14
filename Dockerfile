# 1. Base image ขนาดเล็กและเสถียร
FROM python:3.11-slim

# 2. ตั้งค่า Environment Variables สำหรับ Python ใน Container
# - PYTHONDONTWRITEBYTECODE: ไม่สร้างไฟล์ .pyc ในคอนเทนเนอร์
# - PYTHONUNBUFFERED: ส่ง log ออก console ทันทีโดยไม่ต้องรอ buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

# 3. กำหนด Working directory
WORKDIR /app

# 4. ติดตั้ง dependencies ก่อน (ใช้ประโยชน์จาก Docker Layer Caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. สร้าง Non-root user เพื่อความปลอดภัย (Security Best Practice)
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# 6. คัดลอกซอร์สโค้ดทั้งหมดเข้ามา
COPY . .

# 7. สลับไปใช้ Non-root user (ไม่รันด้วย root)
USER appuser

# 8. เปิดพอร์ตสำหรับการเชื่อมต่อ
EXPOSE 5000

# 9. Healthcheck ให้ Docker ตรวจสอบความพร้อมของ Container
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# 10. รันด้วย Production WSGI Server (Gunicorn)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "app:app"]
