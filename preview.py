import base64

import streamlit.components.v1 as components


def pokaz_pdf(pdf_bytes, height=820):
    b64 = base64.b64encode(pdf_bytes).decode()
    components.html(
        f'<iframe src="data:application/pdf;base64,{b64}" '
        f'width="100%" height="{height}" style="border:none;"></iframe>',
        height=height + 12,
    )
