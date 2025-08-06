import json
from datetime import datetime
from typing import Type
from langchain.tools import BaseTool




class get_current_time_tool(BaseTool):
    """Tool to get current date and time"""
    name: str = "get_current_time"
    description: str = "Lấy thời gian thực hiện tại theo giờ và ngày"
    args_schema: Type = None

    def _run(self) -> str:
        """Execute the tool"""
        try:
            current_time = datetime.now()

            # Format time info
            time_info = {
                "current_datetime": current_time.isoformat(),
                "formatted_time": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                "day_of_week": current_time.strftime("%A"),
                "date": current_time.strftime("%Y-%m-%d"),
                "time": current_time.strftime("%H:%M:%S"),
                "timestamp": current_time.timestamp()
            }

            return json.dumps(time_info, indent=2)

        except Exception as e:
            return f"Error getting current time: {str(e)}"