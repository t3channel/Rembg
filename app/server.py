from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import Response
from rembg import remove
import io
import uvicorn

app = FastAPI()

@app.post("/remove_background")
async def remove_background_api(image_bytes: bytes = Body(..., media_type="image/jpeg")):
    """
    画像データ (バイト配列) を受け取り、rembgを使用して背景を透過した
    PNG画像データ (バイト配列) を返します。
    """
    if not image_bytes:
        raise HTTPException(status_code=400, detail="No image bytes provided.")

    try:
        # 1. rembgによる背景透過処理
        # input_dataはバイト配列 (binary) のままremoveに渡します
        output_data = remove(image_bytes)

        # 2. 結果のバイト配列 (PNG形式) をContent-Typeを指定して返す
        return Response(content=output_data, media_type="image/png")

    except Exception as e:
        # 処理中にエラーが発生した場合
        print(f"Error during image processing: {e}")
        raise HTTPException(status_code=500, detail=f"Image processing failed: {e}")

#if __name__ == "__main__":
uvicorn.run(app, host="0.0.0.0", port=8000)