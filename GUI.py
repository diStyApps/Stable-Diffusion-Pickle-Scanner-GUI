import PySimpleGUI as sg
import os,io
from PIL import Image,ImageTk
import webbrowser
from picklescan.src.picklescan.scanner import scan_directory_path
from picklescan.src.picklescan.scanner import scan_file_path
from picklescan.src.picklescan.scanner import scan_url
from picklescan.src.picklescan.scanner import scan_huggingface_model
from picklescan.src.picklescan.scanner import scanned_files
from picklescan.src.picklescan.scanner import infected_files

COLOR_DARK_GREEN = '#78BA04'
COLOR_DARK_BLUE = '#4974a5'
COLOR_RED_ORANGE = '#C13515'
COLOR_GRAY_9900 = '#0A0A0A'
COLOR_DARK_GRAY = '#1F1F1F'

SCANNED_FILES = 'SCANNED FILES: '
INFECTED_FILES = 'INFECTED FILES: '
DANGEROUS_GLOBALS = 'DANGEROUS GLOBALS: '
SCANNED_FILES_DEF = f'{SCANNED_FILES} 0'
INFECTED_FILES_DEF = f'{INFECTED_FILES} 0'
DANGEROUS_GLOBALS_DEF = f'{DANGEROUS_GLOBALS} 0'

right_click_menu = ['', ['Copy', 'Paste', 'Cut']]

def image_bio(filename,size):
    if os.path.exists(filename):
        image1 = Image.open(filename)
        if size[0]>0:
            image1.thumbnail(size)
        bio = io.BytesIO()
        image1.save(bio,format="PNG")
        del image1
        return bio.getvalue()

def do_clipboard_operation(event, window, element):
    if event == 'Select All':
        element.Widget.selection_clear()
        element.Widget.tag_add('sel', '1.0', 'end')
    elif event == 'Copy':
        try:
            text = element.Widget.selection_get()
            window.TKroot.clipboard_clear()
            window.TKroot.clipboard_append(text)
        except:
            # print('Nothing selected')
            window['-status_info-'].update(value='Nothing selected') 

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
            window['-status_info-'].update(value='Nothing selected') 

