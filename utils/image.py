import os
import asyncio
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

from utils.log import logger


def add_image_watermark_sync(
    input_file: BytesIO,
    watermark_image_path: str,
    image_path: str,
    opacity: int = 128,
):
    original = Image.open(input_file).convert("RGBA")
    if not os.path.exists(watermark_image_path):
        logger.error(
            "There is no watermark image, it has not been applied to the photo"
        )
    else:
        watermark = Image.open(watermark_image_path).convert("RGBA")

        watermark = watermark.resize(original.size, Image.LANCZOS)

        original_width, original_height = original.size
        position = (
            (original_width - watermark.width) // 2,
            (original_height - watermark.height) // 2,
        )

        watermark_with_alpha = watermark.copy()
        watermark_with_alpha.putalpha(opacity)

        original.paste(watermark_with_alpha, position, watermark_with_alpha)

    original.convert("RGB").save(image_path, "JPEG")


async def add_image_watermark(
    input_file: BytesIO,
    watermark_image_path: str,
    image_path: str,
    opacity=128,
):
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        await loop.run_in_executor(
            pool,
            add_image_watermark_sync,
            input_file,
            watermark_image_path,
            image_path,
            opacity,
        )


async def main():
    import os

    input_image_path = os.path.join(
        os.getcwd(), "data/pfp/Screenshot 2024-08-21 at 4.50.59 pm.png"
    )
    watermark_image_path = os.path.join(os.getcwd(), "data/watermark.png")

    await add_image_watermark(
        input_image_path,
        watermark_image_path,
        opacity=128,
    )


if __name__ == "__main__":
    asyncio.run(main())
