import asyncio
from typing import Union

from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles

import numpy as np
from PIL import Image
import cv2
import scipy.stats as stats
import scipy as sp

from icecream import ic

app = FastAPI()

threshold = 0.99


def processing(image):
    dct_coefficients = dct(image.file)
    if dct_coefficients is None:
        return {"error": "Failed to process the image."}

    first_digits = get_first_digit_array(dct_coefficients)

    digit_counts = get_digit_counts(first_digits)

    # Calculate the goodness of fit for each digit
    goodness_of_fit = stats.pearsonr(digit_counts, BENFORD)

    results = abs(goodness_of_fit[0]) < threshold

    return {
        "goodness_of_fit": abs(goodness_of_fit[0]),
        "anomaly": bool(results),
    }


@app.post("/benford")
async def benford(image: UploadFile):
    if image.content_type not in ["image/jpeg", "image/png", "image/bmp"]:
        return {
            "error": "Unsupported file type. Please upload a JPEG, PNG, or BMP image."
        }

    result = await asyncio.to_thread(processing, image)
    return result


app.mount("/", StaticFiles(directory="dist", html=True), name="dist")


# Benford's Law distribution
DIGITS = np.arange(1, 10)
BENFORD = np.log10(1 + 1 / DIGITS)


def zigzag(matrix: np.ndarray) -> np.ndarray:
    """
    Zigzag traversal of a 2D matrix to convert a 2D array to a 1D array.
    """
    rows, cols = matrix.shape
    result = []
    for diag in range(rows + cols - 1):
        if diag % 2 == 0:
            # Even diagonal: traverse from bottom-left to top-right
            start_row = min(diag, rows - 1)
            start_col = diag - start_row
            while start_row >= 0 and start_col < cols:
                result.append(matrix[start_row, start_col])
                start_row -= 1
                start_col += 1
        else:
            # Odd diagonal: traverse from top-right to bottom-left
            start_col = min(diag, cols - 1)
            start_row = diag - start_col
            while start_col >= 0 and start_row < rows:
                result.append(matrix[start_row, start_col])
                start_row += 1
                start_col -= 1
    return np.array(result)


def dct(
    filename,
    block_size: int = 8,
) -> list[float]:
    """Perform FFT on an image and return the flattened DCT coefficients."""
    try:
        img = Image.open(filename).convert("L")
    except Exception as e:
        print(f"Error reading {filename}: {e}")

    height, width = img.size

    # Crop the image to a multiple of block_size
    height = height - height % block_size
    width = width - width % block_size

    img = img.resize((height, width))
    img = np.array(img, dtype=np.float32)

    blocks = img.reshape(
        height // block_size, block_size, width // block_size, block_size
    ).swapaxes(1, 2)

    dct_blocks = np.array(
        [
            [
                zigzag(sp.fft.dctn(blocks[i, j], norm="ortho"))
                for j in range(blocks.shape[1])
            ]
            for i in range(blocks.shape[0])
        ],
    )

    return dct_blocks.flatten()


def get_first_digit(value: float) -> int:
    """Get the first digit of a value."""
    value = abs(value)  # Ensure the number is positive
    while value >= 10:
        value //= 10  # Divide by 10 until it's less than 10
    while value < 1 and value > 0:
        value *= 10  # Multiply by 10 until it's at least 1
    return int(value)  # Return the integer part


def get_first_digit_array(array: list[float]) -> list[int]:
    """Get the first digit of each value in an array."""
    return [get_first_digit(value) for value in array]


def get_digit_counts(array: list[int]) -> list[int]:
    """Count the occurrences of each digit in an array."""
    return [array.count(digit) for digit in DIGITS]


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
