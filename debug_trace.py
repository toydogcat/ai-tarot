import sys
from kinliuren import Liuren
import inspect

class TraceLiuren(Liuren):
    def biyung(self):
        # We can trace by calling the original and checking the file
        pass

def trace_calls(frame, event, arg):
    if event == 'line':
        if 'kinliuren.py' in frame.f_code.co_filename and frame.f_code.co_name == 'biyung':
            line_no = frame.f_lineno
            print(f"Line {line_no}")
    return trace_calls

lr = Liuren("驚蟄", "五", "甲戌", "庚子")
sys.settrace(trace_calls)
lr.biyung()
sys.settrace(None)
