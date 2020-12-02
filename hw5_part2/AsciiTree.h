#pragma once
#include "TreeNode.h"
#include <limits.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <algorithm>


class AsciiTree
{
private:
    struct AsciiTreeNode {
        AsciiTreeNode *left, *right;
        //length of the edge from this node to its children
        int edge_length;
        int height;
        int lablen;
        //-1=I am left, 0=I am root, 1=right
        int parent_dir;
        //max supported unit32 in dec, 10 digits max
        char label[11];
    };

    static const int MAX_HEIGHT = 1000;
    int lprofile[MAX_HEIGHT];
    int rprofile[MAX_HEIGHT];
    //adjust gap between left and right nodes
    const int gap = 3;
    //used for printing next node in the same level,
    //this is the x coordinate of the next char printed
    int print_next;

    AsciiTreeNode *build_ascii_tree_recursive(TreeNode *t) {
        if (!t) return NULL;
        AsciiTreeNode *node = (AsciiTreeNode *)malloc(sizeof(AsciiTreeNode));
        node->left = build_ascii_tree_recursive(t->left);
        node->right = build_ascii_tree_recursive(t->right);

        if (node->left) node->left->parent_dir = -1;
        if (node->right) node->right->parent_dir = 1;

        sprintf(node->label, "%d", t->val);
        node->lablen = strlen(node->label);
        return node;
    }

    //Copy the tree into the ascii node structre
    AsciiTreeNode *build_ascii_tree(TreeNode *t) {
        if (!t) return NULL;
        AsciiTreeNode *node = build_ascii_tree_recursive(t);
        node->parent_dir = 0;
        return node;
    }

    //Free all the nodes of the given tree
    void free_ascii_tree(AsciiTreeNode *node) {
        if (!node) return;
        free_ascii_tree(node->left);
        free_ascii_tree(node->right);
        free(node);
        node = NULL;
    }

    //The following function fills in the lprofile array for the given tree.
    //It assumes that the center of the label of the root of this tree
    //is located at a position (x,y).  It assumes that the edge_length
    //fields have been computed for this tree.
    void compute_lprofile(AsciiTreeNode *node, int x, int y) {
        if (!node) return;
        int isleft = (node->parent_dir == -1);
        lprofile[y] = std::min(lprofile[y], x - ((node->lablen - isleft) / 2));
        if (node->left) {
            for (int i = 1; i <= node->edge_length && y + i < MAX_HEIGHT; i++)
                lprofile[y + i] = std::min(lprofile[y + i], x - i);
        }
        compute_lprofile(node->left, x - node->edge_length - 1, y + node->edge_length + 1);
        compute_lprofile(node->right, x + node->edge_length + 1, y + node->edge_length + 1);
    }

    void compute_rprofile(AsciiTreeNode *node, int x, int y) {
        if (!node) return;
        int notleft = (node->parent_dir != -1);
        rprofile[y] = std::max(rprofile[y], x + ((node->lablen - notleft) / 2));
        if (node->right) {
            for (int i = 1; i <= node->edge_length && y + i < MAX_HEIGHT; i++)
                rprofile[y + i] = std::max(rprofile[y + i], x + i);
        }
        compute_rprofile(node->left, x - node->edge_length - 1, y + node->edge_length + 1);
        compute_rprofile(node->right, x + node->edge_length + 1, y + node->edge_length + 1);
    }

    //This function fills in the edge_length and
    //height fields of the specified tree
    void compute_edge_lengths(AsciiTreeNode *node) {
        if (node == NULL) return;
        compute_edge_lengths(node->left);
        compute_edge_lengths(node->right);

        int hmin, delta;
        /* first fill in the edge_length of node */
        if (node->right == NULL && node->left == NULL) node->edge_length = 0;
        else {
            if (node->left) {
                for (int i = 0; i < node->left->height && i < MAX_HEIGHT; i++)
                    rprofile[i] = -INT_MAX;
                compute_rprofile(node->left, 0, 0);
                hmin = node->left->height;
            }
            else hmin = 0;
            if (node->right) {
                for (int i = 0; i < node->right->height && i < MAX_HEIGHT; i++)
                    lprofile[i] = INT_MAX;
                compute_lprofile(node->right, 0, 0);
                hmin = std::min(node->right->height, hmin);
            }
            else hmin = 0;
            delta = 4;
            for (int i = 0; i < hmin; i++)
                delta = std::max(delta, gap + 1 + rprofile[i] - lprofile[i]);

            //If the node has two children of height 1, then we allow the
            //two leaves to be within 1, instead of 2
            if (((node->left != NULL && node->left->height == 1) ||
                (node->right != NULL && node->right->height == 1)) &&
                delta > 4) delta--;

            node->edge_length = ((delta + 1) / 2) - 1;
        }

        //now fill in the height of node
        int h = 1;
        if (node->left) h = std::max(node->left->height + node->edge_length + 1, h);
        if (node->right) h = std::max(node->right->height + node->edge_length + 1, h);
        node->height = h;
    }

    //This function prints the given level of the given tree, assuming
    //that the node has the given x cordinate.
    void print_level(AsciiTreeNode *node, int x, int level) {
        if (!node) return;
        int i;
        int isleft = (node->parent_dir == -1);
        if (level == 0) {
            for (i = 0; i < (x - print_next - ((node->lablen - isleft) / 2)); i++)
                printf(" ");
            print_next += i;
            printf("%s", node->label);
            print_next += node->lablen;
        }
        else if (node->edge_length >= level) {
            if (node->left) {
                for (i = 0; i < (x - print_next - (level)); i++)
                    printf(" ");
                print_next += i;
                printf("/");
                print_next++;
            }
            if (node->right) {
                for (i = 0; i < (x - print_next + (level)); i++)
                    printf(" ");
                print_next += i;
                printf("\\");
                print_next++;
            }
        }
        else {
            print_level(node->left,
                        x - node->edge_length - 1,
                        level - node->edge_length - 1);
            print_level(node->right,
                        x + node->edge_length + 1,
                        level - node->edge_length - 1);
        }
    }

public:
    AsciiTree() {};
    AsciiTree(TreeNode *t) { print_ascii_tree(t); };

    //prints ascii tree for given Tree structure
    void print_ascii_tree(TreeNode *t) {
        if (t == NULL) return;
        AsciiTreeNode *proot = build_ascii_tree(t);
        compute_edge_lengths(proot);
        for (int i = 0; i < proot->height && i < MAX_HEIGHT; i++)
            lprofile[i] = INT_MAX;
        compute_lprofile(proot, 0, 0);
        int xmin = 0;
        for (int i = 0; i < proot->height && i < MAX_HEIGHT; i++)
            xmin = std::min(xmin, lprofile[i]);
        for (int i = 0; i < proot->height; i++) {
            print_next = 0;
            print_level(proot, -xmin, i);
            printf("\n");
        }
        if (proot->height >= MAX_HEIGHT) {
            printf("(This tree is taller than %d, and may be drawn incorrectly.)\n", MAX_HEIGHT);
        }
        free_ascii_tree(proot);
    }
    
};

