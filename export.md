from pyhwpx import Hwp

# 1. 새로운 한글 인스턴스 생성 (기존 문서 절대 사용 안 함)
hwp = Hwp(new=True)

# 2. 새 문서 생성 (빈 문서 탭 추가)
hwp.XHwpDocuments.Add()

# 3. 10x10 표 생성
rows, cols = 10, 10
tbset = hwp.create_set("TableCreation")
tbset.SetItem("Rows", rows)
tbset.SetItem("Cols", cols)

# 행 높이 / 열 너비 기본값 설정
row_heights = tbset.CreateItemArray("RowHeight", rows)
col_widths = tbset.CreateItemArray("ColWidth", cols)

for r in range(rows):
    row_heights.SetItem(r, hwp.mili_to_hwp_unit(10))
for c in range(cols):
    col_widths.SetItem(c, hwp.mili_to_hwp_unit(20))

# 표 컨트롤 삽입
table = hwp.insert_ctrl("tbl", tbset)

# 4. 테두리 제거
prop = table.Properties  # 표의 Properties = "Table" 파라미터셋
# 모든 테두리 속성 0으로 설정
for border in ["BorderLeft", "BorderRight", "BorderTop", "BorderBottom",
               "BorderHorz", "BorderVert"]:
    prop.SetItem(border, 0)
table.Properties = prop

# 5. 표 안에 1~100 채워 넣기
num = 1
for r in range(rows):
    for c in range(cols):
        hwp.MoveToCell(r, c)   # r행 c열로 이동
        hwp.insert_text(str(num))
        num += 1

# 6. 저장하고 종료
hwp.save_as("table100.hwp")
hwp.quit()
