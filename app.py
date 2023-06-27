import io
import uvicorn
from src.config import parameters
from src.pipline import Pipline
from src.start import tokenizer
import pandas as pd
from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse

app = FastAPI(title="Text-Analysis")

pl = Pipline(tokenizer)


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    input_texts_df = pd.read_csv(file.file, sep="\t")
    try:
        texts = list(input_texts_df.iloc[:, 0])
        stream = io.StringIO()
        unique_texts = pl.duplidelete(texts, 0.8)
        unique_texts_df = pd.DataFrame(unique_texts, columns=["texts"])
        unique_texts_df.to_csv(stream, index=False)
        response = StreamingResponse(iter([stream.getvalue()]),
                                     media_type="text/csv"
                                     )

        response.headers["Content-Disposition"] = "attachment; filename=export.csv"
        return response
    except:
        return {"file name:", file.filename}

if __name__ == "__main__":
    uvicorn.run(app, host=parameters.service_host, port=parameters.service_port)
