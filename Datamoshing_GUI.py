# coding: utf-8

import PySimpleGUI as sg
import webbrowser
from termcolor import colored, cprint
import colorama
import os
import subprocess
import time
from pygame import mixer

import software_info

version = software_info.VERSION()
window_title = 'Datamoshing_GUI v' + version

icon_path = 'data/img/icon_black.ico'

tooltip_input = 'File to be moshed'
tooltip_output = 'output file for the moshed video'

tooltip_startframe = 'start frame of the mosh'
tooltip_endframe = 'end frame of the mosh'
tooltip_fps = 'fps to convert initial video to'
tooltip_delta = 'number of delta frames to repeat'

tooltip_script = 'path to the script'
tooltip_goppreriod = 'I-frame period (in frames)'

tooltip_vector = 'file containing vector data to transfer'
tooltip_extract = 'video to extract motion vector data from'
tooltip_transfer = 'video to transfer motion vector data to'
tooltip_mjoutput = 'output file either for the final video, or for the vector data'

fd_error_sw = 0
vm_error_sw = 0
st_error_sw = 0

colorama.init()

def play_sound(type):
    mixer.init()
    if type == 0:
        mixer.music.load('data/sound/notify.mp3')
    elif type == 1:
        mixer.music.load('data/sound/error.mp3')
    mixer.music.play(1)

def print_info(text):
    print(colored('[INFO] ', 'green'), text)

def print_warning(text):
    print(colored('[WARNING] ', 'yellow'), text)

def print_error(text):
    print(colored('[ERROR] ', 'red'), text)

def isint(s):
    try:
        int(s, 10)
    except ValueError:
        return False
    else:
        return True

#pysimplegui THEME
sg.LOOK_AND_FEEL_TABLE['dark'] = {
	'BACKGROUND': '#000000',
	'TEXT': 'white',
	'INPUT': '#eeeeee',
	'SCROLL': '#4169e1',
	'TEXT_INPUT': 'black',
	'BUTTON': ('black', '#ffffff'),
	'PROGRESS': sg.DEFAULT_PROGRESS_BAR_COLOR,
	'BORDER': 0,
	'SLIDER_DEPTH': 0,
	'PROGRESS_DEPTH': 0
}

sg.theme('dark')

os.system('cls')

print(colored('Datamoshing_GUI', 'cyan'), colored('Version: ' + version, 'green'))
print(colored('https://github.com/CubeZeero/datamoshing_GUI', 'cyan'))
print(colored('Fork from: https://github.com/tiberiuiancu/datamoshing', 'cyan'))

def make_start_window():
        start_layout = [[sg.Image(source = 'data/img/icon_white.png', pad = ((0,0),(30,0)))],
                        [sg.Text(text = 'Datamoshing_GUI', font = ['Meiryo',15,'bold'], pad = ((0,0),(30,0)))],

                        [sg.Button(button_text = 'ffmpeg_datamosh', font = ['Meiryo',10], size = (20,1), pad = ((0,0),(30,0)), key = '-fd_button-'),
                        sg.Button(button_text = 'VectorMotion', font = ['Meiryo',10], size = (20,1), pad = ((10,0),(30,0)), key = '-vm_button-'),
                        sg.Button(button_text = 'StyleTransfer', font = ['Meiryo',10], size = (20,1), pad = ((10,0),(30,0)), key = '-st_button-')],

                        [sg.Button(button_text = 'README.md', font = ['Meiryo',10], size = (20,1), pad = ((0,0),(30,0)), key = '-readme_button-')],

                        [sg.Text(text = 'Fork from: ', font = ['Meiryo',10], pad = ((0,0),(30,0))),
                        sg.Text(text = 'https://github.com/tiberiuiancu/datamoshing', font = ['Meiryo',10,'underline'], enable_events = True, pad = ((0,0),(30,0)), key = '-fork_url-')]]

        return sg.Window(window_title, start_layout, icon = icon_path, size = (700,460), font = ['Meiryo',12], element_justification='c')

