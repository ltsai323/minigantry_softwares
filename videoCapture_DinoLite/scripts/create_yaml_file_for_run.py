#!/usr/bin/env python3

import subprocess
import yaml

debug_mode = False
def BUG(mesg):
    if debug_mode:
        print(f'[DEBUG] {meag}')
def info(stat, mesg):
    print(f'[{stat}] {mesg}')

def __expected_result_checker__(functionNAME, result, expectedRESULT):
    if result == expectedRESULT:
        info('GOOD RESULT', f'{functionNAME}() got good result')
    else:
        info('ERROR', f'{functionNAME}() got unwanted result: "{result}" is differ from "{expectedRESULT}"')
def getResultFromPowerShell(cmd) -> list:
    res = subprocess.run(['powershell', '-Command', cmd], capture_output=True, text=True)
    outputs = [ line.strip() for line in mesg.split('\n') ]
    return res.stdout


def testfunction__getResultFromPowerShell():
    cmd = 'get-StartApps'
    print( getResultFromPowerShell(cmd) )



def showOptions(options:list):
    if len(options) == 0:
        raise IOError('Nothing put into showOptions. Please check')
    if len(options) == 1: return options[0]
    info('Select Item', 'Input index to choose (q/Q to abort)')
    for idx, option in enumerate(options):
        IDX = idx+1
        info(f'{IDX:2d}', option)

    info("I'll modify manually", "No option is available for me, I'll modify it later...")
    info(' 0', '   '.join(options))

    while True:
        val = input('index = ')
        if val.lower() == 'q':
            info('Abort', 'program quit')
            exit(1)
        try:
            IDX = int(val)
            if IDX == 0:
                return '   '.join(options)
            idx = IDX-1
            return options[idx]
        except ValueError:
            info('SelectAgain', f'Invalid input value "{val}"')
        except IndexError:
            info('SelectAgain', f'Invalid index "{val}"')
def testfunc__showOptions():
    showOptions( ['aa', 'bb', 'cccc'] )
    exit(1)

def selectNeededApp(appINFOlist:list, strRECOGNIZER:str):
    app_candidate = [ appINFO for appINFO in appINFOlist if strRECOGNIZER in appINFO ]
    if len(app_candidate) == 0:
        info('NothingFound', 'selectNeededApp() searched 0 candidate from app info list')
        for appINFO in appINFOlist:
            print(f' --> {appINFO}')
        print('')
        info('NothingFound', f'"{strRECOGNIZER}" matched nothing from app info list')
        exit(1)
    return showOptions(app_candidate)


def testfunc__selectNeededApp():
    app_info_list = [
        'DinoCapture 2.0          {7C5A40EF-A0FB-4BFC-874A-C0F2E0B9FA8E}\DinoCapture 2.0\DinoCapture.exe',
        'adlskj                   {alksdj f7C5A40EF-A0FB-4BFC-874A-C0F2E0B9FA8E}\DinoCapture 2.0\DinoCapture.exe',
        'lkasj dflka jsld         {7Ckjl',
        'Clkajsdlk kintj            lakdjoenrivj/.aex',
        ]
    recognizer = 'DinoCapture'
    result = selectNeededApp(app_info_list, recognizer)

    __expected_result_checker__(selectNeededApp.__name__, result,
        'DinoCapture 2.0          {7C5A40EF-A0FB-4BFC-874A-C0F2E0B9FA8E}\DinoCapture 2.0\DinoCapture.exe',)
    exit(1)




def appActivateStr(systemMESSAGE:str) -> str:
    BUG(f'Input string is "{systemMESSAGE}"')

    strs = [ v for v in systemMESSAGE.split('   ') if v and v!=' ' and v!='  ']
    if len(strs) < 2:
        strs = [ v for v in systemMESSAGE.split('  ') if v ]

    output_value = None
    if len(strs) != 2:
        info('Confused', f'String "{systemMESSAGE}" failed to be analyzed. Manually choose correct one')
        output_value = showOptions(strs)
    else:
        if '.exe' in strs[1]:
            output_value = strs[1]
        else:
            output_value = showOptions(strs)
    return output_value.strip() # remove redundant space char

def testfunc__appActivateStr():
    testSAMPLE = 'DinoCapture 2.0          {7C5A40EF-A0FB-4BFC-874A-C0F2E0B9FA8E}\DinoCapture 2.0\DinoCapture.exe'
    out = appActivateStr(testSAMPLE)

    __expected_result_checker__(appActivateStr.__name__, out,
            '{7C5A40EF-A0FB-4BFC-874A-C0F2E0B9FA8E}\DinoCapture 2.0\DinoCapture.exe' )
    exit(1)



def createYamlFile(yamlTEMPLATE:str, outFILEname:str, **xargs):
    print(f'[GotTemplate] Loading template "{yamlTEMPLATE}" and fill in variables')

    fIN = open(yamlTEMPLATE,'r')
    all_content = fIN.read().format(**xargs)

    print(f'[OutputFile] Writing output file "{outFILEname}"')
    f_out = open(fname, 'w')
    f_out.write(all_content)
    f_out.close()

def listAllApps():
    cmd_output = subprocess.run(['powershell', '-Command', 'Get-StartApps'], capture_output=True, text=True)
    info('AllApplications', 'list of all applications information from windows')
    for a in cmd_output.split('\n'):
        print(a)

def searchAppsInPowerShell(appNAME:str) -> tuple:
    cmd_output = subprocess.run(['powershell', '-Command', '$myobj=Get-StartApps -Name {appNAME} | Write-Output $myobj.Name'] , capture_output=True, text=True)
    candidate_names = cmd_output.strip().split('\n')
    cmd_output = subprocess.run(['powershell', '-Command', '$myobj=Get-StartApps -Name {appNAME} | Write-Output $myobj.AppID'], capture_output=True, text=True)
    candidate_appID = cmd_output.strip().split('\n')
    return (candidate_names, candidate_appID)
if __name__ == "__main__":
    #listAllApps()
    candidate_names, candidate_appIDs = searchAppsInPowerShell('Dino Capture')
    app_activate_str = showOptions(candidate_names)
    idx = candidate_names.index(app_activate_str)
    window_name = candidate_appIDs[idx]

    createYamlFile(
            'data/bkg_process_windows_template.yaml',
            'bkg_process_windows__test.yaml',
            app_activate_str=app_activate_str, window_name='kkkk')

