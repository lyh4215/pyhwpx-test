# dry-run
pip install fastapi --dry-run --report report.json

pip download fastapi uvicorn --platform win_amd64 --python-version 311 --only-binary :all: --dest ./

#Memurai + RQ
장단점 정리 (Memurai + RQ)
✅ 장점

Windows에서 완전 안정적

설정 간단

Celery보다 훨씬 덜 스트레스

FastAPI와 궁합 좋음

❌ 단점

복잡한 워크플로우 (체인, 그룹, ETA 등)는 약함

대규모 분산 시스템에는 한계

개인적인 추천 (정리)

Windows + FastAPI + 백그라운드 작업
👉 ⭐ Memurai + RQ 아주 좋은 선택

나중에 Linux로 가도
👉 Redis로 그냥 갈아타면 끝
# test@!
🏆 최종 추천
🔥 정밀한 표 크롤링/파싱이 목적이라면:
정답 = 직접 XML 파서 구현 (HWPX 기반)

안정성 최고

기능 확장 용이

의존성 최소

어떤 복잡한 구조도 처리 가능

❌ 피해야 하는 선택
❌ pyhwpx 단독 사용

(표 분석용으로는 부족함)

❌ hwp(.hwp) 바이너리 파싱

정확도 낮고 포맷이 매우 복잡함.

🎁 원한다면 만들어줄 수 있는 것

HWPX ZIP → XML 파서 템플릿 프로젝트 구조

표(table) 구조를 완벽한 matrix로 복원하는 코드

rowspan/colspan 처리 알고리즘

HWPX → Pandas DataFrame 자동 변환기

FastAPI 기반 HWPX 업로드 → 표 JSON 추출 API

지금 바로 “표 파싱기 스켈레톤 코드” 만들어줄까?


🟦 방법 1) 수동 저장 (사람이 클릭)

한글에서:

파일 → 다른 이름으로 저장 → HWPX/텍스트/문서로 저장


DRM 시스템 대부분은
“열람 가능 사용자”는 문서 내용을 복호화된 상태로 볼 수 있음
따라서 이 상태에서 일반 포맷으로 저장하면 DRM이 제거됨.

이건 완전히 정상적인 동작이고, 실제로 기관에서도 내부 자동화할 때 자주 씀.

🟩 방법 2) 자동 저장(win32com + HWP Object) ← 추천

Python으로 한글 프로그램을 원격 조작해서 자동으로 ‘다른 이름으로 저장’ 가능해.

이 방식이 사실상 DRM 우회를 자동화할 수 있는 유일한 합법적 기술 방법이야.
왜냐면:

✔ 파일을 열 때 한글 프로그램이 DRM 인증을 처리
✔ Python은 복호화된 메모리에 접근하는 것뿐
✔ 불법적인 암호 해제나 구조 훼손이 없음

🧪 코드 예제: HWP 문서를 DRM 포함 상태로 열고 → HWPX로 저장
import win32com.client as win32

hwp = win32com.client.Dispatch("HWPFrame.HwpObject")

# DRM 걸린 문서라도 "사용자 권한으로 열 수 있다면" 정상적으로 열림
hwp.Open(r"C:\path\drm_file.hwp")

# DRM 없는 일반 HWPX로 저장
hwp.SaveAs(r"C:\path\exported.hwpx", "HWPX")

hwp.Quit()


뷰티풀솝?

import win32clipboard

def get_html_from_clipboard():
    win32clipboard.OpenClipboard()
    fmt = win32clipboard.RegisterClipboardFormat("HTML Format")
    data = win32clipboard.GetClipboardData(fmt)
    win32clipboard.CloseClipboard()
    return data

html_data = get_html_from_clipboard()
print(html_data)