def make_fd_window():
        fd_layout = [[sg.Text('Input', pad = ((0,0),(20,0))), sg.Input(font = ['Meiryo',10], size = (63,1),pad = ((30,0),(20,0)), tooltip = tooltip_input, key = '-input_path-'),
                      sg.Button(button_text = 'Browse', font = ['Meiryo',8], size = (10,1), pad = ((20,0),(20,0)), key = '-i_browse_button-')],

                     [sg.Text('Output', pad = ((0,0),(20,0))), sg.Input(font = ['Meiryo',10], size = (63,1),pad = ((20,0),(20,0)), tooltip = tooltip_output, key = '-output_path-'),
                      sg.Button(button_text = 'Browse', font = ['Meiryo',8], size = (10,1), pad = ((20,0),(20,0)), key = '-o_browse_button-')],

                     [sg.Text('StartFrame', pad = ((0,0),(20,0))), sg.Input(font = ['Meiryo',10], size = (10,1),pad = ((20,0),(20,0)), tooltip = tooltip_startframe, key = '-startframe-'),
                      sg.Text('EndFrame', pad = ((20,0),(20,0))), sg.Input(font = ['Meiryo',10], size = (10,1),pad = ((20,0),(20,0)), tooltip = tooltip_endframe, key = '-endframe-'),
                      sg.Text('FPS', pad = ((20,0),(20,0))), sg.Input(font = ['Meiryo',10], size = (10,1),pad = ((20,0),(20,0)), tooltip = tooltip_fps, key = '-fps-'),
                      sg.Text('Delta', pad = ((20,0),(20,0))), sg.Input(font = ['Meiryo',10], size = (10,1),pad = ((20,0),(20,0)), tooltip = tooltip_delta, key = '-delta-')],

                     [sg.Button(button_text = 'Back', font = ['Meiryo',10], size = (40,1), pad = ((0,0),(20,0)), key = '-back_button-'),
                      sg.Button(button_text = 'GLITCH!', button_color = '#ff0000', font = ['Meiryo',10], size = (40,1), pad = ((20,0),(20,0)), key = '-glitch_button-')]]

        return sg.Window(window_title + ' - ffmpeg_datamosh', fd_layout, icon = icon_path, size = (700,210), font = ['Meiryo',10], finalize = True)

def make_vm_window():
        vm_layout = [[sg.Text('Input', pad = ((0,0),(20,0))), sg.Input(font = ['Meiryo',10], size = (63,1),pad = ((30,0),(20,0)), tooltip = tooltip_input, key = '-input_path-'),
                      sg.Button(button_text = 'Browse', font = ['Meiryo',8], size = (10,1), pad = ((20,0),(20,0)), key = '-i_browse_button-')],

                     [sg.Text('Output', pad = ((0,0),(20,0))), sg.Input(font = ['Meiryo',10], size = (63,1),pad = ((20,0),(20,0)), tooltip = tooltip_output, key = '-output_path-'),
                      sg.Button(button_text = 'Browse', font = ['Meiryo',8], size = (10,1), pad = ((20,0),(20,0)), key = '-o_browse_button-')],

                     [sg.Text('Script', pad = ((0,0),(20,0))), sg.Input(font = ['Meiryo',10], size = (63,1),pad = ((27,0),(20,0)), tooltip = tooltip_script, key = '-script_path-'),
                      sg.Button(button_text = 'Browse', font = ['Meiryo',8], size = (10,1), pad = ((20,0),(20,0)), key = '-s_browse_button-')],

                     [sg.Text('I-frame period (in frames)', pad = ((190,0),(20,0))), sg.Input(font = ['Meiryo',10], size = (15,1),pad = ((20,0),(20,0)), tooltip = tooltip_goppreriod, key = '-gop_period-')],

                     [sg.Button(button_text = 'Back', font = ['Meiryo',10], size = (40,1), pad = ((0,0),(20,0)), key = '-back_button-'),
                      sg.Button(button_text = 'GLITCH!', button_color = '#ff0000', font = ['Meiryo',10], size = (40,1), pad = ((20,0),(20,0)), key = '-glitch_button-')]]

        return sg.Window(window_title + ' - VectorMotion', vm_layout, icon = icon_path, size = (700,260), font = ['Meiryo',10], finalize = True)

