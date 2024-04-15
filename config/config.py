from dotenv import load_dotenv
import os


load_dotenv()
token_todoly = os.getenv("TOKEN")

URL_TODO_LY = "https://todo.ly/api"

HEADERS_TODO_LY = {
            "Token": token_todoly
}

abs_path = os.path.abspath(__file__ + "../../../")
