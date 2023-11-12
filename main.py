from typing import Annotated

from fastapi import FastAPI, UploadFile, Form, HTTPException, status
from controllers.AdminController import AC
from controllers.AdminLoginController import log_
import uvicorn
import numpy as np
import cv2
import face_recognition

from services.ServiceEmployer import EmpBaseModel

app = FastAPI()


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile, emp_fullname=Form(min_length=3, max_length=60),
                             emp_password=Form(),
                             emp_email=Form(), emp_ip=Form(default=None)):
    content_file = await file.read()
    np_array = np.frombuffer(content_file, dtype=np.uint8)
    mat = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    codings = face_recognition.face_encodings(mat)
    print(codings)

    if len(codings) != 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="bad image Error in conding")
    model = EmpBaseModel(emp_fullname=emp_fullname.strip(' ').title(), emp_email=emp_email,
                         emp_password=emp_password,
                         emp_coding=codings[0].tobytes())

    return {"success": "upload coding"}


@app.post('/addEmp')
async def create_upload_file(emp_: EmpBaseModel):
    return emp_.emp_ip


app.include_router(AC, tags=['Admin Controller'])
app.include_router(log_, tags=['security'])
if __name__ == '__main__':
    uvicorn.run("main:app", port=8090, reload=True)
