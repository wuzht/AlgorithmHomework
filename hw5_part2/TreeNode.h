#pragma once
typedef int ElemType;
struct TreeNode {
    ElemType val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(ElemType x) : val(x), left(nullptr), right(nullptr) {}
};
