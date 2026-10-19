# 셀1
# ── Pillow 설치 점검 ───────────────────────────────────────────────
# Colab에서 Pillow가 섞여 설치되면(ImageText.py는 12.x, _typing.py는 11.x)
#   ImportError: cannot import name '_Ink' from 'PIL._typing'
# 가 납니다. 아래에서 자동으로 감지해 깨끗이 재설치합니다.
import subprocess, sys

try:
    import PIL.ImageDraw          # ← 여기서 ImageText 를 끌어옵니다
    import PIL
    print(f"✅ Pillow {PIL.__version__} 정상")
except ImportError as e:
    print(f"⚠️ Pillow 설치가 깨져 있습니다: {e}")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q",
                    "--force-reinstall", "--no-cache-dir", "pillow"], check=True)
    print("🔧 Pillow 재설치 완료 → [런타임] → [세션 다시 시작] 후 이어서 실행하세요")
# ──────────────────────────────────────────────────────────────────

