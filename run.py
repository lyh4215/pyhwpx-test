import zipfile
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

def print_first_section_xml_pretty(hwpx_path):
    with zipfile.ZipFile(hwpx_path, 'r') as z:
        all_files = z.namelist()
        print("📂 내부 목록:", all_files)

        section_files = [f for f in all_files if f.startswith("Contents/section")]
        section_files.sort()

        if not section_files:
            print("❌ section XML 없음")
            return

        first_section = section_files[0]
        xml_bytes = z.read(first_section)

        print(f"\n📄 첫 번째 섹션: {first_section}")

        # pretty print
        dom = minidom.parseString(xml_bytes)
        pretty_xml = dom.toprettyxml(indent="  ", newl="\n")

        print("\n===== 예쁘게 출력된 XML =====")
        print(pretty_xml)

# 실행
print_first_section_xml_pretty("test.hwpx")
