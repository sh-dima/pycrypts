import sys

from pycrypts.game import PyCrypts

def main():
    pycrypts = PyCrypts(sys.argv)
    pycrypts.init()

    while pycrypts.tick():
        pass

    pycrypts.quit()

if __name__ == "__main__":
    main()
