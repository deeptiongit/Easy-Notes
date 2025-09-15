import requests
import os
from typing import Dict
from ..utils.logger import ErpAdapterLogger
from ..utils.notifier import Notification


VENDOR_URL = os.getenv("API_URL")
VENDOR_TOKEN = os.getenv("API_TOKEN")


def push_to_erp(data: Dict, vendor: str) -> bool:

    logger = ErpAdapterLogger('ERP_VENDOR')
    notifier = Notification()

    try:
        if not all([VENDOR_URL, VENDOR_TOKEN]):
            logger.error("Missing required environment variables (API_URL/API_TOKEN)")
            return False

        if os.getenv("ERP_VENDOR") != vendor:
            logger.warning(f"Vendor mismatch: {vendor} != {os.getenv('ERP_VENDOR')}")
            return False

        # Initialize notification
        notifier.on_data_ready.subscribe(notifier.listener)

        # Make API request with timeout
        response = requests.post(
            VENDOR_URL,
            json=data,
            headers={
                "Authorization": f"Bearer {VENDOR_TOKEN}",
                "Content-Type": "application/json"
            },
            timeout=30
        )

        # Handle response
        if response.status_code in [200, 201]:
            logger.info(f"ERP sync success: {response.json()}")
            Notification.notification("ERP sync success", data)
            return True
        else:
            error_msg = f"ERP sync failed - Status: {response.status_code}, Response: {response.text}"
            logger.error(error_msg)
            Notification.notification("ERP sync failed", {
                "status_code": response.status_code,
                "error": response.text
            })
            return False

    except requests.exceptions.RequestException as req_err:
        logger.exception(f"Request error: {str(req_err)}")
        Notification.notification("ERP connection error", {
            "error_type": "request_exception",
            "details": str(req_err)
        })
        return False

    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        Notification.notification("ERP processing error", {
            "error_type": "unexpected_exception",
            "details": str(e)
        })
        return False