
import PySimpleGUI as sg
from picklescan.src.picklescan.scanner import scan_directory_path, scan_file_path,scan_huggingface_model, scan_url, scanned_files, infected_files
from util.ui_flattener import flatten_ui_elements
from util.clipboard import do_clipboard_operation, right_click_menu
from util.file_extension import file_ext
import util.support as support
import util.colors as color
from CONSTANTS import *

sg.theme('Dark Gray 15')
__version__ = '0.1.5'
APP_TITLE = f"Disty's Stable Diffusion Pickle Scanner GUI - Ver {__version__}"
isError:int = 0

def main():
    #region layout

    def browse_layout(key_,visible_,disabled=False):
        if key_ == 'huggingface':
            browse_type = sg.Button('Clear',k=f'-{key_}_clear_btn-',disabled=disabled,size=(10,2))       
        if key_ == 'url':
            browse_type = sg.Button('Clear',k=f'-{key_}_clear_btn-',disabled=disabled,size=(10,2))         
        if key_ == 'file':
            browse_type = sg.FileBrowse(k=f'-{key_}_FileBrowse-',file_types=(file_ext),disabled=disabled,size=(10,2)) 
        if key_ == 'directory':
            browse_type = sg.FolderBrowse(k=f'-{key_}_FolderBrowse-',disabled=disabled,size=(10,2))

        layout = sg.Frame('',[
                                [
                                    sg.Input(key=f'-{key_}_inp_files-',enable_events=True,expand_x=True,expand_y=True,font=FONT,
                                    background_color=color.DARK_GRAY,right_click_menu=right_click_menu),
                                    browse_type,
                                ],
                            ],expand_x=True,k=f'-{key_}_frame-',visible=visible_,relief=sg.RELIEF_SOLID,border_width=1,background_color=color.GRAY_9900)
        return layout
        
    top_column = [
        [
            sg.Frame('',[
                [
                    support.buttons_layout(),
                ],
                [
                    sg.Radio(HUGGINGFACE_LBL,TYPE_SELECTOR_INP_RAD_KEY,default=True,k=HUGGINGFACE_RAD_KEY,enable_events=True),
                    sg.Radio(URL_LBL,TYPE_SELECTOR_INP_RAD_KEY,default=False,k=URL_RAD_KEY,enable_events=True),
                    sg.Radio(FILE_LBL,TYPE_SELECTOR_INP_RAD_KEY,default=False,k=FILE_RAD_KEY,enable_events=True),
                    sg.Radio(DIRECTORY_LBL,TYPE_SELECTOR_INP_RAD_KEY,default=False,k=DIRECTORY_RAD_KEY,enable_events=True),
                ],
            ],expand_x=True,expand_y=False,relief=sg.RELIEF_SOLID,border_width=1,visible=True,background_color=color.GRAY_9900)
        ],    
        [
            browse_layout('huggingface',True),
            browse_layout('url',False),        
            browse_layout('file',False),    
            browse_layout('directory',False),    
        ],
    ]

    mid_column = [
        [
            sg.Frame('',[
                    [              
                        sg.Button(SCAN_BTN_LBL,k=SCAN_BTN_KEY,font=FONT,expand_x=True,size=(30,2),mouseover_colors=(color.GRAY_9900,color.DARK_GREEN)),
                    ], 
                    [
                        sg.Text(SCANNED_FILES_DEF,k=SCANNED_FILES_TXT_KEY,expand_x=True,expand_y=True,font=FONT,justification='left',size=(20,1)),
                        sg.Text(INFECTED_FILES_DEF,k=INFECTED_FILES_TXT_KEY,expand_x=True,expand_y=True,font=FONT,justification='c',size=(20,1)),
                        sg.Text(DANGEROUS_GLOBALS_DEF,k=DANGEROUS_GLOBALS_TXT_KEY,expand_x=True,expand_y=True,font=FONT,justification='right',size=(20,1)),
                    ], 
                    [
                        sg.Multiline(k=CONSOLE_ML_KEY,reroute_stdout=True,write_only=False,reroute_cprint=True,
                        autoscroll=True,border_width=0,sbar_width=20,sbar_trough_color=0,
                        background_color=color.GRAY_1111, auto_refresh=True,size=(120,30),expand_x=True,expand_y=True)
                    ],                                              
                    [
                        sg.Frame('',[
                            [
                                sg.Text('',key=STATUS_STATE_TXT_KEY, expand_x=True,expand_y=True,justification='c',font=FONT,background_color=color.GRAY_9900)
                            ],
                        ],expand_x=True,expand_y=False,relief=sg.RELIEF_FLAT,border_width=0,visible=True,element_justification='c',background_color=color.GRAY_9900,size=(50,30))                          
                    ],   
            ],expand_x=True,expand_y=True,border_width=0,relief=sg.RELIEF_FLAT,element_justification="c")
        ],  
    ]
    
    bottom_column = [
        [
            sg.Frame('',[
                    [
                        sg.Frame(' Status',[
                            [
                                sg.Text('',key=STATUS_INFO_TXT_KEY, expand_x=True,font=FONT)
                            ],
                        ],expand_x=True,expand_y=True,relief=sg.RELIEF_SOLID,border_width=0,visible=True,element_justification='c',background_color=color.GRAY_9900,title_color=color.DARK_BLUE)                          
                    ],  

            ],expand_x=True,border_width=0,relief=sg.RELIEF_FLAT,element_justification='c')
        ],    
    ]

    layout = [
        top_column ,       
        mid_column,
        bottom_column,
    ]

    #endregion layout

    window = sg.Window(APP_TITLE,layout,finalize=True, resizable=True,enable_close_attempted_event=False,background_color=color.GRAY_9900)

    #region window elements

    huggingface_inp_elem:sg.Input = window[HUGGINGFACE_INP_KEY]
    url_inp_elem:sg.Input  = window[URL_INP_KEY]
    file_inp_elem:sg.Input  = window[FILE_INP_KEY]
    directory_inp_elem:sg.Input  = window[DIRECTORY_INP_KEY]
    status_state_txt_elem:sg.Text = window[STATUS_STATE_TXT_KEY]
    scanned_files_txt_elem:sg.Text = window[SCANNED_FILES_TXT_KEY]
    infected_files_txt_elem:sg.Text = window[INFECTED_FILES_TXT_KEY]
    dangerous_globals_txt_elem:sg.Text = window[DANGEROUS_GLOBALS_TXT_KEY]
    console_ml_elem:sg.Multiline  = window[CONSOLE_ML_KEY]
    status_info_txt_elem:sg.Text = window[STATUS_INFO_TXT_KEY]
    file_frame_elem:sg.Frame = window[FILE_FRM_KEY]
    directory_frame_elem:sg.Frame = window[DIRECTORY_FRM_KEY]
    url_frame_elem:sg.Frame = window[URL_FRM_KEY]
    huggingface_frame_elem:sg.Frame = window[HUGGINGFACE_FRM_KEY]

    #endregion window elements

    selected_input = {
        HUGGINGFACE_RAD_KEY: {file_frame_elem: False, directory_frame_elem: False, url_frame_elem: False, huggingface_frame_elem: True},
        URL_RAD_KEY: {file_frame_elem: False, directory_frame_elem: False, url_frame_elem: True, huggingface_frame_elem: False},
        FILE_RAD_KEY: {file_frame_elem: True, directory_frame_elem: False, url_frame_elem: False, huggingface_frame_elem: False},
        DIRECTORY_RAD_KEY: {file_frame_elem: False, directory_frame_elem: True, url_frame_elem: False, huggingface_frame_elem: False},
    }    

    flatten_ui_elements(window)

    def reset_ui():
        reset_files_state_display()
        update_status_state('')
        console_ml_elem.update(value='')
        scanned_files.clear()
        infected_files.clear()

    def update_status_state(value):
        status_state_txt_elem.update(value=value)
        status_state_txt_elem.Widget.config(background=color.GRAY_9900)  
        status_state_txt_elem.ParentRowFrame.config(background=color.GRAY_9900)

    def reset_files_state_display():
        status_info_txt_elem.update(value='Scanning. Please wait...') 
        scanned_files_txt_elem.update(value=SCANNED_FILES_DEF) 
        infected_files_txt_elem.update(value=INFECTED_FILES_DEF) 
        dangerous_globals_txt_elem.update(value=DANGEROUS_GLOBALS_DEF) 

    def scan():
        input_files = None
        if values[HUGGINGFACE_RAD_KEY]:
            input_files = values[HUGGINGFACE_INP_KEY]
            scan_target = scan_huggingface_model
        elif values[URL_RAD_KEY]:
            input_files = values[URL_INP_KEY]
            scan_target = scan_url
        elif values[DIRECTORY_RAD_KEY]:
            input_files = values[DIRECTORY_INP_KEY]
            scan_target = scan_directory_path
        elif values[FILE_RAD_KEY]:
            input_files = values[FILE_INP_KEY]
            scan_target = scan_file_path

        if input_files is None or len(input_files) <= 1:
            status_info_txt_elem.update(value='Nothing to scan')
            return

        try:
            return scan_target(input_files)
        except (RuntimeError, ConnectionRefusedError, AttributeError, FileNotFoundError,UnboundLocalError) as e:
            print(e.__class__.__name__, e)
            status_info_txt_elem.update(value='Fail to scan') 

    def update_results_display(scan_result):
        scanned_files_txt_elem.update(value=f'{SCANNED_FILES} {scan_result.scanned_files}') 
        infected_files_txt_elem.update(value=f'{INFECTED_FILES} {scan_result.infected_files}') 
        dangerous_globals_txt_elem.update(value=f'{DANGEROUS_GLOBALS} {scan_result.issues_count}') 
        scanned_files_len = len(scanned_files)
        infected_files_len = len(infected_files)

        print('')
        if scanned_files_len > 0:
            if infected_files_len == 0:
                status_state_txt_elem.update(text_color='white')
                status_state_txt_elem.Widget.config(background=color.DARK_GREEN)  
                status_state_txt_elem.ParentRowFrame.config(background=color.DARK_GREEN)
                status_state_txt_elem.update(value='PASS') 

        if infected_files_len > 0:
            print('')
            print('----------- INFECTED FILES -----------')
            print('')

            for file in infected_files:
                print(f"    {file}")

            status_state_txt_elem.update(text_color='white')
            status_state_txt_elem.Widget.config(background=color.RED_ORANGE)  
            status_state_txt_elem.ParentRowFrame.config(background=color.RED_ORANGE)
            status_state_txt_elem.update(value='FAIL') 

        status_info_txt_elem.update(value='Done') 

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        
        if event == SCAN_BTN_KEY:
                reset_ui()
                scan_result = scan()

                if not isError:
                    if scan_result:
                        update_results_display(scan_result)

        if event == HUGGINGFACE_CLEAR_BTN_KEY:
            huggingface_inp_elem.update(value='')

        if event == URL_CLEAR_BTN_KEY:
            url_inp_elem.update(value='')

        if event in selected_input:
            for frame, visibility in selected_input[event].items():
                frame.update(visible=visibility)    

        if event in right_click_menu[1]:
            if values[HUGGINGFACE_RAD_KEY]:
                do_clipboard_operation(event, window, huggingface_inp_elem,STATUS_INFO_TXT_KEY)
            if values[URL_RAD_KEY]:
                do_clipboard_operation(event, window, url_inp_elem,STATUS_INFO_TXT_KEY)                
            if values[FILE_RAD_KEY]:
                do_clipboard_operation(event, window, file_inp_elem,STATUS_INFO_TXT_KEY)       
            if values[DIRECTORY_RAD_KEY]:
                do_clipboard_operation(event, window, directory_inp_elem,STATUS_INFO_TXT_KEY)   

            window[CONSOLE_ML_KEY].update(value='')
            
        support.buttons(event)

if __name__ == '__main__':
    main() 
