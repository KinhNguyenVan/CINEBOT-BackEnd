from langchain_core.tools import BaseTool
from typing import Type
from pydantic import BaseModel
from app.schemas.user import VerifyUserInput
from pydantic import EmailStr
from app.service.auth_service import verify_email,verify_OTP,OTPVerifyInput
from app.core.database import get_db
from sqlalchemy.orm import Session
from pydantic import EmailStr
from pydantic import Field
from app.utils.otp import verify_otp



class send_otp_tool(BaseTool):
    name: str = "send_otp_tool"
    description :str = "Gửi otp về email người dùng cung cấp để xác nhận email sau khi được cung cấp email"
    args_schema: Type[BaseModel] = VerifyUserInput
    
    def _run(self,email:EmailStr,name: str, **kwargs):
        db: Session = next(get_db())
        user_input = VerifyUserInput(email=email, name=name)
        return verify_email(db, user_input)
    


class verify_otp_tool(BaseTool):
    name: str = "verify_otp_tool"
    description: str = "Xác nhận OTP từ cache và từ OTP người dùng nhập"
    args_schema :Type[BaseModel] = OTPVerifyInput

    def _run(self,email: EmailStr, otp:str, **kwargs):
        db: Session = next(get_db())
        user_input = OTPVerifyInput(email = email,otp=otp)
        return verify_OTP(db,user_input )