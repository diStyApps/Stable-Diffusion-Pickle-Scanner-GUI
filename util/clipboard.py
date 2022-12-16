import PySimpleGUI as sg
right_click_menu = ['', ['Copy', 'Paste', 'Cut', 'Clear']]

def do_clipboard_operation(event, window, element,STATUS_INFO_TXT_KEY):
    if event == 'Select All':
        element.Widget.selection_clear()
        # element.Widget.tag_add('sel', '1.0', 'end')
    elif event == 'Copy':
        try:
            text = element.Widget.selection_get()
            window.TKroot.clipboard_clear()
            window.TKroot.clipboard_append(text)
        except:
            # print('Nothing selected')
            window[STATUS_INFO_TXT_KEY].update(value='Nothing selected') 

    elif event == 'Paste':
        element.Widget.insert(sg.tk.INSERT, window.TKroot.clipboard_get())
    elif event == 'Cut':
        try:
            text = element.Widget.selection_get()
            window.TKroot.clipboard_clear()
            window.TKroot.clipboard_append(text)
            element.update('')
        except:
            # print('Nothing selected')
            window[STATUS_INFO_TXT_KEY].update(value='Nothing selected') 
    elif event == 'Clear':
        try:
            text = element.Widget.selection_get()
            element.update('')
        except:
            # print('Nothing selected')
            window[STATUS_INFO_TXT_KEY].update(value='Nothing selected') 
