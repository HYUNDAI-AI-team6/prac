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


# 셀 9번
def validate_table(rows):                              # [함수 정의] 표(2차원 리스트)를 받아 빈 칸이 있는지 검사
    bad = [                                            # 문제가 있는 칸의 위치를 모을 리스트 (리스트 컴프리헨션)
        (r, c)                                         #   문제 칸의 (행 번호, 열 번호) 를 저장
        for r, row in enumerate(rows)                  #   바깥 반복: 행을 꺼내며 행 번호 r 을 같이 받음 (0부터)
        for c, cell in enumerate(row)                  #   안쪽 반복: 그 행의 칸을 꺼내며 열 번호 c 를 같이 받음 (0부터)
        if cell in (None, "")                          #   칸 값이 None 이거나 빈 문자열이면 → 병합 셀이 깨졌을 가능성
    ]
    return (                                           # 결과 문구 반환
        "⚠️ 빈/병합 의심 셀: " + str(bad)               #   bad 에 하나라도 있으면(비어 있지 않은 리스트는 True) 위치 목록과 함께 경고
        if bad                                         #   (문제 칸이 있는 경우)
        else "✅ 이상 없음"                              #   없으면 정상 문구
    )

print(validate_table(extracted_table))                 # 정상 표: 셀 4 에서 뽑은 실제 표를 검사 → 빈 칸 없음
print(validate_table([["연도", None, None],             # 병합 흉내 표: 머리글 행의 2·3번째 칸이 None (병합 셀이 추출되면 이렇게 비는 경우가 많음)
                       ["2026", "120억", "+8%"]]))      #   → 결과: [(0, 1), (0, 2)] = 0행 1열, 0행 2열이 비어 있다고 알려 줌

#셀 10
# 4단계까지 만든 sample_report.pdf 를 '이미지'로 캡처
import os

PDF = "/content/sample_report.pdf" if os.path.exists("/content/sample_report.pdf") \
      else "sample_report.pdf"
DPI = 300   # 300dpi = 표의 작은 숫자도 또렷하게 (소득세법서 검증된 값)

try:
    # 1순위: pdfplumber — 내부에서 PIL.ImageDraw 를 거칩니다
    import pdfplumber
    with pdfplumber.open(PDF) as pdf:
        pdf.pages[0].to_image(resolution=DPI).save("page_image.png")
    print("캡처 방식: pdfplumber")

except ImportError as e:
    # Pillow가 섞여 설치된 환경이면 위에서 '_Ink' ImportError 가 납니다.
    # pypdfium2(=pdfplumber의 필수 의존성)로 직접 렌더하면 ImageDraw를
    # 거치지 않으므로, 재설치·세션 재시작 없이 그대로 진행할 수 있습니다.
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(PDF)
    doc[0].render(scale=DPI / 72).to_pil().save("page_image.png")
    print(f"캡처 방식: pypdfium2 (pdfplumber 우회 — {e})")

from PIL import Image
img = Image.open("page_image.png")
print(f"✅ PDF 1페이지를 이미지로 캡처: {img.size} px")
img
