import time

# Matrix Operations
def shape(matrix):
    return [len(matrix), len(matrix[0])]

def multiply_matrix(matrix1, matrix2):
    multipliedMatrix = []
    n = shape(matrix1)[0]
    m,p = shape(matrix2)

    for i in range(n):
        arr = []

        for j in range(p):
            arr.append(0)
            for k in range(m):
                arr[j] += matrix1[i][k] * matrix2[k][j]
                
        multipliedMatrix.append(arr)

    return multipliedMatrix

def matrix_operation(matrix1, matrix2, operation, size=None):
    if(size is None): 
        lines, columns = shape(matrix1)
    else: lines, columns = size

    finalMatrix = []

    for line in range(lines):
        arr = []

        for column in range(columns):
            arr.append(operation(matrix1[line][column], matrix2[line][column]))

        finalMatrix.append(arr)
    
    return finalMatrix

def add_matrix(matrix1, matrix2, size=None):
    return matrix_operation(matrix1, matrix2, lambda x,y: x+y, size)

def sub_matrix(matrix1, matrix2, size=None):
    return matrix_operation(matrix1, matrix2, lambda x,y: x-y, size)

# Strassen Algorithm
def get_subArrays(matrix, size, half):
    subArrays = []
    lineIndex = 0

    for _ in range(2):
        firstHalf = []
        lastHalf = []

        for _ in range(half):
            matrixLine = matrix[lineIndex]
            firstHalf.append(matrixLine[0:half])
            lastHalf.append(matrixLine[half:])

            lineIndex += 1

        subArrays.append(firstHalf)
        subArrays.append(lastHalf)

    return subArrays

def get_parts(matrix1, matrix2, size, half=None):
    if(half is None): half = int(size/2)
    matrixSize = [half, half]
    abcd = get_subArrays(matrix1, size, half)
    efgh = get_subArrays(matrix2, size, half)

    p1 = strassen_multiplication(abcd[0], sub_matrix(efgh[1], efgh[3], matrixSize), half)
    p2 = strassen_multiplication(add_matrix(abcd[0], abcd[1], matrixSize), efgh[3], half)
    p3 = strassen_multiplication(add_matrix(abcd[2], abcd[3], matrixSize), efgh[0], half)
    p4 = strassen_multiplication(abcd[3], sub_matrix(efgh[2], efgh[0], matrixSize), half)
    p5 = strassen_multiplication(add_matrix(abcd[0], abcd[3], matrixSize), add_matrix(efgh[0], efgh[3], matrixSize), half)
    p6 = strassen_multiplication(sub_matrix(abcd[1], abcd[3], matrixSize), add_matrix(efgh[2], efgh[3], matrixSize), half)
    p7 = strassen_multiplication(sub_matrix(abcd[0], abcd[2], matrixSize), add_matrix(efgh[0], efgh[1], matrixSize), half)

    return [p1, p2, p3, p4, p5, p6, p7]

def get_final_parts(parts, size):
    lines = columns = size
    finalParts = [[],[],[],[]]

    for line in range(lines):
        sum1 = []
        sum2 = []
        sum3 = []
        sum4 = []

        for column in range(columns):
            sum1.append(parts[4][line][column]+parts[3][line][column]-parts[1][line][column]+parts[5][line][column])
            sum2.append(parts[0][line][column]+parts[1][line][column])
            sum3.append(parts[2][line][column]+parts[3][line][column])
            sum4.append(parts[0][line][column]+parts[4][line][column]-parts[2][line][column]-parts[6][line][column])
        
        finalParts[0].append(sum1)
        finalParts[1].append(sum2)
        finalParts[2].append(sum3)
        finalParts[3].append(sum4)

    return finalParts

def flat_matrix(parts, size):
    lines = size
    upperArray = []
    lowerArray = []

    for line in range(lines):
        upperArray.append(parts[0][line] + parts[1][line])
        lowerArray.append(parts[2][line] + parts[3][line])
    
    return upperArray + lowerArray

def strassen_multiplication(matrix1, matrix2, size=None):
    if(size is None): size = shape(matrix1)[0]

    if(size <= 8):
        return multiply_matrix(matrix1, matrix2)
    else:
        half = int(size/2)
        return flat_matrix(get_final_parts(get_parts(matrix1, matrix2, size, half), half), half)

