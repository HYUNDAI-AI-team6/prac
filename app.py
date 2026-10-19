# 셀1
# ── Pillow 설치 점검 ───────────────────────────────────────────────
# Colab에서 Pillow가 섞여 설치되면(ImageText.py는 12.x, _typing.py는 11.x)
#   ImportError: cannot import name '_Ink' from 'PIL._typing'
# 가 납니다. 아래에서 자동으로 감지해 깨끗이 재설치합니다.
import subprocess, sys
import pypdf

try:
    import PIL.ImageDraw          # ← 여기서 ImageText 를 끌어옵니다
    import PIL
    print(f"✅ Pillow {PIL.__version__} 정상")
except ImportError as e:
    print(f"⚠️ Pillow 설치가 깨져 있습니다: {e}")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q",
                    "--force-reinstall", "--no-cache-dir", "pillow"], check=True)
    print("🔧 Pillow 재설치 완료 → [런타임] → [세션 다시 시작] 후 이어서 실행하세요")
    

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
# 셀 3
import pypdf

reader = pypdf.PdfReader("sample_report.pdf")         # PDF 파일을 열어 읽기 객체(reader) 생성
                                                      #   reader.pages = 페이지 목록 (번호는 0부터 시작)
raw_text = reader.pages[0].extract_text()             # pages[0] = 첫 페이지 / extract_text() = 그 페이지 글자를 문자열 하나로 추출
                                                      #   → 셀 8 에서 '단순 추출본'으로 다시 쓰려고 변수에 저장
print("───── 단순 추출 결과 ─────")                   # 구분용 제목 출력
print(raw_text)    


        
# 셀4번
import pdfplumber

with pdfplumber.open("sample_report.pdf") as pdf:
    extracted_table = pdf.pages[0].extract_tables()[0]   # 2차원 리스트

for row in extracted_table:
    print(row)

# 셀 5

def table_to_markdown(rows):
    header = "| " + " | ".join(rows[0]) + " |"
    divider = "| " + " | ".join(["---"] * len(rows[0])) + " |"
    body = ["| " + " | ".join(r) + " |" for r in rows[1:]]
    return "\n".join([header, divider] + body)

caption = "[표 1] 2026년 1분기 부문별 매출 현황"
table_chunk = caption + "\n" + table_to_markdown(extracted_table)
print(table_chunk)

#셀 6번
big_table = [
    ["구분","매출","증감"],
    ["국내", "120억", "+8%"], ["해외", "85억", "-3%"],   # 데이터 행들
    ["온라인", "47억", "+15%"], ["오프라인", "73억", "-1%"],
    ["B2B", "210억", "+22%"], ["B2C", "88억", "+5%"],
]

header, row = big_table[0], ig_table[1:]         

chunk_size = 2                                      
chunks = []                                        

for i in range(0, len(rows), chunk_size):            
    block = rows[i:i + chunk_size]                  
    chunk = [header] + block                    
                                                     
    chunks.append(table_to_markdown(chunk))         

for n, chunk in enumerate(chunks, 1):               
    print(f"───── 조각 {n} ─────")                    
    print(chunk, "\n")                        
# 셀 7
import uuid

table_original = table_chunk                                       # 답변용
table_summary = "2026년 1분기 부문별 매출과 증감률 표. 국내 해외 온라인 매출 실적"  # 검색용

doc_id = str(uuid.uuid4())
docstore     = {doc_id: table_original}   # 답변용 저장소
search_index = {doc_id: table_summary}    # 검색용 저장소

def search(query):
    for _id, summary in search_index.items():
        if any(word in summary for word in query.split()):
            return _id
    return None

found_id = search("해외 매출 증감 알려줘")
print("🔎 검색은 '요약'으로 → id:", found_id[:8])
print("📦 LLM엔 '원본' 전달:\n", docstore[found_id])
