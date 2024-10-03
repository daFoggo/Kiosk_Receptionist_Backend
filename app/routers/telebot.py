import os
import httpx
from fastapi import APIRouter, HTTPException

from ..schemas import ContactCreate

router = APIRouter()

# Gui tin nhan qua Telegram
class TelegramService:
    def __init__(self, bot_token: str):
        if not bot_token:
            raise ValueError("BOT_TOKEN must be provided")
        self.bot_token = bot_token
        self.base_url = f"https://api.telegram.org/bot{bot_token}"

    async def send_message(self, phone_number: str, message: str):
        try:
            chat_id = await self._get_chat_id_by_phone(phone_number)

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": message,
                        "parse_mode": "Markdown"
                    }
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            raise Exception(f"Failed to send Telegram message: {str(e)}")

    # Tim chat_id tu database ( tam thoi fix cung 1 user )
    async def _get_chat_id_by_phone(self, phone_number: str) -> int:
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        if not chat_id:
            raise ValueError("TELEGRAM_CHAT_ID must be set")
        return chat_id

# API
@router.post("/api/contact")
async def create_contact(contact: ContactCreate):
    try:
        telegram_service = TelegramService(os.getenv("BOT_TOKEN"))

        message = f"""
🔔 *Thông báo có khách liên hệ*

👤 *Thông tin khách:*
- Họ tên: {contact.cccdInfo.name}
- CCCD: {contact.cccdInfo.identityCode}
- Ngày sinh: {contact.cccdInfo.dob}
- Giới tính: {contact.cccdInfo.gender}

📞 *Bên cần liên hệ:*
- Có lịch hẹn: {'Có' if contact.isAppointment else 'Không'}
- Thời gian hẹn: {contact.appointmentTime}
- Số điện thoại: {contact.phoneNumber}
- Phòng ban: {convertDepartment(contact.department)}


📝 *Ghi chú:* {contact.note}
        """

        await telegram_service.send_message(contact.phoneNumber, message)

        return {"status": "success", "message": "Đã gửi thông tin thành công"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def convertDepartment(department: str):
    if department == "bld":
        return "Ban lãnh đạo"
    elif department == "phongTh":
        return "Phòng tổng hợp"
    elif department == "phongKhcnvkhcd":
        return "Phòng Khoa học công nghệ và Kế hoạch kinh doanh"
    elif department == "phongTvtk":
        return "Phòng tư vấn thiết kế"
    elif department == "phongNckyvdvvt":
        return "Phòng nghiên cứu kỹ thuật và dịch vụ viễn thông"
    elif department == "phongDlkdvtccl":
        return "Phòng đo lường kiểm định và tiêu chuẩn chất lượng"
    elif department == "phongUdvcgcns":
        return "Phòng ứng dụng và chuyển giao công nghệ số"
    elif department == "phongNcptcns":
        return "Phòng nghiên cứu phát triển công nghệ số"
    elif department == "cs2":
        return "Cơ sở 2 của Viện tại TP.Hồ Chí Minh"
    else:
        return "Không xác định"