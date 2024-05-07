import numpy as np

count = 1
f = open("Archive.txt", "a")
f.write("\n===== New File =====\n\n ")
f.close()

def writeFile(result, type):
    global count
    with open("Archive.txt", "a") as f:
        f.write("Operasi " + str(count) + ":\n")
        count += 1
        if type == "SPL":
            f.write("Menghitung SPL dengan matriks A:\n{}\ndengan matriks B\n{}\nSehingga didapat penyelesainnya:\n{}\n\n".format(result[0], result[1], result[2]))
        elif type == "Value":
            f.write("Mencari Eigen Value dengan matriks:\n{}\nSehingga didapat nilai EigenValue:\n{}\n\n".format(result[0], result[1]))
        elif type == "Vector":
            f.write("Mencari Eigen Vector dengan matriks:\n{}\nSehingga didapat nilai EigenVector:\n{}\n\n".format(result[0], result[1]))
        elif type == "Diagonal":
            f.write("Membuktikan apakah matriks terdiagonalisasi dengan matriks:\n{}\nDidapat bahwa matrix tersebut {}\n\n".format(result[0], result[1]))
        elif type == "SVD":
            if str(result[1]) == "N":
                f.write("Menghitung SVD dengan matriks:\n{}\nTidak dapat menemukan SVD\n\n".format(result[0]))
            else:
                f.write("Menghitung SVD dengan matriks:\n{}\nSehingga didapat:\nMatrik U:\n{}\n\nNilai Singular Value:\n{}\n\nMatrik V:\n{}\n\n".format(result[0], result[1], result[2], result[3]))
        elif type == "Poly":
            f.write("Mencari Karateristik Polynomial dengan matriks:\n{}\nSehingga didapat karateristik polynomial berupa:\n{}\n\n".format(result[0], result[1]))
        elif type == "Complex":
            f.write("Menghitung SPL Kompleks dengan matriks A:\n{}\ndengan matriks B\n{}\nSehingga didapat penyelesainnya:\n{}\n\n".format(result[0], result[1], result[2]))
        elif type == "Change":
            f.write("User mengubah baris dan kolom Matriks menjadi {}\n\n".format(result[0]))

def inputMatrik(rows, columns):
    Matrix = []
    for _ in range(rows):
        row = [float(x) for x in input().split()]
        Matrix.append(row)
    maxlen = max(len(row) for row in Matrix)
    for row in Matrix:
        row.extend([0] * (maxlen - len(row)))
    return np.array(Matrix)

def inputComplex(rows, columns):
    A = np.zeros((rows, columns), dtype=complex)
    for i in range(rows):
        row = input()
        elements = row.split()
        for j in range(columns):
            element = elements[j]
            if 'i' in element:
                element = element.replace('i', 'j')
            A[i, j] = complex(element)

    return A

def SPL():
    a = int(input("Masukkan jumlah persamaan : "))
    b = int(input("Masukkan jumlah variabel : "))
    print("Masukkan Koefisiensi Matriks A:")
    A = inputMatrik(a, b)
    print("Masukkan Nilai Matriks B:")
    B = inputMatrik(1, a)
    B = B.T
    num = len(A[0])
    try:
        if np.linalg.matrix_rank(A) != np.linalg.matrix_rank(np.column_stack((A, B))):
            result = "Sistem persamaan linier tidak memiliki solusi"
            print(result)
            writeFile([A, B, result], "SPL")
            return
        if np.linalg.matrix_rank(A) < num:
            result = "Sistem persamaan linier memiliki solusi tak terbatas"
            print(result)
            writeFile([A, B, result], "SPL")
            return

        print("Solusi unik dari persamaan linier adalah:")
        for i, v in enumerate(np.linalg.solve(A, B)):
            print("X{} = {}".format(i + 1, v))
        writeFile([A, B, np.linalg.solve(A, B)], "SPL")
    except np.linalg.LinAlgError:
        result = "Matriks tidak dapat diselesaikan."
        print(result)
        writeFile([A, B, result], "SPL")

def eigenValue():
    result = []
    print("Masukkan Koefisiensi Matriks:")
    A = inputMatrik(n, n)
    try:
        print("Eigenvalues:")
        for i in np.linalg.eigvals(A):
            print(i)
            result.append(i)
        writeFile([A, result], "Value")
    except np.linalg.LinAlgError:
        result = "Tidak dapat menentukan eigen value"
        writeFile([A, result], "Value")

