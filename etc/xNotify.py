#encoding:utf-8


'''
需要MacOS支持，Python 2.x 支持与 wxPython支持。

install wxPython:

(sudo) pip install -U wxPython
'''

import wx
import httplib2,math
import  sys
reload(sys)
sys.setdefaultencoding('utf-8')

TRAY_TOOLTIP = 'XNotify'

#### ---------      以下是配置    --------
#stock code list
clist = ['rt_hk01918','rt_hk00175','rt_hk03333','rt_hk00700','rt_hk00656']
#stock display name list
dlist = ['R','J','H','T','F']
#涨幅放大倍数，百分点*dratio向下取整，对应涨0-9（红色），跌[-1,-10]绿色
dratio = 5
#刷新间隔时间(毫秒)
gSleepTime = 2000

#### ---------      配置完毕     ---------
data = dict()

def spider(code):
    addr = 'http://hq.sinajs.cn/list=%s'%code
    h = httplib2.Http(".cache")
    resp, content = h.request(addr, "GET")
    content = content.decode('gbk')
    idx = content.find('"')
    msg = content[idx+1:-3].split(',')
    name = msg[1][:4]
    rate = msg[8]

    if not data.has_key(name): data[name] = '0.0%'
    data[name] = '%s%%'%rate

    return name,rate

def generate_icon(stock_idx):
    code = clist[stock_idx]
    display_name = dlist[stock_idx]
    try:
        name,rate = spider(code)
    except:
        return None

    #修改比例，这里放大5倍
    rate = int(float(rate)*dratio)
    idx = rate
    if idx >=9 : idx = 9
    if idx <=-10 : idx = -10

    if idx >= 0 :
        idx = 9-idx
    if idx < 0:
        idx = idx+20


    print name,display_name, rate, 'idx : ', idx


    bmp = wx.EmptyBitmap(256, 256)
    dc = wx.MemoryDC()
    dc.SelectObject(bmp)

    dc.BeginDrawing()
    # 颜色
    base = [0 + (i + 1) * 20 for i in range(10)]
    cr = [(255, e, e) for e in base]
    cg = [(e, 255, e) for e in base]
    c = cr + cg

    #字体
    font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
    font.SetWeight(wx.BOLD)
    fn = 96
    font.SetPointSize(fn)
    dc.SetFont(font)
    dc.SetTextForeground(c[idx])
    dc.DrawText(display_name, (256 - fn) / 2 + 18, (256 - fn) / 2 - 12)


    #绘制周边20个圆
    th = [math.radians(i*18.0) for i in range(20)]
    px = [math.sqrt(1/(1+math.tan(thi)*math.tan(thi))) for thi in th]
    py = [math.sqrt(1-x*x) for x in px]

    for i in range(len(px)):
        p = int(i / 5)
        if p == 0:
            px[i] *= 1
            py[i] *= 1
        if p == 1:
            px[i] *= -1
            py[i] *= 1
        if p == 2:
            px[i] *= -1
            py[i] *= -1
        if p == 3:
            px[i] *= 1
            py[i] *= -1

    px = [int(x * 128*0.85) + 128 for x in px]
    py = [int(y * 128*0.85*-1) + 128 for y in py]



    for i in range(len(px)):
        color = wx.Colour(*c[i])
        dc.SetPen(wx.Pen(wx.Colour(0,0,255), style=wx.TRANSPARENT))
        dc.SetBrush(wx.Brush(color, wx.SOLID))

        if i!=idx:
            dc.DrawCircle(px[i],py[i], 14)

    color = wx.Colour(*c[idx])
    dc.SetPen(wx.Pen(color, style=wx.TRANSPARENT))
    dc.SetBrush(wx.Brush(color, wx.SOLID))
    dc.DrawCircle(px[idx], py[idx], 20)

    dc.EndDrawing()
    dc.SelectObject(wx.NullBitmap)
    icon = wx.EmptyIcon()
    icon.CopyFromBitmap(bmp)
    return icon

def create_menu_item(menu):
    global data
    for (k,v) in data.items():
        item = wx.MenuItem(menu, -1, '%s : %s'%(k,v))
        menu.Bind(wx.EVT_MENU, None, id=item.GetId())
        menu.AppendItem(item)
    return item

class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self):
        wx.TaskBarIcon.__init__(self,iconType = wx.TBI_DOCK)
        self.set_icon()
        self.n = 0
        global  clist
        self.RANGE = len(clist)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu)
        return menu

    def set_icon(self):
        self.SetIcon(generate_icon(0), TRAY_TOOLTIP)
    def update_icon(self,counter):
        self.n += 1

        idx = self.n % self.RANGE
        self.SetIcon(generate_icon(idx))


class XFrame(wx.Frame):
    def __init__(self,parent=None):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"测试定时器的小程序", pos=wx.DefaultPosition, size=wx.Size(483, 155),
                      style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        # 创建定时器

        self.timer = wx.Timer(self)  # 创建定时器
        self.counter = 0
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)  # 绑定一个定时器事件
        #三秒钟刷新一次
        self.timer.Start(gSleepTime)

    def OnTimer(self, evt):  # 显示时间事件处理函数
        self.counter += 1
        if self.bar :self.bar.update_icon(self.counter)


class App(wx.App):
    def OnInit(self):
        mainWindow =  XFrame()
        mainWindow.Show()
        mainWindow.bar  = TaskBarIcon()
        return True

def main():
    app = wx.PySimpleApp()
    frame = XFrame(None)
    frame.Hide()
    frame.bar = TaskBarIcon()
    app.MainLoop()

if __name__ == '__main__':
    main()
