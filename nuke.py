
"""
Required ubuntu packages and setup
sudo visudo
*user* ALL=(ALL) NOPASSWD:ALL

sudo apt install python3
apt-get install python3-tk
sudo apt install lsscsi
sudo apt-get install glmark2

"""
from time import sleep
from tkinter import *
import multiprocessing
import subprocess
import pexpect
import sys
import os
import re


def get_drive_data():
    """
    Uses lsscsi to grab all drive data.
    Locates all ATA drives
    """
    drives = str(subprocess.getstatusoutput('lsscsi -l'))
    drives_list = drives.split('\\n')
    drive_count = int(drives.count('ATA'))
    print(drive_count, ' drive/s detected')

    for item in drives_list:
        if 'ATA' in item:
            re_drives = re.findall('sd[a-z]', drives)

    return re_drives


def nuke():
    """
    Calls shred function with as a seperate process
        ^is done like it is to be able to shred drives in paralell instead of sequentially
    pulls a list of running processes
    enters while loop that checks if shred is running
    when shred is no longer running calls part function
    """
    drive = get_drive_data()
    for item in drive:
        if item != 'sda':  ### remove in usb version
            p = multiprocessing.Process(target=shred, args=(item,))
            p.start()
            p.join()

    running = subprocess.Popen('ps -A', stdout=subprocess.PIPE, shell=True)
    output = running.stdout.read()

    while 'shred' in output.decode():
        sleep(5)
        running = subprocess.Popen('ps -A', stdout=subprocess.PIPE, shell=True)
        output = running.stdout.read()

    part()


def shred(item):
    """
    shreds whatever drive name is passed to it
    """
    cmd = 'sudo shred -fvzn 0 /dev/' + item + '&'
    os.system(cmd)


def part():
    """
    gets list of drives
    for every drive partitions with fdisk then gives it a ntfs file system
    """
    drives = get_drive_data()
    for item in drives:
        if item != 'sda':  ### remove in usb version
            x = pexpect.spawn('sudo fdisk /dev/' + item)
            x.logfile = sys.stdout.buffer

            x.expect('.*:')
            x.sendline('d')
            x.expect('.*:')
            x.sendline('n')
            x.expect('.*:')
            x.sendline('p')
            x.expect('.*:')
            x.sendline('1')
            x.expect('.*:')
            x.send('\n')
            x.expect('.*:')
            x.send('\n')
            x.expect('.*:')
            x.sendline('y')
            x.expect('.*:')
            x.sendline('w')

            sleep(5)

            cmd = 'sudo mkfs.ntfs -f /dev/' + item
            cmd += '1'
            os.system(cmd)
    done('done', 'Drives erased and partitioned as NTFS.')


def badblocks(drive):
    """
    creates a file named after a drive
        ^ done like this because I couldn't figure out another way to get a useable response from bad blocks
    """
    file = drive + '.txt'
    with open(file, 'w') as f:
        f.write('\n' + drive)
    cmd = 'sudo badblocks -wsv -e 1 -o /home/*USER*/Desktop/' + drive + '.txt -c 65536 /dev/' + drive + '&'
    os.system(cmd)


def hdd_tester():
    """
    gets list of drives
    starts a process to run badblocks for every drive
    checks to see when badblocks is done running
    checks output file to see if drive is bad
    displays bad drives if there is any
    """
    hdds = get_drive_data()
    bad = []
    for drive in hdds:
        if drive != 'sda ': ### remove in usb version
            p = multiprocessing.Process(target=badblocks, args=(drive,))
            p.start()
            p.join()

    sleep(5)

    running = subprocess.Popen('ps -A', stdout=subprocess.PIPE, shell=True)
    output = running.stdout.read()

    while 'badblocks' in output.decode():
        sleep(5)
        running = subprocess.Popen('ps -A', stdout=subprocess.PIPE, shell=True)
        output = running.stdout.read()

    for drive in hdds:
        if drive != 'sda ':  ### remove in usb version
            file = drive + '.txt'
            if '0' in open(file).read():
                bad.append(bad)
    if len(bad) == 0:
        done('HDD test', 'No bad drives detected.')
    else:
        done('HDD test', 'the bad drives are: \n'.join(bad))


def gpu_stress_test():
    """
    runs glmark2 to make sure system does not crash under gpu load
    """
    os.system('glmark2')


# popups


