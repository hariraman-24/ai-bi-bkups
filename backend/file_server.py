import pandas as pd
import pdfplumber
from docx import Document
import os


class FileServer:

    def read_csv(self, file_path):
        df = pd.read_csv(file_path)
        return df.to_dict(orient="records")

    def read_excel(self, file_path):
        df = pd.read_excel(file_path, engine="openpyxl")
        return df.to_dict(orient="records")

    def read_pdf(self, file_path):
        text = ""

        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text()

        return {"pdf_content": text}

    def read_docx(self, file_path):
        doc = Document(file_path)
        text = []

        for para in doc.paragraphs:
            text.append(para.text)

        return {"docx_content": text}

    def process_file(self, file_path):

        if not os.path.exists(file_path):
            return {"error": "File not found"}

        extension = file_path.split(".")[-1].lower()

        if extension == "csv":
            return self.read_csv(file_path)

        elif extension in ["xls", "xlsx"]:
            return self.read_excel(file_path)

        elif extension == "pdf":
            return self.read_pdf(file_path)

        elif extension == "docx":
            return self.read_docx(file_path)

        else:
            return {"error": "Unsupported file type"}


if __name__ == "__main__":

    server = FileServer()

    result = server.process_file("files/samp.xlsx")

    print(result)