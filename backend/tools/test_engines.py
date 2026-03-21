import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.zhuge.engine import ZhugeEngine
    print("ZhugeEngine imported successfully")
except Exception as e:
    print(f"Error importing ZhugeEngine: {e}")

try:
    from core.daliuren.engine import DaliurenEngine
    print("DaliurenEngine imported successfully")
    engine = DaliurenEngine()
    print("DaliurenEngine instantiated successfully")
    print("Sample Output:", engine.draw_lesson())
except Exception as e:
    print(f"Error importing DaliurenEngine: {e}")
