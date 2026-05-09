import logging
import os
from contextlib import contextmanager
from datetime import datetime, timezone

from app.config import LOCK_FILE

@contextmanager
def collector_lock():
    """
    Create an atomic lock file to prevent overlapping collector executions.
    
    If the lock file already exists, another collector execution is probably running, so the caller should skip the new execution.
    """
    
    lock_acquired = False
    
    try:
        lock_fd = os.open(LOCK_FILE, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        
        with os.fdopen(lock_fd, "w", encoding="utf-8") as lock_file:
            lock_file.write(f"pid={os.getpid()}\n")
            lock_file.write(f"created_at={datetime.now(timezone.utc).isoformat()}\n")
            
        lock_acquired = True
        logging.info(f"Collector lock acquired: {LOCK_FILE}")
        
        yield True
        
    except FileExistsError:
        logging.warning(
            f"Collector lock already exists, skipping execution: {LOCK_FILE}"
        )
        yield False
        
    finally:
        if lock_acquired:
            try:
                LOCK_FILE.unlink(missing_ok=True)
                logging.info(f"Collector lock released: {LOCK_FILE}")
            except Exception:
                logging.exception(f"Failed to release collector lock: {LOCK_FILE}")
    