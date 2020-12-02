#include <stdio.h>
#include <vector>
using namespace std;

int numBinarySearchTree(int n) {
    vector<int> G(n + 1, 0);
    G[0] = 1;
    G[1] = 1;
    for (int i = 2; i <= n; i++) {
        for (int j = 1; j <= i; j++) {
            G[i] += G[j - 1] * G[i - j];
        }
    }
    return G[n];
}

int main() {
    for (int i = 0; i <= 15; i++) {
        printf("G(%2d) = %7d\n", i, numBinarySearchTree(i));
    }
    return 0;
}