from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import magic
import io
import logging

# Set up logging to capture any errors
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

# Initialize magic
magic_instance = magic.Magic()

@app.get("/", response_class=HTMLResponse)
async def main():
    html_content = """
    <html>
        <body>
            <h2>Select a file to identify its format:</h2>
            <form action="/identify" method="post" enctype="multipart/form-data">
                <input type="file" name="file" required>
                <input type="submit">
            </form>
        </body>
    </html>
    """
    return html_content

@app.post("/identify", response_class=HTMLResponse)
async def identify_file(file: UploadFile = File(...)):
    try:
        # Read the file
        file_content = await file.read()

        # Log the received file size and part of the content for debugging
        logger.debug(f"Received file with size: {len(file_content)} bytes")

        # Identify the MIME type and file type
        mime_type = magic.from_buffer(file_content, mime=True)
        file_type = magic_instance.from_buffer(file_content)

        # Log the identified file types
        logger.debug(f"Identified MIME Type: {mime_type}")
        logger.debug(f"Identified File Type: {file_type}")

        # Return result
        result = f"<h3>File Type: {file_type}</h3><p>MIME Type: {mime_type}</p>"
        return result
    except Exception as e:
        # Log and return the error message
        logger.error(f"Error processing file: {str(e)}")
        return f"<h3>Error: {str(e)}</h3>"

