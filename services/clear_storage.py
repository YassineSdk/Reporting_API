import logging
from datetime import datetime, timedelta
import shutil
import os


logger = logging.getLogger(__name__)

def clear_storage():
    if not os.path.exists("storage"):
        logger.info("Storage directory does not exist, skipping cleanup")
        return
    
    now = datetime.now()
    cutoff = timedelta(minutes=20)
    deleted = 0

    for folder in os.scandir("storage"):
        if folder.is_dir():
            created_at = datetime.fromtimestamp(folder.stat().st_mtime)
            age = now - created_at
            if age > cutoff:
                shutil.rmtree(folder.path)
                deleted += 1
                logger.info(f"Deleted expired folder: {folder.name} (age: {age})")

    logger.info(f"Storage cleanup done — {deleted} folder(s) deleted")