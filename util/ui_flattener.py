#set_widget_relief_to_flat 

def ui_flattener(window):
    for widget_key in window.key_dict.keys():
        try: 
            window[widget_key].Widget.config(relief='flat')
        except:
            # print("error",widget_key)
            pass
