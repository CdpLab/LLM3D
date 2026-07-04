import sys
import os
sys.path.append(r"C:\Users\d's\Desktop\新建文件夹 (3)\SceneVerse-main")
try:
    from modules.grounding.unified_encoder import UnifiedSpatialCrossEncoderV1
    print("Import successful")
except Exception as e:
    print(f"Failed: {e}")