def vectorEigen():
    print("Masukkan Koefisiensi Matriks:")
    A = inputMatrik(n, n)
    try:
        eigenValues, eigenVector = np.linalg.eig(A)
        np.set_printoptions(suppress=True)
        print("Hasilnya adalah:")
        for i in range(len(eigenValues)):
            print("Nilai eigen:", eigenValues[i])
            print("Vektor eigen:")
            print(eigenVector[:, i])
            print()
        writeFile([A, eigenVector], "Vector")
    except np.linalg.LinAlgError:
        result = "Tidak dapat menentukan vektor eigen"
        print(result)
        writeFile([A, result], "Vector")

def diagonalMatrix():
    result = ""
    print("Masukkan Koefisiensi Matriks:")
    A = inputMatrik(n, n)
    if np.allclose(A, np.diag(np.diagonal(A))):
        result = "Matrix terdiagonalisasi"
    else:
        result = "Matrix tidak terdiagonalisasi"
    print(result)
    writeFile([A, result], "Diagonal")

def SVD():
    a = int(input("Masukkan jumlah baris : "))
    b = int(input("Masukkan jumlah kolom : "))
    print("Masukkan Koefisiensi Matriks:")
    A = inputMatrik(a, b)
    try:
        U, S, V = np.linalg.svd(A)
        np.set_printoptions(suppress=True)
        print("Hasilnya adalah:\nMatrik U:")
        print(U)
        print("\nNilai Singular Value:")
        print(S)
        print("\nMatrik V:")
        print(V)
        writeFile([A, U, S, V], "SVD")
    except np.linalg.LinAlgError:
        result = "Tidak dapat menemukan SVD"
        print(result)
        writeFile([A, "N"], "SVD")

def characteristicPolynomial():
    result = ""
    print("Masukkan Koefisiensi Matriks:")
    A = inputMatrik(n, n)
    try:
        print("Hasilnya:")
        result = -np.polynomial.Polynomial.fromroots(np.linalg.eigvals(A))
    except np.linalg.LinAlgError:
        result = "Tidak dapat menentukan karateristik polynomial"
    print(result)
    writeFile([A, result], "Poly")

def complexSPL():
    result = []
    a = int(input("Masukkan jumlah persamaan : "))
    b = int(input("Masukkan jumlah variabel : "))
    print("Masukkan Koefisiensi Matriks A:")
    A = inputComplex(a, b)
    print("Masukkan Nilai Matriks B:")
    B = inputComplex(1, a)
    B = B.T
    try:
        U, S, Vh = np.linalg.svd(A)
        np.set_printoptions(suppress=True)
        S_inv = np.zeros_like(A.T)
        S_inv[:len(S), :len(S)] = np.diag(1 / S)
        x = Vh.T @ S_inv @ U.T @ B

        print("Hasil dari SPL Kompleks adalah:")
        for i in range(b):
            print("x{} = {}".format(i + 1, x[i, 0]))
            result.append(x[i, 0])
        result = np.array(result)
        writeFile([A, B, result], "Complex")
    except np.linalg.LinAlgError:
        result = "Tidak dapat menentukan complex SPL"
        print(result)
        writeFile([A, B, result], "Complex")

def changeMatrix():
    result = int(input("Masukkan Baris dan Kolom Matriks baru: "))
    print("Baris dan Kolom Matriks telah diubah menjadi " + str(result))
    writeFile([result], "Change")
    return result

print("\n===== Kalkulator Matriks =====\n")
n = int(input("Masukkan Baris dan Kolom Matriks: "))

while True:
    print("\nOperasi:")
    print("1. Menyelesaikan SPL")
    print("2. Mencari Eigen Value")
    print("3. Mencari Eigen Vektor")
    print("4. Membuktikan Matrik Terdiagonalisasi")
    print("5. Menghitung SVD")
    print("6. Mencari Karateristik Polynomial")
    print("7. Menyelesaikan SPL Kompleks")
    print("8. Mengganti Baris dan Kolom Matriks")
    print("0. Keluar Program")
    userChoice = input("Pilihan anda: ")
    if userChoice == '1':
        SPL()
    elif userChoice == '2':
        eigenValue()
    elif userChoice == '3':
        vectorEigen()
    elif userChoice == '4':
        diagonalMatrix()
    elif userChoice == '5':
        SVD()
    elif userChoice == '6':
        characteristicPolynomial()
    elif userChoice == '7':
        complexSPL()
    elif userChoice == '8':
        n = changeMatrix()
    elif userChoice == '0':
        break
    else:
        print("Pilihan tidak valid!")
