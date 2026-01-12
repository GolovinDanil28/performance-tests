from pydantic import BaseModel, HttpUrl

class GRPCClientConfig(BaseModel):
    port: int
    host: str

    @property
    def client_url(self) -> str:
        return f"{self.host}: {self.port}"