def make_st_window():
        st_layout = [[sg.Text('Vector', pad = ((0,0),(20,0))), sg.Input(font = ['Meiryo',10], size = (63,1),pad = ((30,0),(20,0)), tooltip = tooltip_vector, key = '-vector_path-'),
                      sg.Button(button_text = 'Browse', font = ['Meiryo',8], size = (10,1), pad = ((20,0),(20,0)), key = '-v_browse_button-')],

                     [sg.Text('Extract', pad = ((0,0),(20,0))), sg.Input(font = ['Meiryo',10], size = (63,1),pad = ((27,0),(20,0)), tooltip = tooltip_extract, key = '-extract_path-'),
                      sg.Button(button_text = 'Browse', font = ['Meiryo',8], size = (10,1), pad = ((20,0),(20,0)), key = '-e_browse_button-')],

                     [sg.Text('Transfer', pad = ((0,0),(20,0))), sg.Input(font = ['Meiryo',10], size = (63,1),pad = ((20,0),(20,0)), tooltip = tooltip_transfer, key = '-transfer_path-'),
                      sg.Button(button_text = 'Browse', font = ['Meiryo',8], size = (10,1), pad = ((20,0),(20,0)), key = '-t_browse_button-')],

                     [sg.Text('Output', pad = ((0,0),(20,0))), sg.Input(font = ['Meiryo',10], size = (63,1),pad = ((28,0),(20,0)), tooltip = tooltip_mjoutput, key = '-output_path-'),
                      sg.Button(button_text = 'Browse', font = ['Meiryo',8], size = (10,1), pad = ((20,0),(20,0)), key = '-o_browse_button-')],

                     [sg.Button(button_text = 'Back', font = ['Meiryo',10], size = (40,1), pad = ((0,0),(20,0)), key = '-back_button-'),
                      sg.Button(button_text = 'GLITCH!', button_color = '#ff0000', font = ['Meiryo',10], size = (40,1), pad = ((20,0),(20,0)), key = '-glitch_button-')]]

        return sg.Window(window_title + ' - StyleTransfer', st_layout, icon = icon_path, size = (700,260), font = ['Meiryo',10], finalize = True)

start_window = make_start_window()

