#include <stdio.h>
#include <vector>
#include <iostream>
#include <float.h>
#include <assert.h>
#include "AsciiTree.h"
#include "TreeNode.h"
using namespace std;

template <class T>
void printVec(const vector<T> &vec) {
    printf("[");
    for (int i = 0; i < vec.size(); i++)
        printf(std::is_floating_point<T>::value ? "%.2f%s": "%d%s", vec[i], (i == vec.size() - 1) ? "" : ",");
    printf("]\n");
}

template <class T>
void printVec(const vector<vector<T>> &vec) {
    printf("[\n");
    for (int i = 0; i < vec.size(); i++) {
        printf("  ");
        printVec(vec[i]);
    }
    printf("]\n");
}

class OptimalBST
{
private:
    void deleteTree(TreeNode *root) {
        if (root) {
            deleteTree(root->left);
            deleteTree(root->right);
            delete root;
            root = nullptr;
        }
    }
public:
    // If true, the dummy keys are as high as their parents
    const bool version = true;
    // The number of keys
    int n;
    // For each key k[i], we have a probability p[i] that a search will be for k[i].
    vector<double> p;
    // For each dummy key d[i], we have a probability q[i] that a search will correspond to d[i].
    vector<double> q;
    // For a subtree with keys k[i],...,k[j], let us denote this sum of probabilities as w(i, j). The sum of p and q is 1.
    vector<vector<double>> w;
    /* Let us define m(i, j) as the expected cost of
     * searching an optimal binary search tree containing the keys k[i],...,k[j].
     * Ultimately, we wish to compute m(1, n). */
    vector<vector<double>> m;
    /* To help us keep track of the structure of optimal binary search trees, we define
     * root(i, j), for 1 <= i <= j <= n, to be the index r for which k[r] is the root of an
     * optimal binary search tree containing keys k[i],...,k[j]. */
    vector<vector<int>> root;
    double optimalExpectedSearchCost;

    vector<int> keys;
    AsciiTree asciiTree;
    
    OptimalBST(const vector<double> &p, const vector<double> &q, const vector<int> &keys=vector<int>()) {
        assert(p.size() > 1 && p.size() == q.size());
        this->n = p.size() - 1;
        this->p = p;
        this->q = q;
        this->keys = keys;
        if (keys.size() == 0) for (int i = 0; i <= n; i++) this->keys.push_back(i);
        assert(this->p.size() == this->keys.size());
        this->w = vector<vector<double>>(n + 2, vector<double>(n + 1, 0.0));
        this->m = vector<vector<double>>(n + 2, vector<double>(n + 1, 0.0));
        this->root = vector<vector<int>>(n + 2, vector<int>(n + 1, 0));
        // this->run();
        this->speedRun();
        this->optimalExpectedSearchCost = m[1][n];
        this->print(); 
    }

    void run() {
        for (int i = 1; i <= n + 1; i++) {
            m[i][i - 1] = version ? 0.0 : q[i - 1];
            w[i][i - 1] = q[i - 1];
        }
        for (int l = 1; l <= n; l++) {
            for (int i = 1; i <= n - l + 1; i++) {
                int j = i + l - 1;
                m[i][j] = DBL_MAX;
                w[i][j] = w[i][j - 1] + p[j] + q[j];
                for (int r = i; r <= j; r++) {
                    double t = m[i][r - 1] + m[r + 1][j];
                    if (t < m[i][j]) {
                        m[i][j] = t;
                        root[i][j] = r;
                    }
                }
                m[i][j] += w[i][j];
            }
        }
    }

    void speedRun() {
        for (int i = 1; i <= n + 1; i++) {
            m[i][i - 1] = version ? 0.0 : q[i - 1];
            w[i][i - 1] = q[i - 1];
        }
        for (int l = 1; l <= n; l++) {
            for (int i = 1; i <= n - l + 1; i++) {
                int j = i + l - 1;
                m[i][j] = DBL_MAX;
                w[i][j] = w[i][j - 1] + p[j] + q[j];

                int start = root[i][j - 1] > i ? root[i][j - 1] : i;
                int end = root[i + 1][j] > i ? root[i + 1][j] : j;
                for (int r = start; r <= end; r++) {
                    double t = m[i][r - 1] + m[r + 1][j];
                    if (t < m[i][j]) {
                        m[i][j] = t;
                        root[i][j] = r;
                    }
                }
                m[i][j] += w[i][j];
            }
        }
    }

    TreeNode * makeOptimalBST(int i, int j) {
        if (i > j) return nullptr;
        else if (i == j) return new TreeNode(keys[i]);
        else {
            TreeNode *cur_root = new TreeNode(keys[root[i][j]]);
            cur_root->left = makeOptimalBST(i, root[i][j] - 1);
            cur_root->right = makeOptimalBST(root[i][j] + 1, j);
            return cur_root;
        }
    }

    void print() {
        printf("p: "); printVec(p);
        printf("q: "); printVec(q);
        printf("k: "); printVec(keys);
        printf("w: "); printVec(w);
        printf("m: "); printVec(m);
        printf("root: "); printVec(root);
        cout << "Optimal expected search cost: " << optimalExpectedSearchCost << endl;
        cout << "Optimal binary search tree:" << endl;
        TreeNode *tree = makeOptimalBST(1, n);
        asciiTree.print_ascii_tree(tree);
        deleteTree(tree);
    }
};

int main() {
    OptimalBST(
        vector<double>{0.00, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06},
        vector<double>{0.10, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04},
        vector<int>{0, 1, 3, 5, 7, 9, 11, 13, 15, 17}
    );
    vector<vector<double>> testCases{
        vector<double>{0.00, 0.15, 0.10, 0.05, 0.10, 0.20},
        vector<double>{0.05, 0.10, 0.05, 0.05, 0.05, 0.10},
        vector<double>{0.00, 0.04, 0.06, 0.08, 0.02, 0.10, 0.12, 0.14},
        vector<double>{0.06, 0.06, 0.06, 0.06, 0.05, 0.05, 0.05, 0.05}
    };
    for (int i = 0; i < testCases.size(); i += 2) {
        OptimalBST(testCases[i], testCases[i + 1]);
    }
    return 0;
}