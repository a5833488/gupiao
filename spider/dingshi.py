import schedule

def prr():
    i = 0
    for i in range(1,10):
        i = i + 1
        print("我已经是"+str(i))

if __name__ == '__main__':
    # schedule.every(1).seconds.do(prr)
    # while True:
    #     schedule.run_pending()
    prr()