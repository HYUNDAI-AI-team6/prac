import pypdf                                          # 단순 텍스트 추출 라이브러리 (표라는 개념 없이 글자만 읽어 냄)

reader = pypdf.PdfReader("sample_report.pdf")         # PDF 파일을 열어 읽기 객체(reader) 생성
                                                      #   reader.pages = 페이지 목록 (번호는 0부터 시작)
raw_text = reader.pages[0].extract_text()             # pages[0] = 첫 페이지 / extract_text() = 그 페이지 글자를 문자열 하나로 추출
                                                      #   → 셀 8 에서 '단순 추출본'으로 다시 쓰려고 변수에 저장

print("───── 단순 추출 결과 ─────")                   # 구분용 제목 출력
print(raw_text)     