while True:
    start_event, start_values = start_window.read()

    if start_event == sg.WIN_CLOSED:
        break

    if start_event == '-fork_url-':
        webbrowser.open('https://github.com/tiberiuiancu/datamoshing')

    if start_event == '-readme_button-':
        webbrowser.open('https://github.com/CubeZeero/datamoshing_GUI/blob/master/README.md')

    if start_event == '-fd_button-':
        start_window.close()
        fd_window = make_fd_window()

        while True:
            fd_event, fd_values = fd_window.read()

            if fd_event == sg.WIN_CLOSED or fd_event == '-back_button-':
                fd_window.close()
                start_window = make_start_window()
                break

            if fd_event == '-i_browse_button-':
                input_path_tmp = sg.popup_get_file('Input', title = 'Input', default_extension = '.mp4', file_types = (('mp4', '.mp4'),), no_window = True)
                if input_path_tmp != '':
                    fd_window['-input_path-'].update(value = input_path_tmp)

            if fd_event == '-o_browse_button-':
                output_path_tmp = sg.popup_get_file('Output', title = 'Output', default_extension = '.mp4', file_types = (('mp4', '.mp4'),), no_window = True, save_as = True)
                if output_path_tmp != '':
                    fd_window['-output_path-'].update(value = output_path_tmp)

            if fd_event == '-glitch_button-':

                fd_error_sw = 0

                if os.path.exists(fd_values['-input_path-']) == False or fd_values['-input_path-'] == '':
                    print_error('Input file does not exist.')
                    fd_error_sw = 1

                if isint(fd_values['-startframe-']) == False and fd_values['-startframe-'] != '':
                    print_error('StartFrame is not a number.')
                    fd_error_sw = 1

                if isint(fd_values['-endframe-']) == False and fd_values['-endframe-'] != '':
                    print_error('EndFrame is not a number.')
                    fd_error_sw = 1

                if isint(fd_values['-fps-']) == False and fd_values['-fps-'] != '':
                    print_error('FPS is not a number.')
                    fd_error_sw = 1

                if isint(fd_values['-delta-']) == False and fd_values['-delta-'] != '':
                    print_error('Delta is not a number.')
                    fd_error_sw = 1

                if fd_error_sw == 1:
                    play_sound(1)
                    print('\n')
                    sg.popup_ok('ERROR! Please check the console log.', title = window_title + ' - ffmpeg_datamosh', icon = icon_path)

                elif fd_error_sw == 0:

                    fd_window['-i_browse_button-'].update(disabled = True)
                    fd_window['-o_browse_button-'].update(disabled = True)
                    fd_window['-back_button-'].update(disabled = True)
                    fd_window['-glitch_button-'].update(disabled = True)

                    fd_window.Refresh()

                    arg_inputpath = fd_values['-input_path-']

                    if fd_values['-output_path-'] != '':
                        arg_outputpath = ' -o ' + fd_values['-output_path-']
                    elif fd_values['-output_path-'] == '':
                        arg_outputpath = ''

                    if fd_values['-startframe-'] != '':
                        arg_startframe = ' -s ' + fd_values['-startframe-']
                    elif fd_values['-startframe-'] == '':
                        arg_startframe = ''

                    if fd_values['-endframe-'] != '':
                        arg_endframe = ' -e ' + fd_values['-endframe-']
                    elif fd_values['-endframe-'] == '':
                        arg_endframe = ''

                    if fd_values['-fps-'] != '':
                        arg_fps = ' -f ' + fd_values['-fps-']
                    elif fd_values['-fps-'] == '':
                        arg_fps = ''

                    if fd_values['-delta-'] != '':
                        arg_delta = ' -d ' + fd_values['-delta-']
                    elif fd_values['-delta-'] == '':
                        arg_delta = ''

                    commandline_text = 'bin/ffmpeg_datamosh.exe ' + arg_inputpath + arg_outputpath + arg_startframe + arg_endframe + arg_fps + arg_delta
                    print('\n')
                    print_info(commandline_text)

                    subprocess.call(commandline_text)
                    print('\n')
                    print_info('The process is complete. Don\'t worry if you get an ffmpeg error.')

                    fd_window['-i_browse_button-'].update(disabled = False)
                    fd_window['-o_browse_button-'].update(disabled = False)
                    fd_window['-back_button-'].update(disabled = False)
                    fd_window['-glitch_button-'].update(disabled = False)

                    play_sound(0)
                    sg.popup_ok('The process is complete. Please check the console log.', title = window_title + ' - ffmpeg_datamosh', icon = icon_path)

    if start_event == '-vm_button-':
        start_window.close()
        vm_window = make_vm_window()

        while True:
            vm_event, vm_values = vm_window.read()

            if vm_event == sg.WIN_CLOSED or vm_event == '-back_button-':
                vm_window.close()
                start_window = make_start_window()
                break

            if vm_event == '-i_browse_button-':
                input_path_tmp = sg.popup_get_file('Input', title = 'Input', file_types = (('mp4', '.mp4'),), no_window = True)
                if input_path_tmp != '':
                    vm_window['-input_path-'].update(value = input_path_tmp)

            if vm_event == '-o_browse_button-':
                output_path_tmp = sg.popup_get_file('Output', title = 'Output', default_extension = '.mp4', file_types = (('mp4', '.mp4'),), no_window = True, save_as = True)
                if output_path_tmp != '':
                    vm_window['-output_path-'].update(value = output_path_tmp)

            if vm_event == '-s_browse_button-':
                script_path_tmp = sg.popup_get_file('Output', title = 'Output', file_types = (('python', '.py'),('javascript', '.js'),), no_window = True)
                if script_path_tmp != '':
                    vm_window['-script_path-'].update(value = script_path_tmp)

            if vm_event == '-glitch_button-':

                vm_error_sw = 0

                if os.path.exists(vm_values['-input_path-']) == False or vm_values['-input_path-'] == '':
                    print_error('Input file does not exist.')
                    vm_error_sw = 1

                if os.path.exists(vm_values['-script_path-']) == False or vm_values['-script_path-'] == '':
                    print_error('Script file does not exist.')
                    vm_error_sw = 1

                if isint(vm_values['-gop_period-']) == False and vm_values['-gop_period-'] != '':
                    print_error('I-frame period is not a number.')
                    vm_error_sw = 1

                if vm_error_sw == 1:
                    play_sound(1)
                    print('\n')
                    sg.popup_ok('ERROR! Please check the console log.', title = window_title + ' - VectorMotion', icon = icon_path)

                elif vm_error_sw == 0:

                    vm_window['-i_browse_button-'].update(disabled = True)
                    vm_window['-o_browse_button-'].update(disabled = True)
                    vm_window['-s_browse_button-'].update(disabled = True)
                    vm_window['-back_button-'].update(disabled = True)
                    vm_window['-glitch_button-'].update(disabled = True)

                    vm_window.Refresh()

                    arg_inputpath = vm_values['-input_path-']
                    arg_scriptpath = ' -s ' + vm_values['-script_path-']

                    if vm_values['-output_path-'] != '':
                        arg_outputpath = ' -o ' + vm_values['-output_path-']
                    elif vm_values['-output_path-'] == '':
                        arg_outputpath = ''

                    if vm_values['-gop_period-'] != '':
                        arg_gopperiod = ' -g ' + vm_values['-gop_period-']
                    elif vm_values['-gop_period-'] == '':
                        arg_gopperiod = ''

                    commandline_text = 'bin/vector_motion.exe ' + arg_inputpath + arg_scriptpath + arg_gopperiod + arg_outputpath
                    print('\n')
                    print_info(commandline_text)

                    subprocess.call(commandline_text)
                    print('\n')
                    print_info('The process is complete. Don\'t worry if you get an ffmpeg error.')

                    vm_window['-i_browse_button-'].update(disabled = False)
                    vm_window['-o_browse_button-'].update(disabled = False)
                    vm_window['-s_browse_button-'].update(disabled = False)
                    vm_window['-back_button-'].update(disabled = False)
                    vm_window['-glitch_button-'].update(disabled = False)

                    play_sound(0)
                    sg.popup_ok('The process is complete. Please check the console log.', title = window_title + ' - VectorMotion', icon = icon_path)

    if start_event == '-st_button-':
        start_window.close()
        st_window = make_st_window()

        while True:
            st_event, st_values = st_window.read()

            if st_event == sg.WIN_CLOSED or st_event == '-back_button-':
                st_window.close()
                start_window = make_start_window()
                break

            if st_event == '-v_browse_button-':
                vector_path_tmp = sg.popup_get_file('VectorFile', title = 'VectorFile', file_types = (('json', '.json'),), no_window = True)
                if vector_path_tmp != '':
                    st_window['-vector_path-'].update(value = vector_path_tmp)

            if st_event == '-e_browse_button-':
                extract_path_tmp = sg.popup_get_file('Extract', title = 'Extract', file_types = (('mp4', '.mp4'),), no_window = True)
                if extract_path_tmp != '':
                    st_window['-extract_path-'].update(value = extract_path_tmp)

            if st_event == '-t_browse_button-':
                transfer_path_tmp = sg.popup_get_file('Output', title = 'Output', file_types = (('mp4', '.mp4'),), no_window = True)
                if transfer_path_tmp != '':
                    st_window['-transfer_path-'].update(value = transfer_path_tmp)

            if st_event == '-o_browse_button-':
                output_path_tmp = sg.popup_get_file('Output', title = 'Output', default_extension = '.mp4', file_types = (('mp4', '.mp4'),('json', '.json'),), no_window = True, save_as = True)
                if output_path_tmp != '':
                    st_window['-output_path-'].update(value = output_path_tmp)

            if st_event == '-glitch_button-':

                st_error_sw = 0

                if st_values['-output_path-'] == '':
                    print_error('Specify output file. (Required)')
                    st_error_sw = 1

                if (os.path.exists(st_values['-vector_path-']) == False and st_values['-vector_path-'] != '') == True:
                    print_error('Vector Path does not exist.')
                    st_error_sw = 1

                if (os.path.exists(st_values['-transfer_path-']) == False and st_values['-transfer_path-'] != '') == True:
                    print_error('Transfer Path does not exist.')
                    st_error_sw = 1

                if (os.path.exists(st_values['-extract_path-']) == False and st_values['-extract_path-'] != '') == True:
                    print_error('Extract Path does not exist.')
                    st_error_sw = 1

                if not ((st_values['-extract_path-'] == '') ^ (st_values['-vector_path-'] == '')):
                    print_error('Please specify only one, either Extract or Vector.')
                    st_error_sw = 1

                if os.path.exists(st_values['-vector_path-']) == True and st_values['-output_path-'][-4:] == 'json':
                    print_error('It is not possible to output a json file with a json file specified in vector.')
                    st_error_sw = 1

                if os.path.exists(st_values['-vector_path-']) == True and os.path.exists(st_values['-transfer_path-']) == False:
                    print_error('If you want to use Vector to output mp4, specify Transfer as well.')
                    st_error_sw = 1

                if os.path.exists(st_values['-extract_path-']) == True\
                and os.path.exists(st_values['-transfer_path-']) == True and st_values['-output_path-'][-4:] == 'json':
                    print_error('If the Extract and Transfer are specified, it is not possible to output json files, only mp4.')
                    st_error_sw = 1

                if os.path.exists(st_values['-extract_path-']) == True\
                and st_values['-transfer_path-'] == '' and st_values['-output_path-'][-3:] == 'mp4':
                    print_error('If only the Extract is specified, only json files can be output.')
                    st_error_sw = 1

                if st_error_sw == 1:
                    play_sound(1)
                    print('\n')
                    sg.popup_ok('ERROR! Please check the console log.', title = window_title + ' - StyleTransfer', icon = icon_path)

                elif st_error_sw == 0:

                    st_window['-v_browse_button-'].update(disabled = True)
                    st_window['-e_browse_button-'].update(disabled = True)
                    st_window['-t_browse_button-'].update(disabled = True)
                    st_window['-o_browse_button-'].update(disabled = True)
                    st_window['-back_button-'].update(disabled = True)
                    st_window['-glitch_button-'].update(disabled = True)

                    st_window.Refresh()

                    arg_outputpath = ' ' + st_values['-output_path-']

                    if st_values['-vector_path-'] != '':
                        arg_vectorpath = ' -v ' + st_values['-vector_path-']
                    elif st_values['-vector_path-'] == '':
                        arg_vectorpath = ''

                    if st_values['-extract_path-'] != '':
                        arg_extractpath = ' -e ' + st_values['-extract_path-']
                    elif st_values['-extract_path-'] == '':
                        arg_extractpath = ''

                    if st_values['-transfer_path-'] != '':
                        arg_transferpath = ' -t ' + st_values['-transfer_path-']
                    elif st_values['-transfer_path-'] == '':
                        arg_transferpath = ''

                    commandline_text = 'bin/style_transfer.exe ' + arg_vectorpath + arg_extractpath + arg_transferpath + arg_outputpath
                    print('\n')
                    print_info(commandline_text)

                    subprocess.call(commandline_text)
                    print('\n')
                    print_info('The process is complete. Don\'t worry if you get an ffmpeg error.')

                    st_window['-v_browse_button-'].update(disabled = False)
                    st_window['-e_browse_button-'].update(disabled = False)
                    st_window['-t_browse_button-'].update(disabled = False)
                    st_window['-o_browse_button-'].update(disabled = False)
                    st_window['-back_button-'].update(disabled = False)
                    st_window['-glitch_button-'].update(disabled = False)

                    play_sound(0)
                    sg.popup_ok('The process is complete. Please check the console log.', title = window_title + ' - StyleTransfer', icon = icon_path)
