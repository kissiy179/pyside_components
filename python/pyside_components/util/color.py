import sys
import codecs

def char_to_num(c):
    '''
    文字からカラー用数値を取得
    '''
    if sys.version.startswith('3'):
        hex_code = codecs.encode(bytes(c, 'utf-8'), 'hex-codec')

    else:
        hex_code = codecs.encode(c.lower(), 'hex')
        
    col_num = int(hex_code, 16)    
    return col_num

def string_to_color(s, correction=40):
    '''
    文字列からカラー値を取得
    '''
    s = s if s else 'z'
    s = s.ljust(3, '0')
    color = [char_to_num(i) for i in s[:3]]
    avg = sum(color) / len(color)

    if avg < correction:
        sub = correction - avg
        color = [min(255, n + sub) for n in color]

    max_ = max(color)
    min_ = min(color)
    
    if max_ - min_ <= 255:
        maxidx = color.index(max_)
        minidx = color.index(min_)
        color[maxidx] = min(255, max_ + correction)
        color[minidx] = max(0, min_ - correction)
        
    return color

def color_to_hextriplet(color):
    '''
    カラー値から16進数文字列を取得
    '''
    return '#' + ''.join('{:02X}'.format(i) for i in color)
