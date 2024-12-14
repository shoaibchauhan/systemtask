import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'systemtask.settings')
django.setup()



from fastapi import FastAPI
from myapp import router


app = FastAPI()
app.include_router(router.router)


@app.get("/")
def root():
    return {"message": "hello"}