def h_pop():
    """
    this is the popup window that appears when help is clicked
    """
    win = Toplevel()
    win.wm_title('help')
    win.geometry('250x150')
    win.grid_rowconfigure(0, weight=1)
    win.grid_rowconfigure(4, weight=1)
    win.grid_columnconfigure(0, weight=1)
    win.grid_columnconfigure(3, weight=1)

    l = Label(win, text='ILL fill this out later.', wraplength=250)
    l.grid(row=0, column=0)

    b = Button(win, text="Okay", command=win.destroy)
    b.grid(row=3, column=0)


def done(title, msg='Error'):
    """
    This is a notification popup that can be customised depending on the parameters given
    """
    win = Toplevel()
    win.wm_title(title)
    win.geometry('250x150')
    win.grid_rowconfigure(0, weight=1)
    win.grid_rowconfigure(4, weight=1)
    win.grid_columnconfigure(0, weight=1)
    win.grid_columnconfigure(3, weight=1)

    l = Label(win, text=msg, wraplength=250)
    l.grid(row=0, column=0)

    b = Button(win, text="Okay", command=win.destroy)
    b.grid(row=3, column=0)


# end of pop ups

# advanced


def adv():
    """
    This is for a password protected advanced section, it is still under construction
    """
    win = Toplevel()
    win.wm_title('login')
    win.geometry('250x150')
    win.grid_rowconfigure(0, weight=1)
    win.grid_rowconfigure(3, weight=1)
    win.grid_columnconfigure(0, weight=1)
    win.grid_columnconfigure(3, weight=1)

    l = Label(win, text='Enter password.')
    l.grid(row=0, column=1)

    pass_ent = Entry(win)
    pass_ent.grid(row=1, column=1)

    b = Button(win, text="Enter", command=auth)
    b.grid(row=2, column=1)


def auth():
    """
    this is the password authentication for the adv function
    """
    passwd = pass_ent.get()
    if passwd == 'password':
        a_adv()
    else:
        win = Toplevel()
        win.wm_title('error')
        win.geometry('250x150')
        win.grid_rowconfigure(0, weight=1)
        win.grid_rowconfigure(3, weight=1)
        win.grid_columnconfigure(0, weight=1)
        win.grid_columnconfigure(3, weight=1)

        l = Label(win, text='Error.')
        l.grid(row=0, column=1)

        b = Button(win, text="close", command=win.destroy())
        b.grid(row=2, column=1)


def a_adv():
    """
    this will be the advanced menu that is opened once password is authenticated
    """
    win = Toplevel()
    win.wm_title('Advanced')
    win.geometry('250x150')
    win.grid_rowconfigure(0, weight=1)
    win.grid_rowconfigure(4, weight=1)
    win.grid_columnconfigure(0, weight=1)
    win.grid_columnconfigure(3, weight=1)

    l = Label(win, text='Ill fill this out later.', wraplength=250)
    l.grid(row=0, column=0)

    b = Button(win, text="Okay", command=win.destroy)
    b.grid(row=3, column=0)


if __name__ == '__main__':
    root = Tk()
    root.title('Boot\'n Nuke')
    root.geometry('250x300')

    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(9, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(3, weight=1)

    intro = Label(root, text='Wellcome to Boot\'n Nuke.')
    intro.grid(row=0, column=1)

    # options/ tests

    # click to nuke option, calls nuke function
    nuke = Button(text='click to nuke', command=nuke)
    nuke.grid(row=1, column=1)
    nuke.config(width='20')

    # partition button, calls part function
    part_b = Button(text='partition as ntfs', command=part)
    part_b.grid(row=2, column=1)
    part_b.config(width='20')

    # hdd health button calls hdd_tester function
    hard_health = Button(text='hard drive health test', command=hdd_tester)
    hard_health.grid(row=4, column=1)
    hard_health.config(width='20')

    # gpu stress test button calls gpu_stress_test
    gpu_stress = Button(text='gpu stress test', command=gpu_stress_test)
    gpu_stress.grid(row=5, column=1)
    gpu_stress.config(width='20')

    # help button that opens help popup
    help_ = Button(text='help', command=h_pop)
    help_.grid(row=6, column=1)
    help_.config(width='20')

    # advanced button that calls adv function
    adv = Button(text='Advanced', command=adv)
    adv.grid(row=7, column=1)
    adv.config(width='20')

    # end of options/test

    # quit button that destroys root to close program
    quit_ = Button(text='quit', command=root.destroy)
    quit_.grid(row=8, column=1)
    quit_.config(width='20')

    root.mainloop()