def main():
    ver = '0.1.0'
    sg.theme('Dark Gray 15')
    app_title = f"Disty's Stable Diffusion Pickle Scanner GUI - Ver {ver}"
    isError = 0
    file_ext = {
        ("Pytorch Files", "*.ckpt"),
        ("Pytorch Files", "*.pth"),
        ("Pytorch Files", "*.pt"),
        ("Pytorch Files", "*.bin"),
        ("Pickle Files", "*.pkl"),
        ("Pickle Files", "*.pickle"),
        ("Pickle Files", "*.joblib"),
        ("Pickle Files", "*.dat"),
        ("Pickle Files", "*.data"),
        ("Pickle Files", "*.npy"),
        ("Pickle Files", "*.npy"),
        ("Zip Files", "*.npz"),
        ("Zip Files", "*.zip"),
    }

    #region layout
    def browse_layout(type_,visible_,disabled=False):
        if type_ == 'huggingface':
            browse_type = sg.Button('Clear',k=f'-{type_}_clear_button-',disabled=disabled,size=(10,2))       
        if type_ == 'url':
            browse_type = sg.Button('Clear',k=f'-{type_}_clear_button-',disabled=disabled,size=(10,2))         
        if type_ == 'file':
            browse_type = sg.FileBrowse(k=f'-{type_}_FileBrowse-',file_types=(file_ext),disabled=disabled,size=(10,2)) 
        if type_ == 'directory':
            browse_type = sg.FolderBrowse(k=f'-{type_}_FolderBrowse-',disabled=disabled,size=(10,2))

        layout = sg.Frame('',[
                                [
                                    sg.Input(key=f'-input_files_{type_}-',enable_events=True,expand_x=True,expand_y=True,font='Ariel 11',background_color=COLOR_DARK_GRAY,right_click_menu=right_click_menu),
                                    browse_type
                                ],
                            ],expand_x=True,k=f'-frame_{type_}-',visible=visible_,relief=sg.RELIEF_SOLID,border_width=1,background_color=COLOR_GRAY_9900)
        return layout

    top_column = [
        [
            sg.Frame('',[
                [
                    sg.Radio('Hugging Face','-type_selector_input_radio-',default=True,k='-huggingface_radio-',enable_events=True),
                    sg.Radio('URL','-type_selector_input_radio-',default=False,k='-url_radio-',enable_events=True),
                    sg.Radio('File','-type_selector_input_radio-',default=False,k='-file_radio-',enable_events=True),
                    sg.Radio('Directory','-type_selector_input_radio-',default=False,k='-directory_radio-',enable_events=True),
                        sg.Frame('',[
                            [
                                sg.Button(image_data=image_bio('./media/buymeacoffee.png',(133,500)),expand_x=False,visible=True,enable_events=True,key="-buymeacoffee-",button_color=(COLOR_GRAY_9900,COLOR_GRAY_9900)),
                                sg.Button(image_data=image_bio('./media/kofi.png',(60,500)),expand_x=False,visible=True,enable_events=True,key="-kofi-",button_color=(COLOR_GRAY_9900,COLOR_GRAY_9900)),
                                sg.Button(image_data=image_bio('./media/coindrop.png',(95,500)),expand_x=False,visible=True,enable_events=True,key="-coindrop-",button_color=(COLOR_GRAY_9900,COLOR_GRAY_9900)),

                                sg.Button(image_data=image_bio('./media/github.png',(80,500)),expand_x=False,visible=True,enable_events=True,key="-github-",button_color=(COLOR_GRAY_9900,COLOR_GRAY_9900)),
                            ],
                        ],expand_x=True,expand_y=False,relief=sg.RELIEF_SOLID,border_width=1,visible=True,background_color=COLOR_GRAY_9900,element_justification="r")

                ],
                
                
            ],expand_x=True,expand_y=False,relief=sg.RELIEF_SOLID,border_width=1,visible=True,background_color=COLOR_GRAY_9900)
        ],    
        [
            browse_layout('huggingface',True),
            browse_layout('url',False),        
            browse_layout('file',False),    
            browse_layout('directory',False),    
        ],
    ]

    bottom_column = [
        [
            sg.Frame('',[
                    [
                        sg.Frame(' Status',[
                            [
                                sg.Text('',key='-status_info-', expand_x=True)
                            ],
                        ],expand_x=True,expand_y=False,relief=sg.RELIEF_SOLID,border_width=0,visible=True,element_justification='c',background_color=COLOR_GRAY_9900,title_color=COLOR_DARK_BLUE)                          
                    ],  
                [              
                    sg.Button('Scan',k='-scan_button-',disabled=False,expand_x=True),
                ],
            ],expand_x=True,border_width=0,relief=sg.RELIEF_FLAT,element_justification='c')
        ],    
    ]

    console_column = [
        [
            sg.Frame('',[
                [
                    sg.Text(SCANNED_FILES_DEF,k='-scanned_files_text-',expand_x=True,expand_y=True,font='Ariel 12',justification='left',size=(20,1)),
                    sg.Text(INFECTED_FILES_DEF,k='-infected_files_text-',expand_x=True,expand_y=True,font='Ariel 12',justification='c',size=(20,1)),
                    sg.Text(DANGEROUS_GLOBALS_DEF,k='-dangerous_globals_text-',expand_x=True,expand_y=True,font='Ariel 12',justification='right',size=(20,1)),
                ],         
                    [
                        sg.Frame('',[
                            [
                                sg.Text('',key='-status_state_text-', expand_x=True,expand_y=True,justification='c',font='Ariel 12 bold',background_color=COLOR_GRAY_9900)
                            ],
                        ],expand_x=True,expand_y=False,relief=sg.RELIEF_FLAT,border_width=0,visible=True,element_justification='c',background_color=COLOR_GRAY_9900,size=(50,30))                          
                    ],                           
                [
                    sg.MLine(k='-console_ml-',reroute_stdout=True,write_only=False,reroute_cprint=True, autoscroll=True, text_color='white', auto_refresh=True,size=(120,35),expand_x=True,expand_y=True)
                ],
            ],expand_x=True,expand_y=True,border_width=0,relief=sg.RELIEF_FLAT,k='-scanned_frame-')
        ],  
    ]

    layout = [

        top_column ,       
        [ 
            [
                sg.Column(console_column, key='-console_column-', element_justification='r', expand_x=True,expand_y=True,visible=True),
            ],        
        ],
        bottom_column,
    ]

    #endregion layout

    window = sg.Window(app_title,layout,finalize=True, resizable=True,enable_close_attempted_event=False,background_color=COLOR_GRAY_9900)
    window.hide    
    
    #region widget and flating

    scan_button_widget = window["-scan_button-"]
    huggingface_clear_button_widget = window["-huggingface_clear_button-"]
    url_clear_button_widget = window["-url_clear_button-"]
    file_FileBrowse_widget = window["-file_FileBrowse-"]
    directory_FolderBrowse_widget = window["-directory_FolderBrowse-"]
    input_files_huggingface_widget = window["-input_files_huggingface-"]
    input_files_url_widget = window["-input_files_url-"]
    input_files_file_widget = window["-input_files_file-"]
    input_files_directory_widget = window["-input_files_directory-"]
    status_state_text_widget = window["-status_state_text-"]
    scanned_files_text_widget = window["-scanned_files_text-"]
    infected_files_text_widget = window["-infected_files_text-"]
    dangerous_globals_text_widget = window["-dangerous_globals_text-"]
    console_ml_widget = window["-console_ml-"]
    status_info_widget = window["-status_info-"]
    buymeacoffee_widget = window["-buymeacoffee-"]
    kofi_widget = window["-kofi-"]
    coindrop_widget = window["-coindrop-"]

    github_widget = window["-github-"]


    widgets = {
        scan_button_widget,
        huggingface_clear_button_widget,
        url_clear_button_widget,
        file_FileBrowse_widget,
        directory_FolderBrowse_widget,
        input_files_huggingface_widget,
        input_files_url_widget,
        input_files_file_widget,
        input_files_directory_widget,
        buymeacoffee_widget,
        github_widget,
        kofi_widget,
        coindrop_widget
    }
    for widget in widgets:
        widget.Widget.config(relief='flat')  

    #endregion 
        
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        
        if event == '-scan_button-':
                status_info_widget.update(value='Scanning. Please wait...') 
                scanned_files_text_widget.update(value=SCANNED_FILES_DEF) 
                infected_files_text_widget.update(value=INFECTED_FILES_DEF) 
                dangerous_globals_text_widget.update(value=DANGEROUS_GLOBALS_DEF) 
                status_state_text_widget.Widget.config(background=COLOR_GRAY_9900)  
                status_state_text_widget.ParentRowFrame.config(background=COLOR_GRAY_9900)
                status_state_text_widget.update(value='')
                console_ml_widget.update(value='')
                isError = 0
                scanned_files.clear()
                infected_files.clear()

                if values['-huggingface_radio-']:
                    input_files = values['-input_files_huggingface-']
                    if len(input_files)>1:
                        try:
                            scan_result = scan_huggingface_model(input_files)
                            
                        except RuntimeError as e:
                            print(RuntimeError,e)
                            isError = 1
                            status_info_widget.update(value='Fail to scan') 

                        except ConnectionRefusedError as e:
                            print(ConnectionRefusedError,e)   
                            isError = 1
                            status_info_widget.update(value='Fail to scan') 

                        except AttributeError as e:
                            print(AttributeError,e)   
                            status_info_widget.update(value='Fail to scan') 
                            isError = 1 
                    else:
                            isError = 1
                            status_info_widget.update(value='Nothing to scan') 

                if values['-url_radio-']:
                    input_files = values['-input_files_url-']
                    if len(input_files)>1:
                        try:
                            scan_result = scan_url(input_files)
                        except RuntimeError as e:
                            print(RuntimeError,e)
                            isError = 1
                            status_info_widget.update(value='Fail to scan') 

                        except ConnectionRefusedError as e:
                            print(ConnectionRefusedError,e)   
                            isError = 1
                            status_info_widget.update(value='Fail to scan') 

                        except AttributeError as e:
                            print(AttributeError,e)   
                            isError = 1  
                            status_info_widget.update(value='Fail to scan') 
                    else:
                            isError = 1        
                            status_info_widget.update(value='Nothing to scan') 

                if values['-directory_radio-']:
                    input_files = values['-input_files_directory-']
                    if len(input_files)>1:
                        try:
                            scan_result = scan_directory_path(input_files)
                        except FileNotFoundError as e:
                            print(FileNotFoundError,e)   
                            isError = 1
                            status_info_widget.update(value='Fail to scan') 

                    else:
                            isError = 1
                            status_info_widget.update(value='Nothing to scan') 

                if values['-file_radio-']:
                    input_files = values['-input_files_file-']
                    if len(input_files)>1:
                        try:
                            scan_result = scan_file_path(input_files)
                        except FileNotFoundError as e:
                            print(FileNotFoundError,e)   
                            isError = 1
                            status_info_widget.update(value='Fail to scan') 
                    else:
                            isError = 1        
                            status_info_widget.update(value='Nothing to scan') 

                if not isError:
                    scanned_files_text_widget.update(value=f'{SCANNED_FILES} {scan_result.scanned_files}') 
                    infected_files_text_widget.update(value=f'{INFECTED_FILES} {scan_result.infected_files}') 
                    dangerous_globals_text_widget.update(value=f'{DANGEROUS_GLOBALS} {scan_result.issues_count}') 
                    scanned_files_len = len(scanned_files)
                    infected_files_len = len(infected_files)

                    print('')
                    if scanned_files_len > 0:
                        print('----------- SCANNED FILES -----------')
                        for file in scanned_files:
                            print(f"    {file}")

                        if infected_files_len == 0:
                            status_state_text_widget.update(text_color='white')
                            status_state_text_widget.Widget.config(background=COLOR_DARK_GREEN)  
                            status_state_text_widget.ParentRowFrame.config(background=COLOR_DARK_GREEN)
                            status_state_text_widget.update(value='PASS') 

                    if infected_files_len > 0:
                        print('')
                        print('----------- INFECTED FILES -----------')
                        for file in infected_files:
                            print(f"    {file}")

                        status_state_text_widget.update(text_color='white')
                        status_state_text_widget.Widget.config(background=COLOR_RED_ORANGE)  
                        status_state_text_widget.ParentRowFrame.config(background=COLOR_RED_ORANGE)
                        status_state_text_widget.update(value='INFECTED') 

                    status_info_widget.update(value='Done') 

        if event == '-huggingface_radio-':
                window['-frame_file-'].update(visible=False)  
                window['-frame_directory-'].update(visible=False)  
                window['-frame_url-'].update(visible=False)  
                window['-frame_huggingface-'].update(visible=True)          

        if event == '-url_radio-':
                window['-frame_file-'].update(visible=False)  
                window['-frame_directory-'].update(visible=False)  
                window['-frame_url-'].update(visible=True)  
                window['-frame_huggingface-'].update(visible=False)        

        if event == '-file_radio-':
                window['-frame_file-'].update(visible=True)  
                window['-frame_directory-'].update(visible=False)  
                window['-frame_url-'].update(visible=False)  
                window['-frame_huggingface-'].update(visible=False)        

        if event == '-directory_radio-':
                window['-frame_file-'].update(visible=False)  
                window['-frame_directory-'].update(visible=True)  
                window['-frame_url-'].update(visible=False)  
                window['-frame_huggingface-'].update(visible=False)        

        if event == '-huggingface_clear_button-':
            input_files_huggingface_widget.update(value='')

        if event == '-url_clear_button-':
            input_files_url_widget.update(value='')

        if event == "-buymeacoffee-":
            webbrowser.open("https://www.buymeacoffee.com/disty")      
        if event == "-github-":
            webbrowser.open("https://github.com/diStyApps/Stable-Diffusion-Pickle-Scanner-GUI")  
        if event == "-kofi-":
            webbrowser.open("https://ko-fi.com/disty")  
        if event == "-coindrop-":
            webbrowser.open("https://coindrop.to/disty")  
                
        if event in right_click_menu[1]:
            if values['-huggingface_radio-']:
                do_clipboard_operation(event, window, input_files_huggingface_widget)
            if values['-url_radio-']:
                do_clipboard_operation(event, window, input_files_url_widget)                
            if values['-file_radio-']:
                do_clipboard_operation(event, window, input_files_file_widget)       
            if values['-directory_radio-']:
                do_clipboard_operation(event, window, input_files_directory_widget)   

            window['-console_ml-'].update(value='')
            
        # if event == 'Clear':
        #     if values['-huggingface_radio-']:
        #         input_files_huggingface_widget.update(value='')    
        #     if values['-url_radio-']:
        #         input_files_url_widget.update(value='')
        #     if values['-file_radio-']:
        #         input_files_file_widget.update(value='')
        #     if values['-directory_radio-']:
        #         input_files_directory_widget.update(value='')
        
if __name__ == '__main__':
    main() 
