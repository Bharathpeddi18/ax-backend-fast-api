import os
import uuid

from fastapi import UploadFile
from azure.identity import DefaultAzureCredential
from azure.storage.blob.aio import BlobServiceClient
from azure.storage.blob import ContentSettings

ACCOUNT_NAME = "astraxtrailazureblob"
CONTAINER_NAME = "astrax-files"

ACCOUNT_URL = (
    f"https://{ACCOUNT_NAME}.blob.core.windows.net"
)

credential = DefaultAzureCredential()

# region upload_file
async def upload_file(file: UploadFile) -> str:

    # Generate a unique file ID
    file_id = str(uuid.uuid4())

    # Connect to Azure
    async with BlobServiceClient(
        account_url=ACCOUNT_URL,
        credential=credential
    ) as service:

        blob = service.get_blob_client(
            container=CONTAINER_NAME,
            blob=file_id
        )

        # Upload file without loading it all into memory
        await blob.upload_blob(
            file.file,
            overwrite=False,
            content_settings=ContentSettings(
                content_type=file.content_type
                or "application/octet-stream"
            )
        )

    return file_id
# endregion

# region delete_file
async def delete_file(file_id: str) -> None:
    async with BlobServiceClient(
        account_url=ACCOUNT_URL,
        credential=credential
    ) as service:

        blob = service.get_blob_client(
            container=CONTAINER_NAME,
            blob=file_id
        )

        await blob.delete_blob()

def get_file_url(file_id: str | None) -> str | None:
    if not file_id:
        return None
    return f"{ACCOUNT_URL}/{CONTAINER_NAME}/{file_id}"

async def download_file_stream(file_id: str):
    async def iterfile():
        async with BlobServiceClient(
            account_url=ACCOUNT_URL,
            credential=credential
        ) as service:
            blob = service.get_blob_client(
                container=CONTAINER_NAME,
                blob=file_id
            )
            stream = await blob.download_blob()
            async for chunk in stream.chunks():
                yield chunk
    return iterfile()