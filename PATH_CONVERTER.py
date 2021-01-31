import os
from os.path import join
import sys
import gc
if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg
from conversion_ops import conversion_main

def conversion_type_parser(file_path, param_values, save_dir_path, xml_path):
    if param_values['resize_radio']:
        if param_values['absolute_radio']:
            try:
                width, height = int(param_values['width_resize']), int(param_values['height_resize'])
            except:
                raise Exception("All parameters required for this conversion needs to be integers.")
            try:
                print(param_values)
                conversion_main(file_path, 'absolute', (width, height), save_dir_path, param_values['tumor_radio'], xml_path)
            except Exception as e:
                print("Exception occurred while executing absolute length conversion.")
                print(e)
        elif param_values['aspect_radio']:
            try:
                aspect_ratio_rate = int(param_values['aspect_ratio'])
            except:
                raise Exception("All parameters required for this conversion needs to be integers.")
            try:
                conversion_main(file_path, 'ratio', aspect_ratio_rate, save_dir_path, param_values['tumor_radio'], xml_path)
            except Exception as e:
                print("Exception occurred while executing aspect ratio conversion.")
                print(e)
        else:
            raise Exception("Resize type is not supported.")
    elif param_values['patch_radio']:
        try:
            try:
                patch_length, overlap_length = int(param_values['length_patch']), int(param_values['length_overlap'])
            except:
                raise Exception("All parameters required for this conversion needs to be integers.")
            if overlap_length > patch_length:
                raise Exception("Overlap length must be smaller than the patch length.")
            try:
                conversion_main(file_path, 'patch', (patch_length, overlap_length), save_dir_path, param_values['tumor_radio'], xml_path)
            except Exception as e:
                print("Exception occurred while executing patch extraction.")
                print(e)
        except Exception as e:
            raise Exception(e)
    else:
        raise Exception("Conversion type is not supported.")


