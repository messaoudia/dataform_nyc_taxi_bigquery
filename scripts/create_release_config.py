import json
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from google.auth import impersonated_credentials
from google.oauth2 import service_account
from google.cloud import dataform_v1

SA_KEY = json.loads(os.getenv("GCP_DATAFORM_SA_KEY"))
PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION")
REPOSITORY_ID = os.getenv("REPOSITORY_ID")
RELEASE_CONFIG_ID = os.getenv("RELEASE_CONFIG_ID")
TARGET_SA = SA_KEY["client_email"]

source_credentials = service_account.Credentials.from_service_account_info(
    SA_KEY,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

credentials = impersonated_credentials.Credentials(
    source_credentials=source_credentials,
    target_principal=TARGET_SA,
    target_scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

client = dataform_v1.DataformClient(credentials=credentials)

parent = f"projects/{PROJECT_ID}/locations/{LOCATION}/repositories/{REPOSITORY_ID}"
compilation_request = dataform_v1.CreateCompilationResultRequest(
    parent=parent,
    compilation_result=dataform_v1.CompilationResult(
        release_config=f"{parent}/releaseConfigs/{RELEASE_CONFIG_ID}"
    ),
)

compilation_result = client.create_compilation_result(request=compilation_request)
logger.info(f"Created compilation result: {compilation_result.name}")
