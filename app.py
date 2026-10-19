# 셀 2번
table_data = [
    ["구분", "매출", "증감"],   # 머리글 행
    ["국내", "120억", "+8%"],
    ["해외", "85억",  "-3%"],
    ["온라인", "47억", "+15%"],
]

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

pdfmetrics.registerFont(UnicodeCIDFont("HYSMyeongJo-Medium"))
styles = getSampleStyleSheet()
for name in ("Title", "Normal"):
    styles[name].fontName = "HYSMyeongJo-Medium"

pdf_table = Table(table_data)
pdf_table.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ("FONTNAME", (0, 0), (-1, -1), "HYSMyeongJo-Medium"),
]))

SimpleDocTemplate("sample_report.pdf", pagesize=A4).build([
    Paragraph("2026년 1분기 실적 보고", styles["Title"]),
    Spacer(1, 12),
    Paragraph("[표 1] 부문별 매출 현황", styles["Normal"]),
    Spacer(1, 6),
    pdf_table,
])
print("sample_report.pdf 생성 완료")

#셀 3번

import pypdf                                          # 단순 텍스트 추출 라이브러리 (표라는 개념 없이 글자만 읽어 냄)

reader = pypdf.PdfReader("sample_report.pdf")         # PDF 파일을 열어 읽기 객체(reader) 생성
                                                      #   reader.pages = 페이지 목록 (번호는 0부터 시작)
raw_text = reader.pages[0].extract_text()             # pages[0] = 첫 페이지 / extract_text() = 그 페이지 글자를 문자열 하나로 추출
                                                      #   → 셀 8 에서 '단순 추출본'으로 다시 쓰려고 변수에 저장

print("───── 단순 추출 결과 ─────")                   # 구분용 제목 출력
print(raw_text)     