def WSI_PNG_Converter():
    POSSIBLE_CONVERSION_FORMATS = ['svs', 'tif', 'ndpi', 'vms', 'vmu', 'scn', 'mrxs', 'tiff', 'svslide', 'bif']

    file_check = True
    folder_check = False
    resize_check = True
    patch_check = False
    tumor_check = False 
    absolute_check = True
    aspect_check = False
    resizing_height = 1024
    resizing_width = 1024
    aspect_ratio = 20
    patch_length = 512
    patch_length_overlap = 0

    layout = [[sg.Frame("",
                        layout=[[sg.Text('Rename files or folders', font='opensans 10 bold')],
                                [sg.Radio('Convert a file', size=(10, 1), enable_events=True, default=file_check,
                                          group_id='source', key='file_radio'),
                                 sg.Radio('Convert all files in folder', size=(18, 1), enable_events=True,
                                          default=folder_check, group_id='source', key='folder_radio')],
                                [sg.Text('Source for Files ', size=(15, 1)),
                                 sg.InputText(disabled=folder_check, key='file_browse_input'),
                                 sg.FileBrowse(disabled=folder_check, key='file_browse_button')],
                                [sg.Text('Source for Folders', size=(15, 1)),
                                 sg.InputText(disabled=file_check, key='folder_browse_input'),
                                 sg.FolderBrowse(disabled=file_check, key='folder_browse_button')],
                                [sg.Text('Saving Folder', size=(15, 1)),
                                 sg.InputText(key='save_destination'),
                                 sg.FolderBrowse(key='save_dir_browse_button')],
                                ])],
                        [sg.Frame("",
                                  layout=[[sg.Text('Choose to resize image or extract patches from the region of interest', size=(45, 1), font='opensans 10 bold')],
                                            [sg.Radio('Resize Image', size=(10,1), enable_events=True, default=resize_check, group_id='conversion_method', key='resize_radio'),
                                            sg.Radio('Extract Patch', size=(10,1), enable_events=True, default=patch_check, group_id='conversion_method', key='patch_radio'),
                                             sg.Checkbox('Only Tumor Area', size=(18,1), enable_events=True, default=tumor_check, key='tumor_radio')],
                                          [sg.Text('Source for xml Files', size=(18, 1)),
                                           sg.InputText(disabled=folder_check, key='xml_file_destination'),
                                           sg.FileBrowse(disabled=folder_check, key='xml_file_dir_browse_button')],
                                          [sg.Text('Source for xml Folders', size=(18, 1)),
                                           sg.InputText(disabled=file_check, key='xml_folder_destination'),
                                           sg.FolderBrowse(disabled=file_check, key='xml_folder_dir_browse_button')],

                                [sg.Frame("", layout=[[sg.Text('Resizing options', size=(25, 1), font='opensans 10 bold')],
                                                      [sg.Radio('Absolute Length', size=(20, 1), enable_events=True, default=absolute_check, group_id='resize_options', key='absolute_radio')],
                                                      [sg.Text('Height', size=(15, 1)), sg.InputText(resizing_height, disabled=aspect_check, key='height_resize')],
                                                      [sg.Text('Width', size=(15, 1)), sg.InputText(resizing_width, disabled=aspect_check, key='width_resize')],
                                                      [sg.Radio('Aspect Ratio', size=(20, 1), enable_events=True, default=aspect_check, group_id='resize_options', key='aspect_radio')],
                                                      [sg.Text('Ratio', size=(15, 1)), sg.InputText(aspect_ratio, disabled=absolute_check, key='aspect_ratio')]])],
                                [sg.Frame("", layout=[[sg.Text('Patch options', size=(25, 1), font='opensans 10 bold')],
                                                      [sg.Text('Patch length', size=(15, 1)), sg.InputText(patch_length, disabled=resize_check, key='length_patch')],
                                                      [sg.Text('Patch overlap length', size=(15, 1)), sg.InputText(patch_length_overlap, disabled=resize_check, key='length_overlap')]])]])],
              [sg.Submit(), sg.Cancel()]]

    window = sg.Window('PATH Converter', icon='deep_path_logo.ico').Layout(layout)

    while True:                 # Event Loop
        event, values = window.Read()
        if (event is not None) and (values is not None):
            print(event, values)
            print(values)

            input_text_keys = ['file_browse_input', 'folder_browse_input', 'save_destination',
                               'height_resize', 'width_resize', 'aspect_ratio', 'length_patch', 'length_overlap']
            for itk in input_text_keys:
                window.FindElement(itk).Update(values[itk])

            if values['folder_radio']:
                window.FindElement('file_browse_input').Update(disabled=True)
                window.FindElement('file_browse_button').Update(disabled=True)
                window.FindElement('folder_browse_input').Update(disabled=False)
                window.FindElement('folder_browse_button').Update(disabled=False)
            elif values['file_radio']:
                window.FindElement('folder_browse_input').Update(disabled=True)
                window.FindElement('folder_browse_button').Update(disabled=True)
                window.FindElement('file_browse_input').Update(disabled=False)
                window.FindElement('file_browse_button').Update(disabled=False)
            else:
                raise Exception("Unknown Error has been found for toggling Source file/folder")
            if values['tumor_radio']:
                if values['folder_radio']:
                    window.FindElement('xml_file_destination').Update(disabled=True)
                    window.FindElement('xml_file_dir_browse_button').Update(disabled=True)
                    window.FindElement('xml_folder_destination').Update(disabled=False)
                    window.FindElement('xml_folder_dir_browse_button').Update(disabled=False)
                elif values['file_radio']:
                    window.FindElement('xml_file_destination').Update(disabled=False)
                    window.FindElement('xml_file_dir_browse_button').Update(disabled=False)
                    window.FindElement('xml_folder_destination').Update(disabled=True)
                    window.FindElement('xml_folder_dir_browse_button').Update(disabled=True)


                if values['resize_radio']:
                    window.FindElement('length_patch').Update(disabled=True)
                    window.FindElement('length_overlap').Update(disabled=True)
                    if values['aspect_radio']:
                        window.FindElement('height_resize').Update(disabled=True)
                        window.FindElement('width_resize').Update(disabled=True)
                        window.FindElement('aspect_ratio').Update(disabled=False)
                    elif values['absolute_radio']:
                        window.FindElement('height_resize').Update(disabled=False)
                        window.FindElement('width_resize').Update(disabled=False)
                        window.FindElement('aspect_ratio').Update(disabled=True)
                    else:
                        raise Exception("Unknown Error has been found for toggling absolute or aspect selection")
                elif values['patch_radio']:
                    window.FindElement('height_resize').Update(disabled=True)
                    window.FindElement('width_resize').Update(disabled=True)
                    window.FindElement('aspect_ratio').Update(disabled=True)
                    window.FindElement('length_patch').Update(disabled=False)
                    window.FindElement('length_overlap').Update(disabled=False)
                else:
                    raise Exception("Unknown Error has been found for toggling resize/patch selection")
            else:
                window.FindElement('xml_file_destination').Update(disabled=True)
                window.FindElement('xml_file_dir_browse_button').Update(disabled=True)
                window.FindElement('xml_folder_destination').Update(disabled=True)
                window.FindElement('xml_folder_dir_browse_button').Update(disabled=True)
                if values['resize_radio']:
                    window.FindElement('length_patch').Update(disabled=True)
                    window.FindElement('length_overlap').Update(disabled=True)
                    if values['aspect_radio']:
                        window.FindElement('height_resize').Update(disabled=True)
                        window.FindElement('width_resize').Update(disabled=True)
                        window.FindElement('aspect_ratio').Update(disabled=False)
                    elif values['absolute_radio']:
                        window.FindElement('height_resize').Update(disabled=False)
                        window.FindElement('width_resize').Update(disabled=False)
                        window.FindElement('aspect_ratio').Update(disabled=True)
                    else:
                        raise Exception("Unknown Error has been found for toggling absolute or aspect selection")
                elif values['patch_radio']:
                    window.FindElement('height_resize').Update(disabled=True)
                    window.FindElement('width_resize').Update(disabled=True)
                    window.FindElement('aspect_ratio').Update(disabled=True)
                    window.FindElement('length_patch').Update(disabled=False)
                    window.FindElement('length_overlap').Update(disabled=False)
                else:
                    raise Exception("Unknown Error has been found for toggling resize/patch selection")
            if event is None or event == 'Exit' or event == 'Cancel':
                break
            if event == 'Show':
                # change the "output" element to be the value of "input" element
                window.FindElement('_OUTPUT_').Update(values['_IN_'])
            if event == 'Submit':
                try:
                    if values['file_radio']:
                        file_path = values['file_browse_input']
                        xml_path = values['xml_file_destination']
                        print("File conversion is selected")
                        print("Input file path: " + file_path)
                        if (file_path == "") or (not os.path.exists(file_path)):
                            sg.Popup('Please enter a proper file path. \nEither file does not exist or not selected.')
                        else:
                            extension = file_path.split(os.sep)[-1].split('.')[-1]
                            if extension in POSSIBLE_CONVERSION_FORMATS:
                                print("Got it")
                                print("Save destination: " + str(values['save_destination']))
                                sg.Popup(file_path + " is being converted. Please do not turn off the program.", auto_close=True)
                                conversion_type_parser(file_path, param_values=values, save_dir_path=values['save_destination'], xml_path = xml_path)
                                sg.Popup(file_path + " has been converted.")
                            else:
                                sg.Popup('This program only supports below WSI format. \n '
                                         'Please try with a different image file. \n ' + str(POSSIBLE_CONVERSION_FORMATS)[1:-1]).upper()
                    elif values['folder_radio']:
                        invalid_file_types = 0
                        folder_path = values['folder_browse_input']
                        xml_path = values['xml_folder_destination']
                        print("Folder conversion is selected")
                        print("Input folder path: " + folder_path)
                        if (folder_path == "") or (not os.path.exists(folder_path)):
                            sg.Popup('Please enter a proper file path. \nEither file does not exist or not selected.')
                        else:
                            for i, file_name in enumerate(os.listdir(folder_path)):
                                if file_name.split('.')[-1] in POSSIBLE_CONVERSION_FORMATS:
                                    print(join(folder_path, file_name))
                                    print("Save destination: " + str(values['save_destination']))
                                    sg.Popup("Files in " + folder_path + " are being converted. Please do not turn off the program.", auto_close=True)
                                    conversion_type_parser(join(folder_path, file_name), param_values=values, save_dir_path=values['save_destination'], xml_path = xml_path +'/'+ file_name[:-4]+'.xml')
                                else:
                                    invalid_file_types += 1
                        sg.Popup("WSIs in " + folder_path + " have been converted.")
                    else:
                        raise Exception("Unknown Error has been found for toggling Source file/folder after Submit")
                except Exception as e:
                    sg.Popup(e)
        else:
            break
        gc.collect()
    window.Close()


if __name__ == '__main__':
    WSI_PNG_Converter()
