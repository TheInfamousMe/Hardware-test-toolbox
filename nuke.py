
"""
Required ubuntu packages and setup
sudo vi sudo
*user* ALL=(ALL) NOPASSWD:ALL

sudo apt install htop
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


def get_drive_data():
    drives = str(subprocess.getstatusoutput('lsscsi -l'))
    drive_count = int(drives.count('ATA'))
    print(drive_count, ' drive/s detected')
    with open('drive_data.txt', 'w') as f:
        f.write(drives)

    data = []
    drives = []
    raw_data = ''

    with open('drive_data.txt') as f:
        raw_data = str(f.readlines())

    raw_data = raw_data[7:-5]
    data = raw_data.split('\\\\n')

    for item in data:
        if 'ATA' in item:
            drives.append(item[-4:])
    return drives


def nuke():
    wipe()

    running = subprocess.Popen('ps -A', stdout=subprocess.PIPE, shell=True)
    output = running.stdout.read()

    sleep(20)

    while 'shred' in output.decode():
        sleep(5)
        running = subprocess.Popen('ps -A', stdout=subprocess.PIPE, shell=True)
        output = running.stdout.read()

    part()


def shred(item):
    cmd = 'sudo shred -fvzn 0 /dev/' + item + '&'
    os.system(cmd)


def wipe():
    drive = get_drive_data()
    for item in drive:
        p = multiprocessing.Process(target=shred, args=(item,))
        p.start()
        p.join()

    print(drive)


def part():
    drives = get_drive_data()
    for item in drives:
        x = pexpect.spawn('sudo fdisk /dev/' + item)
        x.logfile = sys.stdout.buffer

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
        x.sendline('w')

    for item in drives:
        x = pexpect.spawn('sudo fdisk /dev/' + item)
        x.logfile = sys.stdout.buffer

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
        x.sendline('w')

    drives = get_drive_data()
    for item in drives:
        name = str(item[:3])
        print(name)
        cmd = 'sudo mkfs.ntfs -f /dev/' + name
        cmd += '1'
        print(cmd)
        os.system(cmd)

    for item in drives:
        name = str(item[:3])
        print(name)
        cmd = 'sudo mkfs.ntfs -f /dev/' + name
        cmd += '1'
        print(cmd)
        os.system(cmd)
    done('done', 'Drives erased and partitioned as NTFS.')


def hdd_tester():
    hdds = get_drive_data()
    print(hdds)
    for drive in hdds:
        drive_ = drive[:-1]
        file = drive_ + '.txt'
        with open(file, 'w') as f:
            f.write('\n' + drive_)

        cmd = 'sudo badblocks -wsv -e 1 -o /home/*user*/Desktop/' + drive_ + '.txt -c 65536 /dev/' + drive_
        print(cmd)
        os.system(cmd)

    print('done')

def gpu_stress_test():
    os.system('glmark2')


# popups


def h_pop():
    win = Toplevel()
    win.wm_title('help')
    win.geometry('250x150')
    win.grid_rowconfigure(0, weight=1)
    win.grid_rowconfigure(4, weight=1)
    win.grid_columnconfigure(0, weight=1)
    win.grid_columnconfigure(3, weight=1)

    l = Label(win, text='work in progress', wraplength=250)
    l.grid(row=0, column=0)

    b = Button(win, text="Okay", command=win.destroy)
    b.grid(row=3, column=0)


def done(title, msg):
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
    win = Toplevel()
    win.wm_title('Advanced')
    win.geometry('250x150')
    win.grid_rowconfigure(0, weight=1)
    win.grid_rowconfigure(4, weight=1)
    win.grid_columnconfigure(0, weight=1)
    win.grid_columnconfigure(3, weight=1)

    l = Label(win, text='test', wraplength=250)
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

    nuke = Button(text='click to nuke', command=nuke)
    nuke.grid(row=1, column=1)
    nuke.config(width='20')

    part_b = Button(text='partition as ntfs', command=part)
    part_b.grid(row=2, column=1)
    part_b.config(width='20')

    hard_health = Button(text='hard drive health test', command=hdd_tester)
    hard_health.grid(row=4, column=1)
    hard_health.config(width='20')

    gpu_stress = Button(text='gpu stress test', command=gpu_stress_test)
    gpu_stress.grid(row=5, column=1)
    gpu_stress.config(width='20')

    help_ = Button(text='help', command=h_pop)
    help_.grid(row=6, column=1)
    help_.config(width='20')

    adv = Button(text='Advanced', command=adv)
    adv.grid(row=7, column=1)
    adv.config(width='20')

    # end of options/test

    quit_ = Button(text='quit', command=root.destroy)
    quit_.grid(row=8, column=1)
    quit_.config(width='20')

    root.mainloop()

