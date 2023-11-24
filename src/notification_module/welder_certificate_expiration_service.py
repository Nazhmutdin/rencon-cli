from datetime import datetime, timedelta
import json
import os
import base64

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource

import mimetypes
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from src.db.repository import WelderCertificationRepository, WelderRepository
from src.domain import WelderCertificationRequest, WelderCertificationModel
from src.services.excel_service import ExcelService
from settings import SCOPES, STATIC_DIR


class WelderCertificationExpirationNotificationService:
    certification_repo = WelderCertificationRepository()
    welder_repo = WelderRepository()

    def _create_notification_attachment(self) -> None:
        wb = Workbook()
        ws: Worksheet = wb.active
        header_cells = [ExcelService.data_to_cells(
            (
                    "№",
                    "full name",
                    "kleymo",
                    "certification number",
                    "company",
                    "certification date",
                    "expiration date",
            ),
            ws
        )]

        styled_header_cells = ExcelService.style_like_header_rows(header_cells)

        ExcelService.cells_to_worksheet(styled_header_cells, ws)

        body_rows = []

        names = self._load_names()

        for e, certification in enumerate(self._get_certifications(), start=1):
            welder = self.welder_repo.get(certification.kleymo)

            if welder.full_name not in names:
                continue

            body_rows.append(
                    ExcelService.data_to_cells(
                    (
                        e,
                        welder.full_name,
                        certification.kleymo,
                        certification.certification_number,
                        certification.company,
                        certification.certification_date,
                        certification.expiration_date
                    ),
                    ws
                )
            )
        

        styled_body_rows = ExcelService.style_like_body_rows(body_rows)

        ExcelService.cells_to_worksheet(styled_body_rows, ws)

        ExcelService.fit_worksheet(ws)
        
    
        wb.save(f"{STATIC_DIR}/notification_attachment.xlsx")


    def _get_certifications(self) -> list[WelderCertificationModel]:
        res = self.certification_repo.get_many(
            WelderCertificationRequest(
                expiration_date_from=datetime.now().date(),
                expiration_date_before=datetime.now().date() + timedelta(days=60)
            )
        )

        return res.result


    def _load_names(self) -> list[str]:
        return json.load(
            open(f"{STATIC_DIR}/names.json", "r", encoding="utf-8")
        )
    

    def _get_creds(self) -> Credentials:
        creds = None

        if os.path.exists(f"{STATIC_DIR}/token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        if not creds or not creds.valid:

            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())

            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    f"{STATIC_DIR}/credentials.json", SCOPES
                )

                creds = flow.run_local_server(port=0)
            
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return creds
    

    def notificate(self) -> None:
        self._create_notification_attachment()

        creds = self._get_creds()

        service: Resource = build("gmail", "v1", credentials=creds)
        mime_message = MIMEMultipart()

        mime_message["To"] = "nazhmutdin.gumuev@rencons.com"
        mime_message["From"] = "gumuevnazhmutdin1248@gmail.com"
        mime_message["Subject"] = "sample with attachment"

        body = MIMEText("Dear collegues, this is a automated mail. Please don't reply!\nWelder's certifications in notification_attachment.xlsx will be expired soon!")

        attachment_filename = f"{STATIC_DIR}/notification_attachment.xlsx"

        type_subtype, _ = mimetypes.guess_type(attachment_filename)
        maintype, subtype = type_subtype.split("/")

        with open(attachment_filename, "rb") as fp:
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            attachment.add_header('content-disposition', 'attachment', filename='notification_attachment.xlsx')
            encoders.encode_base64(attachment)

        mime_message.attach(attachment)
        mime_message.attach(body)

        encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()

        create_message = {"raw": encoded_message}
        send_message = (
            service.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )
