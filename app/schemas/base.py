from pydantic import BaseModel

class BaseSchema(BaseModel):
    class Config:
        from_attributes = True
        str_strip_whitespace = True
        use_enum_values = True