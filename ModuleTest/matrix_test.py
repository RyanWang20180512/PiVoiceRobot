from MatrixLedModule.Matrix_Led import Matrix_Led
import time
matrix=Matrix_Led(2,90,0)
#matrix.setBrightChar(1)
matrix.setScrollChar(27)
while True:
    #matrix.brightChar()
    matrix.scrollingChar()
    time.sleep(0.1)
