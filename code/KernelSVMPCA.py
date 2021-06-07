import numpy as np
import utils
from classifiers import RBF_SVM

def latex(toprint):
    outfiletex = '../data/svm_rbfpca_acc.tex'
    f = open(outfiletex, "w")
    print(r"\begin{center}", file=f)
    print(r"\begin{longtable}{|c|c|c|c|c|}", file=f)
    print(r"\caption{Kernel SVM With PCA}\label{tab:svm_rbfpca_acctable}\\", file=f)
    print(r"\hline", file=f)
    print(r"Bias & $\gamma$ & $C$ & PCA & Error Rate \\", file=f)
    print(r"\hline", file=f)
    
    toprint.sort(key=lambda x: x[4], reverse=True)
    for tup in toprint[:10]:
        print(f"{tup[0]} & {tup[1]} & {tup[2]} & {tup[3]} & {(1-tup[4])*100:.3f}\\% \\\\", file=f)
        print(r"\hline", file=f)

    print(r"\end{longtable}", file=f)
    print(r"\end{center}", file=f)

if __name__ == '__main__':
    trdataset = utils.load_train_data()
    tedataset = utils.load_test_data()

    trsamp, trlab = trdataset[:-1, :], trdataset[-1, :]
    tesamp, telab = tedataset[:-1, :], tedataset[-1, :]

    w, v = utils.PCA(trsamp, feat_label=False)

    toprint = []
    biases = [0, 1.]
    boundaries = [.1, 1]
    gammas = [5, 10]
    nPCA = [10, 9, 8, 7, 6, 5, 4]
    for bias in biases:
        for gamma in gammas:
            for boundary in boundaries:
                for n in nPCA:
                    vt = v[:, :n]
                    ptrsamp, ptesamp = vt.T @ trsamp, vt.T @ tesamp
                    scores, predictions, acc = RBF_SVM(
                        ptrsamp, ptesamp, datasetl=trlab, test_datasetl=telab, gamma=gamma, reg_bias=bias, boundary=boundary)
                    toprint.append((bias, gamma, boundary, n, acc))
    
    latex(toprint)
